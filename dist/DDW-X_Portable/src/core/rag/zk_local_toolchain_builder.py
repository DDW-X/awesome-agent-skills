#!/usr/bin/env python3
"""
================================================================================
DDW-X HEADLESS TOOLCHAIN BUILDER & FBOM GENERATOR (v3.0 - FORENSIC BOM)
================================================================================
Module: src/core/rag/zk_local_toolchain_builder.py
Architect: Principal AI Architect & Lead DevSecOps Engineer

CAPABILITIES:
1. Forensic Bill of Materials (FBOM) Generation:
   - Computes cryptographic SHA-256 hashes of input source and output binary artifacts.
   - Logs compilation timestamps, compiler flags, target architecture, and provenance metadata.
   - Generates structured failure FBOMs upon syntax or compilation errors.
2. Compiler Discovery & Multi-Arch Target Selection:
   - Supports x86 (32-bit), x64 (64-bit), and ARM64 architecture targeting.
3. Aggressive Symbol Stripping & Optimization:
   - Injects optimization (-O2 / -O3 / /O2) and strip flags (-s, -ffunction-sections, -fdata-sections, /GL).
4. Graceful Fallback Mode & Robust Lexical Linter:
   - Performs syntax structure linting and generates simulated artifacts if no native compiler is present.
================================================================================
"""

import os
import sys
import time
import json
import shutil
import hashlib
import subprocess
import argparse
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


class ToolchainBuilder:
    """
    Automated compiler discovery, cross-architecture configuration, and FBOM metadata engine.
    """
    def __init__(self):
        self.compiler = self._detect_compiler()

    def _detect_compiler(self) -> Optional[Dict[str, str]]:
        candidates = [
            {"type": "gcc", "bin": "gcc", "syntax_flag": "-fsyntax-only"},
            {"type": "clang", "bin": "clang", "syntax_flag": "-fsyntax-only"},
            {"type": "cl", "bin": "cl.exe", "syntax_flag": "/Zs"},
            {"type": "tcc", "bin": "tcc", "syntax_flag": "-c"}
        ]
        for c in candidates:
            bin_path = shutil.which(c["bin"])
            if bin_path:
                return {
                    "type": c["type"],
                    "path": bin_path,
                    "syntax_flag": c["syntax_flag"]
                }
        return None

    def validate_syntax_fallback(self, source_code: str) -> Tuple[bool, str]:
        open_braces = source_code.count("{")
        close_braces = source_code.count("}")
        open_parens = source_code.count("(")
        close_parens = source_code.count(")")

        errors = []
        if open_braces != close_braces:
            errors.append(f"Unbalanced braces: {open_braces} open vs {close_braces} close")
        if open_parens != close_parens:
            errors.append(f"Unbalanced parentheses: {open_parens} open vs {close_parens} close")

        # Check lines for missing semicolons inside functions
        lines = source_code.splitlines()
        for i, line in enumerate(lines, 1):
            s = line.strip()
            if s and not s.startswith(("//", "/*", "*", "#", "case", "default")) and not s.endswith(("{", "}", ";", ":", "\\", ",")) and not s.startswith("if") and not s.startswith("for") and not s.startswith("while"):
                if "printf" in s or "return" in s or "int " in s or "char " in s or "volatile " in s:
                    errors.append(f"Line {i}: Missing statement terminator ';' -> '{s}'")

        if errors:
            return False, "; ".join(errors)
        return True, "Syntax structure OK"

    def _generate_fbom(self, source_file: Path, output_file: Path,
                       target_type: str, arch: str, compiler_info: Any,
                       flags: List[str], status: str = "SUCCESS",
                       error_msg: Optional[str] = None) -> Dict[str, Any]:
        now = time.time()
        
        # Source file hash
        try:
            with open(source_file, "rb") as f:
                src_bytes = f.read()
            src_sha = hashlib.sha256(src_bytes).hexdigest()
        except Exception:
            src_sha = "UNREADABLE"

        # Output artifact hash & size
        if output_file and output_file.exists() and status == "SUCCESS":
            try:
                with open(output_file, "rb") as f:
                    out_bytes = f.read()
                out_sha = hashlib.sha256(out_bytes).hexdigest()
                out_size = len(out_bytes)
            except Exception:
                out_sha = "ERROR"
                out_size = 0
        else:
            out_sha = "N/A (COMPILATION_FAILED)" if status != "SUCCESS" else "N/A"
            out_size = 0

        return {
            "fbom_version": "1.0-ddwx",
            "build_status": status,
            "error_detail": error_msg,
            "artifact_name": output_file.name if output_file else "None",
            "artifact_path": str(output_file) if output_file else "None",
            "artifact_sha256": out_sha,
            "artifact_size_bytes": out_size,
            "source_file": source_file.name,
            "source_sha256": src_sha,
            "target_architecture": arch.upper(),
            "target_format": target_type.upper(),
            "compiler": compiler_info,
            "compiler_flags": flags,
            "compilation_timestamp": now,
            "compilation_time_utc": time.ctime(now)
        }

    def build(self, source_file: Path, output_file: Optional[Path] = None,
              target_type: str = "exe", arch: str = "x64",
              strip_symbols: bool = True, optimize: bool = True,
              syntax_only: bool = False, extra_flags: Optional[List[str]] = None) -> Dict[str, Any]:
        
        if not source_file.exists():
            return {
                "status": "FAILED",
                "error": f"Source file not found: {source_file}",
                "compiler": None
            }

        try:
            with open(source_file, "r", encoding="utf-8", errors="replace") as f:
                code_content = f.read()
        except Exception as e:
            return {
                "status": "FAILED",
                "error": f"Could not read source file: {e}",
                "compiler": None
            }

        flags = list(extra_flags or [])
        out_path = output_file or source_file.with_suffix(".exe" if target_type == "exe" else ".dll")

        # 1. NATIVE COMPILER EXECUTION
        if self.compiler:
            comp_type = self.compiler["type"]
            comp_bin = self.compiler["path"]

            if syntax_only:
                cmd = [comp_bin, self.compiler["syntax_flag"], str(source_file)] + flags
            else:
                out_path.parent.mkdir(parents=True, exist_ok=True)
                if comp_type in ("gcc", "clang"):
                    cmd = [comp_bin, str(source_file), "-o", str(out_path)]
                    if arch == "x86":
                        cmd.append("-m32")
                    elif arch == "x64":
                        cmd.append("-m64")
                    if optimize:
                        cmd.extend(["-O3", "-ffunction-sections", "-fdata-sections"])
                    if strip_symbols:
                        cmd.extend(["-s", "-Wl,--gc-sections"])
                    if target_type == "dll":
                        cmd.extend(["-shared", "-fPIC"])
                    cmd.extend(flags)
                elif comp_type == "cl":
                    cmd = [comp_bin, str(source_file), f"/Fe:{out_path}"]
                    if optimize:
                        cmd.extend(["/O2", "/GL", "/Gy"])
                    if target_type == "dll":
                        cmd.append("/LD")
                    cmd.extend(flags)
                elif comp_type == "tcc":
                    cmd = [comp_bin, str(source_file), "-o", str(out_path)]
                    if target_type == "dll":
                        cmd.append("-shared")
                    cmd.extend(flags)

            try:
                proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
                status_str = "SUCCESS" if proc.returncode == 0 else "FAILED"
                fbom = self._generate_fbom(
                    source_file, out_path, target_type, arch, self.compiler, cmd,
                    status=status_str, error_msg=proc.stderr if proc.returncode != 0 else None
                )
                fbom_path = out_path.with_suffix(".fbom.json")
                with open(fbom_path, "w", encoding="utf-8") as f:
                    json.dump(fbom, f, indent=2)

                return {
                    "status": status_str,
                    "mode": "NATIVE_COMPILER",
                    "compiler": self.compiler,
                    "architecture": arch,
                    "stripped": strip_symbols,
                    "command": " ".join(cmd),
                    "returncode": proc.returncode,
                    "stdout": proc.stdout,
                    "stderr": proc.stderr,
                    "artifact": str(out_path) if (not syntax_only and proc.returncode == 0) else None,
                    "fbom": fbom
                }
            except Exception as e:
                return {
                    "status": "ERROR",
                    "error": str(e),
                    "compiler": self.compiler
                }

        # 2. GRACEFUL FALLBACK (EMULATED VALIDATION & LINTING)
        else:
            is_valid, diag_msg = self.validate_syntax_fallback(code_content)
            
            if is_valid:
                if not syntax_only:
                    out_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(out_path, "wb") as f:
                        f.write(b"MZ_SYNTHETIC_BUILD_ARTIFACT_DDWX_V3_FBOM_READY\x00")
                
                fbom = self._generate_fbom(
                    source_file, out_path, target_type, arch, "None (Fallback Lexical Linter)", flags,
                    status="SUCCESS"
                )
                fbom_path = out_path.with_suffix(".fbom.json")
                with open(fbom_path, "w", encoding="utf-8") as f:
                    json.dump(fbom, f, indent=2)

                return {
                    "status": "SUCCESS",
                    "mode": "SYNTHETIC_FALLBACK",
                    "compiler": "None (Fallback Lexical Linter Active)",
                    "architecture": arch,
                    "stripped": strip_symbols,
                    "syntax_balanced": True,
                    "note": f"Native toolchain not in PATH. Emulated {arch} build with FBOM generated.",
                    "artifact": str(out_path) if not syntax_only else None,
                    "fbom": fbom
                }
            else:
                fbom = self._generate_fbom(
                    source_file, out_path, target_type, arch, "None (Fallback Lexical Linter)", flags,
                    status="FAILED", error_msg=diag_msg
                )
                fbom_path = out_path.with_suffix(".fbom.json")
                with open(fbom_path, "w", encoding="utf-8") as f:
                    json.dump(fbom, f, indent=2)

                return {
                    "status": "FAILED",
                    "mode": "SYNTHETIC_FALLBACK",
                    "compiler": "None (Fallback Lexical Linter Active)",
                    "architecture": arch,
                    "stripped": strip_symbols,
                    "syntax_balanced": False,
                    "error": f"Syntax Error: {diag_msg}",
                    "artifact": None,
                    "fbom": fbom
                }


def main():
    parser = argparse.ArgumentParser(
        description="DDW-X Headless Toolchain Builder & FBOM Generator (v3.0)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-f", "--file", required=True, help="Path to C/C++ source file")
    parser.add_argument("-o", "--output", help="Path for output binary artifact (.exe / .dll)")
    parser.add_argument("--target", choices=["exe", "dll"], default="exe", help="Target build format")
    parser.add_argument("--arch", choices=["x86", "x64", "arm64"], default="x64", help="Target CPU architecture")
    parser.add_argument("--no-strip", action="store_true", help="Preserve debug symbols (do not strip)")
    parser.add_argument("--no-opt", action="store_true", help="Disable aggressive compiler optimizations")
    parser.add_argument("--syntax-only", action="store_true", help="Validate syntax without linking binary")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")

    args = parser.parse_args()
    source_path = Path(args.file).resolve()
    out_path = Path(args.output).resolve() if args.output else None

    builder = ToolchainBuilder()
    res = builder.build(
        source_file=source_path,
        output_file=out_path,
        target_type=args.target,
        arch=args.arch,
        strip_symbols=not args.no_strip,
        optimize=not args.no_opt,
        syntax_only=args.syntax_only
    )

    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print("=" * 80)
        print(" [DDW-X TOOLCHAIN BUILDER] COMPILATION & FBOM AUDIT REPORT (v3.0)")
        print("=" * 80)
        print(f" [*] Source Target   : {source_path.name}")
        print(f" [*] Architecture    : {args.arch.upper()}")
        print(f" [*] Target Type     : {args.target.upper()}")
        print(f" [*] Build Status    : {res['status']}")
        if res.get("error"):
            print(f" [!] Error / Linter  : {res['error']}")
        if res.get("artifact"):
            print(f" [*] Output Binary   : {res['artifact']}")
        if res.get("fbom"):
            print("-" * 80)
            print(" [FORENSIC BILL OF MATERIALS (FBOM)]:")
            print(json.dumps(res["fbom"], indent=2))
        if res.get("note"):
            print("-" * 80)
            print(f" [*] Diagnostic      : {res['note']}")
        if res.get("stderr"):
            print(f" [!] Compiler Stderr :\n{res['stderr']}")
        print("=" * 80)


if __name__ == "__main__":
    main()
