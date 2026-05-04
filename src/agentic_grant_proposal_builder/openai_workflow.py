from __future__ import annotations

import asyncio
import concurrent.futures
import os
from collections.abc import Callable
from typing import Any

from pydantic import BaseModel, Field

from agentic_grant_proposal_builder.models import FitScore, OrganizationProfile, ProposalArtifact
from agentic_grant_proposal_builder.retrieval import RetrievedChunk
from agentic_grant_proposal_builder.reviewer import build_budget_plan
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



def _format_evidence(chunks: list[RetrievedChunk]) -> str:
    if not chunks:
        return "No retrieved evidence."

    blocks = []
    for index, chunk in enumerate(chunks, start=1):
        blocks.append(
            "\n".join(
                [
                    f"[E{index}] Source: {chunk.source}",
                    f"[E{index}] Relevance: {chunk.score:.3f}",
                    f"[E{index}] Text: {chunk.text}",
                ]
            )
        )
    return "\n\n".join(blocks)


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
        return _format_evidence(evidence)

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
        instructions=(
            "Extract a detailed funder requirements matrix from retrieved evidence. "
            "Return concrete requirements, not generic categories. Include eligibility, applicant type, geography, population, required proposal sections, review criteria, budget rules, allowable or unallowable costs, cost sharing, attachments, data management, reporting, deadlines, page limits, and compliance risks when present. "
            "Each requirement must include priority and evidence. Evidence must cite the retrieved evidence ID or exact source phrase. "
            "If the guidance is incomplete, mark the requirement as requiring human verification rather than inventing missing rules."
        ),
        tools=[get_retrieved_evidence, list_evidence_sources],
        output_type=FunderRequirementsOutput,
    )

    proposal_agent = Agent(
        name="Grant Proposal Writer Agent",
        model=model,
        instructions=(
            "You are a senior grant writer and federal proposal strategist. "
            "Draft a rich, funder-specific grant proposal using only the applicant profile, fit score, and retrieved evidence. "
            "Every section must be specific to the applicant, the funder opportunity, the target population, the project duration, and the requested budget. "
            "Use concrete program activities, staffing logic, implementation phases, measurable outputs, measurable outcomes, data sources, reporting cadence, risk controls, and sustainability mechanisms. "
            "Do not write generic phrases such as 'coordinated support,' 'measurable outcomes,' or 'continuous improvement' unless they are immediately followed by specific operational details. "
            "Ground funder alignment in retrieved evidence. Reference evidence IDs like [E1], [E2], and [E3] inside the prose when a claim depends on funder guidance. "
            "Executive summary must be 250-400 words. Need statement must be 500-800 words. Project design must be 700-1000 words. Outcomes must include a numbered target table in prose. "
            "Budget narrative must explain each major line item, why it is necessary, and how it supports implementation. Evaluation plan must define indicators, baseline source, target, collection method, frequency, responsible owner, and use of findings. "
            "Sustainability must identify post-award funding, institutionalization, partner commitments, data assets, and reusable infrastructure. "
            "Reviewer risks must be specific, funder-aware, and actionable."
        ),
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
        instructions=(
            "Act as a skeptical grant reviewer. Review the proposal against the retrieved funder guidance, fit score, applicant profile, and likely review criteria. "
            "Find weaknesses that would reduce reviewer confidence: generic need statement, missing eligibility proof, weak evidence, vague implementation plan, unclear staffing, unsupported outcomes, budget misalignment, missing evaluation detail, sustainability weakness, compliance risk, or poor funder-priority alignment. "
            "Each finding must state the exact weakness, why it matters for this funder, the proposal section affected, and a concrete revision that would fix it. "
            "Prefer specific medium and high findings over generic low findings."
        ),
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
        instructions=(
            "Create a detailed grant budget and budget narrative. "
            "Use the requested amount from the applicant profile as the total request. "
            "Allocate the budget across personnel, fringe or benefits if appropriate, program delivery, participant support, technology or data systems, evaluation, travel or convening if justified, indirect costs, and administration. "
            "Every line item must include a calculation basis, implementation purpose, funder allowability caveat, and relationship to outcomes. "
            "Do not use round-number filler without justification. "
            "The narrative must explain how the budget supports the work plan and why the cost structure is reasonable."
        ),
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
        instructions=(
            "Evaluate whether the proposal package is ready for submission. "
            "Use the proposal, funder requirements, reviewer findings, budget plan, fit score, and retrieved evidence. "
            "Score readiness strictly. Flag any unresolved high-priority funder requirement, missing eligibility confirmation, missing local data, missing measurable target, weak budget allowability proof, vague implementation detail, or missing evidence citation. "
            "Each check must include status, severity, finding, and exact recommended fix. "
            "The final recommendation must tell the user what to revise before submission."
        ),
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

    return _run_async_safely(lambda: _run_agent_workflow(profile, fit_score, evidence))
