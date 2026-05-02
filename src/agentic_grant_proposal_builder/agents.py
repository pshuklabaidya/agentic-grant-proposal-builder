from __future__ import annotations

import os

from agentic_grant_proposal_builder.models import OrganizationProfile, ProposalArtifact
from agentic_grant_proposal_builder.retrieval import RetrievedChunk


def evidence_block(chunks: list[RetrievedChunk]) -> str:
    if not chunks:
        return "No retrieved funder evidence available."

    return "\n\n".join(
        [
            "\n".join(
                [
                    f"Source: {chunk.source}",
                    f"Relevance: {chunk.score:.3f}",
                    f"Text: {chunk.text}",
                ]
            )
            for chunk in chunks
        ]
    )


def deterministic_proposal(
    profile: OrganizationProfile,
    chunks: list[RetrievedChunk],
) -> ProposalArtifact:
    evidence = evidence_block(chunks)

    return ProposalArtifact(
        title=f"{profile.organization_name}: Grant Proposal Draft",
        executive_summary=(
            f"{profile.organization_name} seeks {profile.requested_amount} to advance its "
            f"mission: {profile.mission} The proposed {profile.project_duration} initiative "
            f"will serve {profile.target_population} in {profile.geography} through "
            f"{profile.current_programs}."
        ),
        need_statement=(
            "The target population faces persistent barriers requiring coordinated support. "
            "The final submission should add current local data, service utilization trends, "
            f"and funder-specific support. Retrieved guidance: {evidence[:900]}"
        ),
        project_design=(
            f"The project will integrate {profile.current_programs} into a structured service "
            "model with intake, participant support, milestone tracking, and continuous improvement."
        ),
        outcomes=(
            "Expected outcomes should include participation, completion, skill-gain, placement, "
            "retention, satisfaction, and equity measures with baselines, targets, data sources, "
            "and reporting cadence."
        ),
        budget_narrative=(
            f"The requested amount is {profile.requested_amount}. Budget categories should connect "
            "to personnel, program delivery, participant support, technology, evaluation, and "
            "allowable indirect costs."
        ),
        evaluation_plan=(
            "Evaluation should combine output tracking, outcome measurement, participant feedback, "
            "implementation review, and funder reporting."
        ),
        sustainability=(
            "Sustainability should combine diversified funding, reusable program infrastructure, "
            "partnership development, documented outcomes, and board-level oversight."
        ),
        funder_alignment=(
            "Funder alignment depends on eligibility, priority population fit, allowable uses, "
            "evidence strength, implementation capacity, and measurable outcomes."
        ),
        reviewer_risks=[
            "Need statement requires current local data before submission.",
            "Budget must be checked against funder allowability rules.",
            "Eligibility should be verified against complete funder guidance.",
        ],
        evidence_used=[f"{chunk.source}: {chunk.text[:180]}" for chunk in chunks],
    )


def llm_proposal(profile: OrganizationProfile, chunks: list[RetrievedChunk]) -> ProposalArtifact:
    if not os.getenv("OPENAI_API_KEY"):
        return deterministic_proposal(profile, chunks)

    try:
        from openai import OpenAI

        client = OpenAI()
        model = os.getenv("AGPB_MODEL", "gpt-4.1-mini")
        prompt = "\n".join(
            [
                "Applicant profile:",
                profile.model_dump_json(indent=2),
                "",
                "Retrieved funder evidence:",
                evidence_block(chunks),
                "",
                "Return a complete grant proposal artifact as JSON.",
            ]
        )

        response = client.responses.create(
            model=model,
            input=prompt,
            text={
                "format": {
                    "type": "json_schema",
                    "name": "proposal_artifact",
                    "schema": ProposalArtifact.model_json_schema(),
                    "strict": True,
                }
            },
        )
        return ProposalArtifact.model_validate_json(response.output_text)
    except Exception:
        return deterministic_proposal(profile, chunks)
