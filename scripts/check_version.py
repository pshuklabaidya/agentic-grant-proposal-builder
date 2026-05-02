from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class VersionCheck:
    name: str
    status: str
    details: str


def read_pyproject_version() -> str:
    data = tomllib.loads(Path("pyproject.toml").read_text())
    return str(data["project"]["version"])


def read_package_version() -> str:
    text = Path("src/agentic_grant_proposal_builder/__init__.py").read_text()
    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', text)

    if not match:
        return ""

    return match.group(1)


def changelog_contains_version(version: str) -> bool:
    path = Path("CHANGELOG.md")
    if not path.exists():
        return False

    return f"## [{version}]" in path.read_text()


def release_checklist_contains_version(version: str) -> bool:
    path = Path("docs/RELEASE_CHECKLIST.md")
    if not path.exists():
        return False

    return version in path.read_text()


def semver_like(version: str) -> bool:
    return bool(re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][A-Za-z0-9.-]+)?", version))


def run_checks() -> list[VersionCheck]:
    checks: list[VersionCheck] = []

    pyproject_version = read_pyproject_version()
    package_version = read_package_version()

    checks.append(
        VersionCheck(
            name="pyproject_version_present",
            status="pass" if pyproject_version else "fail",
            details=pyproject_version or "missing",
        )
    )

    checks.append(
        VersionCheck(
            name="package_version_present",
            status="pass" if package_version else "fail",
            details=package_version or "missing",
        )
    )

    checks.append(
        VersionCheck(
            name="versions_match",
            status="pass" if pyproject_version == package_version else "fail",
            details=f"pyproject={pyproject_version}, package={package_version}",
        )
    )

    checks.append(
        VersionCheck(
            name="semver_like_version",
            status="pass" if semver_like(pyproject_version) else "fail",
            details=pyproject_version,
        )
    )

    checks.append(
        VersionCheck(
            name="changelog_mentions_version",
            status="pass" if changelog_contains_version(pyproject_version) else "fail",
            details=f"CHANGELOG.md contains ## [{pyproject_version}]",
        )
    )

    checks.append(
        VersionCheck(
            name="release_checklist_mentions_version",
            status="pass" if release_checklist_contains_version(pyproject_version) else "fail",
            details=f"docs/RELEASE_CHECKLIST.md contains {pyproject_version}",
        )
    )

    return checks


def main() -> int:
    checks = run_checks()

    print("Version consistency checks:")
    for check in checks:
        print(f"- {check.name}: {check.status} - {check.details}")

    failed = [check for check in checks if check.status != "pass"]

    if failed:
        print(f"Failed checks: {len(failed)}")
        return 1

    print("All version checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
