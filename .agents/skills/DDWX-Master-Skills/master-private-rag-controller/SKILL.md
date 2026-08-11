---
name: "<DDW-X> Master: Private RAG Controller"
description: "Privacy-first zero-exposure retrieval controller for DDW-X private knowledge corpus (D-csR). Use when answering questions about private documents, sensitive datasets, internal notes, or proprietary code. Enforces strictly tool-mediated search via query_private_index.py without direct file access."
---

# <DDW-X> Master Skill: Private RAG Controller (Blind Retrieval Engine)

## 1. Executive Privacy Architecture & Purpose

This Master Skill establishes a **Zero-Exposure / Blind Retrieval-Augmented Generation (RAG)** protocol for the sensitive dataset located in `D-csR/`.

The AI Agent acts as a **Blind Controller**:
- **Zero Raw File Inspection**: The Agent is strictly forbidden from directly opening, listing contents of, reading (`cat`, `head`, `view_file`, `grep_search`), or printing raw files within the `D-csR/` directory.
- **Isolated Tool Mediation**: All contextual lookups MUST occur exclusively through the local retrieval tool `src/core/rag/query_private_index.py`.
- **Minimal Context Exposure**: The Agent only receives the top-k relevant text chunks returned by the local search engine, preserving end-to-end data confidentiality.

---

## 2. When to Activate

Activate this skill when:
- The user asks questions regarding documents, notes, internal logs, specifications, or code stored in the private directory (`D-csR`).
- Searching, summarizing, or cross-referencing sensitive or internal enterprise materials.
- Managing, querying, or troubleshooting the local RAG indexing pipeline.

---

## 3. Tool Calling Protocol & Commands

### A. Context Retrieval Command (Agent Primary Tool)

Whenever private context is required to fulfill a user request, execute the search tool via command line:

```bash
python src/core/rag/query_private_index.py "USER_SEARCH_QUERY" --top-k 3
```

#### Optional Retrieval Flags:
- `--top-k <N>` : Retrieve top N most relevant chunks (default: `3`).
- `--json`       : Output results as a structured JSON object.
- `--db-path <PATH>` : Custom path to index database (default: `D-csR_Index/private_rag.db`).

### B. Index Building & Updating (User/System Tool)

To build or refresh the local search index across `D-csR`:

```bash
python src/core/rag/build_private_index.py --source-dir D-csR --index-dir D-csR_Index
```

#### Optional Indexing Flags:
- `--chunk-size <TOKENS>` : Target token count per chunk (default: `500`).
- `--overlap <TOKENS>`    : Overlap token count between adjacent chunks (default: `50`).
- `--rebuild`             : Re-index the entire dataset from scratch.

---

## 4. Operational Workflow for AI Agents

```
┌─────────────────────────┐
│  User Query Received    │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────┐
│ Formulate Search Keywords from User Query               │
└───────────┬─────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────┐
│ Run: python src/core/rag/query_private_index.py "<QUERY>"│
└───────────┬─────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────┐
│ Silently Ingest Retrieved Top-K Chunks into Memory      │
└───────────┬─────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────┐
│ Synthesize Professional, Factual Answer for User       │
│ (Citing source file names only as references)           │
└─────────────────────────────────────────────────────────┘
```

---

## 5. Strict Behavioral Patterns & Guardrails

### ✅ Approved Pattern: Tool-Mediated Querying
```bash
# Agent runs query tool with extracted search terms
python src/core/rag/query_private_index.py "database migration schema" --top-k 3
```
*Agent reads stdout of the query tool silently and formulates the answer based exclusively on the returned chunks.*

---

### ❌ FORBIDDEN Pattern: Direct Raw File Inspection
```bash
# STRICTLY PROHIBITED - DO NOT EXECUTE
cat D-csR/database_notes.md
head -n 50 D-csR/private_config.txt
type D-csR\secret.md
```
*Direct file reading violates the zero-knowledge privacy directive.*

---

### ❌ FORBIDDEN Pattern: Dumping Entire Chunks Unprocessed
*Do not vomit raw internal chunk formatting directly to the user. Always synthesize clear, structured explanations answering the specific question.*

---

## 6. Verification & Execution Checklist

Before responding to queries involving private data:
1. [ ] **Verify No Direct File Access**: Ensure no `view_file`, `cat`, `head`, `tail`, or wildcards were executed on `D-csR`.
2. [ ] **Execute Targeted Query**: Run `query_private_index.py` with refined, relevant keyword phrases.
3. [ ] **Handle Empty Results**: If no chunks are returned, re-run with broader search keywords or notify the user to run `build_private_index.py`.
4. [ ] **Synthesize Factually**: Ground the answer strictly in the retrieved context without hallucinating internal details.
