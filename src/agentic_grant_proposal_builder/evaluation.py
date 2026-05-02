from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from agentic_grant_proposal_builder.models import GrantDocument, OrganizationProfile
from agentic_grant_proposal_builder.pipeline import build_proposal


class EvaluationScenario(BaseModel):
    scenario_id: str
    title: str
    organization_profile: OrganizationProfile
    documents: list[GrantDocument] = Field(default_factory=list)


class EvaluationResult(BaseModel):
    scenario_id: str
    title: str
    overall_fit_score: int
    evidence_count: int
    funder_requirement_count: int
    reviewer_finding_count: int
    compliance_needs_review_count: int
    budget_total_request: float
    budget_line_item_total: float
    quality_status: str
    quality_readiness_score: int
    runtime_path: str


def load_scenarios(directory: str | Path = "sample_data/scenarios") -> list[EvaluationScenario]:
    scenario_dir = Path(directory)
    scenarios: list[EvaluationScenario] = []

    for path in sorted(scenario_dir.glob("*.json")):
        scenarios.append(EvaluationScenario.model_validate_json(path.read_text()))

    return scenarios


def run_scenario(scenario: EvaluationScenario) -> EvaluationResult:
    proposal, fit_score, evidence, package = build_proposal(
        scenario.organization_profile,
        scenario.documents,
    )
    _ = proposal

    compliance_needs_review_count = sum(
        1 for check in package.compliance_checks if check.status.lower() == "needs review"
    )
    budget_total = round(sum(item.amount for item in package.budget_plan.line_items), 2)

    quality_status = "not_available"
    quality_score = 0
    if package.quality_report is not None:
        quality_status = package.quality_report.overall_status
        quality_score = package.quality_report.readiness_score

    runtime_path = "deterministic fallback"
    for step in package.workflow_trace:
        if "OpenAI Agents SDK" in step.output_summary:
            runtime_path = "OpenAI Agents SDK"
            break

    return EvaluationResult(
        scenario_id=scenario.scenario_id,
        title=scenario.title,
        overall_fit_score=int(fit_score.overall),
        evidence_count=len(evidence),
        funder_requirement_count=len(package.funder_requirements),
        reviewer_finding_count=len(package.reviewer_findings),
        compliance_needs_review_count=compliance_needs_review_count,
        budget_total_request=round(package.budget_plan.total_request, 2),
        budget_line_item_total=budget_total,
        quality_status=quality_status,
        quality_readiness_score=quality_score,
        runtime_path=runtime_path,
    )


def run_all_scenarios(directory: str | Path = "sample_data/scenarios") -> list[EvaluationResult]:
    return [run_scenario(scenario) for scenario in load_scenarios(directory)]


def results_to_markdown(results: list[EvaluationResult]) -> str:
    lines = [
        "# Agentic Grant Proposal Builder Evaluation Report",
        "",
        "| Scenario | Runtime | Fit Score | Evidence | Requirements | Reviewer Findings | Quality Status | Quality Score |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for result in results:
        lines.append(
            "| "
            + " | ".join(
                [
                    result.title,
                    result.runtime_path,
                    str(result.overall_fit_score),
                    str(result.evidence_count),
                    str(result.funder_requirement_count),
                    str(result.reviewer_finding_count),
                    result.quality_status,
                    str(result.quality_readiness_score),
                ]
            )
            + " |"
        )

    average_fit = 0.0
    average_quality = 0.0

    if results:
        average_fit = sum(result.overall_fit_score for result in results) / len(results)
        average_quality = sum(result.quality_readiness_score for result in results) / len(results)

    lines.extend(
        [
            "",
            "## Summary Metrics",
            "",
            f"- Scenario count: {len(results)}",
            f"- Average fit score: {average_fit:.1f}",
            f"- Average quality readiness score: {average_quality:.1f}",
            "",
        ]
    )

    return "\n".join(lines)


def write_evaluation_reports(
    results: list[EvaluationResult],
    output_dir: str | Path = "reports",
) -> dict[str, str]:
    report_dir = Path(output_dir)
    report_dir.mkdir(parents=True, exist_ok=True)

    json_path = report_dir / "evaluation_results.json"
    markdown_path = report_dir / "evaluation_report.md"

    json_payload: list[dict[str, Any]] = [result.model_dump() for result in results]
    json_path.write_text(json.dumps(json_payload, indent=2))
    markdown_path.write_text(results_to_markdown(results))

    return {"json": str(json_path), "markdown": str(markdown_path)}


def main() -> None:
    results = run_all_scenarios()
    paths = write_evaluation_reports(results)

    print("Evaluation complete.")
    print("JSON:", paths["json"])
    print("Markdown:", paths["markdown"])


if __name__ == "__main__":
    main()
