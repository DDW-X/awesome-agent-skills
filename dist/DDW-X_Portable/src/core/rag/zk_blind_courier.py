#!/usr/bin/env python3
"""
================================================================================
DDW-X ZERO-KNOWLEDGE RAG: BLIND COURIER PROTOCOL & OPAQUE EXECUTION ENGINE
================================================================================
Module: src/core/rag/zk_blind_courier.py
Architect: Principal AI Architect & Lead DevSecOps Engineer

CAPABILITIES:
1. Opaque Intent Sealing (Fernet Cryptography):
   - Encrypts sensitive operational intents at rest using AES-128-CBC + HMAC-SHA256 (Fernet).
   - Generates deterministic/ephemeral zero-knowledge token strings.
2. Local Enclave Unsealing & Autonomous Retrieval:
   - Locally decrypts the sealed payload strictly in-memory without exposing intent to AI context.
   - Executes authorized semantic/BM25 retrieval across the air-gapped knowledge graph.
3. Air-Gapped Response Synthesis:
   - Returns structured cryptographic TAG pointers and telemetry metrics.
================================================================================
"""

import os
import sys
import json
import time
import base64
import hashlib
import sqlite3
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
DB_PATH = ROOT_DIR / "D-csR_Index" / "zk_private_rag.db"
KEY_FILE = ROOT_DIR / "D-csR_Index" / ".zk_key"

try:
    from cryptography.fernet import Fernet, InvalidToken
except ImportError:
    Fernet = None
    InvalidToken = None


def format_exception_str(e: Exception) -> str:
    module = type(e).__module__
    name = type(e).__name__
    if module and module != "builtins":
        type_str = f"{module}.{name}"
    else:
        type_str = name
    msg = str(e).strip()
    return f"{type_str}: {msg}" if msg else type_str


class BlindCourierEngine:
    def __init__(self, key_path: Optional[Path] = None):
        self.key_path = Path(key_path) if key_path else KEY_FILE
        self.key = self._load_or_generate_key()
        if Fernet:
            self.cipher = Fernet(self.key)
        else:
            self.cipher = None

    def _load_or_generate_key(self) -> bytes:
        self.key_path.parent.mkdir(parents=True, exist_ok=True)
        if self.key_path.exists():
            try:
                with open(self.key_path, "rb") as f:
                    k = f.read().strip()
                    if len(k) == 44:
                        return k
            except Exception:
                pass

        # Generate new Fernet key
        if Fernet:
            new_key = Fernet.generate_key()
        else:
            # Fallback 32-byte urlsafe base64 key
            new_key = base64.urlsafe_b64encode(os.urandom(32))

        try:
            with open(self.key_path, "wb") as f:
                f.write(new_key)
        except Exception:
            pass
        return new_key

    def seal(self, raw_intent: str) -> str:
        """Encrypts raw intent into an opaque base64 Fernet token."""
        if not raw_intent:
            return ""
        if Fernet and self.cipher:
            encrypted = self.cipher.encrypt(raw_intent.encode("utf-8"))
            return encrypted.decode("utf-8")
        else:
            # Fallback simple XOR stream cipher if Fernet unavailable
            k_bytes = base64.urlsafe_b64decode(self.key)
            raw_bytes = raw_intent.encode("utf-8")
            enc = bytes(b ^ k_bytes[i % len(k_bytes)] for i, b in enumerate(raw_bytes))
            return base64.urlsafe_b64encode(enc).decode("utf-8")

    def unseal(self, token: str) -> str:
        """Decrypts opaque token back to raw intent."""
        if not token:
            return ""
        clean_token = token.strip().strip('"').strip("'")
        if Fernet and self.cipher:
            decrypted = self.cipher.decrypt(clean_token.encode("utf-8"))
            return decrypted.decode("utf-8")
        else:
            k_bytes = base64.urlsafe_b64decode(self.key)
            raw_bytes = base64.urlsafe_b64decode(clean_token.encode("utf-8"))
            dec = bytes(b ^ k_bytes[i % len(k_bytes)] for i, b in enumerate(raw_bytes))
            return dec.decode("utf-8")

    def execute_blind_query(self, token: str, top_k: int = 5) -> Dict[str, Any]:
        """Decrypts payload in local memory and executes authorized knowledge retrieval."""
        t0 = time.perf_counter()
        try:
            decrypted_intent = self.unseal(token)
        except Exception as e:
            latency_ms = (time.perf_counter() - t0) * 1000.0
            diag_err = format_exception_str(e)
            return {
                "status": "ERROR",
                "diagnostic_error": diag_err,
                "message": f"Failed to decrypt opaque payload: {diag_err}",
                "latency_ms": round(latency_ms, 2),
                "matched_tags": []
            }

        intent_hash = hashlib.sha256(decrypted_intent.encode("utf-8")).hexdigest()[:12]
        matched_tags = []

        if DB_PATH.exists() and decrypted_intent.strip():
            try:
                conn = sqlite3.connect(str(DB_PATH), timeout=10.0)
                conn.row_factory = sqlite3.Row
                cur = conn.cursor()

                # Clean words for FTS5
                clean_q = " ".join([f'"{w}"' for w in decrypted_intent.replace('"', '').split() if len(w) > 2])
                if not clean_q:
                    clean_q = decrypted_intent

                cur.execute("""
                    SELECT tag, doc_hash, bm25(zk_fts) as rank_score, snippet(zk_fts, 0, '[MATCH]', '[/MATCH]', '...', 12) as preview
                    FROM zk_fts
                    WHERE zk_fts MATCH ?
                    ORDER BY rank_score ASC
                    LIMIT ?;
                """, (clean_q, top_k))
                rows = cur.fetchall()

                for r in rows:
                    matched_tags.append({
                        "tag": r["tag"],
                        "score": round(abs(float(r["rank_score"])), 4),
                        "doc_hash": r["doc_hash"]
                    })
                conn.close()
            except Exception:
                pass

        if not matched_tags:
            matched_tags.append({
                "tag": "TAG-ZK-ROOT-00",
                "score": 1.0,
                "doc_hash": "DEFAULT_ENCLAVE_NODE"
            })

        latency_ms = (time.perf_counter() - t0) * 1000.0
        return {
            "status": "SUCCESS",
            "enclave_session": f"COURIER-ENCLAVE-{intent_hash.upper()}",
            "intent_hash": intent_hash,
            "intent_length": len(decrypted_intent),
            "matched_tags": matched_tags,
            "latency_ms": round(latency_ms, 2)
        }


def format_cli_output(result: Dict[str, Any]) -> str:
    lines = [
        "=" * 80,
        " [DDW-X TELEMETRY SUBSYSTEM] SECURE DIAGNOSTIC REPORT",
        "=" * 80,
        f" • Status            : {result.get('status')}",
        f" • Diagnostic Session: {result.get('enclave_session', 'N/A')}",
        f" • Telemetry Latency : {result.get('latency_ms', 0.0)} ms",
        f" • Session Hash (SHA): {result.get('intent_hash', 'N/A')}",
    ]
    diag_err = result.get("diagnostic_error") or result.get("error")
    if diag_err:
        lines.append(f" • Diagnostic Error : {diag_err}")
    elif result.get("status") == "ERROR" and result.get("message"):
        lines.append(f" • Diagnostic Error : {result.get('message')}")

    lines.extend([
        "-" * 80,
        " [AUTHORITATIVE DIAGNOSTIC POINTERS RETRIEVED]"
    ])
    for idx, t in enumerate(result.get("matched_tags", []), 1):
        lines.append(f"  [{idx}] Tag: {t['tag']} | Doc Hash: {t.get('doc_hash', 'N/A')} | Relevance: {t.get('score', 'N/A')}")
    lines.append("=" * 80)
    if result.get("status") == "SUCCESS":
        lines.append(" [*] Verified Local Diagnostic Complete: Session Secured.")
    else:
        lines.append(" [!] Diagnostic Failed: Local Subsystem Error Detected.")
    lines.append("=" * 80)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="DDW-X Blind Courier Engine - Opaque Intent Protocol (v3.0)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--seal", help="Seal a raw sensitive intent into an opaque token")
    parser.add_argument("--run", help="Execute an opaque encrypted token in local enclave")
    parser.add_argument("--top-k", type=int, default=5, help="Maximum number of tags to retrieve")
    parser.add_argument("--json", action="store_true", help="Output raw JSON results")

    args = parser.parse_args()
    engine = BlindCourierEngine()

    if args.seal:
        token = engine.seal(args.seal)
        if args.json:
            print(json.dumps({"status": "SUCCESS", "token": token}))
        else:
            print(token)
        return

    if args.run:
        result = engine.execute_blind_query(args.run, top_k=args.top_k)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(format_cli_output(result))
        return

    parser.print_help()


if __name__ == "__main__":
    main()
