# `<CS>/<DDW-X>` Offline Brain Database Archive

```text
  ██████╗ ██████╗  █████╗ ██╗███╗   ██╗███████╗
  ██╔══██╗██╔══██╗██╔══██╗██║████╗  ██║██╔════╝
  ██████╔╝██████╔╝███████║██║██╔██╗ ██║███████╗
  ██╔══██╗██╔══██╗██╔══██║██║██║╚██╗██║╚════██║
  ██████╔╝██║  ██║██║  ██║██║██║ ╚████║███████║
  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝
   ── 160MB+ Offline Intelligence Corpus ──
```

## ⚠️ MANDATORY EXTRACTION DIRECTIVE

> [!WARNING]
> **CRITICAL SETUP REQUIREMENT**:
> To bypass GitHub's 100MB file limit, the plaintext knowledge bases in this directory are distributed as compressed `.zip` archives.
> 
> **You MUST extract `cs_parsed_brains.zip` directly into this folder before utilizing ANY of the CS Division Master Skills (`Skills-CS/`).**

---

### ⚡ Why Extraction is Required

The `<CS>/<DDW-X>` Master Skills operate as **Active RAG Controllers**. Their embedded Python search engines rely on **zero-copy memory mapping (`mmap`)** to perform sub-millisecond regular expression searches across 160MB+ of uncompressed plaintext.

`mmap` requires raw, uncompressed `.txt` files on the local filesystem. Without unzipping, RAG queries will fail to locate the target knowledge bases.

---

### 🚀 Extraction Commands

#### PowerShell (Windows):
```powershell
Expand-Archive -Path "cs_parsed_brains\cs_parsed_brains.zip" -DestinationPath "cs_parsed_brains\" -Force
```

#### Bash (Linux / macOS):
```bash
unzip -o cs_parsed_brains/cs_parsed_brains.zip -d cs_parsed_brains/
```

#### Python CLI:
```python
import zipfile
with zipfile.ZipFile("cs_parsed_brains/cs_parsed_brains.zip", "r") as zip_ref:
    zip_ref.extractall("cs_parsed_brains/")
print("[+] Brain database unpacked successfully.")
```

---

### 📊 Database Manifest (Extracted Contents)

| Brain File | Uncompressed Size | Operational Domain |
|---|---|---|
| `art_brain.txt` | **108.4 MB** | 954 Atomic Red Team tests, CLI execution logs, EVTX Event IDs |
| `Anthropic-Cybersecurity-Skills_brain.txt` | **22.8 MB** | 817 Blue/Red Team skills, 291 MITRE techniques across 14 tactics |
| `Awesome-Redteam_brain.txt` | **24.5 MB** | Telemetry baselines, injection traces, command-line indicators |
| `PATT_brain.txt` | **9.2 MB** | PE/ELF/Mach-O headers, structural binary dissection, entropy |
| `ck_brain.txt` | **1.7 MB** | C/C++ assembly, calling conventions, stack frames, OLLVM CFG |
| `Lab-Notes_brain.txt` | **1.1 MB** | Forensics playbooks, host artifacts, kernel debugging logs |
| `awesome-clinerules_brain.txt` | **881 KB** | Multi-IDE system prompts, bash sandbox rules, secure linters |
| `AI-Red-Teaming-Guide_brain.txt` | **557 KB** | Prompt injection defenses, roleplay jailbreaks, delimiter filters |
| `ce_brain.txt` | **520 KB** | Historical CVE mechanics, vulnerability catalogs, remediation diffs |
| `GhidraMCP_brain.txt` | **163 KB** | FastMCP JSON-RPC schemas, `DecompInterface`, Ghidra socket bridge |
| `awesome-malware-analysis_brain.txt` | **140 KB** | Dynamic sandboxing, memory dump forensics, static unpacking |
| `PMAT-labs_brain.txt` | **78 KB** | 4-phase PMAT triage pipeline, Procmon automation, sample profiling |
| `cursor-security-rules_brain.txt` | **65 KB** | Multi-language `.cursorrules`, OWASP Top 10 guardrails |
| `Red-Teaming-Toolkit_brain.txt` | **53 KB** | Defense evasion baselines, network IDS signatures |
| `awesome-cyber-security-mcp_brain.txt`| **11.5 KB** | MCP server configurations, tool execution boundaries |
| `ed_brain.txt` | **104 B** | Endpoint detection primitives and telemetry signatures |
