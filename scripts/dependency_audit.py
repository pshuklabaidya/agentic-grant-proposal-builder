from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


REPORT_JSON = Path("reports/dependency_audit.json")
REPORT_MD = Path("reports/dependency_audit.md")


def run_pip_audit() -> tuple[int, str, str]:
    commands = [
        [sys.executable, "-m", "pip_audit", "--format=json"],
        ["pip-audit", "--format=json"],
    ]

    last_status = 1
    last_stdout = ""
    last_stderr = ""

    for command in commands:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )
        last_status = result.returncode
        last_stdout = result.stdout
        last_stderr = result.stderr

        if result.stdout.strip():
            return last_status, last_stdout, last_stderr

    return last_status, last_stdout, last_stderr


def parse_payload(stdout: str) -> dict[str, Any]:
    try:
        payload = json.loads(stdout)
    except json.JSONDecodeError:
        payload = {"dependencies": [], "raw_output": stdout}

    if not isinstance(payload, dict):
        payload = {"dependencies": [], "raw_output": stdout}

    payload.setdefault("dependencies", [])
    return payload


def vulnerability_rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for dependency in payload.get("dependencies", []):
        name = dependency.get("name", "unknown")
        version = dependency.get("version", "unknown")

        for vulnerability in dependency.get("vulns", []):
            rows.append(
                {
                    "package": name,
                    "version": version,
                    "id": vulnerability.get("id", "unknown"),
                    "fix_versions": ", ".join(vulnerability.get("fix_versions", [])) or "none listed",
                    "description": vulnerability.get("description", "").replace("\n", " ")[:240],
                }
            )

    return rows


def write_reports(payload: dict[str, Any], status: int, stderr: str) -> int:
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)

    rows = vulnerability_rows(payload)
    report_payload = {
        "pip_audit_exit_code": status,
        "vulnerability_count": len(rows),
        "vulnerabilities": rows,
        "stderr": stderr,
    }

    REPORT_JSON.write_text(json.dumps(report_payload, indent=2))

    lines = [
        "# Dependency Audit Report",
        "",
        f"pip-audit exit code: {status}",
        f"Known vulnerability count: {len(rows)}",
        "",
    ]

    if rows:
        lines.extend(
            [
                "## Vulnerabilities",
                "",
                "| Package | Version | Advisory | Fix Versions | Description |",
                "|---|---:|---|---|---|",
            ]
        )

        for row in rows:
            lines.append(
                f"| {row['package']} | {row['version']} | {row['id']} | "
                f"{row['fix_versions']} | {row['description']} |"
            )
    else:
        lines.extend(
            [
                "## Vulnerabilities",
                "",
                "No known vulnerabilities were reported by pip-audit for the audited environment.",
            ]
        )

    if stderr.strip():
        lines.extend(
            [
                "",
                "## Tool Output",
                "",
                stderr.strip()[:2000],
            ]
        )

    REPORT_MD.write_text("\n".join(lines) + "\n")
    return len(rows)


def main() -> int:
    status, stdout, stderr = run_pip_audit()
    payload = parse_payload(stdout)
    vulnerability_count = write_reports(payload, status, stderr)

    print("Dependency audit report written.")
    print("JSON:", REPORT_JSON)
    print("Markdown:", REPORT_MD)
    print("Known vulnerability count:", vulnerability_count)

    strict = os.getenv("AGPB_STRICT_DEPENDENCY_AUDIT", "0") == "1"
    if strict and vulnerability_count > 0:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
