from __future__ import annotations

import asyncio
import concurrent.futures
import os
from collections.abc import Callable
from typing import Any

from pydantic import BaseModel, Field

from agentic_grant_proposal_builder.agents import deterministic_proposal
from agentic_grant_proposal_builder.models import FitScore, OrganizationProfile, ProposalArtifact
from agentic_grant_proposal_builder.retrieval import RetrievedChunk
from agentic_grant_proposal_builder.reviewer import (
    build_budget_plan,
    build_funder_requirements,
    build_quality_report,
    build_reviewer_findings,
)
from agentic_grant_proposal_builder.workflow import (
    BudgetPlan,
    FunderRequirement,
    QualityReport,
    ReviewerFinding,
)


class FunderRequirementsOutput(BaseModel):
    requirements: list[FunderRequirement] = Field(default_factory=list)


class ReviewerFindingsOutput(BaseModel):
    findings: list[ReviewerFinding] = Field(default_factory=list)


class OpenAIAgentOutputs(BaseModel):
    funder_requirements: list[FunderRequirement]
    proposal: ProposalArtifact
    reviewer_findings: list[ReviewerFinding]
    budget_plan: BudgetPlan
    quality_report: QualityReport


def openai_agents_enabled() -> bool:
    return bool(os.getenv("OPENAI_API_KEY")) and os.getenv("AGPB_USE_OPENAI_AGENTS", "1") == "1"


def _run_async_safely(coro_factory: Callable[[], Any]) -> Any:
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro_factory())

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(lambda: asyncio.run(coro_factory()))
        return future.result()


async def _run_agent_workflow(
    profile: OrganizationProfile,
    fit_score: FitScore,
    evidence: list[RetrievedChunk],
) -> OpenAIAgentOutputs:
    from agents import Agent, Runner, function_tool

    model = os.getenv("AGPB_MODEL", "gpt-4.1-mini")

    @function_tool
    def get_applicant_profile() -> str:
        """Return the normalized applicant profile as JSON."""
        return profile.model_dump_json(indent=2)

    @function_tool
    def get_retrieved_evidence() -> str:
        """Return retrieved funder evidence from uploaded documents."""
        return "\n\n".join(chunk.text for chunk in evidence) or "No retrieved evidence."

    @function_tool
    def get_fit_score() -> str:
        """Return the funder-fit score as JSON."""
        return fit_score.model_dump_json(indent=2)

    @function_tool
    def calculate_budget_plan() -> str:
        """Return a deterministic draft budget plan as JSON."""
        return build_budget_plan(profile).model_dump_json(indent=2)

    @function_tool
    def list_evidence_sources() -> str:
        """Return source names and relevance scores for retrieved evidence chunks."""
        return "\n".join(f"{chunk.source}: {chunk.score:.3f}" for chunk in evidence)

    requirements_agent = Agent(
        name="Funder Requirements Extractor Agent",
        model=model,
        instructions="Extract funder requirements from retrieved evidence.",
        tools=[get_retrieved_evidence, list_evidence_sources],
        output_type=FunderRequirementsOutput,
    )

    proposal_agent = Agent(
        name="Grant Proposal Writer Agent",
        model=model,
        instructions="Draft a grounded grant proposal from applicant profile and evidence.",
        tools=[
            get_applicant_profile,
            get_retrieved_evidence,
            get_fit_score,
            list_evidence_sources,
        ],
        output_type=ProposalArtifact,
    )

    reviewer_agent = Agent(
        name="Grant Reviewer Agent",
        model=model,
        instructions="Return reviewer findings with severity and fixes.",
        tools=[
            get_applicant_profile,
            get_retrieved_evidence,
            get_fit_score,
            list_evidence_sources,
        ],
        output_type=ReviewerFindingsOutput,
    )

    budget_agent = Agent(
        name="Budget Narrative Agent",
        model=model,
        instructions="Create budget line items and a budget narrative.",
        tools=[
            get_applicant_profile,
            get_retrieved_evidence,
            get_fit_score,
            calculate_budget_plan,
        ],
        output_type=BudgetPlan,
    )

    quality_agent = Agent(
        name="Proposal Quality Gate Agent",
        model=model,
        instructions="Evaluate readiness and unresolved proposal risks.",
        tools=[
            get_applicant_profile,
            get_retrieved_evidence,
            get_fit_score,
            list_evidence_sources,
            calculate_budget_plan,
        ],
        output_type=QualityReport,
    )

    requirements_result = await Runner.run(
        requirements_agent,
        input="Extract funder requirements.",
        max_turns=8,
    )
    requirements_output = FunderRequirementsOutput.model_validate(
        requirements_result.final_output
    )

    proposal_result = await Runner.run(
        proposal_agent,
        input="Create the proposal artifact.",
        max_turns=8,
    )
    proposal = ProposalArtifact.model_validate(proposal_result.final_output)

    reviewer_result = await Runner.run(
        reviewer_agent,
        input=proposal.model_dump_json(indent=2),
        max_turns=8,
    )
    reviewer_output = ReviewerFindingsOutput.model_validate(reviewer_result.final_output)

    budget_result = await Runner.run(
        budget_agent,
        input="Create the budget plan.",
        max_turns=8,
    )
    budget_plan = BudgetPlan.model_validate(budget_result.final_output)

    quality_result = await Runner.run(
        quality_agent,
        input="\n".join(
            [
                proposal.model_dump_json(indent=2),
                reviewer_output.model_dump_json(indent=2),
                budget_plan.model_dump_json(indent=2),
            ]
        ),
        max_turns=8,
    )
    quality_report = QualityReport.model_validate(quality_result.final_output)

    return OpenAIAgentOutputs(
        funder_requirements=requirements_output.requirements,
        proposal=proposal,
        reviewer_findings=reviewer_output.findings,
        budget_plan=budget_plan,
        quality_report=quality_report,
    )


def run_openai_agent_workflow(
    profile: OrganizationProfile,
    fit_score: FitScore,
    evidence: list[RetrievedChunk],
) -> OpenAIAgentOutputs | None:
    if not openai_agents_enabled():
        return None

    try:
        return _run_async_safely(lambda: _run_agent_workflow(profile, fit_score, evidence))
    except Exception:
        proposal = deterministic_proposal(profile, evidence)
        requirements = build_funder_requirements(evidence)
        findings = build_reviewer_findings(proposal, fit_score, evidence, requirements)
        budget = build_budget_plan(profile)
        quality = build_quality_report(proposal, fit_score, evidence, requirements, findings, budget)
        return OpenAIAgentOutputs(
            funder_requirements=requirements,
            proposal=proposal,
            reviewer_findings=findings,
            budget_plan=budget,
            quality_report=quality,
        )
