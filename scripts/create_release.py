from __future__ import annotations

import argparse
import json
import subprocess
import tomllib
from dataclasses import asdict, dataclass
from pathlib import Path


REPO_FULL_NAME = "pshuklabaidya/agentic-grant-proposal-builder"
REPORT_DIR = Path("reports")
RELEASE_DIR = REPORT_DIR / "release"


@dataclass(frozen=True)
class ReleaseAsset:
    path: str
    exists: bool


@dataclass(frozen=True)
class ReleasePlan:
    version: str
    tag: str
    repo: str
    title: str
    release_notes: str
    assets: list[ReleaseAsset]
    commands: list[list[str]]


def run_command(command: list[str]) -> tuple[int, str, str]:
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def project_version() -> str:
    data = tomllib.loads(Path("pyproject.toml").read_text())
    return str(data["project"]["version"])


def release_tag(version: str) -> str:
    return f"v{version}"


def expected_assets() -> list[str]:
    schema_assets = sorted(str(path) for path in Path("reports/schemas").glob("*.schema.json"))

    base_assets = [
        "reports/evaluation_results.json",
        "reports/evaluation_report.md",
        "reports/repo_health.json",
        "reports/repo_health.md",
        "reports/dependency_audit.json",
        "reports/dependency_audit.md",
        "reports/publication_readiness.json",
        "reports/publication_readiness.md",
        "docs/SCHEMAS.md",
        "CHANGELOG.md",
        "README.md",
    ]

    return base_assets + schema_assets


def release_notes_path(version: str) -> Path:
    return RELEASE_DIR / f"release_notes_v{version}.md"


def manifest_path(version: str) -> Path:
    return RELEASE_DIR / f"release_manifest_v{version}.json"


def write_release_notes(version: str) -> Path:
    RELEASE_DIR.mkdir(parents=True, exist_ok=True)
    tag = release_tag(version)
    path = release_notes_path(version)

    lines = [
        f"# Agentic Grant Proposal Builder {tag}",
        "",
        "## Summary",
        "",
        "Portfolio-ready release of Agentic Grant Proposal Builder.",
        "",
        "## Included Capabilities",
        "",
        "- Streamlit dashboard for grant proposal workflows",
        "- Local document ingestion and retrieval",
        "- Funder-fit scoring",
        "- Funder requirements extraction",
        "- Proposal drafting",
        "- Reviewer findings",
        "- Budget planning",
        "- Proposal quality gate",
        "- Deterministic fallback mode",
        "- Optional OpenAI Agents SDK runtime path",
        "- CLI scenario and local-file workflows",
        "- Evaluation harness",
        "- Repository health report",
        "- Dependency audit report",
        "- Publication readiness report",
        "- JSON Schema contract exports",
        "- Docker packaging",
        "- CI artifact bundle",
        "",
        "## Human Review Boundary",
        "",
        "Generated proposal materials require human review before any real-world submission.",
        "",
        "The application does not guarantee eligibility, compliance, award likelihood, or funder acceptance.",
        "",
    ]

    path.write_text("\n".join(lines))
    return path


def build_release_plan(version: str | None = None) -> ReleasePlan:
    resolved_version = version or project_version()
    tag = release_tag(resolved_version)
    notes_path = write_release_notes(resolved_version)

    assets = [ReleaseAsset(path=path, exists=Path(path).exists()) for path in expected_assets()]

    existing_assets = [asset.path for asset in assets if asset.exists]

    commands = [
        ["git", "tag", "-a", tag, "-m", f"Agentic Grant Proposal Builder {tag}"],
        ["git", "push", "origin", tag],
        [
            "gh",
            "release",
            "create",
            tag,
            *existing_assets,
            "--repo",
            REPO_FULL_NAME,
            "--title",
            f"Agentic Grant Proposal Builder {tag}",
            "--notes-file",
            str(notes_path),
            "--verify-tag",
        ],
    ]

    return ReleasePlan(
        version=resolved_version,
        tag=tag,
        repo=REPO_FULL_NAME,
        title=f"Agentic Grant Proposal Builder {tag}",
        release_notes=str(notes_path),
        assets=assets,
        commands=commands,
    )


def write_manifest(plan: ReleasePlan) -> Path:
    RELEASE_DIR.mkdir(parents=True, exist_ok=True)
    path = manifest_path(plan.version)
    path.write_text(json.dumps(asdict(plan), indent=2))
    return path


def validate_assets(plan: ReleasePlan) -> list[str]:
    return [asset.path for asset in plan.assets if not asset.exists]


def tag_exists(tag: str) -> bool:
    status, _, _ = run_command(["git", "rev-parse", "-q", "--verify", f"refs/tags/{tag}"])
    return status == 0


def create_release(plan: ReleasePlan) -> int:
    missing = validate_assets(plan)
    if missing:
        print("Missing release assets:")
        for item in missing:
            print(f"- {item}")
        return 1

    if not tag_exists(plan.tag):
        status, stdout, stderr = run_command(plan.commands[0])
        print(stdout)
        print(stderr)
        if status != 0:
            return status
    else:
        print(f"Tag already exists locally: {plan.tag}")

    status, stdout, stderr = run_command(["git", "push", "origin", plan.tag])
    print(stdout)
    print(stderr)
    if status != 0:
        return status

    status, stdout, stderr = run_command(plan.commands[2])
    print(stdout)
    print(stderr)
    return status


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a release plan or publish a GitHub release.")
    parser.add_argument("--version", default=None, help="Release version. Defaults to pyproject.toml version.")
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Create the annotated tag, push it, and create the GitHub release.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = create_parser()
    args = parser.parse_args(argv)

    plan = build_release_plan(args.version)
    manifest = write_manifest(plan)

    missing = validate_assets(plan)

    print("Release plan written.")
    print("Manifest:", manifest)
    print("Release notes:", plan.release_notes)
    print("Tag:", plan.tag)
    print("Repository:", plan.repo)
    print("Missing assets:", len(missing))

    for command in plan.commands:
        print("$ " + " ".join(command))

    if missing:
        print("Missing assets must be generated before release creation.")
        for item in missing:
            print(f"- {item}")
        return 1

    if args.execute:
        return create_release(plan)

    print("Dry run only. Add --execute to publish the release.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
