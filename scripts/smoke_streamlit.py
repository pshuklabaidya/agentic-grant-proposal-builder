from __future__ import annotations

import http.client
import os
import subprocess
import sys
import time


APP_PATH = "src/agentic_grant_proposal_builder/app.py"
PORT = int(os.environ.get("AGPB_SMOKE_PORT", "8509"))
HOST = "127.0.0.1"


def wait_for_app(timeout_seconds: int = 30) -> bool:
    deadline = time.time() + timeout_seconds

    while time.time() < deadline:
        try:
            connection = http.client.HTTPConnection(HOST, PORT, timeout=2)
            connection.request("GET", "/")
            response = connection.getresponse()
            body = response.read(512)
            connection.close()

            if response.status in {200, 302, 304} and body is not None:
                return True
        except Exception:
            time.sleep(1)

    return False


def main() -> int:
    command = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        APP_PATH,
        "--server.headless=true",
        f"--server.port={PORT}",
        "--browser.gatherUsageStats=false",
    ]

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    try:
        ok = wait_for_app()
        if not ok:
            print("Streamlit smoke test failed. App did not respond in time.")
            if process.stdout is not None:
                print(process.stdout.read())
            return 1

        print(f"Streamlit smoke test passed at http://{HOST}:{PORT}")
        return 0
    finally:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()


if __name__ == "__main__":
    raise SystemExit(main())
