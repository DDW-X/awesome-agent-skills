# DDW-X MASTER OPERATIONS MANUAL (v3.0 - PRODUCTION GENESIS)
**Zero-Knowledge Threat Intelligence, Air-Gapped RAG & Command-and-Control (C2) Ecosystem**

---

## TABLE OF CONTENTS
1. [Executive Overview & Security Axioms](#1-executive-overview--security-axioms)
2. [Ecosystem Architecture & Data Flow](#2-ecosystem-architecture--data-flow)
3. [Zero-Knowledge Database & Inverted Index (D-csR)](#3-zero-knowledge-database--inverted-index-d-csr)
4. [Cognitive Firewall & IOC Interceptor](#4-cognitive-firewall--ioc-interceptor)
5. [The Apex Core Engines (v3.0)](#5-the-apex-core-engines-v30)
   - [5.1 Swarm Blackboard & Ephemeral State Bus](#51-swarm-blackboard--ephemeral-state-bus)
   - [5.2 AST Cryptographic Mutator & Watermarker](#52-ast-cryptographic-mutator--watermarker)
   - [5.3 Bulk Threat Harvester & Graph Mapper](#53-bulk-threat-harvester--graph-mapper)
   - [5.4 Local Toolchain & FBOM Builder](#54-local-toolchain--fbom-builder)
6. [Hybrid BM25 / RRF Multi-Query Router](#6-hybrid-bm25--rrf-multi-query-router)
7. [Automated Zero-Knowledge Integrity Auditor](#7-automated-zero-knowledge-integrity-auditor)
8. [Command & Control (C2) REST API & Web Dashboard](#8-command--control-c2-rest-api--web-dashboard)
9. [Interactive CLI Console (`ddwx_console.py`)](#9-interactive-cli-console-ddwx_consolepy)
10. [Quick Start & Operations Guide](#10-quick-start--operations-guide)
11. [Crucible Concurrency & Benchmark Specifications](#11-crucible-concurrency--benchmark-specifications)
12. [DevSecOps & Deployment Runbook](#12-devsecops--deployment-runbook)

---

## 1. EXECUTIVE OVERVIEW & SECURITY AXIOMS

DDW-X is an enterprise-grade, air-gapped security intelligence platform designed for zero-knowledge data retrieval, tactical cognitive isolation, and automated forensic correlation.

### Core Security Axioms
* **Zero-Knowledge Air-Gap (D-csR):** All sensitive private corpora are indexed strictly into abstract topological nodes (`TAG-XXXX-YY`). The AI reasoning context NEVER ingests raw, unmasked, or unauthenticated proprietary files.
* **Deterministic Mathematical Indexing:** SQLite 3.45+ engine utilizing Write-Ahead Logging (WAL), BM25 term weighting, and FTS5 inverted indices.
* **Cognitive Vault Isolation:** Outbound intelligence queries are stripped of sensitive indicators of compromise (IOCs), internal hostnames, and telemetry tags before context ingestion.
* **Cryptographic Payload Integrity:** Every compiled artifact, state bus payload, and mutated test script is watermarked with SHA-256 HMAC digest chains.

---

## 2. ECOSYSTEM ARCHITECTURE & DATA FLOW

```
                      +-----------------------------+
                      |   DDW-X C2 Web Dashboard    |
                      |   (Liquid Glass UI / REST)  |
                      +--------------+--------------+
                                     |
                                     v
                      +-----------------------------+
                      |    DDW-X REST API Engine    |
                      |   (Threaded Non-Blocking)   |
                      +--------------+--------------+
                                     |
    +--------------------------------+-------------------------------+
    |                                |                               |
    v                                v                               v
+-----------------------+ +-----------------------+ +-----------------------+
|  Cognitive Firewall   | |  Hybrid RRF Router    | |   Swarm Blackboard    |
| (Single-Pass Tokenizer| | (Multi-Query BM25 FTS)| | (ChaCha20-Poly1305 Bus|
+-----------------------+ +-----------+-----------+ +-----------------------+
                                      |
                                      v
                      +-----------------------------+
                      | Zero-Knowledge SQLite Core  |
                      |  (51,000+ Chunks / WAL Mode)|
                      +-----------------------------+
```

---

## 3. ZERO-KNOWLEDGE DATABASE & INVERTED INDEX (D-csR)

* **Location:** `D-csR_Index/zk_private_rag.db` & `D-csR_Index/zk_topology_map.json`
* **Schema Topology:**
  - `zk_meta`: Metadata flags, schema versioning, and creation timestamps.
  - `zk_documents`: Cryptographic document hashes, original paths, file sizes, and chunk counts.
  - `zk_chunks`: Tag identifier (`TAG-XXXX-YY`), chunk index, encrypted content, token metrics.
  - `zk_fts`: SQLite FTS5 inverted search index enabling sub-millisecond BM25 keyword matching.
  - `zk_threat_iocs`: Extracted and normalized indicators (IPv4, Domains, SHA-256, MITRE techniques).

---

## 4. COGNITIVE FIREWALL & IOC INTERCEPTOR

* **Engine:** `src/core/rag/zk_cognitive_firewall.py`
* **Operation:**
  - Intercepts sensitive prompts before AI inference.
  - Generates secure session tokens (`{{EDR_SAFE_1}}`, `{{IP_SAFE_1}}`, `{{TARGET_SAFE_1}}`).
  - Utilizes single-pass compiled regex callbacks for ultra-high throughput (>1.5 MB/s on large payloads).
  - Performs reversible reverse translation on LLM responses.

---

## 5. THE APEX CORE ENGINES (v3.0)

### 5.1 Swarm Blackboard & Ephemeral State Bus
* **Engine:** `src/core/rag/zk_swarm_blackboard.py`
* **Features:**
  - AES-256-GCM and ChaCha20-Poly1305 authenticated state bus.
  - `--ttl <seconds>` automated state expiration with SQLite VACUUM cleanup.
  - In-memory event dispatcher hooks for agent state changes.

### 5.2 AST Cryptographic Mutator & Watermarker
* **Engine:** `src/core/rag/zk_polymorphic_mutator.py`
* **Features:**
  - Python AST-level control flow transformation and variable obfuscation.
  - Cryptographic HMAC-SHA256 watermarking embedded in AST docstrings.
  - Verification sub-system to audit author provenance and AST tamper resistance.

### 5.3 Bulk Threat Harvester & Graph Mapper
* **Engine:** `src/core/rag/zk_bulk_threat_harvester.py`
* **Features:**
  - Parallel multi-threaded file ingestion (`ThreadPoolExecutor`).
  - Automatic IOC extraction and relational graph compilation (`doc -> chunk -> ioc`).
  - High-speed batch insertion into SQLite WAL database (`>250 files/second`).

### 5.4 Local Toolchain & FBOM Builder
* **Engine:** `src/core/rag/zk_local_toolchain_builder.py`
* **Features:**
  - Builds standalone single-file binary executables using PyInstaller / Nuitka toolchains.
  - Exports Forensic Bill of Materials (`FBOM.json`) with deterministic artifact digests.

---

## 6. HYBRID BM25 / RRF MULTI-QUERY ROUTER

* **Engine:** `src/core/rag/zk_hybrid_router.py`
* **Mechanism:**
  - Generates multi-angle query expansions from a single intent.
  - Executes simultaneous FTS5 BM25 searches.
  - Merges and ranks results using Reciprocal Rank Fusion (RRF):
    $$RRF\_Score(d) = \sum_{q \in Q} \frac{1}{60 + Rank_q(d)}$$

---

## 7. AUTOMATED ZERO-KNOWLEDGE INTEGRITY AUDITOR

* **Engine:** `src/core/rag/zk_integrity_auditor.py`
* **Features:**
  - `PRAGMA quick_check` and table constraint validation.
  - FTS5 inverted index parity verification.
  - Automatic topology map drift detection and auto-healing.
  - 100% Zero-Knowledge plain-text leak verification scan.

---

## 8. COMMAND & CONTROL (C2) REST API & WEB DASHBOARD

* **API Engine:** `src/core/api/ddwx_api.py`
* **UI Interface:** `src/core/ui/index.html`
* **Key REST Endpoints:**
  - `GET /api/status`: Real-time telemetry, DB metrics, IOC counts, memory caching.
  - `GET /api/search?q=<query>&top_k=5`: Multi-query BM25 search.
  - `GET /api/graph`: Relational threat graph export.
  - `GET /api/blackboard/list`: Swarm tasks and encrypted state bus entries.
  - `POST /api/firewall/mask`: Outbound sensitive prompt interceptor.
  - `POST /api/firewall/unmask`: Inbound reverse translation reconstitutor.
  - `POST /api/audit/run`: Deep integrity and leak verification scan.

---

## 9. INTERACTIVE CLI CONSOLE (`ddwx_console.py`)

* **Engine:** `src/core/rag/ddwx_console.py`
* **Features:**
  - Cyber-tactical terminal user interface with interactive commands:
    - `search <query>`: Interactive ZK Hybrid RAG search.
    - `firewall <mask>|<unmask> <text>`: Live prompt sanitization.
    - `blackboard <push>|<pull>|<list>`: Swarm memory management.
    - `harvest <dir>`: Ingest threat intel feeds into DB.
    - `audit`: Run full zero-knowledge integrity check.

---

## 10. QUICK START & OPERATIONS GUIDE

### Prerequisites
- Python 3.10+ (Recommended Python 3.11 - 3.14)
- Standard virtual environment or system Python.

### Step 1: Launch the C2 Web Dashboard
```bash
# Launch server on port 8080
python src/core/api/ddwx_api.py --port 8080
```
Open browser to: `http://127.0.0.1:8080`

### Step 2: Launch the Tactical CLI Console
```bash
python src/core/rag/ddwx_console.py
```

### Step 3: Run the System Integrity Auditor
```bash
python src/core/rag/zk_integrity_auditor.py
```

---

## 11. CRUCIBLE CONCURRENCY & BENCHMARK SPECIFICATIONS

The system has passed **Phase 9: The Crucible** under high-stress concurrency:
* **API Bombardment:** 200 concurrent requests, 25 worker threads, 100% success (0 dropped packets).
* **Firewall Throughput:** 1.67 MB/s on large 10,000-entity synthetic text payloads (<730ms).
* **Harvester Ingestion:** 500 files ingested in 1.69 seconds (~295 files/sec).
* **Blackboard State Bus:** 100 encrypted ChaCha20 pushes & pulls in <2.1 seconds.
* **Integrity Audit:** 51,614 chunks and FTS records verified 100% in-sync with zero plaintext leaks.

---

## 12. DEVSECOPS & DEPLOYMENT RUNBOOK

### Creating a Standalone Distribution
```bash
python src/core/ddwx_packager.py
```
This builds `dist/DDW-X_Portable/` with all necessary runtimes, database indexes, and single-click Windows batch launchers.

---
*DDW-X Security Intelligence Systems &bull; Phase 10 Genesis Release*
