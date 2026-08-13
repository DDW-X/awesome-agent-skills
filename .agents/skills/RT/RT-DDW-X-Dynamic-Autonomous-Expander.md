---
name: "<RT>/<DDW-X> Dynamic Autonomous Expander"
description: "Autonomous OSINT & Dynamic RAG Expansion Engine for DDW-X. Activates when offline database coverage is insufficient, searching live intelligence sources and blindly injecting refined knowledge into zk_private_rag.db with zero context window pollution."
---

# `<RT>/<DDW-X>` Dynamic Autonomous Expander (Self-Expanding RAG Engine)

## 1. Domain Architecture & The Autonomous Expansion Loop

The **`<RT>/<DDW-X> Dynamic Autonomous Expander`** equips AI agents with the capability to autonomously detect knowledge gaps, discover relevant OSINT and documentation URLs, and blindly ingest them into the private SQLite FTS5 database (`D-csR_Index/zk_private_rag.db`) without dumping raw web data into the AI reasoning context.

```
┌────────────────────────────────────────────────────────────────────────┐
│               THE AUTONOMOUS DYNAMIC EXPANSION LOOP                    │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 1. INITIAL QUERY & GAP DETECTION                                       │
│    Agent runs: python src/core/rag/zk_hybrid_router.py "<QUERY>"       │
│    Condition: Confidence < 60.0% OR Zero Matching TAGs Returned        │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 2. OSINT URL DISCOVERY (Zero Raw Ingestion)                            │
│    Agent performs targeted web search to locate authoritative URL.      │
│    STRICT RULE: Do NOT read or summarize full HTML in context!         │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 3. STEALTH BLIND INJECTION                                             │
│    Agent runs: python src/core/rag/zk_stealth_injector.py --url "<URL>"│
│    Engine fetches, strips HTML, refines chunks, and mints TAGs.        │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 4. IMMEDIATE RAG RE-QUERY & AIR-GAPPED COMPILATION                     │
│    Agent re-runs: zk_hybrid_router.py --tags-only ──► Obtains TAGs     │
│    Agent runs: zk_payload_compiler.py TAG-1 TAG-2 ──► Workspace.md    │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 5. CIRCUIT-BREAKER ENFORCEMENT & DELIVERY                              │
│    Max 1 Expansion Retry per session.                                  │
│    Conclude with Zero-Knowledge verification or '++' Cognitive Bridge. │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Trigger Conditions

This skill automatically activates when:
1. **Low Retrieval Confidence**: `zk_hybrid_router.py` returns RRF fused confidence scores below `60.0%`.
2. **Zero Route Coverage**: `zk_hybrid_router.py` returns `Zero matching cryptographic routes discovered`.
3. **Explicit User Mandate**: The user explicitly directs the agent: *"Search the web and update your RAG database"*, *"Inject new threat intel for CVE-XXXX"*, or *"Expand your offline index"*.

---

## 3. Step-by-Step Autonomous Execution Protocol

### Step 1: Baseline Query & Knowledge Gap Assessment
Execute the hybrid router with user search terms:
```bash
python src/core/rag/zk_hybrid_router.py "TARGET_QUERY_KEYWORDS" --top-k 5
```
*If high-confidence TAGs (>70%) exist, proceed normally to compilation. If confidence is low or empty, activate the Expansion Loop.*

---

### Step 2: Targeted OSINT URL Discovery
Use search tools to locate authoritative technical references, vendor advisories, or documentation:
- **Search Query Formulation**: Formulate strict, targeted technical queries (e.g. `CVE-2026-XXXX advisory mitigation github`).
- **Context Protection Guardrail**: Obtain only the destination URL. **NEVER** ask search tools to return, dump, or summarize full page bodies into the conversation context.

---

### Step 3: Execute Blind Stealth Injection
Pass the discovered URL directly to the stealth injector:
```bash
python src/core/rag/zk_stealth_injector.py --url "https://target-advisory-url.com/spec" --source-tag "cve_2026_advisory"
```

The script will fetch, clean DOM tags, refine semantic chunks, atomically write to `zk_private_rag.db`, and synchronize `zk_topology_map.json`:
```text
[SUCCESS] Stealth Injection Completed Successfully!
 * Ingested Source ID       : a891f2c410be
 * New Chunks Minted        : 4
 * Minted Cryptographic TAGs : TAG-E1A4-0B, TAG-7C29-F3, TAG-9D08-2A
```

---

### Step 4: Immediate Re-Query & Payload Compilation
Immediately re-run the hybrid router to capture the newly indexed knowledge:
```bash
# Standard inspection
python src/core/rag/zk_hybrid_router.py "TARGET_QUERY_KEYWORDS" --top-k 5

# Direct pipeline tags
python src/core/rag/zk_hybrid_router.py "TARGET_QUERY_KEYWORDS" --tags-only
```

Pass the returned high-confidence TAGs to the payload compiler:
```bash
python src/core/rag/zk_payload_compiler.py TAG-E1A4-0B TAG-7C29-F3
```

---

## 4. Architectural Safety & Circuit-Breaker Rules

### 🛑 Circuit-Breaker 1: Infinite Loop Prevention (Max 1 Retry)
- The AI is permitted **strictly ONE (1) injection attempt** per user query.
- If the re-query after injection still fails to achieve confidence >= 60.0%, the AI must **NOT** search for more URLs.
- The AI must immediately halt and notify the user:
  > *"Autonomous expansion attempted 1 injection cycle. Retrieval confidence remains below operational threshold. Please provide specific manual source URLs or review `Secure_Output_Workspace.md`."*

### 🔒 Circuit-Breaker 2: Context Window Protection & Data Boundary
- The AI is **strictly forbidden** from reading, previewing, or summarizing web page contents prior to injection.
- The AI's role during web discovery is exclusively that of an **URL Router**: discover the target URL string and hand it off directly to `zk_stealth_injector.py`.
- Raw text parsing occurs strictly within the offline Python process.

---

## 5. Standard Delivery Output Formats

### For Standard Zero-Knowledge Mode:
> ### `[AUTONOMOUS RAG EXPANSION COMPLETE]`
> - **Source Injected:** `[URL or Domain Masked]`
> - **New Cryptographic TAGs:** `TAG-E1A4-0B, TAG-7C29-F3`
> - **RRF Re-Query Confidence:** `99.2%`
> 
> "I have autonomously expanded the offline database with the requested intelligence, re-routed your request through the BM25 index, and compiled the optimal payload into `Secure_Output_Workspace.md`. I have not viewed the contents."

### For `++` Cognitive Bridge Mode:
> ### `[COGNITIVE BRIDGE ACTIVE - AUTONOMOUS EXPANSION]`
> *(Ingests `Secure_Output_Workspace.md` after successful expansion and provides full architectural synthesis, code refactors, and mitigation steps).*

---

## 6. Operational Checklist for AI Agents

When executing autonomous expansion:
1. [ ] **Verify Knowledge Gap**: Confirm baseline query confidence is < 60% or returns zero tags.
2. [ ] **Check Circuit Breaker**: Verify no prior expansion cycle was executed in the current turn (Max 1 limit).
3. [ ] **Locate URL Only**: Extract targeted URL without dumping web text into reasoning context.
4. [ ] **Run Stealth Injector**: `python src/core/rag/zk_stealth_injector.py --url "<URL>"`.
5. [ ] **Execute Re-Query & Compilation**: Run `zk_hybrid_router.py --tags-only` -> `zk_payload_compiler.py`.
6. [ ] **Deliver Structured Conclusion**: Report injection telemetry and output confirmation.
