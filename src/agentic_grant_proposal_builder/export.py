from __future__ import annotations

import json

from agentic_grant_proposal_builder.models import FitScore, ProposalArtifact
from agentic_grant_proposal_builder.workflow import ProposalPackage


def proposal_to_markdown(
    proposal: ProposalArtifact,
    fit_score: FitScore,
    package: ProposalPackage | None = None,
) -> str:
    parts = [
        f"# {proposal.title}",
        "",
        "## Funder-Fit Score",
        "",
        f"Overall score: {fit_score.overall}/100",
        "",
        fit_score.rationale,
        "",
        "## Executive Summary",
        "",
        proposal.executive_summary,
        "",
        "## Need Statement",
        "",
        proposal.need_statement,
        "",
        "## Project Design",
        "",
        proposal.project_design,
        "",
        "## Outcomes",
        "",
        proposal.outcomes,
        "",
        "## Budget Narrative",
        "",
        proposal.budget_narrative,
        "",
        "## Evaluation Plan",
        "",
        proposal.evaluation_plan,
        "",
        "## Sustainability",
        "",
        proposal.sustainability,
        "",
        "## Funder Alignment",
        "",
        proposal.funder_alignment,
        "",
    ]

    if package is not None:
        parts.extend(
            [
                "## Funder Requirements",
                "",
                *[
                    f"- {item.priority.upper()} - {item.requirement_type}: {item.requirement}"
                    for item in package.funder_requirements
                ],
                "",
                "## Reviewer Findings",
                "",
                *[
                    f"- {item.severity.upper()} - {item.category}: {item.finding}"
                    for item in package.reviewer_findings
                ],
                "",
                "## Budget Plan",
                "",
                f"Total request: ${package.budget_plan.total_request:,.2f}",
                "",
                *[
                    f"- {item.category}: ${item.amount:,.2f} - {item.justification}"
                    for item in package.budget_plan.line_items
                ],
                "",
            ]
        )

        if package.quality_report is not None:
            parts.extend(
                [
                    "## Quality Gate Report",
                    "",
                    f"Overall status: {package.quality_report.overall_status}",
                    "",
                    f"Readiness score: {package.quality_report.readiness_score}/100",
                    "",
                    package.quality_report.final_recommendation,
                    "",
                ]
            )

    return "\n".join(parts)


def package_to_json(
    proposal: ProposalArtifact,
    fit_score: FitScore,
    package: ProposalPackage,
) -> str:
    payload = {
        "proposal": proposal.model_dump(),
        "fit_score": fit_score.model_dump(),
        "proposal_package": package.model_dump(),
    }

    return json.dumps(payload, indent=2)
