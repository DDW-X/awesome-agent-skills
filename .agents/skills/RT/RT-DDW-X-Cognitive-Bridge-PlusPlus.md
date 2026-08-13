---
name: "<RT>/<DDW-X> ++"
description: "Cognitive Bridge & Synthesis Modifier for DDW-X. Activates when '++' is appended to tasks, granting permission to ingest Secure_Output_Workspace.md for high-level technical analysis, code synthesis, and problem solving while maintaining raw dataset isolation."
---

# `<RT>/<DDW-X> ++` Cognitive Bridge (Active Synthesis Modifier)

## 1. Domain Architecture & The `++` Cognitive Paradigm

The `<RT>/<DDW-X> ++` skill acts as an **Active Cognitive Bridge & State Modifier**. 

By default, base `<RT>/<DDW-X>` skills operate as **Blind Orchestrators**: they formulate semantic queries, route mathematical TAGs via BM25, and dump extracted context directly into `Secure_Output_Workspace.md` on disk without reading or analyzing the text in the AI context.

When the user appends the **`++` Modifier** to their request (e.g., *"Use Threat Hunting ++"*, *"Analyze reversing artifacts ++"*, *"Audit code with SAST ++"*), this skill overrides the blind execution limitation. It grants explicit authorization to ingest the compiled workspace file into the AI's active reasoning context, enabling high-performance technical synthesis, custom remediation, and problem solving.

```
┌────────────────────────────────────────────────────────────────────────┐
│             User Request with '++' Modifier Received                   │
│             (e.g., "Analyze reversing artifacts ++")                   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ PHASE 1: THE OVERRIDE PROTOCOL (Base ZK Execution)                     │
│ 1. Formulate dense technical search keywords.                          │
│ 2. Run: python src/core/rag/zk_hybrid_router.py "<QUERY>" --tags-only  │
│ 3. Run: python src/core/rag/zk_payload_compiler.py TAG-1 TAG-2         │
│ 4. Verified output generated in Secure_Output_Workspace.md.            │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ PHASE 2: THE INGESTION PROTOCOL (Isolated Workspace Read)              │
│ - Ingest ONLY Secure_Output_Workspace.md into context window.          │
│ - STRICT DIRECTIVE: Never touch raw files in D-csR directly.           │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ PHASE 3: COGNITIVE SYNTHESIS & ARCHITECTURAL RESOLUTION                │
│ - Unleash elite DevSecOps & Security Engineering reasoning.            │
│ - Deeply evaluate extracted payload blocks, ASTs, and TTPs.            │
│ - Rewrite insecure code, correlate forensics, and solve user problem.  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ MANDATORY CONCLUSION PROTOCOL                                          │
│ "I have engaged the '++' Cognitive Bridge, ingested the secure         │
│  workspace payload, and synthesized the following elite analysis..."   │
│└───────────────────────────────────┬────────────────────────────────────┘
```

---

## 2. Activation Triggers

This skill automatically activates when:
- The user appends `++` to any command, skill name, or prompt (e.g., `Threat Hunting ++`, `Reverse Engineering ++`, `SAST ++`, `Blind Orchestrator ++`).
- The user explicitly requests: *"Ingest the compiled workspace"*, *"Synthesize the output from the RAG engine"*, or *"Bridge the zero-knowledge payload into context"*.

---

## 3. Strict 3-Phase Execution Protocol

### Phase 1: The Override Protocol (Base Zero-Knowledge Execution)
The AI must first allow the base Zero-Knowledge infrastructure to complete its targeted retrieval:
1. **Multi-Query RRF Hybrid Routing**:
   ```bash
   # Standard telemetry inspection
   python src/core/rag/zk_hybrid_router.py "EXPLICIT_TECHNICAL_KEYWORDS" --top-k 5

   # Direct pipeline tags for compilation chaining
   python src/core/rag/zk_hybrid_router.py "EXPLICIT_TECHNICAL_KEYWORDS" --tags-only
   ```
2. **Compile Payload to Disk**:
   ```bash
   python src/core/rag/zk_payload_compiler.py TAG-XXXX-YY TAG-AAAA-BB
   ```
3. **Verify File Creation**: Ensure `Secure_Output_Workspace.md` exists and was written successfully.

---

### Phase 2: The Ingestion Protocol (Workspace Ingestion)
Once `Secure_Output_Workspace.md` is compiled, the AI is granted permission to ingest **ONLY** this single output file:
- **Authorized Action**: Read `Secure_Output_Workspace.md` via file viewing tools or CLI (`python -c "print(open('Secure_Output_Workspace.md').read())"`).
- **Absolute Boundary Rule**: Direct reading of raw files inside `D-csR` remains **STRICTLY PROHIBITED**. All data ingestion must pass through the SQLite BM25 compilation filter first.

---

### Phase 3: Cognitive Synthesis & Deep Problem Solving
With the compiled payload now loaded in context, the AI acts as a **Principal DevSecOps & Security Architect**:
1. **Technical Dissection**: Correlate technical indicators, decompiled ASTs, header structures, and telemetry rules extracted from the payload blocks.
2. **Direct Code Remediation & Architecture**: Rewrite vulnerable code segments, construct end-to-end automation scripts, generate YARA/Sigma signatures, or configure CI/CD guardrail policies.
3. **Strategic TTP Synthesis**: Formulate actionable defensive mitigation strategies tailored to the user's specific problem.

---

## 4. Boundary & Confidentiality Matrix

| Resource | Access Permission | Method |
|---|---|---|
| **Raw Corpus Directory (`D-csR/`)** | ❌ **STRICTLY FORBIDDEN** | Direct reading, `cat`, `view_file` prohibited |
| **ZK SQLite Database (`zk_private_rag.db`)** | 🔒 **TOOL-MEDIATED ONLY** | Accessed via `zk_hybrid_router.py` & `zk_payload_compiler.py` |
| **Compiled Workspace (`Secure_Output_Workspace.md`)** | ✅ **AUTHORIZED WITH `++`** | Read into context for analysis and synthesis |
| **AI Context Window** | 🧠 **ACTIVE REASONING** | Receives ONLY targeted, compiled workspace payload |

---

## 5. Mandatory Response Format

Whenever `<RT>/<DDW-X> ++` is invoked, the AI MUST preface its technical response with the standard Cognitive Bridge opening:

> ### `[COGNITIVE BRIDGE ACTIVE]`
> **I have engaged the `++` Cognitive Bridge, ingested the secure workspace payload, and synthesized the following elite analysis:**
>
> *(Followed by comprehensive, production-grade technical breakdowns, code refactors, forensic analysis, and step-by-step remediation plans).*

---

## 6. Operational Checklist for AI Agents

When executing a `++` modified task:
1. [ ] **Verify `++` Intent**: Confirm user prompt explicitly invoked the `++` modifier.
2. [ ] **Execute Base ZK Retrieval**: Run `zk_hybrid_router.py --tags-only` -> `zk_payload_compiler.py`.
3. [ ] **Safely Ingest Workspace**: Load `Secure_Output_Workspace.md` into context. Never touch `D-csR/`.
4. [ ] **Deliver Elite Synthesis**: Apply full architectural intelligence to solve the user's problem.
5. [ ] **Format Header**: Include the mandatory `[COGNITIVE BRIDGE ACTIVE]` preamble.
