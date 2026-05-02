from __future__ import annotations

from agentic_grant_proposal_builder.agents import llm_proposal
from agentic_grant_proposal_builder.models import GrantDocument, OrganizationProfile, ProposalArtifact
from agentic_grant_proposal_builder.openai_workflow import run_openai_agent_workflow
from agentic_grant_proposal_builder.retrieval import LocalRetriever, RetrievedChunk
from agentic_grant_proposal_builder.reviewer import build_proposal_package
from agentic_grant_proposal_builder.scoring import score_funder_fit
from agentic_grant_proposal_builder.workflow import ProposalPackage


def build_proposal(
    profile: OrganizationProfile,
    documents: list[GrantDocument],
) -> tuple[ProposalArtifact, object, list[RetrievedChunk], ProposalPackage]:
    retriever = LocalRetriever(documents)
    query = " ".join(
        [
            profile.mission,
            profile.target_population,
            profile.current_programs,
            "eligibility priorities budget evaluation outcomes reporting",
        ]
    )

    evidence = retriever.search(query, top_k=6)
    fit_score = score_funder_fit(profile, evidence)
    openai_outputs = run_openai_agent_workflow(profile, fit_score, evidence)

    if openai_outputs is not None:
        proposal = openai_outputs.proposal
        package = build_proposal_package(
            profile=profile,
            proposal=proposal,
            fit_score=fit_score,
            evidence=evidence,
            funder_requirements=openai_outputs.funder_requirements,
            reviewer_findings=openai_outputs.reviewer_findings,
            budget_plan=openai_outputs.budget_plan,
            quality_report=openai_outputs.quality_report,
            used_openai_agents=True,
        )
        return proposal, fit_score, evidence, package

    proposal = llm_proposal(profile, evidence)
    package = build_proposal_package(
        profile=profile,
        proposal=proposal,
        fit_score=fit_score,
        evidence=evidence,
        used_openai_agents=False,
    )

    return proposal, fit_score, evidence, package
