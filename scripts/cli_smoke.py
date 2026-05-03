from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path


def run_command(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, capture_output=True, text=True, check=False)


def main() -> int:
    commands = [
        ["agpb", "--help"],
        ["agpb", "list-scenarios"],
        ["agpb", "evaluate-scenario", "education_access"],
    ]

    for command in commands:
        result = run_command(command)
        print("$ " + " ".join(command))
        print(result.stdout)
        if result.returncode != 0:
            print(result.stderr)
            return result.returncode

    with tempfile.TemporaryDirectory() as temp_dir:
        output_dir = Path(temp_dir) / "cli_outputs"

        scenario_result = run_command(
            [
                "agpb",
                "build-scenario",
                "education_access",
                "--output-dir",
                str(output_dir),
            ]
        )
        print("$ agpb build-scenario education_access")
        print(scenario_result.stdout)

        if scenario_result.returncode != 0:
            print(scenario_result.stderr)
            return scenario_result.returncode

        payload = json.loads(scenario_result.stdout)
        for key in ["markdown", "json", "summary"]:
            path = Path(payload[key])
            if not path.exists():
                print(f"Missing expected scenario artifact: {path}")
                return 1

        file_result = run_command(
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
        print("$ agpb build-files")
        print(file_result.stdout)

        if file_result.returncode != 0:
            print(file_result.stderr)
            return file_result.returncode

        file_payload = json.loads(file_result.stdout)
        for key in ["markdown", "json", "summary"]:
            path = Path(file_payload[key])
            if not path.exists():
                print(f"Missing expected file-build artifact: {path}")
                return 1

    print("CLI smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
