#!/usr/bin/env python3
import subprocess
import time
import http.client

print(" [*] Starting server...")
server_proc = subprocess.Popen(
    ["python", "src/core/api/ddwx_api.py", "--port", "8080"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)
time.sleep(1.5)

endpoints = [
    "/api/status",
    "/api/search?q=kernel+driver&top_k=3",
    "/api/search?q=AST+security+linters&top_k=3",
    "/api/blackboard/list",
    "/api/graph"
]

try:
    for ep in endpoints:
        t0 = time.perf_counter()
        conn = http.client.HTTPConnection("127.0.0.1", 8080, timeout=5.0)
        conn.request("GET", ep, headers={"Connection": "close"})
        resp = conn.getresponse()
        data = resp.read()
        conn.close()
        elapsed = (time.perf_counter() - t0) * 1000.0
        print(f" [*] {ep} -> Status: {resp.status}, Len: {len(data)}, Time: {elapsed:.2f} ms")
finally:
    server_proc.terminate()
    try:
        server_proc.wait(timeout=2)
    except Exception:
        server_proc.kill()
