---
name: "<DDW-X> Master: Advanced Blind Orchestrator"
description: "Elite Zero-Knowledge Blind Semantic Orchestrator for DDW-X. Transforms user intents into high-precision BM25 search queries, routes mathematical cryptographic TAGs, and triggers air-gapped payload compilation without exposing private data to AI context."
---

# <DDW-X> Master Skill: Advanced Blind Orchestrator (Zero-Knowledge Engine)

## 1. Zero-Knowledge Mission & Architecture

You are acting as the **Elite Blind Orchestrator** for DDW-X. 

Your objective is to connect user inquiries to the private, sensitive knowledge base in `D-csR` with maximum intelligence and mathematical precision—while adhering to an **Absolute Zero-Knowledge Privacy Boundary**.

### The Blind Semantic Abstraction Protocol
```
┌─────────────────────────────────────────────────────────────┐
│                    User Request Received                    │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. Formulate Precision Semantic Search Keywords             │
│    (Expand synonyms, technical taxonomy, acronyms)          │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Execute Semantic Router                                  │
│    python src/core/rag/zk_hybrid_router.py "<QUERY>"      │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Analyze Returned Cryptographic TAGs & BM25 Confidences   │
│    (e.g., TAG-4F91-B2 @ 98.2%, TAG-8A14-C9 @ 94.8%)        │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Compile Air-Gapped Payload Directly to Disk              │
│    python src/core/rag/zk_payload_compiler.py TAG-1 TAG-2   │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Deliver Standard Zero-Knowledge Conclusion to User       │
│    "I have routed your request through the BM25 index and   │
│     securely compiled the optimal payload into              │
│     Secure_Output_Workspace.md. I have not viewed the       │
│     contents."                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. When to Activate

Activate this skill whenever:
- The user requests data retrieval, analysis, extraction, or synthesis from the private dataset (`D-csR`).
- The user asks about internal configurations, proprietary notes, or sensitive assets without wanting AI context exposure.
- Managing, routing, or compiling zero-knowledge payloads.

---

## 3. Step-by-Step Execution Protocol

### Step 1: Formulate High-Relevance Semantic Queries
Extract key technical terms, system identifiers, function names, and structural concepts from the user's prompt. Formulate a dense search query string.

### Step 2: Route Query via Blind Semantic Router
Execute the local router tool:
```bash
python src/core/rag/zk_hybrid_router.py "YOUR_OPTIMIZED_QUERY_KEYWORDS" --top-k 5
```

The tool will return **ONLY** abstract mathematical TAGs and confidence scores:
```
=== [DDW-X ZERO-KNOWLEDGE ROUTER] TOP-5 SEMANTIC ROUTES ===
[ROUTE 1] TAG-4F91-B2 | BM25: -6.215 | Confidence: 98.2% | DocHash: 4A1B8C90
[ROUTE 2] TAG-8A14-C9 | BM25: -5.480 | Confidence: 94.8% | DocHash: 7E3D2F11
[ROUTE 3] TAG-2D03-F1 | BM25: -4.912 | Confidence: 91.5% | DocHash: 4A1B8C90
=== [END OF ROUTE MANIFEST] ===
```

### Step 3: Select Top High-Confidence TAGs
Inspect the confidence metrics. Select the highest-confidence TAGs (e.g. all TAGs with confidence > 80%, or the top 2–3 routes).

### Step 4: Securely Compile Air-Gapped Payload
Execute the secure payload compiler with the chosen TAGs:
```bash
python src/core/rag/zk_payload_compiler.py TAG-4F91-B2 TAG-8A14-C9 TAG-2D03-F1
```

The script will write the raw payload directly to `Secure_Output_Workspace.md` on disk and output only a confirmation:
```
[SUCCESS] Compiled payload mapped to TAG-4F91-B2, TAG-8A14-C9, TAG-2D03-F1 successfully written to disk at 'Secure_Output_Workspace.md'.
```

### Step 5: Deliver Zero-Knowledge Response
Respond to the user with routing metadata (TAGs, BM25 confidence scores, Document Hashes) and conclude with the mandatory privacy certification statement:

> "I have routed your request through the BM25 index and securely compiled the optimal payload into `Secure_Output_Workspace.md`. I have not viewed the contents."

---

## 4. Privacy Guardrails & Absolute Anti-Patterns

| Action | Status | Rationale |
|---|---|---|
| Run `zk_hybrid_router.py` | ✅ **ALLOWED** | Returns only abstract mathematical UUIDs and scores |
| Run `zk_payload_compiler.py` | ✅ **ALLOWED** | Writes directly to disk; never prints raw text |
| Read `Secure_Output_Workspace.md` | ❌ **STRICTLY FORBIDDEN** | Violates zero-knowledge air-gap delivery |
| Direct inspection of `D-csR/` (`cat`, `view_file`, `head`) | ❌ **STRICTLY FORBIDDEN** | Direct data leak into context window |
| Printing raw text chunks to stdout | ❌ **STRICTLY FORBIDDEN** | Breaks zero-knowledge protocol |

---

## 5. Offline Indexing Command Reference (For User)

If the user needs to build or rebuild the underlying zero-knowledge index:
```bash
python src/core/rag/zk_advanced_indexer.py --source-dir D-csR --index-dir D-csR_Index --rebuild
```

---

## 6. Operational Checklist for AI Agents

When handling zero-knowledge retrieval requests:
1. [ ] **Do NOT touch raw files**: Avoid `view_file`, `cat`, `grep_search` on `D-csR` or `Secure_Output_Workspace.md`.
2. [ ] **Execute `zk_hybrid_router.py`**: Retrieve mathematical TAGs and confidence scores.
3. [ ] **Execute `zk_payload_compiler.py`**: Pass top-scoring TAGs to write the payload to disk.
4. [ ] **Conclude with Privacy Certification**:
   *"I have routed your request through the BM25 index and securely compiled the optimal payload into `Secure_Output_Workspace.md`. I have not viewed the contents."*
