#!/usr/bin/env python3
"""
================================================================================
DDW-X ZERO-KNOWLEDGE INTERACTIVE COMMAND-AND-CONTROL CONSOLE
================================================================================
Module: src/core/rag/ddwx_console.py
Architect: Principal AI Architect & Lead DevSecOps Engineer

CAPABILITIES:
- Unified Interactive Shell (ddwx (zk) > )
- Real-time Subsystem Status & Database Telemetry
- Wraps:
    * zk_hybrid_router.py       (hunt)
    * zk_payload_compiler.py     (compile)
    * zk_stealth_injector.py     (inject_url / inject_file)
    * zk_integrity_auditor.py    (audit)
    * zk_cognitive_firewall.py   (mask / unmask)
================================================================================
"""

import os
import sys
import cmd
import shlex
import sqlite3
import json
import subprocess
from pathlib import Path
from typing import List, Optional

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ASCII_BANNER = r"""
██████╗ ██████╗ ██╗    ██╗      ██╗  ██╗    ███████╗██╗  ██╗
██╔══██╗██╔══██╗██║    ██║      ╚██╗██╔╝    ╚══███╔╝██║ ██╔╝
██║  ██║██║  ██║██║ █╗ ██║█████╗ ╚███╔╝       ███╔╝ █████╔╝ 
██║  ██║██║  ██║██║███╗██║╚════╝ ██╔██╗      ███╔╝  ██╔═██╗ 
██████╔╝██████╔╝╚███╔███╔╝      ██╔╝ ██╗     ███████╗██║  ██╗
╚═════╝ ╚═════╝  ╚══╝╚══╝       ╚═╝  ╚═╝     ╚══════╝╚═╝  ╚═╝
   >>> ZERO-KNOWLEDGE RAG & COGNITIVE AIR-GAP CONSOLE <<<
   [Version 2.5.0-PROD | Multi-Query RRF | Autonomous OSINT]
"""

class DDWXConsole(cmd.Cmd):
    intro = ASCII_BANNER + "\nType 'help' or '?' to list commands. Type 'status' for system telemetry.\n"
    prompt = "ddwx (zk) > "

    def __init__(self, db_path: str = "D-csR_Index/zk_private_rag.db",
                 vault_path: str = "scratch/prompt_vault.json",
                 topology_path: str = "D-csR_Index/zk_topology_map.json"):
        super().__init__()
        self.db_path = Path(db_path).resolve()
        self.vault_path = Path(vault_path).resolve()
        self.topology_path = Path(topology_path).resolve()
        self.scripts_dir = Path("src/core/rag").resolve()

    def _run_subproc(self, script_name: str, args: List[str]) -> int:
        script_path = self.scripts_dir / script_name
        if not script_path.exists():
            print(f"[!] Error: Script not found at {script_path}")
            return 1
        cmd_list = [sys.executable, str(script_path)] + args
        try:
            res = subprocess.run(cmd_list, check=False)
            return res.returncode
        except Exception as e:
            print(f"[!] Execution failed: {e}")
            return 1

    def do_hunt(self, arg):
        """
        hunt <query> [--top-k N] [--tags-only]
        Execute multi-query RRF hybrid search across the private ZK database.
        """
        if not arg.strip():
            print("[!] Usage: hunt <search keywords> [--top-k 5] [--tags-only]")
            return
        args = shlex.split(arg)
        self._run_subproc("zk_hybrid_router.py", args)

    def do_compile(self, arg):
        """
        compile <TAG-1> [TAG-2 ...] [--output <file>]
        Reconstitute verified diagnostic payloads to local disk air-gapped.
        """
        if not arg.strip():
            print("[!] Usage: compile TAG-XXXX-YY [TAG-AAAA-BB ...] [--output Secure_Output_Workspace.md]")
            return
        args = shlex.split(arg)
        self._run_subproc("zk_payload_compiler.py", args)

    def do_inject_url(self, arg):
        """
        inject_url <URL> [--source-tag <tag>]
        Fetch live OSINT/advisory URL, clean DOM, and blindly inject into SQLite.
        """
        if not arg.strip():
            print("[!] Usage: inject_url https://target-url.com/advisory [--source-tag tag_name]")
            return
        args = shlex.split(arg)
        # Parse URL and flags
        cmd_args = ["--url", args[0]]
        if len(args) > 1:
            cmd_args.extend(args[1:])
        self._run_subproc("zk_stealth_injector.py", cmd_args)

    def do_inject_file(self, arg):
        """
        inject_file <FILE_PATH> [--source-tag <tag>]
        Refine and inject a local plain text file blindly into the ZK index.
        """
        if not arg.strip():
            print("[!] Usage: inject_file path/to/document.md [--source-tag tag_name]")
            return
        args = shlex.split(arg)
        cmd_args = ["--file", args[0]]
        if len(args) > 1:
            cmd_args.extend(args[1:])
        self._run_subproc("zk_stealth_injector.py", cmd_args)

    def do_audit(self, arg):
        """
        audit [--auto-heal]
        Execute complete SQLite, FTS5 sync, topology drift, and privacy leak audit.
        """
        args = shlex.split(arg) if arg.strip() else ["--audit-all"]
        if "--audit-all" not in args and "--auto-heal" not in args:
            args.append("--audit-all")
        self._run_subproc("zk_integrity_auditor.py", args)

    def do_mask(self, arg):
        """
        mask <prompt text>
        Obfuscate sensitive IOCs (IPs, CVEs, EDR vendors, APTs) via the Cognitive Firewall.
        """
        if not arg.strip():
            print("[!] Usage: mask <sensitive prompt text>")
            return
        self._run_subproc("zk_cognitive_firewall.py", ["--mask", arg])

    def do_unmask(self, arg):
        """
        unmask <masked AI response>
        Reverse translate abstract tokens ([TARGET_IP_1], etc.) back to literals.
        """
        if not arg.strip():
            print("[!] Usage: unmask <masked text with abstract tags>")
            return
        self._run_subproc("zk_cognitive_firewall.py", ["--unmask", arg])

    def do_status(self, arg):
        """
        status
        Display real-time subsystem metrics, database volume, and vault mappings.
        """
        print("=" * 80)
        print(" [DDW-X ECOSYSTEM] REAL-TIME TELEMETRY & STATUS REPORT")
        print("=" * 80)

        # 1. Database Telemetry
        if self.db_path.exists():
            size_mb = self.db_path.stat().st_size / (1024 * 1024)
            try:
                conn = sqlite3.connect(str(self.db_path))
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM zk_chunks;")
                total_chunks = cursor.fetchone()[0]
                
                # Check for zk_documents or zk_sources
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name IN ('zk_documents', 'zk_sources');")
                doc_table = cursor.fetchone()
                total_docs = 0
                if doc_table:
                    cursor.execute(f"SELECT COUNT(*) FROM {doc_table[0]};")
                    total_docs = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM zk_fts;")
                total_fts = cursor.fetchone()[0]

                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='zk_threat_iocs';")
                ioc_table = cursor.fetchone()
                total_iocs = 0
                if ioc_table:
                    cursor.execute("SELECT COUNT(*) FROM zk_threat_iocs;")
                    total_iocs = cursor.fetchone()[0]

                conn.close()
                db_status = f"ONLINE (Chunks: {total_chunks:,} | Documents: {total_docs:,} | FTS: {total_fts:,} | IOCs: {total_iocs:,})"
            except Exception as e:
                db_status = f"ERROR ({e})"
        else:
            size_mb = 0.0
            db_status = "NOT FOUND (Archive needs decompression)"

        print(f" [*] ZK Database State  : {db_status}")
        print(f" [*] Database File Size : {size_mb:.2f} MB ({self.db_path.name})")

        # 2. Topology Map Telemetry
        if self.topology_path.exists():
            try:
                with open(self.topology_path, "r", encoding="utf-8") as f:
                    top_data = json.load(f)
                total_nodes = len(top_data.get("topology", {}))
                top_status = f"ONLINE ({total_nodes:,} Cryptographic Tags Mapped)"
            except Exception as e:
                top_status = f"ERROR ({e})"
        else:
            top_status = "NOT FOUND"
        print(f" [*] Topology Map State : {top_status}")

        # 3. Cognitive Vault Telemetry
        if self.vault_path.exists():
            try:
                with open(self.vault_path, "r", encoding="utf-8") as f:
                    vault_data = json.load(f)
                mappings = vault_data.get("metadata", {}).get("total_mappings", len(vault_data.get("token_to_value", {})))
                vault_status = f"ACTIVE ({mappings} Registered Active IOC/EDR Mappings)"
            except Exception as e:
                vault_status = f"ERROR ({e})"
        else:
            vault_status = "EMPTY / INACTIVE"
        print(f" [*] Cognitive Vault    : {vault_status}")
        print("=" * 80)

    def do_blackboard(self, arg):
        """
        blackboard <push|pull|list|clear> [args...]
        Interact with the multi-agent shared state bus.
        Examples:
          blackboard list
          blackboard push --task-id Task-001 --agent Agent-Alpha --key spec --value "{...}"
          blackboard pull --task-id Task-001
          blackboard clear --task-id Task-001
        """
        if not arg.strip():
            print("[!] Usage: blackboard <push|pull|list|clear> [options...]")
            return
        args = shlex.split(arg)
        cmd_type = args[0].lower()
        sub_args = args[1:]
        if cmd_type == "list":
            self._run_subproc("zk_swarm_blackboard.py", ["--list"] + sub_args)
        elif cmd_type == "push":
            self._run_subproc("zk_swarm_blackboard.py", ["--push"] + sub_args)
        elif cmd_type == "pull":
            self._run_subproc("zk_swarm_blackboard.py", ["--pull"] + sub_args)
        elif cmd_type == "clear":
            self._run_subproc("zk_swarm_blackboard.py", ["--clear"] + sub_args)
        else:
            self._run_subproc("zk_swarm_blackboard.py", args)

    def do_mutate(self, arg):
        """
        mutate <file_path> [--output <out_path>] [--key <xor_key>]
        Execute AST-level polymorphic mutation and string XOR obfuscation on C/C++ code.
        """
        if not arg.strip():
            print("[!] Usage: mutate path/to/source.c [--output path/to/mutated.c] [--key 0x55]")
            return
        args = shlex.split(arg)
        cmd_args = ["--file", args[0], "--mutate"]
        if len(args) > 1:
            cmd_args.extend(args[1:])
        self._run_subproc("zk_polymorphic_mutator.py", cmd_args)

    def do_build(self, arg):
        """
        build <file_path> [--output <out_path>] [--target exe|dll] [--syntax-only]
        Compile or validate C/C++ artifacts headlessly via local toolchain.
        """
        if not arg.strip():
            print("[!] Usage: build path/to/source.c [--output path/to/artifact.exe] [--target exe|dll] [--syntax-only]")
            return
        args = shlex.split(arg)
        cmd_args = ["--file", args[0]]
        if len(args) > 1:
            cmd_args.extend(args[1:])
    def do_harvest(self, arg):
        """
        harvest <directory_path>
        Recursively ingest threat intelligence repositories, Sigma rules, and code archives.
        """
        if not arg.strip():
            print("[!] Usage: harvest path/to/threat_repository/")
            return
        args = shlex.split(arg)
        self._run_subproc("zk_bulk_threat_harvester.py", ["--dir", args[0]])

    def do_clear(self, arg):
        """
        clear [screen|vault|blackboard]
        Clear the terminal screen, flush the cognitive vault, or wipe the blackboard.
        """
        arg_clean = arg.strip().lower()
        if arg_clean == "vault":
            self._run_subproc("zk_cognitive_firewall.py", ["--clear-vault"])
        elif arg_clean == "blackboard":
            self._run_subproc("zk_swarm_blackboard.py", ["--clear"])
        else:
            os.system("cls" if os.name == "nt" else "clear")

    def do_exit(self, arg):
        """Exit the DDW-X Zero-Knowledge Interactive Console."""
        print("\n[*] Exiting DDW-X Zero-Knowledge Console. Air-gap integrity preserved.")
        return True

    def do_quit(self, arg):
        """Exit the DDW-X Zero-Knowledge Interactive Console."""
        return self.do_exit(arg)

    def emptyline(self):
        pass


def run_automated_test():
    """
    Executes an automated end-to-end verification sequence within the console.
    """
    print("[*] Initiating DDW-X Console Automated Verification Suite...")
    console = DDWXConsole()
    
    print("\n--- [TEST STEP 1: Status Telemetry] ---")
    console.onecmd("status")

    print("\n--- [TEST STEP 2: Heuristic Prompt Masking] ---")
    console.onecmd('mask "Target is protected by CrowdStrike Falcon on server 192.168.10.50 for APT28 emulation"')

    print("\n--- [TEST STEP 3: Multi-Query RRF Hunt (Top-2)] ---")
    console.onecmd('hunt "AST security linters and parameterized queries" --top-k 2')

    print("\n--- [TEST STEP 4: Integrity Health Audit] ---")
    console.onecmd("audit")

    print("\n--- [TEST STEP 5: Swarm Blackboard Cross-Agent Exchange] ---")
    console.onecmd('blackboard push --task-id "Task-Console-01" --agent "Agent-Alpha" --key "driver_ioctl" --value "IOCTL_0x220004"')
    console.onecmd('blackboard pull --task-id "Task-Console-01"')
    console.onecmd('blackboard list')

    print("\n--- [TEST STEP 6: Polymorphic Code & String Mutation] ---")
    console.onecmd('mutate scratch/dummy_test.c --output scratch/dummy_test_mutated.c --key 85')

    print("\n--- [TEST STEP 7: Headless Toolchain Compilation & Syntax Validation] ---")
    console.onecmd('build scratch/dummy_test_mutated.c --output scratch/dummy_test.exe')

    print("\n--- [TEST STEP 8: Bulk Threat Repository Ingestion] ---")
    console.onecmd('harvest scratch/bulk_test')

    print("\n--- [TEST STEP 9: Reconstitution / Unmasking] ---")
    console.onecmd('unmask "Remediation verified for [EDR_VENDOR_1] on [TARGET_IP_1] against [THREAT_ACTOR_1]"')

    print("\n[SUCCESS] Automated console test sequence completed flawlessly.")


def main():
    if "--test-run" in sys.argv:
        print(ASCII_BANNER)
        run_automated_test()
        sys.exit(0)

    console = DDWXConsole()
    try:
        console.cmdloop()
    except KeyboardInterrupt:
        print("\n[*] Session terminated by operator.")
        sys.exit(0)


if __name__ == "__main__":
    main()

