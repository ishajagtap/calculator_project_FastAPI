"""Root conftest.py — provides the live_server_url fixture for E2E tests."""
import subprocess
import sys
import time

import pytest


@pytest.fixture(scope="session")
def live_server_url():
    """Start a uvicorn server for Playwright E2E tests and yield its base URL."""
    port = 8765
    proc = subprocess.Popen(
        [
            sys.executable, "-m", "uvicorn",
            "fastapi_app:app",
            "--host", "127.0.0.1",
            "--port", str(port),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # Poll until the server is ready (max 15 s)
    import urllib.request
    health_url = f"http://127.0.0.1:{port}/health"
    for _ in range(30):
        try:
            urllib.request.urlopen(health_url, timeout=1)
            break
        except Exception:
            time.sleep(0.5)

    yield f"http://127.0.0.1:{port}"

    proc.terminate()
    proc.wait(timeout=10)
