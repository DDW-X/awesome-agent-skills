#!/usr/bin/env python3
"""
================================================================================
DDW-X COURIER HOTFIX LIVE VERIFICATION SUITE (PHASE 11.1)
================================================================================
Module: scratch/test_courier_hotfix.py
Architect: Principal AI Architect & Lead DevSecOps Engineer

VERIFICATION SCOPE:
1. Static Fernet Key Synchronization across API and Courier CLI
2. Sealing raw payloads via DDWXTelemetryEngine and unsealing via CLI subprocess
3. High-visibility diagnostic error output verification (InvalidToken diagnostic tracing)
4. End-to-end C2 REST API integration test (/api/diagnostic/seal)
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

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.core.api.ddwx_api import DDWXTelemetryEngine, KEY_FILE
from src.core.rag.zk_blind_courier import BlindCourierEngine, format_cli_output


def test_key_synchronization():
    print("=" * 80)
    print(" [TEST 1] STATIC KEY SYNCHRONIZATION VERIFICATION")
    print("=" * 80)
    
    assert KEY_FILE.exists(), f"Key file does not exist at {KEY_FILE}"
    with open(KEY_FILE, "rb") as f:
        raw_key = f.read().strip()
    
    print(f" [*] Static Key Location : {KEY_FILE}")
    print(f" [*] Key Byte Length     : {len(raw_key)} bytes")
    assert len(raw_key) == 44, f"Invalid key length: {len(raw_key)}"

    courier = BlindCourierEngine(KEY_FILE)
    assert courier.key == raw_key, "Courier key mismatch with static key file!"
    print(" [PASS] Key synchronization verified across components.")


def test_api_sealing_and_cli_execution():
    print("\n" + "=" * 80)
    print(" [TEST 2] API SEALING & CLI UNSEALING EXECUTION")
    print("=" * 80)

    test_intent = "Query endpoint API telemetry and kernel driver hooks for EDR baseline"
    print(f" [*] Raw Intent Payload : '{test_intent}'")

    seal_result = DDWXTelemetryEngine.seal_courier_payload(test_intent)
    assert seal_result.get("status") == "SUCCESS", f"Sealing failed: {seal_result}"
    token = seal_result.get("token")
    print(f" [*] Generated Token    : {token}")
    assert token, "Token is empty"

    # Execute via CLI subprocess
    print(" [*] Executing zk_blind_courier.py --run via subprocess...")
    t0 = time.perf_counter()
    proc = subprocess.run(
        [sys.executable, "src/core/rag/zk_blind_courier.py", "--run", token],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        errors="replace",
        check=True
    )
    elapsed = (time.perf_counter() - t0) * 1000.0

    print(f" [*] Process Exit Code  : {proc.returncode}")
    print(f" [*] Execution Time     : {elapsed:.2f} ms")
    print("\n" + "=" * 80)
    print(" [CLI STDOUT RECEIPT]")
    print("=" * 80)
    print(proc.stdout.strip())
    print("=" * 80)

    assert "• Status            : SUCCESS" in proc.stdout, "Missing SUCCESS status in CLI output"
    assert "• Diagnostic Session: COURIER-ENCLAVE-" in proc.stdout, "Missing diagnostic session"
    assert "[AUTHORITATIVE DIAGNOSTIC POINTERS RETRIEVED]" in proc.stdout, "Missing pointers header"
    assert "Verified Local Diagnostic Complete: Session Secured." in proc.stdout, "Missing completion statement"
    print(" [PASS] CLI successfully unsealed payload and executed retrieval.")


def test_error_visibility_patch():
    print("\n" + "=" * 80)
    print(" [TEST 3] ERROR VISIBILITY & EXCEPTION TRACING")
    print("=" * 80)

    corrupted_token = "gAAAAABqfR5SKZ89invalidCorruptedTokenPayload1234567890=="
    print(f" [*] Testing Corrupted Token : {corrupted_token}")

    proc = subprocess.run(
        [sys.executable, "src/core/rag/zk_blind_courier.py", "--run", corrupted_token],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        errors="replace"
    )

    print(f" [*] Process Exit Code : {proc.returncode}")
    print("\n" + "=" * 80)
    print(" [CLI ERROR RECEIPT OUTPUT]")
    print("=" * 80)
    print(proc.stdout.strip())
    print("=" * 80)

    assert "• Status            : ERROR" in proc.stdout, "Expected Status: ERROR"
    assert "• Diagnostic Error :" in proc.stdout, "Missing '• Diagnostic Error :' line in receipt"
    assert "InvalidToken" in proc.stdout or "Error" in proc.stdout, "Expected exception details in output"
    assert "Diagnostic Failed: Local Subsystem Error Detected." in proc.stdout, "Missing failure statement"
    print(" [PASS] Error visibility patch verified with explicit Diagnostic Error line.")


def test_rest_api_end_to_end():
    print("\n" + "=" * 80)
    print(" [TEST 4] LIVE REST API END-TO-END TELEMETRY")
    print("=" * 80)

    port = 8089
    server_proc = subprocess.Popen(
        [sys.executable, "src/core/api/ddwx_api.py", "--port", str(port)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    time.sleep(2.0)

    try:
        url = f"http://127.0.0.1:{port}/api/diagnostic/seal"
        payload = json.dumps({"intent": "Validate memory integrity across ring-0 hooks"}).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json", "Connection": "close"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=5.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        print(f" [*] API Status Code: 200 OK")
        print(f" [*] API Response   : {data}")
        assert data.get("status") == "SUCCESS", "API status was not SUCCESS"
        
        token = data.get("token")
        proc = subprocess.run(
            [sys.executable, "src/core/rag/zk_blind_courier.py", "--run", token],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
            errors="replace",
            check=True
        )
        assert "• Status            : SUCCESS" in proc.stdout, "CLI run of API token failed"
        print(" [PASS] Full REST API -> CLI Telemetry pipeline verified.")
    finally:
        server_proc.terminate()
        try:
            server_proc.wait(timeout=2)
        except Exception:
            server_proc.kill()


def main():
    print("=" * 80)
    print(" [*] INITIATING DDW-X ABSOLUTE VERIFICATION LOOP: PHASE 11.1 HOTFIX")
    print("=" * 80)
    t_start = time.perf_counter()

    test_key_synchronization()
    test_api_sealing_and_cli_execution()
    test_error_visibility_patch()
    test_rest_api_end_to_end()

    total_time = (time.perf_counter() - t_start) * 1000.0
    print("\n" + "=" * 80)
    print(f" [ALL PASS] ABSOLUTE VERIFICATION LOOP COMPLETED IN {total_time:.2f} ms")
    print("=" * 80)


if __name__ == "__main__":
    main()
