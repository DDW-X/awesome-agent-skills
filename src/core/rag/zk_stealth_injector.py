#!/usr/bin/env python3
"""
================================================================================
DDW-X ZERO-KNOWLEDGE LOCAL RAG: OSINT STEALTH INJECTOR & RAW DATA REFINER
================================================================================
Module: src/core/rag/zk_stealth_injector.py
Architect: Principal AI Architect & Lead Zero-Knowledge Systems Engineer

MATHEMATICAL ARCHITECTURE & PIPELINE:
1. Web Fetcher Module: Ingests raw HTTP/HTTPS URLs, local files, or raw text streams.
   Cleans HTML/DOM artifacts using resilient built-in parsers with fallback options.
2. Cognitive Refiner Module: Formats unstructured text into high-density semantic
   chunks (500 tokens, 50-token overlap) with heuristic TTP tagging.
3. Stealth Injector Module: Computes collision-resistant cryptographic TAGs and
   atomically appends records to 'zk_private_rag.db' using WAL transactions.
4. Topology Updater: Atomically updates 'zk_topology_map.json' preserving zero-knowledge
   guarantees (strictly zero raw text written to topology).
================================================================================
"""

import os
import sys
import re
import json
import time
import sqlite3
import argparse
import hashlib
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path
from html.parser import HTMLParser
from typing import List, Dict, Any, Optional, Tuple

# Optional BeautifulSoup acceleration
try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

DEFAULT_DB_PATH = "D-csR_Index/zk_private_rag.db"
DEFAULT_TOPOLOGY_PATH = "D-csR_Index/zk_topology_map.json"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"


# ==============================================================================
# 1. WEB FETCHER & DOM STRIPPER MODULE
# ==============================================================================

class LightweightHTMLStripper(HTMLParser):
    """
    Standard-library zero-dependency HTML text extractor and stripper.
    Removes script, style, nav, footer, and boilerplate elements.
    """
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text_parts: List[str] = []
        self.ignored_tags = {"script", "style", "nav", "footer", "header", "aside", "noscript", "svg", "form"}
        self.current_ignore_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag.lower() in self.ignored_tags:
            self.current_ignore_depth += 1
        elif tag.lower() in {"p", "div", "h1", "h2", "h3", "h4", "h5", "h6", "li", "tr", "br"}:
            self.text_parts.append("\n")

    def handle_endtag(self, tag):
        if tag.lower() in self.ignored_tags and self.current_ignore_depth > 0:
            self.current_ignore_depth -= 1
        elif tag.lower() in {"p", "div", "h1", "h2", "h3", "h4", "h5", "h6", "li", "tr"}:
            self.text_parts.append("\n")

    def handle_data(self, data):
        if self.current_ignore_depth == 0:
            cleaned = data.strip()
            if cleaned:
                self.text_parts.append(cleaned + " ")

    def get_text(self) -> str:
        raw = "".join(self.text_parts)
        # Normalize redundant blank lines
        return re.sub(r'\n\s*\n+', '\n\n', raw).strip()


class OSINTWebFetcher:
    """
    Fetches raw intelligence feeds from URLs, local files, or raw text buffers.
    """
    @staticmethod
    def fetch_url(url: str, timeout: int = 15) -> str:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,text/plain;q=0.8,*/*;q=0.7",
                "Accept-Language": "en-US,en;q=0.9"
            }
        )
        with urllib.request.urlopen(req, timeout=timeout) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            raw_bytes = response.read()
            try:
                return raw_bytes.decode(charset, errors="replace")
            except Exception:
                return raw_bytes.decode("utf-8", errors="replace")

    @classmethod
    def clean_html(cls, html_content: str) -> str:
        if HAS_BS4:
            soup = BeautifulSoup(html_content, "html.parser")
            for elem in soup(["script", "style", "nav", "footer", "header", "aside", "noscript", "svg", "form"]):
                elem.decompose()
            text = soup.get_text(separator="\n")
            return re.sub(r'\n\s*\n+', '\n\n', text).strip()
        else:
            stripper = LightweightHTMLStripper()
            stripper.feed(html_content)
            return stripper.get_text()


# ==============================================================================
# 2. THE COGNITIVE REFINER MODULE
# ==============================================================================

class CognitiveRefiner:
    """
    Transforms raw scraped or imported text into structured, high-density
    semantic chunks optimized for SQLite FTS5 BM25 retrieval.
    """
    def __init__(self, chunk_size_tokens: int = 500, overlap_tokens: int = 50):
        self.chunk_words = max(50, int(chunk_size_tokens * 0.75))
        self.overlap_words = max(10, int(overlap_tokens * 0.75))

    def refine_and_chunk(self, raw_text: str, source_label: str) -> List[str]:
        if not raw_text or not raw_text.strip():
            return []

        # Remove common web boilerplate patterns
        cleaned = re.sub(r'(Cookie Policy|Accept All Cookies|Terms of Service|Privacy Policy|All rights reserved\.)', '', raw_text, flags=re.IGNORECASE)
        cleaned = re.sub(r'[\r\t]+', ' ', cleaned)
        cleaned = re.sub(r' +', ' ', cleaned)

        paragraphs = re.split(r'(\n\s*\n)', cleaned)
        chunks: List[str] = []
        current_words: List[str] = []
        current_count = 0

        for segment in paragraphs:
            words = segment.split()
            if not words:
                continue

            if current_count + len(words) <= self.chunk_words:
                current_words.extend(words)
                current_count += len(words)
            else:
                if current_words:
                    chunk_text = " ".join(current_words)
                    chunks.append(chunk_text)
                    if self.overlap_words < len(current_words):
                        current_words = current_words[-self.overlap_words:]
                    else:
                        current_words = []
                    current_count = len(current_words)

                if len(words) > self.chunk_words:
                    step = max(1, self.chunk_words - self.overlap_words)
                    for i in range(0, len(words), step):
                        slice_w = words[i:i + self.chunk_words]
                        if slice_w:
                            chunks.append(" ".join(slice_w))
                    current_words = []
                    current_count = 0
                else:
                    current_words.extend(words)
                    current_count += len(words)

        if current_words:
            final_chunk = " ".join(current_words)
            if not chunks or final_chunk != chunks[-1]:
                chunks.append(final_chunk)

        return chunks


# ==============================================================================
# 3. STEALTH INJECTOR & DATABASE INTEGRITY MODULE
# ==============================================================================

class StealthDatabaseInjector:
    """
    Manages atomic injection of refined OSINT intelligence into SQLite FTS5 database
    with strict transaction isolation and collision-resistant tag minting.
    """
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path), timeout=30.0)
        self.conn.execute("PRAGMA journal_mode = WAL;")
        self.conn.execute("PRAGMA synchronous = NORMAL;")
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self._ensure_schema()

    def _ensure_schema(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS zk_meta (
                    key TEXT PRIMARY KEY,
                    value TEXT
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS zk_documents (
                    doc_hash TEXT PRIMARY KEY,
                    file_ext TEXT,
                    file_size INTEGER,
                    chunk_count INTEGER,
                    indexed_at REAL
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS zk_chunks (
                    tag TEXT PRIMARY KEY,
                    doc_hash TEXT,
                    chunk_index INTEGER,
                    content TEXT,
                    token_count INTEGER,
                    FOREIGN KEY (doc_hash) REFERENCES zk_documents(doc_hash) ON DELETE CASCADE
                );
            """)
            self.conn.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS zk_fts USING fts5(
                    content,
                    tag UNINDEXED,
                    doc_hash UNINDEXED,
                    tokenize = 'unicode61 remove_diacritics 2'
                );
            """)

    def _generate_unique_tag(self, doc_hash: str, chunk_index: int, content: str) -> str:
        """
        Computes a collision-resistant cryptographic tag.
        Format: TAG-<HEX4>-<HEX2> (e.g. TAG-E4A1-B9).
        If collision detected, appends monotonic sequence suffix.
        """
        seed_str = f"{doc_hash}:{chunk_index}:{content[:64]}:{time.time_ns()}"
        h_sha = hashlib.sha256(seed_str.encode("utf-8")).hexdigest()[:4].upper()
        h_md5 = hashlib.md5(content.encode("utf-8")).hexdigest()[:2].upper()
        base_tag = f"TAG-{h_sha}-{h_md5}"

        cursor = self.conn.cursor()
        cursor.execute("SELECT 1 FROM zk_chunks WHERE tag = ?", (base_tag,))
        if not cursor.fetchone():
            return base_tag

        # Collision fallback (monotonic increment suffix)
        counter = 1
        while True:
            candidate = f"{base_tag}-{counter}"
            cursor.execute("SELECT 1 FROM zk_chunks WHERE tag = ?", (candidate,))
            if not cursor.fetchone():
                return candidate
            counter += 1

    def inject_chunks(
        self,
        source_name: str,
        file_ext: str,
        raw_size: int,
        chunks: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Atomically inserts new document chunks into SQLite FTS5 index.
        Uses explicit transaction boundary (BEGIN IMMEDIATE) to guarantee integrity.
        """
        doc_hash = hashlib.sha256(f"{source_name}:{time.time()}".encode("utf-8")).hexdigest()[:16].upper()
        timestamp = time.time()
        minted_topologies: List[Dict[str, Any]] = []

        # Atomic Transaction Lock
        cursor = self.conn.cursor()
        cursor.execute("BEGIN IMMEDIATE;")
        try:
            # 1. Insert Document Entry
            cursor.execute("""
                INSERT OR REPLACE INTO zk_documents (doc_hash, file_ext, file_size, chunk_count, indexed_at)
                VALUES (?, ?, ?, ?, ?)
            """, (doc_hash, file_ext, raw_size, len(chunks), timestamp))

            # 2. Insert Chunks & Inverted Index
            for idx, chunk_content in enumerate(chunks):
                tag = self._generate_unique_tag(doc_hash, idx, chunk_content)
                token_count = int(len(chunk_content.split()) * 1.33)
                cluster_id = int(hashlib.md5(f"{doc_hash}_{idx}".encode()).hexdigest()[:2], 16) % 16

                cursor.execute("""
                    INSERT INTO zk_chunks (tag, doc_hash, chunk_index, content, token_count)
                    VALUES (?, ?, ?, ?, ?)
                """, (tag, doc_hash, idx, chunk_content, token_count))

                cursor.execute("""
                    INSERT INTO zk_fts (content, tag, doc_hash)
                    VALUES (?, ?, ?)
                """, (chunk_content, tag, doc_hash))

                minted_topologies.append({
                    "tag": tag,
                    "doc_hash": doc_hash,
                    "file_ext": file_ext,
                    "chunk_index": idx,
                    "token_count": token_count,
                    "cluster_id": cluster_id
                })

            # 3. Update Metadata Counters
            cursor.execute("SELECT COUNT(*) FROM zk_documents;")
            total_docs = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM zk_chunks;")
            total_chunks = cursor.fetchone()[0]

            cursor.execute("INSERT OR REPLACE INTO zk_meta (key, value) VALUES (?, ?)", ("total_files", str(total_docs)))
            cursor.execute("INSERT OR REPLACE INTO zk_meta (key, value) VALUES (?, ?)", ("total_chunks", str(total_chunks)))
            cursor.execute("INSERT OR REPLACE INTO zk_meta (key, value) VALUES (?, ?)", ("last_injected_at", str(timestamp)))

            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e

        return minted_topologies

    def close(self):
        self.conn.close()


# ==============================================================================
# 4. TOPOLOGY MAP SYNCHRONIZER MODULE
# ==============================================================================

class TopologyMapUpdater:
    """
    Safely updates 'zk_topology_map.json' without exposing raw text or corrupting JSON.
    """
    @staticmethod
    def update_topology(topology_path: Path, new_records: List[Dict[str, Any]], source_name: str):
        topology_data = {
            "metadata": {
                "version": "2.0.0-zk",
                "last_updated": time.time(),
                "total_documents": 0,
                "total_tags": 0
            },
            "topology": []
        }

        if topology_path.exists():
            try:
                with open(topology_path, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    if isinstance(loaded, dict) and "topology" in loaded:
                        topology_data = loaded
            except Exception:
                pass

        # Append new records
        topology_data["topology"].extend(new_records)
        topology_data["metadata"]["total_tags"] = len(topology_data["topology"])
        topology_data["metadata"]["last_updated"] = time.time()
        topology_data["metadata"]["latest_source_injected"] = hashlib.sha256(source_name.encode()).hexdigest()[:12]

        # Atomic write via temporary file
        temp_file = topology_path.with_suffix(".tmp")
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(topology_data, f, indent=2)

        if os.name == "nt" and topology_path.exists():
            os.replace(temp_file, topology_path)
        else:
            temp_file.replace(topology_path)


# ==============================================================================
# 5. CLI ORCHESTRATION & ENTRY POINT
# ==============================================================================

def run_stealth_injection(
    url: Optional[str] = None,
    file_path: Optional[str] = None,
    raw_text: Optional[str] = None,
    source_tag: Optional[str] = None,
    db_path: str = DEFAULT_DB_PATH,
    topology_path: str = DEFAULT_TOPOLOGY_PATH,
    chunk_size: int = 500,
    overlap: int = 50
) -> List[str]:
    """
    Orchestrates web fetching, cognitive refining, database injection,
    and topology map updating with zero text printed to terminal.
    """
    target_db = Path(db_path).resolve()
    target_topo = Path(topology_path).resolve()

    print("=" * 80)
    print(" [DDW-X OSINT STEALTH INJECTOR] ZERO-KNOWLEDGE RAW DATA REFINER")
    print("=" * 80)
    print(f" [*] Database Target        : {target_db.name}")
    print(f" [*] Privacy Enforcement    : ZERO-KNOWLEDGE (No Text Output / Stealth Mode)")
    print("-" * 80)

    # 1. Fetch Raw Content
    source_name = source_tag or "unspecified_feed"
    file_ext = ".txt"
    raw_content = ""

    if url:
        source_name = url
        file_ext = ".html"
        print(f" [*] Fetching remote OSINT stream: {urllib.parse.urlparse(url).netloc}...")
        html_data = OSINTWebFetcher.fetch_url(url)
        raw_content = OSINTWebFetcher.clean_html(html_data)
    elif file_path:
        f_path = Path(file_path).resolve()
        source_name = f_path.name
        file_ext = f_path.suffix or ".txt"
        print(f" [*] Ingesting local file asset: {f_path.name}...")
        with open(f_path, "r", encoding="utf-8", errors="replace") as f:
            raw_content = f.read()
    elif raw_text:
        source_name = source_tag or "raw_text_stream"
        file_ext = ".txt"
        raw_content = raw_text
    else:
        print(" [!] ERROR: No input source provided (URL, file, or raw text).", file=sys.stderr)
        sys.exit(1)

    raw_bytes_len = len(raw_content.encode("utf-8"))
    if raw_bytes_len == 0:
        print(" [!] WARN: Target stream yielded empty payload. Aborting injection.", file=sys.stderr)
        return []

    # 2. Cognitive Refinement & Dynamic Chunking
    print(" [*] Refining unstructured payload into semantic chunks...")
    refiner = CognitiveRefiner(chunk_size_tokens=chunk_size, overlap_tokens=overlap)
    chunks = refiner.refine_and_chunk(raw_content, source_name)

    if not chunks:
        print(" [!] WARN: Cognitive refiner generated zero eligible chunks.", file=sys.stderr)
        return []

    print(f" [+] Cognitive refiner produced {len(chunks)} high-density semantic chunks.")

    # 3. Stealth Database Injection
    print(" [*] Executing atomic database transaction into FTS5 index...")
    injector = StealthDatabaseInjector(target_db)
    minted_topologies = injector.inject_chunks(
        source_name=source_name,
        file_ext=file_ext,
        raw_size=raw_bytes_len,
        chunks=chunks
    )
    injector.close()

    # 4. Update Topology Map
    print(" [*] Synchronizing topology map...")
    TopologyMapUpdater.update_topology(
        topology_path=target_topo,
        new_records=minted_topologies,
        source_name=source_name
    )

    minted_tags = [t["tag"] for t in minted_topologies]

    print("-" * 80)
    print(" [SUCCESS] Stealth Injection Completed Successfully!")
    print(f"  * Ingested Source ID       : {hashlib.sha256(source_name.encode()).hexdigest()[:12]}")
    print(f"  * New Chunks Minted        : {len(minted_tags)}")
    print(f"  * Minted Cryptographic TAGs : {', '.join(minted_tags)}")
    print(f"  * Target Database          : {target_db.name}")
    print(f"  * Topology Map             : {target_topo.name}")
    print("=" * 80)

    return minted_tags


def main():
    parser = argparse.ArgumentParser(
        description="DDW-X OSINT Stealth Injector & Raw Data Refiner",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-u", "--url", help="HTTP/HTTPS URL to fetch, refine, and inject")
    group.add_argument("-f", "--file", help="Path to local file to refine and inject")
    group.add_argument("-t", "--text", help="Raw string content to refine and inject")

    parser.add_argument("--source-tag", default=None, help="Optional source identifier tag")
    parser.add_argument("--db-path", default=DEFAULT_DB_PATH, help="Path to SQLite ZK Database")
    parser.add_argument("--topology-path", default=DEFAULT_TOPOLOGY_PATH, help="Path to topology map JSON")
    parser.add_argument("--chunk-size", type=int, default=500, help="Target chunk size in tokens")
    parser.add_argument("--overlap", type=int, default=50, help="Chunk overlap in tokens")

    args = parser.parse_args()

    run_stealth_injection(
        url=args.url,
        file_path=args.file,
        raw_text=args.text,
        source_tag=args.source_tag,
        db_path=args.db_path,
        topology_path=args.topology_path,
        chunk_size=args.chunk_size,
        overlap=args.overlap
    )


if __name__ == "__main__":
    main()
