from __future__ import annotations

import argparse
import json
from pathlib import Path

from agentic_grant_proposal_builder.evaluation import load_scenarios, run_scenario
from agentic_grant_proposal_builder.export import package_to_json, proposal_to_markdown
from agentic_grant_proposal_builder.models import GrantDocument, OrganizationProfile
from agentic_grant_proposal_builder.pipeline import build_proposal


def scenario_choices() -> list[str]:
    return [scenario.scenario_id for scenario in load_scenarios()]


def build_from_scenario(scenario_id: str, output_dir: Path) -> dict[str, str]:
    scenarios = {scenario.scenario_id: scenario for scenario in load_scenarios()}

    if scenario_id not in scenarios:
        available = ", ".join(sorted(scenarios))
        raise ValueError(f"Unknown scenario '{scenario_id}'. Available scenarios: {available}")

    scenario = scenarios[scenario_id]
    proposal, fit_score, evidence, package = build_proposal(
        scenario.organization_profile,
        scenario.documents,
    )

    output_dir.mkdir(parents=True, exist_ok=True)

    markdown_path = output_dir / f"{scenario_id}_proposal.md"
    json_path = output_dir / f"{scenario_id}_proposal_package.json"
    summary_path = output_dir / f"{scenario_id}_summary.json"

    markdown_path.write_text(proposal_to_markdown(proposal, fit_score, package))
    json_path.write_text(package_to_json(proposal, fit_score, package))

    summary = {
        "scenario_id": scenario_id,
        "title": scenario.title,
        "overall_fit_score": fit_score.overall,
        "evidence_count": len(evidence),
        "funder_requirement_count": len(package.funder_requirements),
        "reviewer_finding_count": len(package.reviewer_findings),
        "quality_status": (
            package.quality_report.overall_status
            if package.quality_report is not None
            else "not_available"
        ),
        "quality_readiness_score": (
            package.quality_report.readiness_score
            if package.quality_report is not None
            else 0
        ),
        "markdown": str(markdown_path),
        "json": str(json_path),
    }
    summary_path.write_text(json.dumps(summary, indent=2))

    return {
        "markdown": str(markdown_path),
        "json": str(json_path),
        "summary": str(summary_path),
    }


def build_from_files(
    profile_path: Path,
    document_paths: list[Path],
    output_dir: Path,
    stem: str,
) -> dict[str, str]:
    profile_data = json.loads(profile_path.read_text())
    profile = OrganizationProfile.model_validate(profile_data)

    documents = [
        GrantDocument(
            name=path.name,
            text=path.read_text(errors="ignore"),
            source_type="cli",
        )
        for path in document_paths
    ]

    proposal, fit_score, evidence, package = build_proposal(profile, documents)

    output_dir.mkdir(parents=True, exist_ok=True)

    markdown_path = output_dir / f"{stem}_proposal.md"
    json_path = output_dir / f"{stem}_proposal_package.json"
    summary_path = output_dir / f"{stem}_summary.json"

    markdown_path.write_text(proposal_to_markdown(proposal, fit_score, package))
    json_path.write_text(package_to_json(proposal, fit_score, package))

    summary = {
        "profile": str(profile_path),
        "documents": [str(path) for path in document_paths],
        "overall_fit_score": fit_score.overall,
        "evidence_count": len(evidence),
        "funder_requirement_count": len(package.funder_requirements),
        "reviewer_finding_count": len(package.reviewer_findings),
        "quality_status": (
            package.quality_report.overall_status
            if package.quality_report is not None
            else "not_available"
        ),
        "quality_readiness_score": (
            package.quality_report.readiness_score
            if package.quality_report is not None
            else 0
        ),
        "markdown": str(markdown_path),
        "json": str(json_path),
    }
    summary_path.write_text(json.dumps(summary, indent=2))

    return {
        "markdown": str(markdown_path),
        "json": str(json_path),
        "summary": str(summary_path),
    }


def list_scenarios() -> list[dict[str, str]]:
    return [
        {
            "scenario_id": scenario.scenario_id,
            "title": scenario.title,
            "organization_name": scenario.organization_profile.organization_name,
        }
        for scenario in load_scenarios()
    ]


def evaluate_scenario(scenario_id: str) -> dict[str, object]:
    scenarios = {scenario.scenario_id: scenario for scenario in load_scenarios()}

    if scenario_id not in scenarios:
        available = ", ".join(sorted(scenarios))
        raise ValueError(f"Unknown scenario '{scenario_id}'. Available scenarios: {available}")

    return run_scenario(scenarios[scenario_id]).model_dump()


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agpb",
        description="Agentic Grant Proposal Builder command line interface.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list-scenarios", help="List available synthetic demo scenarios.")

    scenario_parser = subparsers.add_parser(
        "build-scenario",
        help="Build proposal artifacts from a synthetic scenario.",
    )
    scenario_parser.add_argument("scenario_id", help="Scenario id from sample_data/scenarios.")
    scenario_parser.add_argument(
        "--output-dir",
        default="reports/cli",
        help="Directory where CLI artifacts will be written.",
    )

    eval_parser = subparsers.add_parser(
        "evaluate-scenario",
        help="Run one scenario and print evaluation metrics as JSON.",
    )
    eval_parser.add_argument("scenario_id", help="Scenario id from sample_data/scenarios.")

    file_parser = subparsers.add_parser(
        "build-files",
        help="Build proposal artifacts from a profile JSON file and one or more text files.",
    )
    file_parser.add_argument("--profile", required=True, help="Path to OrganizationProfile JSON.")
    file_parser.add_argument(
        "--documents",
        nargs="+",
        required=True,
        help="One or more plain-text guidance/source files.",
    )
    file_parser.add_argument(
        "--output-dir",
        default="reports/cli",
        help="Directory where CLI artifacts will be written.",
    )
    file_parser.add_argument(
        "--stem",
        default="custom",
        help="Filename stem for generated artifacts.",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = create_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "list-scenarios":
            print(json.dumps(list_scenarios(), indent=2))
            return 0

        if args.command == "build-scenario":
            paths = build_from_scenario(args.scenario_id, Path(args.output_dir))
            print(json.dumps(paths, indent=2))
            return 0

        if args.command == "evaluate-scenario":
            result = evaluate_scenario(args.scenario_id)
            print(json.dumps(result, indent=2))
            return 0

        if args.command == "build-files":
            paths = build_from_files(
                profile_path=Path(args.profile),
                document_paths=[Path(path) for path in args.documents],
                output_dir=Path(args.output_dir),
                stem=args.stem,
            )
            print(json.dumps(paths, indent=2))
            return 0

    except Exception as exc:
        parser.error(str(exc))
        return 2

    parser.error("Unknown command.")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
