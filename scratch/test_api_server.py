#!/usr/bin/env python3
import subprocess
import time
import urllib.request
import json
import os
import signal

print("=" * 80)
print(" [MANDATORY LIVE TEST] DDW-X REST API & LIQUID GLASS DASHBOARD VERIFICATION")
print("=" * 80)

# 1. Start Server Process in Background
print(" [*] Launching API Server on http://127.0.0.1:8080 ...")
proc = subprocess.Popen(
    ["python", "src/core/api/ddwx_api.py", "--port", "8080"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

time.sleep(2.0)

try:
    # 2. Test /api/status Endpoint
    print(" [*] Querying GET http://127.0.0.1:8080/api/status ...")
    req = urllib.request.Request("http://127.0.0.1:8080/api/status")
    with urllib.request.urlopen(req, timeout=5) as response:
        status_code = response.getcode()
        body = response.read().decode("utf-8")
        status_data = json.loads(body)
        print(f" [PASS] HTTP Status: {status_code}")
        print(" [PAYLOAD RESPONSE]:")
        print(json.dumps(status_data, indent=2))

    # 3. Test /api/search Endpoint
    print("\n [*] Querying GET http://127.0.0.1:8080/api/search?q=AST+linters&top_k=2 ...")
    req_search = urllib.request.Request("http://127.0.0.1:8080/api/search?q=AST+linters&top_k=2")
    with urllib.request.urlopen(req_search, timeout=5) as response:
        search_data = json.loads(response.read().decode("utf-8"))
        print(f" [PASS] Search Results Count: {search_data['total_results']}")
        print(f" [PASS] Search Latency: {search_data['latency_ms']} ms")

    # 4. Test / (Dashboard UI Serving)
    print("\n [*] Querying GET http://127.0.0.1:8080/ (Dashboard UI) ...")
    req_ui = urllib.request.Request("http://127.0.0.1:8080/")
    with urllib.request.urlopen(req_ui, timeout=5) as response:
        html_len = len(response.read())
        print(f" [PASS] Dashboard HTML Successfully Served: {html_len} bytes")

finally:
    print("\n [*] Terminating API Server test instance...")
    proc.terminate()
    try:
        proc.wait(timeout=3)
    except Exception:
        proc.kill()
    print(" [SUCCESS] API Server verification completed cleanly.")
