# `<RT>/<DDW-X>` Zero-Knowledge Private RAG Database (`D-csR_Index`)

```text
  ███████╗██╗  ██╗    ██████╗  █████╗  ██████╗ 
  ╚══███╔╝██║ ██╔╝    ██╔══██╗██╔══██╗██╔════╝ 
    ███╔╝ █████╔╝     ██████╔╝███████║██║  ███╗
   ███╔╝  ██╔═██╗     ██╔══██╗██╔══██║██║   ██║
  ███████╗██║  ██╗    ██║  ██║██║  ██║╚██████╔╝
  ╚══════╝╚═╝  ╚═╝    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ 
   ── ~480MB Zero-Knowledge SQLite FTS5 Index ──
```

## 1. Directory Purpose & Architecture

This directory houses the **Zero-Knowledge BM25 FTS5 Database (`zk_private_rag.db`)** powering the `<RT>/<DDW-X>` Master Skills ecosystem.

Unlike conventional RAG databases that stream raw text into LLM context windows, this database decouples semantic search from payload retrieval:
- **Blind Semantic Indexing**: Documents are tokenized and assigned immutable, mathematical cryptographic UUID tags (e.g., `TAG-0x89F2`, `TAG-0xA1C4`, `TAG-XXXX-YY`).
- **Context Isolation**: When an AI agent performs a query, it interacts exclusively with `zk_semantic_router.py`, which returns only abstract TAG identifiers.
- **Air-Gapped Local Compilation**: The local script `zk_payload_compiler.py` resolves the TAGs directly from `zk_private_rag.db` to disk (`Secure_Output_Workspace.md`) without transmitting sensitive plain text to external AI inference endpoints.

---

## 2. ⚠️ Mandatory Decompression Requirement (RAR4 Format)

> [!WARNING]
> **CRITICAL SETUP DIRECTIVE**:
> Due to the substantial volume of the pre-indexed knowledge base (**~479,848 KB / ~480 MB uncompressed**), the database is archived using **WinRAR with the RAR4 compression format** (`zk_private_rag.rar`).
> 
> **You MUST extract `zk_private_rag.rar` directly inside this `D-csR_Index/` folder to restore `zk_private_rag.db` before running any `<RT>/<DDW-X>` Master Skills.**

---

## 3. 🚀 Decompression Instructions

Ensure the extracted database file `zk_private_rag.db` is located directly inside `D-csR_Index/`:

### CLI / Terminal (Linux / macOS / WSL / Git Bash):
```bash
# Navigate to repository root and extract directly into D-csR_Index/
unrar x D-csR_Index/zk_private_rag.rar D-csR_Index/
```

### Windows (PowerShell / WinRAR CLI):
```powershell
# Using unrar CLI:
& "C:\Program Files\WinRAR\UnRAR.exe" x D-csR_Index\zk_private_rag.rar D-csR_Index\
```

### Windows GUI (WinRAR / 7-Zip):
1. Right-click `zk_private_rag.rar` inside `D-csR_Index/`.
2. Select **Extract Here** (or **WinRAR -> Extract to current folder**).
3. Verify that `zk_private_rag.db` (~480 MB) is present in `D-csR_Index/`.

---

## 4. Alternative: Rebuild Index from Source

If you have extracted the raw `D-csR/` dataset and wish to regenerate a fresh index from scratch:

```bash
python src/core/rag/zk_advanced_indexer.py --source-dir D-csR --index-dir D-csR_Index --rebuild
```

---

## 5. Integration with `<RT>/<DDW-X>` Master Skills

Once `zk_private_rag.db` is extracted, the Master Skills interact with the database via two dedicated CLI tools:

```text
 ┌──────────────────────┐        Query String         ┌────────────────────────┐
 │ AI Agent Reasoning   │ ──────────────────────────► │ zk_semantic_router.py  │
 │ (Zero Raw Context)   │ ◄────────────────────────── │ (BM25 FTS5 Search)     │
 └──────────┬───────────┘        List of TAG UUIDs    └───────────┬────────────┘
            │                                                     │
            │ Execute Local Compilation                           │ Queries DB
            ▼                                                     ▼
 ┌──────────────────────┐     Reconstitutes Payloads  ┌────────────────────────┐
 │ zk_payload_compiler  │ ──────────────────────────► │ zk_private_rag.db      │
 │ (Local Air-Gap Proc) │ ──► Secure_Output_Workspace │ (D-csR_Index/ SQLite)  │
 └──────────────────────┘                             └────────────────────────┘
```

1. **Step 1: Router Search**
   ```bash
   python src/core/rag/zk_semantic_router.py --query "AST static vulnerability auditing"
   ```
2. **Step 2: Air-Gapped Payload Compilation**
   ```bash
   python src/core/rag/zk_payload_compiler.py --tags TAG-0x101,TAG-0x102 --output Secure_Output_Workspace.md
   ```
