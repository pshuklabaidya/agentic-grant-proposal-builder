from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class HealthCheck:
    name: str
    status: str
    details: str


REQUIRED_FILES = [
    "scripts/docker_smoke.py",
    "docs/DOCKER.md",
    ".dockerignore",
    "Dockerfile",
    "README.md",
    "pyproject.toml",
    "LICENSE",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "SUPPORT.md",
    "SECURITY.md",
    "DEPLOYMENT.md",
    "Makefile",
    ".gitignore",
    ".github/workflows/ci.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/feature_request.yml",
    ".github/pull_request_template.md",
    ".streamlit/config.toml",
    ".streamlit/secrets.toml.example",
    "src/agentic_grant_proposal_builder/app.py",
    "src/agentic_grant_proposal_builder/evaluation.py",
    "sample_data/scenarios/education_access.json",
    "sample_data/scenarios/rural_health.json",
    "sample_data/scenarios/small_business_support.json",
    "docs/ARCHITECTURE.md",
    "docs/AI_USAGE_AND_LIMITATIONS.md",
    "docs/HUMAN_REVIEW_CHECKLIST.md",
    "docs/DOCS_INDEX.md",
    "docs/SCENARIOS.md",
    "docs/DEMO_WALKTHROUGH.md",
    "docs/INTERVIEW_TALK_TRACK.md",
    "docs/PORTFOLIO_REVIEW.md",
    "docs/STREAMLIT_DEPLOYMENT_CHECKLIST.md",
]


README_EXPECTED_TERMS = [
    "Agentic Grant Proposal Builder",
    "OpenAI",
    "Streamlit",
    "Evaluation",
    "Safety",
    "docs/ARCHITECTURE.md",
    "docs/DOCS_INDEX.md",
]


def check_required_files() -> list[HealthCheck]:
    checks: list[HealthCheck] = []

    for file_name in REQUIRED_FILES:
        path = Path(file_name)
        checks.append(
            HealthCheck(
                name=f"required_file:{file_name}",
                status="pass" if path.exists() else "fail",
                details="found" if path.exists() else "missing",
            )
        )

    return checks


def check_readme_content() -> list[HealthCheck]:
    path = Path("README.md")

    if not path.exists():
        return [
            HealthCheck(
                name="readme_content",
                status="fail",
                details="README.md missing",
            )
        ]

    text = path.read_text()
    checks: list[HealthCheck] = []

    for term in README_EXPECTED_TERMS:
        checks.append(
            HealthCheck(
                name=f"readme_term:{term}",
                status="pass" if term in text else "fail",
                details="present" if term in text else "missing",
            )
        )

    return checks


def check_gitignore() -> list[HealthCheck]:
    path = Path(".gitignore")

    if not path.exists():
        return [
            HealthCheck(
                name="gitignore",
                status="fail",
                details=".gitignore missing",
            )
        ]

    text = path.read_text()
    required_patterns = [
        ".env",
        ".streamlit/secrets.toml",
        ".venv/",
        "__pycache__/",
        "*.egg-info/",
    ]

    return [
        HealthCheck(
            name=f"gitignore_pattern:{pattern}",
            status="pass" if pattern in text else "fail",
            details="present" if pattern in text else "missing",
        )
        for pattern in required_patterns
    ]


def check_ci_content() -> list[HealthCheck]:
    path = Path(".github/workflows/ci.yml")

    if not path.exists():
        return [
            HealthCheck(
                name="ci_workflow",
                status="fail",
                details="CI workflow missing",
            )
        ]

    text = path.read_text()
    required_terms = [
        "python -m ruff check .",
        "python -m pytest",
        "python -m agentic_grant_proposal_builder.evaluation",
    ]

    return [
        HealthCheck(
            name=f"ci_term:{term}",
            status="pass" if term in text else "fail",
            details="present" if term in text else "missing",
        )
        for term in required_terms
    ]


def build_report(checks: list[HealthCheck]) -> str:
    total = len(checks)
    passed = sum(1 for check in checks if check.status == "pass")
    failed = total - passed
    score = round((passed / total) * 100, 1) if total else 0.0

    lines = [
        "# Repository Health Report",
        "",
        f"Total checks: {total}",
        f"Passed checks: {passed}",
        f"Failed checks: {failed}",
        f"Health score: {score}%",
        "",
        "## Checks",
        "",
        "| Check | Status | Details |",
        "|---|---:|---|",
    ]

    for check in checks:
        lines.append(f"| {check.name} | {check.status} | {check.details} |")

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "A passing health report means the repository includes the expected portfolio, community, security, deployment, documentation, CI, and evaluation assets.",
            "",
        ]
    )

    return "\n".join(lines)


def main() -> int:
    checks: list[HealthCheck] = []
    checks.extend(check_required_files())
    checks.extend(check_readme_content())
    checks.extend(check_gitignore())
    checks.extend(check_ci_content())

    reports_dir = Path("reports")
    reports_dir.mkdir(parents=True, exist_ok=True)

    json_path = reports_dir / "repo_health.json"
    md_path = reports_dir / "repo_health.md"

    json_path.write_text(json.dumps([asdict(check) for check in checks], indent=2))
    md_path.write_text(build_report(checks))

    failed = [check for check in checks if check.status != "pass"]

    print("Repository health report written.")
    print("JSON:", json_path)
    print("Markdown:", md_path)
    print("Failed checks:", len(failed))

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
