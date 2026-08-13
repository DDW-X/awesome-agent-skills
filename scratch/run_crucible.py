#!/usr/bin/env python3
import subprocess
import time
import sys

print("=" * 80)
print(" [*] INITIATING PHASE 9: THE CRUCIBLE LIVE EXECUTION RUNNER")
print("=" * 80)

print(" [*] Starting DDW-X C2 Server on port 8080...")
server_proc = subprocess.Popen(
    ["python", "src/core/api/ddwx_api.py", "--port", "8080"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

time.sleep(2.0)

try:
    print(" [*] Spawning Omni-Stress Test Suite (Unbuffered Mode)...", flush=True)
    test_proc = subprocess.run(
        [sys.executable, "-u", "scratch/zk_omni_stress_test.py"],
        text=True,
        check=True
    )
finally:
    print("\n [*] Shutting down C2 background server...")
    server_proc.terminate()
    try:
        server_proc.wait(timeout=3)
    except Exception:
        server_proc.kill()
    print(" [*] Server shutdown complete.")
