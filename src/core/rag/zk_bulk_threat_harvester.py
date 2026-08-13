#!/usr/bin/env python3
"""
================================================================================
DDW-X BULK THREAT HARVESTER & GRAPH TOPOLOGY MAPPER (v3.0 - RELATIONAL GRAPH)
================================================================================
Module: src/core/rag/zk_bulk_threat_harvester.py
Architect: Principal AI Architect & Lead DevSecOps Engineer

CAPABILITIES:
1. Relational Threat Graph Mapping (Adjacency List):
   - Builds graph edges linking extracted IOC entities (IPs, Hashes, CVEs, Domains)
     back to originating files, cryptographic chunk tags, and document hashes.
2. Automated Multi-Pattern IOC Extraction:
   - Scans and indexes IPv4 addresses, SHA-256/MD5 hashes, CVE identifiers, and domains
     into dedicated structured metadata tables (zk_threat_iocs).
3. Concurrent Multi-Threaded Chunking & Processing:
   - High-throughput parallel ingestion pipeline using ThreadPoolExecutor.
4. Atomic SQLite WAL Batch Ingestion:
   - Batch database insertion utilizing BEGIN IMMEDIATE transactions.
   - Synchronizes zk_private_rag.db, zk_threat_iocs, and zk_topology_map.json.
================================================================================
"""

import os
import sys
import re
import time
import json
import sqlite3
import hashlib
import random
import argparse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any, Tuple, Set

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

DEFAULT_DB_PATH = "D-csR_Index/zk_private_rag.db"
DEFAULT_TOPOLOGY_PATH = "D-csR_Index/zk_topology_map.json"
DEFAULT_GRAPH_PATH = "scratch/relational_threat_graph.json"
SUPPORTED_EXTENSIONS = {".md", ".txt", ".c", ".cpp", ".h", ".hpp", ".yml", ".yaml", ".yar", ".yara", ".json"}

# IOC PATTERNS
RE_IPV4 = re.compile(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b')
RE_SHA256 = re.compile(r'\b[A-Fa-f0-9]{64}\b')
RE_MD5 = re.compile(r'\b[A-Fa-f0-9]{32}\b')
RE_CVE = re.compile(r'\bCVE-\d{4}-\d{4,7}\b', re.IGNORECASE)
RE_DOMAIN = re.compile(r'\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+(?:com|net|org|io|ru|cn|de|uk|gov|mil|edu)\b', re.IGNORECASE)


class BulkThreatHarvester:
    """
    High-performance recursive file parser, IOC extractor, relational graph builder, and SQLite WAL injector.
    """
    def __init__(self, db_path: str = DEFAULT_DB_PATH, topology_path: str = DEFAULT_TOPOLOGY_PATH,
                 graph_path: str = DEFAULT_GRAPH_PATH, chunk_size: int = 500, overlap: int = 50,
                 max_workers: int = 4):
        self.db_path = Path(db_path).resolve()
        self.topology_path = Path(topology_path).resolve()
        self.graph_path = Path(graph_path).resolve()
        self.chunk_words = max(50, int(chunk_size * 0.75))
        self.overlap_words = max(10, int(overlap * 0.75))
        self.max_workers = max_workers
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.graph_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_schema()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path), timeout=60.0)
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def _ensure_schema(self):
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS zk_meta (
                    key TEXT PRIMARY KEY,
                    value TEXT
                );
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS zk_documents (
                    doc_hash TEXT PRIMARY KEY,
                    file_ext TEXT,
                    file_size INTEGER,
                    chunk_count INTEGER,
                    indexed_at REAL
                );
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS zk_chunks (
                    tag TEXT PRIMARY KEY,
                    doc_hash TEXT,
                    chunk_index INTEGER,
                    content TEXT,
                    token_count INTEGER,
                    FOREIGN KEY (doc_hash) REFERENCES zk_documents(doc_hash) ON DELETE CASCADE
                );
            """)
            conn.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS zk_fts USING fts5(
                    content,
                    tag UNINDEXED,
                    doc_hash UNINDEXED,
                    tokenize = 'unicode61 remove_diacritics 2'
                );
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS zk_threat_iocs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ioc_type TEXT NOT NULL,
                    ioc_value TEXT NOT NULL,
                    tag TEXT,
                    doc_hash TEXT,
                    discovered_at REAL,
                    FOREIGN KEY (tag) REFERENCES zk_chunks(tag) ON DELETE CASCADE
                );
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_ioc_val ON zk_threat_iocs(ioc_value);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_ioc_type ON zk_threat_iocs(ioc_type);")
            conn.commit()

    def extract_iocs(self, text: str) -> List[Tuple[str, str]]:
        iocs: Set[Tuple[str, str]] = set()
        for ip in RE_IPV4.findall(text):
            if not ip.startswith("127.") and not ip.startswith("0."):
                iocs.add(("IPV4", ip))
        for sha in RE_SHA256.findall(text):
            iocs.add(("SHA256", sha.lower()))
        for md5 in RE_MD5.findall(text):
            iocs.add(("MD5", md5.lower()))
        for cve in RE_CVE.findall(text):
            iocs.add(("CVE", cve.upper()))
        for dom in RE_DOMAIN.findall(text):
            if not dom.endswith(".exe") and not dom.endswith(".dll"):
                iocs.add(("DOMAIN", dom.lower()))
        return list(iocs)

    def chunk_text(self, text: str) -> List[str]:
        if not text or not text.strip():
            return []

        cleaned = re.sub(r'[\r\t]+', ' ', text)
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
                    chunks.append(" ".join(current_words))
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

    def discover_files(self, target_dir: Path) -> List[Path]:
        discovered = []
        for root, _, files in os.walk(target_dir):
            for file in files:
                p = Path(root) / file
                if p.suffix.lower() in SUPPORTED_EXTENSIONS:
                    discovered.append(p)
        return discovered

    def _process_single_file(self, f_path: Path, now: float) -> Optional[Dict[str, Any]]:
        try:
            with open(f_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            raw_size = len(content.encode("utf-8"))
            chunks = self.chunk_text(content)
            if not chunks:
                return None

            doc_hash = hashlib.sha256(f"{f_path.name}:{now}:{raw_size}".encode()).hexdigest()[:16].upper()
            ext = f_path.suffix.lower()

            chunk_records = []
            fts_records = []
            ioc_records = []
            topology_nodes = {}
            graph_links = []

            # Document Node in Relational Graph
            doc_node_id = f"doc:{f_path.name}"

            for idx, chunk_content in enumerate(chunks):
                seed_str = f"{doc_hash}:{idx}:{chunk_content[:64]}:{time.time_ns()}:{random.randint(1000, 9999)}"
                h_sha = hashlib.sha256(seed_str.encode("utf-8")).hexdigest()[:4].upper()
                h_md5 = hashlib.md5(f"{seed_str}:{idx}".encode("utf-8")).hexdigest()[:2].upper()
                tag = f"TAG-{h_sha}-{h_md5}"

                token_count = int(len(chunk_content.split()) * 1.33)
                cluster_id = int(hashlib.md5(f"{doc_hash}_{idx}".encode()).hexdigest()[:2], 16) % 16

                chunk_records.append((tag, doc_hash, idx, chunk_content, token_count))
                fts_records.append((chunk_content, tag, doc_hash))

                chunk_node_id = f"chunk:{tag}"
                graph_links.append({
                    "source": doc_node_id,
                    "target": chunk_node_id,
                    "relation": "CONTAINS_CHUNK"
                })

                # Extract IOCs for this chunk
                found_iocs = self.extract_iocs(chunk_content)
                for ioc_type, ioc_val in found_iocs:
                    ioc_records.append((ioc_type, ioc_val, tag, doc_hash, now))
                    ioc_node_id = f"ioc:{ioc_type}:{ioc_val}"
                    graph_links.append({
                        "source": chunk_node_id,
                        "target": ioc_node_id,
                        "relation": f"EXPOSES_{ioc_type}",
                        "ioc_value": ioc_val
                    })

                topology_nodes[tag] = {
                    "tag": tag,
                    "doc_hash": doc_hash,
                    "file_ext": ext,
                    "chunk_index": idx,
                    "token_count": token_count,
                    "cluster_id": cluster_id
                }

            return {
                "file_name": f_path.name,
                "doc_record": (doc_hash, ext, raw_size, len(chunks), now),
                "chunks": chunk_records,
                "fts": fts_records,
                "iocs": ioc_records,
                "topologies": topology_nodes,
                "graph_links": graph_links
            }
        except Exception as e:
            print(f"[!] Error reading {f_path.name}: {e}")
            return None

    def harvest_directory(self, target_dir: Path) -> Dict[str, Any]:
        start_time = time.perf_counter()
        files = self.discover_files(target_dir)

        if not files:
            return {
                "status": "EMPTY",
                "files_scanned": 0,
                "chunks_minted": 0,
                "iocs_extracted": 0,
                "latency_ms": 0.0
            }

        now = time.time()
        batch_documents = []
        batch_chunks = []
        batch_fts = []
        batch_iocs = []
        all_graph_links = []
        new_topologies: Dict[str, Any] = {}

        # Phase 1: Parallel File Processing & Relational Mapping
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_file = {executor.submit(self._process_single_file, f, now): f for f in files}
            for future in as_completed(future_to_file):
                res = future.result()
                if res:
                    batch_documents.append(res["doc_record"])
                    batch_chunks.extend(res["chunks"])
                    batch_fts.extend(res["fts"])
                    batch_iocs.extend(res["iocs"])
                    all_graph_links.extend(res["graph_links"])
                    new_topologies.update(res["topologies"])

        # Phase 2: Atomic WAL Database Insertion
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("BEGIN IMMEDIATE;")
        try:
            cursor.executemany("""
                INSERT OR REPLACE INTO zk_documents (doc_hash, file_ext, file_size, chunk_count, indexed_at)
                VALUES (?, ?, ?, ?, ?);
            """, batch_documents)

            cursor.executemany("""
                INSERT OR REPLACE INTO zk_chunks (tag, doc_hash, chunk_index, content, token_count)
                VALUES (?, ?, ?, ?, ?);
            """, batch_chunks)

            cursor.executemany("""
                INSERT INTO zk_fts (content, tag, doc_hash)
                VALUES (?, ?, ?);
            """, batch_fts)

            if batch_iocs:
                cursor.executemany("""
                    INSERT INTO zk_threat_iocs (ioc_type, ioc_value, tag, doc_hash, discovered_at)
                    VALUES (?, ?, ?, ?, ?);
                """, batch_iocs)

            # Metadata updates
            cursor.execute("SELECT COUNT(*) FROM zk_documents;")
            total_docs = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM zk_chunks;")
            total_db_chunks = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM zk_threat_iocs;")
            total_iocs_db = cursor.fetchone()[0]

            cursor.execute("INSERT OR REPLACE INTO zk_meta (key, value) VALUES ('total_documents', ?);", (str(total_docs),))
            cursor.execute("INSERT OR REPLACE INTO zk_meta (key, value) VALUES ('total_chunks', ?);", (str(total_db_chunks),))
            cursor.execute("INSERT OR REPLACE INTO zk_meta (key, value) VALUES ('total_iocs', ?);", (str(total_iocs_db),))
            cursor.execute("INSERT OR REPLACE INTO zk_meta (key, value) VALUES ('last_updated', ?);", (str(now),))

            conn.commit()
        except Exception as e:
            conn.rollback()
            conn.close()
            raise e
        finally:
            conn.close()

        # Phase 3: Synchronize Topology Map
        if self.topology_path.exists():
            try:
                with open(self.topology_path, "r", encoding="utf-8") as f:
                    top_map = json.load(f)
            except Exception:
                top_map = {"metadata": {}, "topology": []}
        else:
            top_map = {"metadata": {}, "topology": []}

        existing_topology = top_map.get("topology", [])
        if isinstance(existing_topology, list):
            existing_tags = {node["tag"] for node in existing_topology if isinstance(node, dict) and "tag" in node}
            for tag, node in new_topologies.items():
                if tag not in existing_tags:
                    node_entry = dict(node)
                    node_entry["tag"] = tag
                    existing_topology.append(node_entry)
            top_map["topology"] = existing_topology
            total_tags_count = len(existing_topology)
        elif isinstance(existing_topology, dict):
            existing_topology.update(new_topologies)
            top_map["topology"] = existing_topology
            total_tags_count = len(existing_topology)
        else:
            top_map["topology"] = list(new_topologies.values())
            total_tags_count = len(top_map["topology"])

        top_map["metadata"] = {
            "version": "2.0.0-zk-hybrid",
            "last_updated": now,
            "total_tags": total_tags_count
        }

        temp_top = self.topology_path.with_suffix(".tmp")
        with open(temp_top, "w", encoding="utf-8") as f:
            json.dump(top_map, f, indent=2)

        if os.name == "nt" and self.topology_path.exists():
            os.replace(temp_top, self.topology_path)
        else:
            temp_top.replace(self.topology_path)

        # Phase 4: Export Relational Threat Graph JSON
        threat_graph = {
            "version": "3.0-relational-graph",
            "generated_at": now,
            "target_dir": str(target_dir),
            "total_edges": len(all_graph_links),
            "edges": all_graph_links
        }
        with open(self.graph_path, "w", encoding="utf-8") as f:
            json.dump(threat_graph, f, indent=2)

        latency_ms = (time.perf_counter() - start_time) * 1000.0

        return {
            "status": "SUCCESS",
            "target_directory": str(target_dir),
            "files_scanned": len(files),
            "chunks_minted": len(batch_chunks),
            "iocs_extracted": len(batch_iocs),
            "graph_edges_created": len(all_graph_links),
            "graph_file": str(self.graph_path),
            "total_db_chunks": total_db_chunks,
            "total_iocs_in_db": total_iocs_db,
            "latency_ms": latency_ms,
            "graph_sample": all_graph_links[:5]
        }


def main():
    parser = argparse.ArgumentParser(
        description="DDW-X Bulk Threat Harvester & Relational Graph Mapper (v3.0)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-d", "--dir", required=True, help="Target directory to harvest recursively")
    parser.add_argument("--db-path", default=DEFAULT_DB_PATH, help="Path to SQLite database")
    parser.add_argument("--topology-path", default=DEFAULT_TOPOLOGY_PATH, help="Path to topology JSON map")
    parser.add_argument("--graph-path", default=DEFAULT_GRAPH_PATH, help="Path for output relational graph JSON")
    parser.add_argument("--workers", type=int, default=4, help="Concurrent worker threads")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")

    args = parser.parse_args()
    target_dir = Path(args.dir).resolve()

    if not target_dir.exists() or not target_dir.is_dir():
        print(f"[!] Error: Target directory not found: {target_dir}")
        sys.exit(1)

    harvester = BulkThreatHarvester(
        db_path=args.db_path,
        topology_path=args.topology_path,
        graph_path=args.graph_path,
        max_workers=args.workers
    )
    res = harvester.harvest_directory(target_dir)

    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print("=" * 80)
        print(" [DDW-X BULK THREAT HARVESTER] RELATIONAL GRAPH REPORT (v3.0)")
        print("=" * 80)
        print(f" [*] Target Directory   : {res.get('target_directory')}")
        print(f" [*] Files Ingested     : {res.get('files_scanned')}")
        print(f" [*] Chunks Minted      : {res.get('chunks_minted')}")
        print(f" [*] IOCs Indexed       : {res.get('iocs_extracted')} (Structured DB Table)")
        print(f" [*] Graph Edges Built  : {res.get('graph_edges_created')} (Relational Adjacency List)")
        print(f" [*] Graph Export Path  : {res.get('graph_file')}")
        print(f" [*] Ingestion Latency  : {res.get('latency_ms', 0.0):.2f} ms")
        print(f" [*] Ingestion Status   : {res.get('status')}")
        if res.get("graph_sample"):
            print("-" * 80)
            print(" [RELATIONAL GRAPH EDGES (SAMPLE)]:")
            print(json.dumps(res["graph_sample"], indent=2))
        print("=" * 80)


if __name__ == "__main__":
    main()
