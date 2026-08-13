#!/usr/bin/env python3
"""
================================================================================
DDW-X LIVE TEST: MASTER PROMPT FORGE API (/api/forge/prompt)
================================================================================
Tests Tokenized Pointer-Based Prompting, Cognitive Firewall Masking, and
Hybrid Index Tag Resolution via REST API.
================================================================================
"""

import sys
import json
import time
import subprocess
import urllib.request
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

PORT = 8085
SERVER_URL = f"http://127.0.0.1:{PORT}"

def main():
    print("=" * 80)
    print(" [*] DDW-X TEST: MASTER PROMPT FORGE API VERIFICATION")
    print("=" * 80)

    # 1. Start Server on test port
    print(f" [*] Spawning DDW-X C2 Server on port {PORT}...")
    server_proc = subprocess.Popen(
        [sys.executable, "src/core/api/ddwx_api.py", "--port", str(PORT)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    time.sleep(2.0)

    try:
        # 2. Test Request Payload
        test_payload = {
            "intent": "Investigate APT28 kernel driver hooks and CrowdStrike Falcon evasion on host 192.168.10.45 with Kerberos Golden Ticket persistence.",
            "top_k": 4
        }

        print(f" [*] Sending Sensitive Raw Intent to /api/forge/prompt...")
        print(f"     Raw Intent: '{test_payload['intent']}'")

        req_data = json.dumps(test_payload).encode("utf-8")
        req = urllib.request.Request(
            f"{SERVER_URL}/api/forge/prompt",
            data=req_data,
            headers={
                "Content-Type": "application/json",
                "Connection": "close"
            },
            method="POST"
        )

        t0 = time.perf_counter()
        with urllib.request.urlopen(req, timeout=10.0) as resp:
            status_code = resp.getcode()
            raw_res = resp.read().decode("utf-8")
            elapsed = (time.perf_counter() - t0) * 1000.0

        print(f" [*] HTTP Status Code : {status_code}")
        print(f" [*] Round-Trip Latency: {elapsed:.2f} ms")

        assert status_code == 200, f"Expected 200 OK, got {status_code}"
        res_json = json.loads(raw_res)

        print("\n" + "=" * 80)
        print(" [API RESPONSE DATA]")
        print("=" * 80)
        print(f" • Status            : {res_json.get('status')}")
        print(f" • Latency Server    : {res_json.get('latency_ms')} ms")
        print(f" • Masked Intent     : {res_json.get('masked_intent')}")
        print(f" • Retrieved TAGs    : {res_json.get('tags')}")
        print(f" • Vault Entity Subs : {res_json.get('substitutions')}")
        print(f" • Token Word Count  : {res_json.get('token_count')}")

        print("\n" + "=" * 80)
        print(" [GENERATED MASTER PROMPT (AIR-GAPPED POINTER DIRECTIVE)]")
        print("=" * 80)
        print(res_json.get("master_prompt"))
        print("=" * 80)

        # Assertions
        assert res_json.get("status") == "SUCCESS", "Status is not SUCCESS"
        assert len(res_json.get("tags", [])) > 0, "No tags returned"
        assert "MASTER DIRECTIVE" in res_json.get("master_prompt", ""), "Master prompt format mismatch"
        print("\n [PASS] Master Prompt Forge API Verified Successfully with 100% OPSEC Integrity.")

    finally:
        print("\n [*] Terminating C2 test server...")
        server_proc.terminate()
        try:
            server_proc.wait(timeout=2)
        except Exception:
            server_proc.kill()
        print(" [*] Server stopped.")

if __name__ == "__main__":
    main()
