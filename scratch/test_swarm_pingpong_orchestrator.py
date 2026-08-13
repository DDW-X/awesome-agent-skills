#!/usr/bin/env python3
"""
================================================================================
DDW-X PHASE 12: SWARM ORCHESTRATOR & PING-PONG EXECUTION LOOP VERIFICATION SUITE
================================================================================
Module: scratch/test_swarm_pingpong_orchestrator.py
Architect: Principal AI Architect & Lead DevSecOps Engineer

TEST SCOPE:
1. Dynamic Agent Action Plan & Directive Generation from zk_blind_courier.py
2. Polymorphic Code Mutation (Watermarking, Dual-XOR Obfuscation, CFF Dispatcher)
3. Headless Toolchain Compilation & Forensic Bill of Materials (FBOM) Generation
4. Swarm Blackboard Shared Memory State Bus Publication and Retrieval
5. End-to-End Autonomous Ping-Pong Pipeline Orchestration
================================================================================
"""

import sys
import json
import time
import subprocess
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.core.rag.zk_blind_courier import BlindCourierEngine
from src.core.rag.zk_polymorphic_mutator import PolymorphicMutator
from src.core.rag.zk_local_toolchain_builder import ToolchainBuilder
from src.core.rag.zk_swarm_blackboard import SwarmBlackboard


def test_dynamic_courier_action_plan():
    print("=" * 80)
    print(" [TEST 1] COURIER DYNAMIC AGENT ACTION PLAN & DIRECTIVE GENERATION")
    print("=" * 80)

    engine = BlindCourierEngine()
    intent = "Process telemetry standard template through full DDW-X pipeline"
    token = engine.seal(intent)
    assert token, "Failed to seal intent"
    print(f" [*] Sealed Token: {token[:32]}...")

    result = engine.execute_blind_query(token)
    assert result.get("status") == "SUCCESS", f"Query failed: {result}"
    assert "agent_directive" in result, "Missing 'agent_directive' in result"
    assert "action_plan" in result, "Missing 'action_plan' in result"
    assert len(result["action_plan"]) == 3, f"Expected 3 steps, got {len(result['action_plan'])}"

    print(f" [*] Enclave Session : {result['enclave_session']}")
    print(f" [*] Agent Directive : {result['agent_directive']}")
    for step in result["action_plan"]:
        print(f"     Step {step['step']}: {step['action']}")
        print(f"     Command: {step['command']}")

    # Verify CLI output formatting
    proc = subprocess.run(
        [sys.executable, "-u", "src/core/rag/zk_blind_courier.py", "--run", token],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        errors="replace",
        check=True
    )
    assert "[TELEMETRY DATA FETCHED]" in proc.stdout, "Missing [TELEMETRY DATA FETCHED]"
    assert "[AGENT DIRECTIVE]:" in proc.stdout, "Missing [AGENT DIRECTIVE]:"
    assert "[DYNAMIC AGENT ACTION PLAN]:" in proc.stdout, "Missing [DYNAMIC AGENT ACTION PLAN]:"
    print(" [PASS] Dynamic Agent Action Plan and Directives verified.")


def test_polymorphic_mutation():
    print("\n" + "=" * 80)
    print(" [TEST 2] POLYMORPHIC AST MUTATION & FORENSIC ATTRIBUTION")
    print("=" * 80)

    src_file = ROOT_DIR / "scratch" / "dummy_telemetry.c"
    mut_file = ROOT_DIR / "scratch" / "mutated_telemetry.c"
    assert src_file.exists(), f"Source file not found: {src_file}"

    proc = subprocess.run(
        [sys.executable, "-u", "src/core/rag/zk_polymorphic_mutator.py", "-f", str(src_file), "-o", str(mut_file), "--mutate"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        errors="replace",
        check=True
    )
    assert mut_file.exists(), f"Mutated file not created at {mut_file}"
    with open(mut_file, "r", encoding="utf-8") as f:
        mut_code = f.read()

    assert "_ddwx_watermark_sig" in mut_code, "Missing watermark signature in mutated code"
    assert "_ddwx_provenance_id" in mut_code, "Missing provenance ID in mutated code"
    assert "_zk_decode_layer2" in mut_code, "Missing dual-XOR decoder function"
    assert "_cff_state" in mut_code, "Missing CFF state machine dispatcher"
    print(f" [*] Mutated Code Size : {len(mut_code)} bytes")
    print(" [PASS] Polymorphic AST mutation verified.")


def test_headless_toolchain_builder():
    print("\n" + "=" * 80)
    print(" [TEST 3] HEADLESS TOOLCHAIN COMPILATION & FBOM GENERATION")
    print("=" * 80)

    mut_file = ROOT_DIR / "scratch" / "mutated_telemetry.c"
    bin_file = ROOT_DIR / "scratch" / "telemetry.exe"
    fbom_file = ROOT_DIR / "scratch" / "telemetry.fbom.json"

    proc = subprocess.run(
        [sys.executable, "-u", "src/core/rag/zk_local_toolchain_builder.py", "-f", str(mut_file), "-o", str(bin_file), "--arch", "x64"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        errors="replace",
        check=True
    )
    assert bin_file.exists(), f"Binary artifact not created: {bin_file}"
    assert fbom_file.exists(), f"FBOM metadata not created: {fbom_file}"

    with open(fbom_file, "r", encoding="utf-8") as f:
        fbom_data = json.load(f)

    assert fbom_data.get("build_status") == "SUCCESS", f"FBOM build status not SUCCESS: {fbom_data}"
    assert fbom_data.get("target_architecture") == "X64", "Incorrect target architecture"
    assert fbom_data.get("artifact_name") == "telemetry.exe", "Incorrect artifact name in FBOM"
    print(f" [*] Generated FBOM Artifact SHA256: {fbom_data.get('artifact_sha256')}")
    print(f" [*] Source SHA256 in FBOM         : {fbom_data.get('source_sha256')}")
    print(" [PASS] Toolchain compilation and FBOM audit verified.")


def test_swarm_blackboard_synchronization():
    print("\n" + "=" * 80)
    print(" [TEST 4] SWARM BLACKBOARD TRANSACTIONAL STATE BUS PUBLICATION")
    print("=" * 80)

    task_id = "TASK-SWARM-TEST-PHASE12"
    agent = "Agent-Orchestrator"
    key = "telemetry_fbom"
    fbom_file = ROOT_DIR / "scratch" / "telemetry.fbom.json"

    # Push to Blackboard
    proc_push = subprocess.run(
        [
            sys.executable, "-u", "src/core/rag/zk_swarm_blackboard.py",
            "--push", "--task-id", task_id, "--agent", agent,
            "--key", key, "--value-file", str(fbom_file)
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        errors="replace",
        check=True
    )
    assert "[DDW-X SWARM BLACKBOARD] MEMORY PUSH CONFIRMED" in proc_push.stdout

    # Pull from Blackboard
    proc_pull = subprocess.run(
        [
            sys.executable, "-u", "src/core/rag/zk_swarm_blackboard.py",
            "--pull", "--task-id", task_id, "--key", key, "--json"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        errors="replace",
        check=True
    )
    pull_data = json.loads(proc_pull.stdout)
    assert pull_data.get("count", 0) >= 1, "No entries pulled from blackboard"
    entry = pull_data["entries"][0]
    assert entry["task_id"] == task_id
    assert entry["agent_name"] == agent
    assert entry["key"] == key
    assert entry["value"]["fbom_version"] == "1.0-ddwx"
    print(f" [*] Swarm Memory Entry ID: #{entry['id']}")
    print(f" [*] Verified FBOM in Blackboard: {entry['value']['artifact_name']} (Status: {entry['value']['build_status']})")
    print(" [PASS] Swarm Blackboard memory synchronization verified.")


def main():
    print("=" * 80)
    print(" [*] INITIATING DDW-X PHASE 12: SWARM ORCHESTRATOR ABSOLUTE VERIFICATION")
    print("=" * 80)
    t0 = time.perf_counter()

    test_dynamic_courier_action_plan()
    test_polymorphic_mutation()
    test_headless_toolchain_builder()
    test_swarm_blackboard_synchronization()

    elapsed = (time.perf_counter() - t0) * 1000.0
    print("\n" + "=" * 80)
    print(f" [ALL PASS] PHASE 12 VERIFICATION COMPLETED SUCCESSFULLY IN {elapsed:.2f} ms")
    print("=" * 80)


if __name__ == "__main__":
    main()
