#!/usr/bin/env python3
"""
================================================================================
DDW-X PRIVACY-FIRST LOCAL RAG: RETRIEVAL ENGINE & CONTEXT SEARCHER
================================================================================
Module: src/core/rag/query_private_index.py
Architect: Principal Infrastructure Architect & Privacy-First AI Engineer

PURPOSE:
- Acts as the isolated search bridge between the AI Agent and the private index.
- Executes sub-millisecond BM25 ranking across indexed chunks.
- Outputs ONLY the retrieved top-k context chunks to stdout.
================================================================================
"""

import os
import sys
import re
import sqlite3
import argparse
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

# Ensure UTF-8 output where supported, or graceful fallback
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

DEFAULT_DB_PATH = "D-csR_Index/private_rag.db"


def sanitize_fts_query(raw_query: str) -> Tuple[str, str]:
    """
    Sanitizes natural language query for SQLite FTS5.
    Returns (strict_query, lenient_query).
    """
    # Extract alphanumeric and underscore tokens
    tokens = re.findall(r'\b\w+\b', raw_query.lower())
    if not tokens:
        return ('""', '""')

    # Filter standard stopwords to improve ranking focus
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

    # Strict query: all keywords must match (AND)
    strict_query = " AND ".join(f'"{t}"' for t in filtered_tokens)

    # Lenient query: any keyword matching (OR) with prefix matching
    lenient_query = " OR ".join(f'"{t}"*' for t in filtered_tokens)

    return (strict_query, lenient_query)


def search_private_index(db_path: Path, query_str: str, top_k: int = 3) -> List[Dict[str, Any]]:
    """
    Queries the SQLite FTS5 database and returns top_k ranked chunks.
    """
    if not db_path.exists():
        # Check alternative common locations
        alt_paths = [
            Path("D-csR_Index/private_rag.db"),
            Path("../D-csR_Index/private_rag.db"),
            Path("../../D-csR_Index/private_rag.db")
        ]
        found = False
        for alt in alt_paths:
            if alt.exists():
                db_path = alt.resolve()
                found = True
                break
        if not found:
            print(f"[ERROR] Index database not found at '{db_path}'. Please run build_private_index.py first.", file=sys.stderr)
            return []

    strict_q, lenient_q = sanitize_fts_query(query_str)
    results: List[Dict[str, Any]] = []

    try:
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        cursor = conn.cursor()

        # Phase 1: Try strict match (AND)
        sql_query = """
            SELECT
                c.chunk_id,
                d.rel_path,
                c.chunk_index,
                d.chunk_count,
                c.content,
                bm25(chunks_fts) as score
            FROM chunks_fts
            JOIN chunks c ON chunks_fts.chunk_id = c.chunk_id
            JOIN documents d ON c.doc_id = d.doc_id
            WHERE chunks_fts MATCH ?
            ORDER BY score ASC
            LIMIT ?;
        """

        cursor.execute(sql_query, (strict_q, top_k))
        rows = cursor.fetchall()

        # Phase 2: If strict match returned fewer than top_k, try lenient match (OR)
        if len(rows) < top_k and lenient_q != strict_q:
            cursor.execute(sql_query, (lenient_q, top_k))
            rows = cursor.fetchall()

        for row in rows:
            chunk_id, rel_path, chunk_idx, total_chunks, content, score = row
            results.append({
                "chunk_id": chunk_id,
                "source_file": rel_path,
                "chunk_index": chunk_idx,
                "total_chunks": total_chunks,
                "relevance_score": round(score, 4),
                "content": content
            })

        conn.close()
    except sqlite3.OperationalError as e:
        print(f"[SQLITE ERROR] {e}", file=sys.stderr)
    except Exception as e:
        print(f"[RETRIEVAL ERROR] {e}", file=sys.stderr)

    return results


def format_text_output(results: List[Dict[str, Any]]) -> str:
    """
    Renders clean, structured context blocks for AI consumption.
    """
    if not results:
        return "[DDW-X RAG] No matching records retrieved for the given query."

    lines = []
    lines.append(f"=== [DDW-X PRIVACY RAG] RETRIEVED CONTEXT ({len(results)} CHUNKS) ===")
    lines.append("")

    for rank, item in enumerate(results, 1):
        lines.append(f"--- [CHUNK {rank}/{len(results)}] Source: {item['source_file']} (Part {item['chunk_index'] + 1}/{item['total_chunks']} | Score: {item['relevance_score']}) ---")
        lines.append(item['content'].strip())
        lines.append("")

    lines.append("=== [END OF RETRIEVED CONTEXT] ===")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="DDW-X Local Retrieval Searcher for Private Datasets",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "query",
        nargs="?",
        default=None,
        help="Search query string (positional)"
    )
    parser.add_argument(
        "-q", "--query-str",
        dest="flag_query",
        default=None,
        help="Search query string (flag)"
    )
    parser.add_argument(
        "-k", "--top-k",
        type=int,
        default=3,
        help="Number of most relevant chunks to retrieve"
    )
    parser.add_argument(
        "--db-path",
        default=DEFAULT_DB_PATH,
        help="Path to the SQLite private index database"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON array of retrieved chunks"
    )

    args = parser.parse_args()
    query = args.query or args.flag_query

    if not query or not query.strip():
        print("[ERROR] Search query string must be provided.", file=sys.stderr)
        parser.print_usage(file=sys.stderr)
        sys.exit(1)

    db_path = Path(args.db_path)
    results = search_private_index(db_path=db_path, query_str=query.strip(), top_k=args.top_k)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(format_text_output(results))


if __name__ == "__main__":
    main()
