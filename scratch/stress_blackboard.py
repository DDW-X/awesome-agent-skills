#!/usr/bin/env python3
import json
import subprocess

print("=" * 80)
print("[STRESS 1A: Pull Non-Existent Task]")
print("=" * 80)
subprocess.run(["python", "src/core/rag/zk_swarm_blackboard.py", "--pull", "--task-id", "Task-NonExistent-404"])

print("\n" + "=" * 80)
print("[STRESS 1B: Push Massive 50KB Payload via File]")
print("=" * 80)
big_data = {"buffer": "A" * 50000, "items": list(range(500))}
with open("scratch/big_payload.json", "w") as f:
    json.dump(big_data, f)

subprocess.run([
    "python", "src/core/rag/zk_swarm_blackboard.py",
    "--push", "--task-id", "Task-Stress-50K",
    "--agent", "Agent-Stress", "--key", "heavy_payload",
    "--value-file", "scratch/big_payload.json",
    "--encrypt"
])

print("\n" + "=" * 80)
print("[STRESS 1C: Pull Massive Encrypted Payload]")
print("=" * 80)
res = subprocess.run([
    "python", "src/core/rag/zk_swarm_blackboard.py",
    "--pull", "--task-id", "Task-Stress-50K",
    "--key", "heavy_payload", "--json"
], capture_output=True, text=True)

pulled_json = json.loads(res.stdout)
val = pulled_json["entries"][0]["value"]
print(f"[*] Pulled Status: SUCCESS")
print(f"[*] Buffer Length: {len(val.get('buffer', ''))} characters")
print(f"[*] Items Count  : {len(val.get('items', []))}")
print(f"[*] Is Encrypted : {pulled_json['entries'][0]['is_encrypted']}")
