#!/usr/bin/env python3
"""
================================================================================
DDW-X ZERO-KNOWLEDGE LOCAL RAG: SECURE PAYLOAD COMPILER
================================================================================
Module: src/core/rag/zk_payload_compiler.py
Architect: Principal AI Architect, Lead Cryptographer & ZK Systems Engineer

PURPOSE:
- Securely extracts raw text data corresponding to Agent-routed abstract TAGs.
- AIR-GAPPED DELIVERY: Writes the compiled payload directly to disk in
  'Secure_Output_Workspace.md' for the user.
- Zero Context Leak: Returns strictly a confirmation message to stdout.
  The Agent never sees or processes the raw payload text.
================================================================================
"""

import os
import sys
import sqlite3
import argparse
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

DEFAULT_DB_PATH = "D-csR_Index/zk_private_rag.db"
DEFAULT_OUTPUT_FILE = "Secure_Output_Workspace.md"


def compile_payload_from_tags(
    db_path: Path,
    tags: List[str],
    output_path: Path
) -> Tuple[int, List[str]]:
    """
    Queries database for given cryptographic tags and writes compiled payload to disk.
    Returns (num_found, found_tags).
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
            print(f"[ERROR] ZK Database not found at '{db_path}'.", file=sys.stderr)
            return (0, [])

    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    cursor = conn.cursor()

    compiled_blocks = []
    found_tags = []

    for rank, tag in enumerate(tags, 1):
        clean_tag = tag.strip().strip(",")
        if not clean_tag:
            continue

        cursor.execute("""
            SELECT
                c.tag,
                c.doc_hash,
                c.chunk_index,
                c.content,
                c.token_count,
                d.file_ext
            FROM zk_chunks c
            LEFT JOIN zk_documents d ON c.doc_hash = d.doc_hash
            WHERE c.tag = ?;
        """, (clean_tag,))

        row = cursor.fetchone()
        if row:
            t_tag, doc_hash, chunk_idx, content, token_cnt, file_ext = row
            found_tags.append(t_tag)
            compiled_blocks.append({
                "rank": rank,
                "tag": t_tag,
                "doc_hash": doc_hash or "N/A",
                "chunk_index": chunk_idx,
                "token_count": token_cnt,
                "file_ext": file_ext or ".txt",
                "content": content
            })

    conn.close()

    if not compiled_blocks:
        return (0, [])

    # Assemble Air-Gapped Secure Markdown Payload for the User
    timestamp_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    tag_str = ", ".join(found_tags)

    lines = []
    lines.append("# DDW-X Secure Output Workspace")
    lines.append(f"> **Compilation Timestamp:** `{timestamp_str}`  ")
    lines.append(f"> **Cryptographic Tags:** `{tag_str}`  ")
    lines.append(f"> **Confidentiality Level:** AIR-GAPPED (Unexposed to AI Context)")
    lines.append("")
    lines.append("---")
    lines.append("")

    for block in compiled_blocks:
        lines.append(f"## [Payload Block {block['rank']}] Cryptographic Tag: `{block['tag']}`")
        lines.append(f"- **Document Identifier (Hash):** `{block['doc_hash']}`")
        lines.append(f"- **Chunk Sequence:** `Index #{block['chunk_index']}`")
        lines.append(f"- **Token Density:** `{block['token_count']} tokens`")
        lines.append(f"- **File Format:** `{block['file_ext']}`")
        lines.append("")
        lines.append("### Context Payload:")
        lines.append("```")
        lines.append(block["content"].strip())
        lines.append("```")
        lines.append("")
        lines.append("---")
        lines.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8", errors="replace") as f:
        f.write("\n".join(lines))

    return (len(compiled_blocks), found_tags)


def main():
    parser = argparse.ArgumentParser(
        description="DDW-X Zero-Knowledge Payload Compiler (Air-Gapped Local File Delivery)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "tags",
        nargs="*",
        help="List of abstract cryptographic TAGs to compile (e.g. TAG-4F91-B2 TAG-8A14-C9)"
    )
    parser.add_argument(
        "-t", "--tag-list",
        dest="tag_flag",
        default=None,
        help="Comma or space-separated list of TAGs"
    )
    parser.add_argument(
        "-o", "--output",
        default=DEFAULT_OUTPUT_FILE,
        help="Destination markdown workspace file path"
    )
    parser.add_argument(
        "--db-path",
        default=DEFAULT_DB_PATH,
        help="Path to ZK SQLite Database"
    )

    args = parser.parse_args()

    # Consolidate tags from positional and flag arguments
    all_tags = []
    if args.tags:
        all_tags.extend(args.tags)
    if args.tag_flag:
        all_tags.extend(re.split(r'[\s,]+', args.tag_flag.strip()))

    all_tags = [t.strip() for t in all_tags if t.strip()]

    if not all_tags:
        print("[ERROR] At least one cryptographic TAG must be provided for payload compilation.", file=sys.stderr)
        parser.print_usage(file=sys.stderr)
        sys.exit(1)

    db_path = Path(args.db_path)
    output_path = Path(args.output).resolve()

    count, found_tags = compile_payload_from_tags(
        db_path=db_path,
        tags=all_tags,
        output_path=output_path
    )

    if count > 0:
        tag_display = ", ".join(found_tags)
        print(f"[SUCCESS] Compiled payload mapped to {tag_display} successfully written to disk at '{output_path.name}'.")
    else:
        print(f"[ERROR] None of the provided TAGs ({', '.join(all_tags)}) could be resolved in the ZK index.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
