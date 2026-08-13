#!/usr/bin/env python3
"""
================================================================================
DDW-X PORTABLE DISTRIBUTION PACKAGER & RELEASE ENGINE (PHASE 10: GENESIS)
================================================================================
Author: DDW-X DevSecOps Core
Purpose: Builds a standalone, zero-leak, portable distribution of the DDW-X
         ecosystem under `dist/DDW-X_Portable/` with launcher scripts.
================================================================================
"""

import os
import sys
import shutil
import time
from pathlib import Path
from typing import List, Dict, Any

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DIST_DIR = ROOT_DIR / "dist"
PORTABLE_DIR = DIST_DIR / "DDW-X_Portable"


def create_portable_distribution() -> Dict[str, Any]:
    print("=" * 80)
    print(" [*] INITIATING DDW-X PHASE 10: THE GENESIS PACKAGER ENGINE")
    print("=" * 80)
    start_time = time.perf_counter()

    # Step 1: Clean/Prepare dist/DDW-X_Portable/
    if PORTABLE_DIR.exists():
        print(f" [*] Preparing release directory: {PORTABLE_DIR}")
        try:
            shutil.rmtree(PORTABLE_DIR, ignore_errors=True)
        except Exception:
            pass

    PORTABLE_DIR.mkdir(parents=True, exist_ok=True)
    print(f" [PASS] Created release directory: {PORTABLE_DIR}")

    # Step 2: Copy src/ directory
    src_source = ROOT_DIR / "src"
    src_target = PORTABLE_DIR / "src"
    if src_source.exists():
        print(f" [*] Copying core engine modules from {src_source} ...")
        shutil.copytree(
            src_source,
            src_target,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo")
        )
        print(f" [PASS] Core modules copied to {src_target}")

    # Step 3: Copy D-csR_Index/ (Database & Topology Map)
    index_source = ROOT_DIR / "D-csR_Index"
    index_target = PORTABLE_DIR / "D-csR_Index"
    index_target.mkdir(parents=True, exist_ok=True)

    db_file = index_source / "zk_private_rag.db"
    top_file = index_source / "zk_topology_map.json"
    key_file = index_source / ".zk_key"

    if db_file.exists():
        print(f" [*] Copying SQLite Database: {db_file.name} ({db_file.stat().st_size / (1024*1024):.2f} MB)...")
        shutil.copy2(db_file, index_target / "zk_private_rag.db")
        print(f" [PASS] Copied {db_file.name}")

    if top_file.exists():
        print(f" [*] Copying Topology Map: {top_file.name} ({top_file.stat().st_size / (1024*1024):.2f} MB)...")
        shutil.copy2(top_file, index_target / "zk_topology_map.json")
        print(f" [PASS] Copied {top_file.name}")

    if key_file.exists():
        print(f" [*] Copying Static ZK Key: {key_file.name} ...")
        shutil.copy2(key_file, index_target / ".zk_key")
        print(f" [PASS] Copied {key_file.name}")

    # Step 4: Copy requirements.txt & DDWX_OPERATIONS_MANUAL.md
    req_file = ROOT_DIR / "requirements.txt"
    if req_file.exists():
        shutil.copy2(req_file, PORTABLE_DIR / "requirements.txt")
        print(f" [PASS] Copied requirements.txt")

    manual_file = ROOT_DIR / "DDWX_OPERATIONS_MANUAL.md"
    if manual_file.exists():
        shutil.copy2(manual_file, PORTABLE_DIR / "DDWX_OPERATIONS_MANUAL.md")
        print(f" [PASS] Copied DDWX_OPERATIONS_MANUAL.md")

    # Step 5: Generate Windows Batch Launchers
    c2_launcher = PORTABLE_DIR / "START_C2_DASHBOARD.bat"
    console_launcher = PORTABLE_DIR / "START_INTERACTIVE_CONSOLE.bat"

    c2_content = """@echo off
title DDW-X COMMAND & CONTROL (C2) DASHBOARD
echo ===============================================================================
echo   DDW-X COMMAND & CONTROL (C2) - ZERO-KNOWLEDGE INTELLIGENCE SUITE
echo ===============================================================================
echo  [*] Launching Threaded C2 Web API Server on port 8080...
echo  [*] Web Dashboard URL: http://127.0.0.1:8080
echo -------------------------------------------------------------------------------
python src/core/api/ddwx_api.py --port 8080
pause
"""

    console_content = """@echo off
title DDW-X TACTICAL CLI CONSOLE
echo ===============================================================================
echo   DDW-X TACTICAL COMMAND LINE INTERFACE (CLI CONSOLE)
echo ===============================================================================
python src/core/rag/ddwx_console.py
pause
"""

    with open(c2_launcher, "w", encoding="utf-8") as f:
        f.write(c2_content)
    print(f" [PASS] Generated Launcher: {c2_launcher.name}")

    with open(console_launcher, "w", encoding="utf-8") as f:
        f.write(console_content)
    print(f" [PASS] Generated Launcher: {console_launcher.name}")

    # Step 6: Workspace Scratch Cleanup
    scratch_dir = ROOT_DIR / "scratch"
    cleaned_count = 0
    if scratch_dir.exists():
        print(f" [*] Cleaning temporary scratch files from {scratch_dir} ...")
        for item in scratch_dir.iterdir():
            # Preserve graph outputs and bulk folders if needed, delete temp scripts and logs
            if item.name.startswith("tmp_") or item.name.endswith(".tmp") or item.name == "omni_bulk":
                if item.is_dir():
                    shutil.rmtree(item, ignore_errors=True)
                else:
                    item.unlink(missing_ok=True)
                cleaned_count += 1
        print(f" [PASS] Cleaned {cleaned_count} temporary stress-test artifacts.")

    elapsed = (time.perf_counter() - start_time) * 1000.0
    print("=" * 80)
    print(f" [SUCCESS] DDW-X PORTABLE DISTRIBUTION PACKAGED IN {elapsed:.2f} ms")
    print(f" [LOCATION] {PORTABLE_DIR}")
    print("=" * 80)

    return {
        "status": "SUCCESS",
        "portable_directory": str(PORTABLE_DIR),
        "launchers": ["START_C2_DASHBOARD.bat", "START_INTERACTIVE_CONSOLE.bat"],
        "elapsed_ms": elapsed
    }


if __name__ == "__main__":
    create_portable_distribution()
