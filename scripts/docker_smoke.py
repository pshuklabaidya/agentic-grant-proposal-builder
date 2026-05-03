from __future__ import annotations

import http.client
import shutil
import subprocess
import time


IMAGE_NAME = "agentic-grant-proposal-builder:local"
CONTAINER_NAME = "agentic-grant-proposal-builder-smoke"
HOST = "127.0.0.1"
HOST_PORT = 8510
CONTAINER_PORT = 8501


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, capture_output=True, text=True, check=False)


def wait_for_container(timeout_seconds: int = 45) -> bool:
    deadline = time.time() + timeout_seconds

    while time.time() < deadline:
        try:
            connection = http.client.HTTPConnection(HOST, HOST_PORT, timeout=2)
            connection.request("GET", "/")
            response = connection.getresponse()
            response.read(512)
            connection.close()

            if response.status in {200, 302, 304}:
                return True
        except Exception:
            time.sleep(1)

    return False


def main() -> int:
    if shutil.which("docker") is None:
        print("Docker CLI not found. Docker smoke test skipped.")
        return 0

    cleanup = run(["docker", "rm", "-f", CONTAINER_NAME])
    if cleanup.returncode not in {0, 1}:
        print(cleanup.stdout)
        print(cleanup.stderr)

    build = run(["docker", "build", "-t", IMAGE_NAME, "."])
    print(build.stdout)
    if build.returncode != 0:
        print(build.stderr)
        return build.returncode

    run_result = run(
        [
            "docker",
            "run",
            "-d",
            "--name",
            CONTAINER_NAME,
            "-p",
            f"{HOST_PORT}:{CONTAINER_PORT}",
            IMAGE_NAME,
        ]
    )
    print(run_result.stdout)
    if run_result.returncode != 0:
        print(run_result.stderr)
        return run_result.returncode

    try:
        if wait_for_container():
            print(f"Docker smoke test passed at http://{HOST}:{HOST_PORT}")
            return 0

        logs = run(["docker", "logs", CONTAINER_NAME])
        print("Docker smoke test failed. Container logs:")
        print(logs.stdout)
        print(logs.stderr)
        return 1
    finally:
        run(["docker", "rm", "-f", CONTAINER_NAME])


if __name__ == "__main__":
    raise SystemExit(main())
