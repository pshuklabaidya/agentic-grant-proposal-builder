from __future__ import annotations

import json
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path


REPO_FULL_NAME = "pshuklabaidya/agentic-grant-proposal-builder"
REPO_URL = f"https://github.com/{REPO_FULL_NAME}"
STREAMLIT_APP_PATH = "src/agentic_grant_proposal_builder/app.py"

EXPECTED_TOPICS = [
    "agentic-rag",
    "openai-agents",
    "streamlit",
    "rag",
    "grant-writing",
    "llm-evaluation",
    "portfolio-project",
]

EXPECTED_FILES = [
    "README.md",
    "CHANGELOG.md",
    "LICENSE",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "SUPPORT.md",
    "SECURITY.md",
    "DEPLOYMENT.md",
    "Dockerfile",
    ".github/workflows/ci.yml",
    ".github/dependabot.yml",
    ".streamlit/config.toml",
    ".streamlit/secrets.toml.example",
    STREAMLIT_APP_PATH,
    "docs/DOCS_INDEX.md",
    "docs/ARCHITECTURE.md",
    "docs/STREAMLIT_DEPLOYMENT_CHECKLIST.md",
    "docs/CI_ARTIFACTS.md",
    "docs/SCHEMAS.md",
    "reports/evaluation_report.md",
    "reports/repo_health.md",
    "reports/schemas/OrganizationProfile.schema.json",
    "reports/schemas/ProposalPackage.schema.json",
]


@dataclass(frozen=True)
class PublicationCheck:
    name: str
    status: str
    details: str


def run_command(command: list[str]) -> tuple[int, str, str]:
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def check_expected_files() -> list[PublicationCheck]:
    checks: list[PublicationCheck] = []

    for file_name in EXPECTED_FILES:
        path = Path(file_name)
        checks.append(
            PublicationCheck(
                name=f"file:{file_name}",
                status="pass" if path.exists() else "fail",
                details="found" if path.exists() else "missing",
            )
        )

    return checks


def check_git_remote() -> PublicationCheck:
    status, stdout, stderr = run_command(["git", "remote", "-v"])

    if status != 0:
        return PublicationCheck("git_remote", "warn", stderr or "git remote command failed")

    expected = REPO_FULL_NAME in stdout or REPO_URL in stdout
    return PublicationCheck(
        "git_remote",
        "pass" if expected else "warn",
        stdout or "no remote configured",
    )


def check_current_branch() -> PublicationCheck:
    status, stdout, stderr = run_command(["git", "branch", "--show-current"])

    if status != 0:
        return PublicationCheck("current_branch", "warn", stderr or "branch command failed")

    return PublicationCheck(
        "current_branch",
        "pass" if stdout == "main" else "warn",
        stdout or "unknown",
    )


def check_working_tree() -> PublicationCheck:
    status, stdout, stderr = run_command(["git", "status", "--porcelain"])

    if status != 0:
        return PublicationCheck("working_tree", "warn", stderr or "git status failed")

    return PublicationCheck(
        "working_tree",
        "pass" if not stdout else "warn",
        "clean" if not stdout else stdout.replace("\n", "; "),
    )


def check_gh_cli_repo_visibility() -> PublicationCheck:
    status, stdout, stderr = run_command(
        ["gh", "repo", "view", REPO_FULL_NAME, "--json", "nameWithOwner,url"]
    )

    if status != 0:
        return PublicationCheck(
            "gh_repo_view",
            "warn",
            stderr or "GitHub CLI not authenticated or repo unavailable",
        )

    return PublicationCheck(
        "gh_repo_view",
        "pass" if REPO_FULL_NAME in stdout else "warn",
        stdout,
    )


def deployment_values() -> dict[str, str]:
    return {
        "Repository": REPO_URL,
        "Branch": "main",
        "Main file path": STREAMLIT_APP_PATH,
        "OpenAI secrets location": "Streamlit Community Cloud secrets",
        "Local app command": f"streamlit run {STREAMLIT_APP_PATH}",
    }


def suggested_topic_command() -> str:
    topics = " ".join(f'--add-topic "{topic}"' for topic in EXPECTED_TOPICS)
    return (
        f'gh repo edit {REPO_FULL_NAME} '
        f'--description "Agentic RAG grant proposal builder with OpenAI tool-calling agents, Streamlit dashboard, quality gates, and evaluation reports." '
        f"{topics}"
    )


def build_report(checks: list[PublicationCheck]) -> str:
    total = len(checks)
    passed = sum(1 for check in checks if check.status == "pass")
    warnings = sum(1 for check in checks if check.status == "warn")
    failed = sum(1 for check in checks if check.status == "fail")

    lines = [
        "# Publication Readiness Report",
        "",
        f"Repository: {REPO_URL}",
        f"Total checks: {total}",
        f"Passed: {passed}",
        f"Warnings: {warnings}",
        f"Failed: {failed}",
        "",
        "## Streamlit Deployment Values",
        "",
    ]

    for key, value in deployment_values().items():
        lines.append(f"- {key}: {value}")

    lines.extend(
        [
            "",
            "## Suggested Repository Topics",
            "",
            ", ".join(EXPECTED_TOPICS),
            "",
            "## Optional GitHub Metadata Command",
            "",
            "Run only after GitHub CLI authentication has repository administration permission:",
            "",
            f"    {suggested_topic_command()}",
            "",
            "## Checks",
            "",
            "| Check | Status | Details |",
            "|---|---:|---|",
        ]
    )

    for check in checks:
        safe_details = check.details.replace("|", "/").replace("\n", "<br>")
        lines.append(f"| {check.name} | {check.status} | {safe_details} |")

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "Failed file checks should be fixed before portfolio sharing. GitHub CLI warnings may be acceptable when local credentials do not have repository administration permission.",
            "",
        ]
    )

    return "\n".join(lines)


def run_checks() -> list[PublicationCheck]:
    checks: list[PublicationCheck] = []
    checks.extend(check_expected_files())
    checks.append(check_git_remote())
    checks.append(check_current_branch())
    checks.append(check_working_tree())
    checks.append(check_gh_cli_repo_visibility())
    return checks


def main() -> int:
    checks = run_checks()

    reports_dir = Path("reports")
    reports_dir.mkdir(parents=True, exist_ok=True)

    json_path = reports_dir / "publication_readiness.json"
    md_path = reports_dir / "publication_readiness.md"

    json_path.write_text(json.dumps([asdict(check) for check in checks], indent=2))
    md_path.write_text(build_report(checks))

    failed = [check for check in checks if check.status == "fail"]

    print("Publication readiness report written.")
    print("JSON:", json_path)
    print("Markdown:", md_path)
    print("Failed checks:", len(failed))

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
