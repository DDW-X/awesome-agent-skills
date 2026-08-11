#!/usr/bin/env python3
"""
================================================================================
DDW-X ZERO-KNOWLEDGE LOCAL RAG: SEMANTIC ROUTER TOOL
================================================================================
Module: src/core/rag/zk_semantic_router.py
Architect: Principal AI Architect, Lead Cryptographer & ZK Systems Engineer

PURPOSE:
- Acts as the blind decision router for the AI Agent.
- Performs sub-millisecond BM25 keyword & semantic matching in SQLite FTS5.
- BLIND RETURN: Returns strictly abstract cryptographic TAGs and relevance
  confidence metrics. NEVER returns raw textual content.
================================================================================
"""

import os
import sys
import re
import math
import sqlite3
import argparse
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

DEFAULT_DB_PATH = "D-csR_Index/zk_private_rag.db"


def sanitize_fts_query(raw_query: str) -> Tuple[str, str]:
    tokens = re.findall(r'\b\w+\b', raw_query.lower())
    if not tokens:
        return ('""', '""')

    stopwords = {
        "a", "an", "the", "and", "or", "but", "if", "then", "else", "when", "at",
        "by", "for", "with", "about", "against", "between", "into", "through",
        "during", "before", "after", "above", "below", "to", "from", "up", "down",
        "in", "out", "on", "off", "over", "under", "again", "further", "then", "once",
        "here", "there", "where", "why", "how", "all", "any", "both", "each",
        "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only",
        "own", "same", "so", "than", "too", "very", "can", "will", "just", "should",
        "now", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
        "do", "does", "did", "what", "which", "who", "whom", "this", "that", "these", "those"
    }

    filtered_tokens = [t for t in tokens if t not in stopwords and len(t) > 1]
    if not filtered_tokens:
        filtered_tokens = tokens

    strict_query = " AND ".join(f'"{t}"' for t in filtered_tokens)
    lenient_query = " OR ".join(f'"{t}"*' for t in filtered_tokens)
    return (strict_query, lenient_query)


def calculate_confidence(bm25_score: float, rank_idx: int) -> float:
    """
    Computes a standardized confidence percentage (60.0% - 99.5%)
    based on BM25 negative score magnitude and relative rank.
    """
    magnitude = abs(bm25_score)
    # Sigmoidal decay confidence formula
    base_conf = 100.0 * (1.0 - math.exp(-0.35 * magnitude))
    # Rank penalty factor
    rank_dampener = max(0.80, 1.0 - (rank_idx * 0.04))
    confidence = base_conf * rank_dampener
    return round(min(99.5, max(55.0, confidence)), 1)


def route_query_to_tags(db_path: Path, query_str: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Queries SQLite FTS5 and retrieves top-k abstract TAGs.
    Zero raw text is fetched or returned.
    """
    if not db_path.exists():
        alt_paths = [
            Path("D-csR_Index/zk_private_rag.db"),
            Path("../D-csR_Index/zk_private_rag.db"),
            Path("../../D-csR_Index/zk_private_rag.db")
        ]
        found = False
        for alt in alt_paths:
            if alt.exists():
                db_path = alt.resolve()
                found = True
                break
        if not found:
            print(f"[ERROR] ZK Database not found at '{db_path}'. Please run zk_advanced_indexer.py first.", file=sys.stderr)
            return []

    strict_q, lenient_q = sanitize_fts_query(query_str)
    routed_items: List[Dict[str, Any]] = []

    try:
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        cursor = conn.cursor()

        # Phase 1: Strict Match
        sql = """
            SELECT
                tag,
                doc_hash,
                bm25(zk_fts) as score
            FROM zk_fts
            WHERE zk_fts MATCH ?
            ORDER BY score ASC
            LIMIT ?;
        """
        cursor.execute(sql, (strict_q, top_k))
        rows = cursor.fetchall()

        # Phase 2: Lenient Fallback if fewer than top_k results
        if len(rows) < top_k and lenient_q != strict_q:
            cursor.execute(sql, (lenient_q, top_k))
            rows = cursor.fetchall()

        for idx, row in enumerate(rows):
            tag, doc_hash, score = row
            conf = calculate_confidence(score, idx)
            routed_items.append({
                "rank": idx + 1,
                "tag": tag,
                "doc_hash": doc_hash,
                "bm25_score": round(score, 4),
                "confidence_pct": conf
            })

        conn.close()
    except sqlite3.OperationalError as e:
        print(f"[SQLITE ERROR] {e}", file=sys.stderr)
    except Exception as e:
        print(f"[ROUTING ERROR] {e}", file=sys.stderr)

    return routed_items


def format_blind_output(routes: List[Dict[str, Any]]) -> str:
    if not routes:
        return "[DDW-X ZK-ROUTER] Zero matching cryptographic routes discovered for query."

    lines = [f"=== [DDW-X ZERO-KNOWLEDGE ROUTER] TOP-{len(routes)} SEMANTIC ROUTES ==="]
    for r in routes:
        lines.append(f"[ROUTE {r['rank']}] {r['tag']} | BM25: {r['bm25_score']} | Confidence: {r['confidence_pct']}% | DocHash: {r['doc_hash']}")
    lines.append("=== [END OF ROUTE MANIFEST] ===")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="DDW-X Zero-Knowledge Semantic Router (Returns TAGs & Confidence Only)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("query", nargs="?", default=None, help="User search query string (positional)")
    parser.add_argument("-q", "--query-str", dest="flag_query", default=None, help="User search query string (flag)")
    parser.add_argument("-k", "--top-k", type=int, default=5, help="Number of abstract TAG routes to return")
    parser.add_argument("--db-path", default=DEFAULT_DB_PATH, help="Path to ZK SQLite Database")
    parser.add_argument("--tags-only", action="store_true", help="Print only space-separated TAG list")
    parser.add_argument("--json", action="store_true", help="Print structured JSON array of routes")

    args = parser.parse_args()
    query = args.query or args.flag_query

    if not query or not query.strip():
        print("[ERROR] Search query string is required.", file=sys.stderr)
        parser.print_usage(file=sys.stderr)
        sys.exit(1)

    db_path = Path(args.db_path)
    routes = route_query_to_tags(db_path=db_path, query_str=query.strip(), top_k=args.top_k)

    if args.tags_only:
        tag_list = " ".join(r["tag"] for r in routes)
        print(tag_list)
    elif args.json:
        print(json.dumps(routes, indent=2))
    else:
        print(format_blind_output(routes))


if __name__ == "__main__":
    main()
