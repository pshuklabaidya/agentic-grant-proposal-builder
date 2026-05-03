from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path


COMMAND_TIMEOUT_SECONDS = 60


def smoke_environment() -> dict[str, str]:
    env = os.environ.copy()

    env.pop("OPENAI_API_KEY", None)
    env["AGPB_USE_OPENAI_AGENTS"] = "0"
    env["OPENAI_AGENTS_DISABLE_TRACING"] = "1"

    return env


def run_command(command: list[str]) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            timeout=COMMAND_TIMEOUT_SECONDS,
            env=smoke_environment(),
        )
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        return subprocess.CompletedProcess(
            command,
            124,
            stdout if isinstance(stdout, str) else stdout.decode(errors="ignore"),
            stderr if isinstance(stderr, str) else stderr.decode(errors="ignore"),
        )


def require_success(command: list[str]) -> subprocess.CompletedProcess[str]:
    result = run_command(command)

    print("$ " + " ".join(command))
    print(result.stdout)

    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError(f"Command failed with status {result.returncode}: {' '.join(command)}")

    return result


def assert_artifacts_exist(payload_text: str) -> None:
    payload = json.loads(payload_text)

    for key in ["markdown", "json", "summary"]:
        path = Path(payload[key])
        if not path.exists():
            raise RuntimeError(f"Missing expected CLI artifact: {path}")


def main() -> int:
    try:
        require_success(["agpb", "--help"])
        require_success(["agpb", "list-scenarios"])
        require_success(["agpb", "evaluate-scenario", "education_access"])

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "cli_outputs"

            scenario_result = require_success(
                [
                    "agpb",
                    "build-scenario",
                    "education_access",
                    "--output-dir",
                    str(output_dir),
                ]
            )
            assert_artifacts_exist(scenario_result.stdout)

            file_result = require_success(
                [
                    "agpb",
                    "build-files",
                    "--profile",
                    "sample_data/cli_example/profile.json",
                    "--documents",
                    "sample_data/cli_example/funder_guidance.txt",
                    "sample_data/cli_example/program_notes.txt",
                    "--output-dir",
                    str(output_dir),
                    "--stem",
                    "riverbend",
                ]
            )
            assert_artifacts_exist(file_result.stdout)

        print("CLI smoke test passed.")
        return 0

    except Exception as exc:
        print(f"CLI smoke test failed: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
