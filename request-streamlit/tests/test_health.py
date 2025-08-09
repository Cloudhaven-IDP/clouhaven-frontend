import multiprocessing
import time
import requests
import sys
import os

def _run_flask():
    # make sure import path works
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from src import health
    health.app.run(host="127.0.0.1", port=5055)

def test_health_and_ready():
    proc = multiprocessing.Process(target=_run_flask)
    proc.start()
    try:
        # give Flask a moment to start
        time.sleep(1)
        for endpoint in ("/health", "/ready"):
            r = requests.get(f"http://127.0.0.1:5055{endpoint}", timeout=3)
            assert r.status_code == 200
            assert r.text.strip() in ("OK", "READY")
    finally:
        proc.terminate()
        proc.join()
