#!/usr/bin/env python3
"""
================================================================================
DDW-X ZERO-KNOWLEDGE RAG: MULTI-QUERY RECIPROCAL RANK FUSION (RRF) ROUTER
================================================================================
Module: src/core/rag/zk_hybrid_router.py
Architect: Principal AI Architect & Lead DevSecOps Engineer

MATHEMATICAL ARCHITECTURE:
1. Dynamic Query Expander:
   Transforms single natural language queries into 4 orthogonal search spaces:
   - Vector 1: Base Keyword & Semantic Phrasing
   - Vector 2: MITRE ATT&CK TTP & Matrix Mapping (e.g. T1558.001, Privilege Escalation)
   - Vector 3: Telemetry & Event Log Signatures (Sysmon EID, Auditd, Event 4624/4768)
   - Vector 4: Exploitation Artifacts & Tool Signatures (Mimikatz, Rubeus, AST, OLLVM)
2. Multi-Pass FTS5 Execution:
   Executes individual parameterized BM25 search passes against SQLite FTS5.
3. Reciprocal Rank Fusion (RRF):
   Fuses orthogonal rank lists with smooth rank discounting:
   RRF_Score(d) = SUM_q [ w_q / (k + rank_q(d)) ]
4. Zero-Knowledge Gatekeeper:
   Outputs abstract cryptographic TAGs and confidence scores only. ZERO raw text.
================================================================================
"""

import os
import sys
import re
import json
import math
import time
import sqlite3
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any, Optional

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

DEFAULT_DB_PATH = "D-csR_Index/zk_private_rag.db"
DEFAULT_RRF_K = 60


# ==============================================================================
# 1. SECURITY & DOMAIN ONTOLOGY EXPANSION DICTIONARY
# ==============================================================================

DOMAIN_ONTOLOGY = {
    # Active Directory & Kerberos
    "kerberos": {
        "ttps": ["T1558.001", "T1558.003", "T1078", "Credential Access", "KRBTGT", "Golden Ticket", "Silver Ticket"],
        "telemetry": ["Event ID 4768", "Event ID 4769", "Event ID 4624", "Event ID 4672", "Sysmon EID 10", "AS-REQ", "TGS-REQ"],
        "tools": ["Mimikatz", "Rubeus", "Kekeo", "Impacket", "sekurlsa", "kerberos::golden", "RC4-HMAC", "AES256-CTS"]
    },
    "golden ticket": {
        "ttps": ["T1558.001", "Steal or Forge Kerberos Tickets", "KRBTGT", "Domain Persistence"],
        "telemetry": ["Event 4768", "Event 4769", "Ticket Granting Service", "Sysmon 10", "PAC validation"],
        "tools": ["Mimikatz", "Rubeus", "klist", "sekurlsa::tickets", "ticket.kirbi"]
    },
    "lateral movement": {
        "ttps": ["T1021.002", "T1021.006", "T1570", "Lateral Movement", "Pass the Hash", "Pass the Ticket", "WMI Execution"],
        "telemetry": ["Event ID 4624 Type 3", "Event ID 4625", "Event ID 4672", "Sysmon EID 1", "Sysmon EID 3", "RPC 135", "SMB 445"],
        "tools": ["PsExec", "WMIexec", "WinRM", "CrackMapExec", "Impacket", "Evil-WinRM"]
    },
    # Reverse Engineering & Binaries
    "reverse engineering": {
        "ttps": ["Binary Analysis", "Decompilation", "Disassembly", "Control Flow", "PE Forensics", "ELF Analysis"],
        "telemetry": ["Shannon Entropy", "Import Address Table", "IAT Hooking", "Section Headers", "Relocations"],
        "tools": ["Ghidra", "IDA Pro", "Binary Ninja", "Radare2", "x64dbg", "DecompInterface"]
    },
    "ollvm": {
        "ttps": ["Obfuscation", "Control Flow Flattening", "Bogus Control Flow", "Instruction Substitution"],
        "telemetry": ["State Variable Dispatcher", "Basic Block Recovery", "Symbolic Execution", "CFG Reconstruction"],
        "tools": ["Triton", "Angr", "Miasm", "Ghidra P-Code", "D-Flat"]
    },
    # SAST & Code Auditing
    "sast": {
        "ttps": ["OWASP Top 10", "A01 Broken Access Control", "A03 Injection", "A10 SSRF", "Static Analysis"],
        "telemetry": ["AST Taint Tracking", "Source-to-Sink Dataflow", "Abstract Syntax Tree", "CFG"],
        "tools": ["Bandit", "Semgrep", "CodeQL", "ast.NodeVisitor", "SonarQube"]
    },
    "sql injection": {
        "ttps": ["CWE-89", "OWASP A03", "SQLi", "Blind SQL Injection", "Time-Based SQLi"],
        "telemetry": ["Unparameterized Concatenation", "cursor.execute", "Raw SQL Sink", "Prepared Statements"],
        "tools": ["SQLmap", "AST Auditor", "Parameterized Query", "ORM"]
    },
    # AI Safety & LLM
    "prompt injection": {
        "ttps": ["CWE-1426", "OWASP LLM01", "Direct Injection", "Indirect Injection", "Jailbreak"],
        "telemetry": ["Delimiter Isolation", "Canary Tokens", "System Prompt Extraction", "Dual-Pass Verification"],
        "tools": ["Llama Guard", "NeMo Guardrails", "Constitutional AI", "Garak"]
    }
}


# ==============================================================================
# 2. MULTI-QUERY EXPANDER
# ==============================================================================

class QueryPass:
    def __init__(self, name: str, query_str: str, weight: float = 1.0):
        self.name = name
        self.query_str = query_str
        self.weight = weight


class MultiQueryExpander:
    """
    Expands a single user prompt into orthogonal search vectors:
    1. Base Keyword Vector
    2. MITRE ATT&CK TTP Vector
    3. Telemetry & Log Signature Vector
    4. Tool & Artifact Vector
    """
    STOPWORDS = {
        "a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
        "has", "he", "in", "is", "it", "its", "of", "on", "that", "the",
        "to", "was", "were", "will", "with", "how", "what", "where", "why"
    }

    @classmethod
    def clean_tokens(cls, text: str) -> List[str]:
        raw = re.sub(r'[^a-zA-Z0-9_\-\.\:\/]', ' ', text)
        tokens = [t.strip() for t in raw.split() if t.strip()]
        return [t for t in tokens if t.lower() not in cls.STOPWORDS and len(t) > 1]

    @classmethod
    def expand_query(cls, user_query: str) -> List[QueryPass]:
        passes: List[QueryPass] = []
        lower_q = user_query.lower()
        cleaned_tokens = cls.clean_tokens(user_query)

        # 1. Base Keyword Pass (Weight: 1.0)
        base_str = " ".join(cleaned_tokens)
        passes.append(QueryPass("Base Keyword", base_str, weight=1.0))

        # Ontology Concept Matching
        matched_ttps: List[str] = []
        matched_telemetry: List[str] = []
        matched_tools: List[str] = []

        for concept_key, ontology_data in DOMAIN_ONTOLOGY.items():
            if concept_key in lower_q:
                matched_ttps.extend(ontology_data.get("ttps", []))
                matched_telemetry.extend(ontology_data.get("telemetry", []))
                matched_tools.extend(ontology_data.get("tools", []))

        # 2. MITRE ATT&CK / TTP Pass (Weight: 1.25)
        if matched_ttps:
            ttp_str = " ".join(matched_ttps[:6])
            passes.append(QueryPass("MITRE ATT&CK / TTP", f"{base_str} {ttp_str}", weight=1.25))
        else:
            passes.append(QueryPass("MITRE ATT&CK / TTP", f"{base_str} MITRE ATT&CK TTP threat technique", weight=1.0))

        # 3. Telemetry & Log Signature Pass (Weight: 1.15)
        if matched_telemetry:
            telem_str = " ".join(matched_telemetry[:6])
            passes.append(QueryPass("Telemetry & Signatures", f"{base_str} {telem_str}", weight=1.15))
        else:
            passes.append(QueryPass("Telemetry & Signatures", f"{base_str} Sysmon Event ID log signature telemetry", weight=0.9))

        # 4. Tool & Exploit Artifact Pass (Weight: 1.05)
        if matched_tools:
            tool_str = " ".join(matched_tools[:6])
            passes.append(QueryPass("Tooling & Artifacts", f"{base_str} {tool_str}", weight=1.05))
        else:
            passes.append(QueryPass("Tooling & Artifacts", f"{base_str} artifact payload syntax signature", weight=0.85))

        return passes


# ==============================================================================
# 3. FTS5 BM25 SEARCHER & RECIPROCAL RANK FUSION
# ==============================================================================

class FTS5QuerySearcher:
    """
    Executes parameterized BM25 search passes against SQLite FTS5.
    """
    def __init__(self, db_path: Path):
        self.db_path = db_path

    def format_fts_query(self, query_text: str) -> Tuple[str, str]:
        tokens = MultiQueryExpander.clean_tokens(query_text)
        if not tokens:
            tokens = ["security", "threat"]

        strict_q = " AND ".join(f'"{t}"' for t in tokens)
        lenient_q = " OR ".join(f'"{t}"*' for t in tokens)
        return strict_q, lenient_q

    def execute_pass(self, query_str: str, limit: int = 30) -> List[Dict[str, Any]]:
        strict_q, lenient_q = self.format_fts_query(query_str)
        candidates: List[Dict[str, Any]] = []

        try:
            conn = sqlite3.connect(f"file:{self.db_path}?mode=ro", uri=True, timeout=15.0)
            cursor = conn.cursor()
            sql = """
                SELECT tag, doc_hash, bm25(zk_fts) as score
                FROM zk_fts
                WHERE zk_fts MATCH ?
                ORDER BY score ASC
                LIMIT ?;
            """
            cursor.execute(sql, (strict_q, limit))
            rows = cursor.fetchall()

            # Lenient fallback if needed
            if len(rows) < limit and lenient_q != strict_q:
                cursor.execute(sql, (lenient_q, limit))
                rows = cursor.fetchall()

            conn.close()

            for rank_idx, (tag, doc_hash, score) in enumerate(rows):
                candidates.append({
                    "rank": rank_idx + 1,
                    "tag": tag,
                    "doc_hash": doc_hash,
                    "bm25_score": round(score, 4)
                })
        except Exception as e:
            pass

        return candidates


class ReciprocalRankFusionEngine:
    """
    Executes Reciprocal Rank Fusion (RRF) across multi-pass search results:
    RRF(d) = SUM_q [ w_q / (k + rank_q(d)) ]
    """
    @staticmethod
    def fuse(
        pass_results: List[Tuple[QueryPass, List[Dict[str, Any]]]],
        k_constant: int = DEFAULT_RRF_K,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        tag_scores: Dict[str, float] = {}
        tag_doc_hashes: Dict[str, str] = {}
        tag_pass_counts: Dict[str, int] = {}
        tag_best_bm25: Dict[str, float] = {}

        for qpass, results in pass_results:
            w_q = qpass.weight
            for item in results:
                tag = item["tag"]
                rank = item["rank"]
                doc_hash = item["doc_hash"]
                bm25_s = item["bm25_score"]

                rrf_contribution = w_q / (k_constant + rank)
                tag_scores[tag] = tag_scores.get(tag, 0.0) + rrf_contribution
                tag_doc_hashes[tag] = doc_hash
                tag_pass_counts[tag] = tag_pass_counts.get(tag, 0) + 1

                if tag not in tag_best_bm25 or bm25_s < tag_best_bm25[tag]:
                    tag_best_bm25[tag] = bm25_s

        if not tag_scores:
            return []

        # Sort tags by descending RRF score
        sorted_tags = sorted(tag_scores.items(), key=lambda x: x[1], reverse=True)
        max_rrf = sorted_tags[0][1] if sorted_tags else 1.0

        fused_manifest: List[Dict[str, Any]] = []
        for rank_idx, (tag, rrf_score) in enumerate(sorted_tags[:top_k]):
            consensus_count = tag_pass_counts.get(tag, 1)
            # Normalized confidence formula factoring RRF score and consensus cross-validation
            norm_ratio = rrf_score / max_rrf
            consensus_boost = min(1.15, 1.0 + (consensus_count - 1) * 0.05)
            confidence_pct = round(min(99.8, max(65.0, (75.0 + norm_ratio * 20.0) * consensus_boost)), 1)

            fused_manifest.append({
                "rank": rank_idx + 1,
                "tag": tag,
                "doc_hash": tag_doc_hashes.get(tag, "UNKNOWN"),
                "rrf_score": round(rrf_score, 6),
                "consensus_passes": f"{consensus_count}/{len(pass_results)}",
                "best_bm25": tag_best_bm25.get(tag, 0.0),
                "confidence_pct": confidence_pct
            })

        return fused_manifest


# ==============================================================================
# 4. ORCHESTRATION & CLI ENTRY POINT
# ==============================================================================

def run_hybrid_routing(
    query_str: str,
    db_path_str: str = DEFAULT_DB_PATH,
    top_k: int = 5,
    rrf_k: int = DEFAULT_RRF_K,
    tags_only: bool = False,
    as_json: bool = False,
    verbose: bool = False
) -> List[str]:
    """
    Orchestrates query expansion, multi-pass search, and Reciprocal Rank Fusion.
    """
    t_start = time.perf_counter()
    db_path = Path(db_path_str).resolve()

    if not db_path.exists():
        print(f"[!] ERROR: Database not found at: {db_path}", file=sys.stderr)
        sys.exit(1)

    # 1. Expand Single Query into Orthogonal Query Vectors
    expander = MultiQueryExpander()
    query_passes = expander.expand_query(query_str)

    # 2. Execute Multi-Pass FTS5 Searches
    searcher = FTS5QuerySearcher(db_path)
    pass_results: List[Tuple[QueryPass, List[Dict[str, Any]]]] = []

    for qpass in query_passes:
        results = searcher.execute_pass(qpass.query_str, limit=top_k * 4)
        pass_results.append((qpass, results))

    # 3. Mathematically Fuse Results using RRF
    fused_results = ReciprocalRankFusionEngine.fuse(pass_results, k_constant=rrf_k, top_k=top_k)
    duration_ms = (time.perf_counter() - t_start) * 1000

    minted_tags = [item["tag"] for item in fused_results]

    if tags_only:
        print(" ".join(minted_tags))
        return minted_tags

    if as_json:
        payload = {
            "query": query_str,
            "duration_ms": round(duration_ms, 2),
            "passes": [
                {
                    "name": qpass.name,
                    "query": qpass.query_str,
                    "weight": qpass.weight,
                    "candidates_retrieved": len(res)
                }
                for qpass, res in pass_results
            ],
            "fused_results": fused_results
        }
        print(json.dumps(payload, indent=2))
        return minted_tags

    # Formatted Visual Terminal Output
    print("=" * 80)
    print(" [DDW-X ZERO-KNOWLEDGE HYBRID ROUTER] MULTI-QUERY RECIPROCAL RANK FUSION")
    print("=" * 80)
    print(f" [*] Target Query          : \"{query_str}\"")
    print(f" [*] Database Target       : {db_path.name}")
    print(f" [*] RRF Smoothing (k)     : {rrf_k} | Top-K: {top_k}")
    print("-" * 80)
    print(" [1] DYNAMIC QUERY EXPANSION MATRIX:")
    for idx, (qpass, res) in enumerate(pass_results):
        print(f"     Vector {idx+1} [{qpass.name:<22} | W={qpass.weight:.2f}]:")
        print(f"       --> Query Terms : {qpass.query_str}")
        print(f"       --> Candidates  : {len(res)} matched")

    print("-" * 80)
    print(" [2] RECIPROCAL RANK FUSION (RRF) RANKINGS:")
    if not fused_results:
        print("     [!] Zero matching cryptographic routes discovered across all vectors.")
    else:
        for item in fused_results:
            print(f"  [ROUTE {item['rank']}] {item['tag']} | Conf: {item['confidence_pct']}% | Consensus: {item['consensus_passes']} | RRF: {item['rrf_score']:.6f} | DocHash: {item['doc_hash']}")

    print("-" * 80)
    print(f" [*] Multi-Vector Fusion Completed in {duration_ms:.2f} ms")
    print(f" [*] Optimal Cryptographic TAGs : {', '.join(minted_tags)}")
    print("=" * 80)

    return minted_tags


def main():
    parser = argparse.ArgumentParser(
        description="DDW-X Multi-Query Reciprocal Rank Fusion Router",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("query", nargs="?", default="Kerberos Golden Ticket persistence and lateral movement", help="Natural language query")
    parser.add_argument("--db-path", default=DEFAULT_DB_PATH, help="Path to SQLite ZK Database")
    parser.add_argument("--top-k", type=int, default=5, help="Number of fused tags to return")
    parser.add_argument("--rrf-k", type=int, default=DEFAULT_RRF_K, help="RRF smoothing constant k")
    parser.add_argument("--tags-only", action="store_true", help="Output only space-separated TAGs")
    parser.add_argument("--json", action="store_true", help="Output full JSON manifest")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose query telemetry")

    args = parser.parse_args()

    run_hybrid_routing(
        query_str=args.query,
        db_path_str=args.db_path,
        top_k=args.top_k,
        rrf_k=args.rrf_k,
        tags_only=args.tags_only,
        as_json=args.json,
        verbose=args.verbose
    )


if __name__ == "__main__":
    main()
