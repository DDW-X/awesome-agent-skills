#!/usr/bin/env python3
"""
================================================================================
DDW-X PRIVACY-FIRST LOCAL RAG: BLIND INGESTION & VECTOR/BM25 INDEXER
================================================================================
Module: src/core/rag/build_private_index.py
Architect: Principal Infrastructure Architect & Privacy-First AI Engineer

CRITICAL PRIVACY GUARANTEE:
- Zero Content Output: Operates completely blind. Does NOT print file contents,
  sample snippets, or extracted tokens to stdout/stderr.
- Local Storage: Stores chunked records and FTS5 inverted indices strictly in
  a local SQLite database in D-csR_Index/.
================================================================================
"""

import os
import sys
import re
import math
import sqlite3
import argparse
import hashlib
import time
from pathlib import Path
from typing import List, Tuple, Generator, Dict, Any

# Ensure UTF-8 output where supported, or graceful fallback
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Target text-based file extensions
SUPPORTED_EXTENSIONS = {
    ".md", ".txt", ".markdown", ".rst", ".org",
    ".json", ".jsonl", ".csv", ".tsv", ".xml", ".yaml", ".yml", ".toml", ".ini", ".cfg",
    ".py", ".c", ".cpp", ".cc", ".cxx", ".h", ".hpp", ".hxx", ".rs", ".go",
    ".java", ".kt", ".js", ".ts", ".jsx", ".tsx", ".sh", ".bash", ".zsh", ".ps1",
    ".bat", ".cmd", ".sql", ".html", ".htm", ".css", ".scss", ".log"
}

# Directories to ignore
IGNORE_DIRS = {
    ".git", ".svn", ".hg", "__pycache__", ".venv", "venv", "env",
    "node_modules", "target", "build", "dist", ".idea", ".vscode",
    ".agents", "D-csR_Index", "scratch"
}


class BlindChunker:
    """
    Splits text content into overlapping token/word chunks cleanly
    without splitting words or sentences abruptly.
    """

    def __init__(self, chunk_size_tokens: int = 500, overlap_tokens: int = 50):
        self.chunk_size_tokens = chunk_size_tokens
        self.overlap_tokens = overlap_tokens
        # Heuristic: 1 token ~= 0.75 words, or 1 word ~= 1.33 tokens
        # Target word count per chunk: ~375 - 400 words
        self.chunk_words = max(50, int(chunk_size_tokens * 0.75))
        self.overlap_words = max(10, int(overlap_tokens * 0.75))

    def chunk_text(self, text: str) -> List[str]:
        if not text or not text.strip():
            return []

        # Split into paragraph / structural units
        paragraphs = re.split(r'(\n\s*\n)', text)
        chunks: List[str] = []
        current_chunk_words: List[str] = []
        current_count = 0

        for segment in paragraphs:
            words = segment.split()
            if not words:
                continue

            if current_count + len(words) <= self.chunk_words:
                current_chunk_words.extend(words)
                current_count += len(words)
            else:
                # If current chunk has enough words, finalize it
                if current_chunk_words:
                    chunk_str = " ".join(current_chunk_words)
                    chunks.append(chunk_str)

                    # Retain overlap words from the end of the previous chunk
                    if self.overlap_words < len(current_chunk_words):
                        current_chunk_words = current_chunk_words[-self.overlap_words:]
                    else:
                        current_chunk_words = []
                    current_count = len(current_chunk_words)

                # If the single segment is longer than chunk_words, slice it by words
                if len(words) > self.chunk_words:
                    step = max(1, self.chunk_words - self.overlap_words)
                    for i in range(0, len(words), step):
                        sub_slice = words[i:i + self.chunk_words]
                        if sub_slice:
                            chunks.append(" ".join(sub_slice))
                    current_chunk_words = []
                    current_count = 0
                else:
                    current_chunk_words.extend(words)
                    current_count += len(words)

        if current_chunk_words:
            chunk_str = " ".join(current_chunk_words)
            if not chunks or chunk_str != chunks[-1]:
                chunks.append(chunk_str)

        return chunks


class PrivateIndexDatabase:
    """
    Manages SQLite FTS5 Full-Text Search (BM25) and document metadata
    storage with zero data leak to console.
    """

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.execute("PRAGMA journal_mode = WAL;")
        self.conn.execute("PRAGMA synchronous = NORMAL;")
        self._init_schema()

    def _init_schema(self):
        with self.conn:
            # Metadata table
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS index_meta (
                    key TEXT PRIMARY KEY,
                    value TEXT
                );
            """)

            # Document registry
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    doc_id TEXT UNIQUE,
                    rel_path TEXT,
                    file_size INTEGER,
                    chunk_count INTEGER,
                    indexed_timestamp REAL
                );
            """)

            # Chunk storage
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS chunks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chunk_id TEXT UNIQUE,
                    doc_id TEXT,
                    chunk_index INTEGER,
                    content TEXT,
                    token_estimate INTEGER,
                    FOREIGN KEY (doc_id) REFERENCES documents(doc_id) ON DELETE CASCADE
                );
            """)

            # FTS5 Virtual Table for sub-millisecond BM25 ranking
            self.conn.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
                    content,
                    chunk_id UNINDEXED,
                    doc_id UNINDEXED,
                    rel_path UNINDEXED,
                    tokenize = 'unicode61 remove_diacritics 2'
                );
            """)

    def reset_index(self):
        with self.conn:
            self.conn.execute("DELETE FROM chunks_fts;")
            self.conn.execute("DELETE FROM chunks;")
            self.conn.execute("DELETE FROM documents;")
            self.conn.execute("DELETE FROM index_meta;")

    def insert_document_and_chunks(
        self,
        doc_id: str,
        rel_path: str,
        file_size: int,
        chunks: List[str]
    ) -> int:
        timestamp = time.time()
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO documents (doc_id, rel_path, file_size, chunk_count, indexed_timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (doc_id, rel_path, file_size, len(chunks), timestamp))

            for idx, chunk_text in enumerate(chunks):
                chunk_id = f"{doc_id}_c{idx:04d}"
                token_est = int(len(chunk_text.split()) * 1.33)

                self.conn.execute("""
                    INSERT OR REPLACE INTO chunks (chunk_id, doc_id, chunk_index, content, token_estimate)
                    VALUES (?, ?, ?, ?, ?)
                """, (chunk_id, doc_id, idx, chunk_text, token_est))

                self.conn.execute("""
                    INSERT INTO chunks_fts (content, chunk_id, doc_id, rel_path)
                    VALUES (?, ?, ?, ?)
                """, (chunk_text, chunk_id, doc_id, rel_path))

        return len(chunks)

    def finalize_metadata(self, total_files: int, total_chunks: int, source_dir: str):
        with self.conn:
            self.conn.execute("INSERT OR REPLACE INTO index_meta (key, value) VALUES (?, ?)", ("version", "1.0.0"))
            self.conn.execute("INSERT OR REPLACE INTO index_meta (key, value) VALUES (?, ?)", ("source_dir", str(source_dir)))
            self.conn.execute("INSERT OR REPLACE INTO index_meta (key, value) VALUES (?, ?)", ("total_files", str(total_files)))
            self.conn.execute("INSERT OR REPLACE INTO index_meta (key, value) VALUES (?, ?)", ("total_chunks", str(total_chunks)))
            self.conn.execute("INSERT OR REPLACE INTO index_meta (key, value) VALUES (?, ?)", ("last_indexed_at", str(time.time())))

    def close(self):
        self.conn.close()


def read_file_safely(file_path: Path) -> str:
    """
    Reads text file content attempting UTF-8, then Latin-1/CP1252.
    Errors are ignored to guarantee indexing never halts on binary artifacts.
    """
    for enc in ("utf-8", "utf-8-sig", "latin-1", "cp1252"):
        try:
            with open(file_path, "r", encoding=enc, errors="replace") as f:
                return f.read()
        except Exception:
            continue
    return ""


def discover_files(source_dir: Path) -> List[Path]:
    """
    Recursively scans the target directory for supported text files.
    """
    discovered: List[Path] = []
    if not source_dir.exists() or not source_dir.is_dir():
        return discovered

    for root, dirs, files in os.walk(source_dir):
        # Filter out ignored directories in-place
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith(".")]

        for file_name in files:
            if file_name.startswith("."):
                continue
            ext = Path(file_name).suffix.lower()
            if ext in SUPPORTED_EXTENSIONS or ext == "":
                discovered.append(Path(root) / file_name)

    return discovered


def run_blind_indexing(source_dir_path: str, index_dir_path: str, chunk_size: int, overlap: int, rebuild: bool = False):
    """
    Orchestrates the blind indexing process with strict privacy controls.
    """
    source_dir = Path(source_dir_path).resolve()
    index_dir = Path(index_dir_path).resolve()
    db_file = index_dir / "private_rag.db"

    print("=" * 80)
    print(" [DDW-X PRIVACY-FIRST RAG] BLIND INDEX INGESTION ENGINE")
    print("=" * 80)
    print(f" [*] Target Source Directory : {source_dir.name}/")
    print(f" [*] Destination Index Store : {index_dir.name}/")
    print(f" [*] Chunking Parameters     : {chunk_size} tokens (overlap: {overlap})")
    print(f" [*] Privacy Enforcement     : ACTIVE (Zero Content Preview Mode)")
    print("-" * 80)

    if not source_dir.exists():
        print(f" [!] ERROR: Source directory '{source_dir}' does not exist.")
        sys.exit(1)

    print(" [*] Scanning directory structure...")
    files = discover_files(source_dir)
    total_files = len(files)

    if total_files == 0:
        print(" [!] No eligible text documents discovered in source directory.")
        return

    print(f" [+] Discovered {total_files} documents eligible for blind indexing.")
    print(" [*] Initializing SQLite FTS5 Search Engine...")

    db = PrivateIndexDatabase(db_file)
    if rebuild:
        print(" [*] Rebuild requested: Purging existing index...")
        db.reset_index()

    chunker = BlindChunker(chunk_size_tokens=chunk_size, overlap_tokens=overlap)
    total_indexed_chunks = 0
    start_time = time.time()

    print(" [*] Ingesting and indexing chunks...")
    for idx, file_path in enumerate(files, 1):
        try:
            rel_path = str(file_path.relative_to(source_dir))
        except ValueError:
            rel_path = file_path.name

        doc_id = hashlib.sha256(rel_path.encode("utf-8")).hexdigest()[:16]
        file_size = file_path.stat().st_size

        # Read and chunk locally in memory
        content = read_file_safely(file_path)
        chunks = chunker.chunk_text(content)

        if chunks:
            chunk_count = db.insert_document_and_chunks(
                doc_id=doc_id,
                rel_path=rel_path,
                file_size=file_size,
                chunks=chunks
            )
            total_indexed_chunks += chunk_count

        # Strictly silent progress indicator (NO content printed)
        if idx % 5 == 0 or idx == total_files:
            elapsed = time.time() - start_time
            rate = idx / max(0.01, elapsed)
            print(f" [PROGRESS] Indexed file [{idx}/{total_files}] ({total_indexed_chunks} total chunks indexed | {rate:.1f} files/s)")

    db.finalize_metadata(total_files=total_files, total_chunks=total_indexed_chunks, source_dir=str(source_dir))
    db.close()

    elapsed = time.time() - start_time
    print("-" * 80)
    print(f" [SUCCESS] Blind Indexing Complete!")
    print(f"  * Total Documents Processed : {total_files}")
    print(f"  * Total Chunks Indexed     : {total_indexed_chunks}")
    print(f"  * Index Database Saved To  : {db_file}")
    print(f"  * Total Execution Time     : {elapsed:.2f} seconds")
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(
        description="DDW-X Blind Ingestion & Vector/BM25 Indexer for Sensitive Datasets",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    # Default to 'D-csR' in current directory or parent
    default_source = "D-csR" if Path("D-csR").exists() else "../D-csR"
    default_index = "D-csR_Index"

    parser.add_argument(
        "--source-dir",
        "-s",
        default=default_source,
        help="Path to sensitive source data directory (e.g. D-csR)"
    )
    parser.add_argument(
        "--index-dir",
        "-o",
        default=default_index,
        help="Destination directory for private search index (e.g. D-csR_Index)"
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=500,
        help="Target chunk size in tokens"
    )
    parser.add_argument(
        "--overlap",
        type=int,
        default=50,
        help="Chunk overlap size in tokens"
    )
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Rebuild the entire index from scratch"
    )

    args = parser.parse_args()
    run_blind_indexing(
        source_dir_path=args.source_dir,
        index_dir_path=args.index_dir,
        chunk_size=args.chunk_size,
        overlap=args.overlap,
        rebuild=args.rebuild
    )


if __name__ == "__main__":
    main()
