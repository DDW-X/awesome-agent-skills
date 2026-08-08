# `<DDW-X>` Master Cybersecurity & Agentic AI Taxonomy Index

```text
  ████████╗ █████╗ ██╗  ██╗ ██████╗ ███╗   ██╗ ██████╗ ███╗   ███╗██╗   ██╗
  ╚══██╔══╝██╔══██╗╚██╗██╔╝██╔═══██╗████╗  ██║██╔═══██╗████╗ ████║╚██╗ ██╔╝
     ██║   ███████║ ╚███╔╝ ██║   ██║██╔██╗ ██║██║   ██║██╔████╔██║ ╚████╔╝ 
     ██║   ██╔══██║ ██╔██╗ ██║   ██║██║╚██╗██║██║   ██║██║╚██╔╝██║  ╚██╔╝  
     ██║   ██║  ██║██╔╝ ██╗╚██████╔╝██║ ╚████║╚██████╔╝██║ ╚═╝ ██║   ██║   
     ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝   ╚═╝   
       ── Master Search Index, Keyword Matrix & Technical Glossary ──
```

Welcome to the **Master Taxonomy & Keyword Index** for the `<DDW-X>` Agentic Knowledge Base. This directory organizes all core architectural domains, technical concepts, frameworks, and tools integrated into our 35 Agent Skills, RAG-controller databases, and FastMCP bridges.

---

## 1. Agentic AI & Model Context Protocol (MCP)

| Keyword Cluster | Primary Context | Applied `<DDW-X>` Component |
|---|---|---|
| **Model Context Protocol (MCP)** | JSON-RPC 2.0 Agentic standard | `FastMCP`, `bridge_mcp_ghidra.py`, MCP Tools |
| **FastMCP Server Framework** | Python 3.11+ async server runtime | `DDWX-Ghidra-MCP-Bridge`, `mcp.server.fastmcp` |
| **Progressive Disclosure** | 3-tier token optimization standard | Level 1 YAML, Level 2 Rules, Level 3 References |
| **Autonomous IDE Agents** | Cross-IDE developer copilot runtimes | Google Antigravity, Cursor AI, Claude Code, Copilot |
| **Context Window Conservation** | Token reduction & cache preservation | 98.5% savings via decoupled prompt architectures |
| **Agentic Tool Calling** | Dynamic schema invocation & dispatch | Structured JSON payloads, tool schemas, Pydantic |
| **System Prompt Constitutional** | Immutable behavioral anchors & rules | Role definition, safety guardrails, execution boundaries |
| **Self-Correcting State Graphs** | Cyclic agent graph workflows | LangGraph cyclic nodes, crewAI swarms, n8n orchestration |

---

## 2. Advanced Reverse Engineering & Binary Forensics

| Keyword Cluster | Primary Context | Applied `<DDW-X>` Component |
|---|---|---|
| **Ghidra Headless Analyzer** | Automated command-line decompilation | `analyzeHeadless`, `GhidraMCPBridge.py` |
| **DecompInterface API** | Ghidra C-AST decompiler interface | Pseudo-C reconstruction, function recovery |
| **Symbol Table & XRefs** | Memory symbol manipulation | `SymbolTable`, `getReferencesTo`, `rename_symbol` |
| **PE Header Structural Dissection** | `IMAGE_DOS_HEADER`, `IMAGE_NT_HEADERS` | PE32/PE64 parsing, `e_lfanew`, Optional Header |
| **ELF Header Analysis** | Executable & Linkable Format dissection | ELF32/ELF64 magic, program/section headers |
| **Shannon Entropy Calculation** | High-entropy packing detection | Per-section byte distribution, packer indicators |
| **OLLVM Control-Flow De-flattening** | Obfuscation state-machine recovery | Switch dispatcher reconstruction, state variable tracing |
| **FlatProgramAPI & Memory Reads** | Virtual address space inspection | Hex byte dumps, virtual memory reads, relocation fixups |
| **Opaque Predicates & Dead Code** | Anti-disassembly pattern removal | Unreachable code pruning, conditional branch folding |
| **Calling Conventions & Frames** | Low-level stack frame analysis | `__cdecl`, `__stdcall`, `__fastcall`, shadow space |

---

## 3. Defensive Malware Analysis & Sandbox Triage (PMAT)

| Keyword Cluster | Primary Context | Applied `<DDW-X>` Component |
|---|---|---|
| **PMAT 4-Phase Pipeline** | Practical malware analysis workflow | Basic Static, Basic Dynamic, Adv Static, Adv Dynamic |
| **Cryptographic Hashing** | File integrity & sample identification | MD5, SHA1, SHA256, ImpHash, SSDEEP, RichPE |
| **FLOSS String Extraction** | Deobfuscating encoded string buffers | ASCII, UTF-16LE, stack strings, XOR strings |
| **INetSim Service Simulation** | Air-gapped network traffic sinkhole | DNS mock, HTTP/HTTPS fakefiles, SMTP sinkhole |
| **FakeNet-NG Network Sinkhole** | Automated Windows network mocking | HTTP GET/POST response generation, SSL interception |
| **Process Monitor (Procmon) Logs** | Host filesystem & registry telemetry | PML logs, CSV export, filtered registry capture |
| **Air-Gapped VM Sandboxing** | Hypervisor containment & isolation | Host-Only adapters, read-only snapshot reversion |
| **YARA Signature Engineering** | Enterprise binary detection rules | Hex string matches, PE condition logic, regex |
| **Memory Dump Forensics** | Volatility 3 kernel artifact triage | Process injection detection, injected PE unmapping |
| **API Hooking & Hook Detection** | Runtime function interception triage | IAT hooking, inline detours, syscall monitoring |

---

## 4. IDE Security, SAST & Secure Code Auditing

| Keyword Cluster | Primary Context | Applied `<DDW-X>` Component |
|---|---|---|
| **Static App Security Testing (SAST)** | Abstract Syntax Tree vulnerability scan | Python native `ast.NodeVisitor`, Tree-Sitter |
| **`.cursorrules` Guardrails** | IDE prompt constraints for security | SQLi prevention, path normalization, safe child processes |
| **`.clinerules` System Directives** | Autonomous CLI safety rules | Safe command limits, sandbox boundary assertions |
| **OWASP Top 10 A01: Access Control** | Path traversal & authorization flaws | `path.normalize()`, root directory boundary assertions |
| **OWASP Top 10 A03: Injection** | SQL, command, and code injection | Parameterized queries, typed argument lists, `eval()` ban |
| **OWASP Top 10 A10: SSRF Defense** | Server-Side Request Forgery filtering | RFC 1918 private CIDR blocking, loopback prevention |
| **Secrets & Credential Hygiene** | Hardcoded API key elimination | Environment variables, `.env` gitignore, secrets scrubbing |
| **Safe Deserialization Paradigms** | Remote code execution via objects | `pickle` deprecation, `yaml.safe_load()`, JSON schemas |
| **Argon2id Password Hashing** | Cryptographic key derivation | Memory-hard hashing, bcrypt cost >= 12, salt generation |
| **Taint Tracking & Data Flow** | Untrusted input propagation check | Source-to-sink AST analysis, sanitization assertions |

---

## 5. Detection Engineering, Telemetry & Threat Hunting

| Keyword Cluster | Primary Context | Applied `<DDW-X>` Component |
|---|---|---|
| **Sigma Detection Format** | Generic YAML threat signature standard | Multi-target compiler, detection selections |
| **Splunk Search Processing (SPL)** | Enterprise SIEM search language | `index=windows`, Sysmon Event correlation |
| **Elasticsearch Query DSL** | Elastic Security JSON query schema | `must_clauses`, `match_phrase`, `terms.keyword` |
| **Windows Sysmon XML Filtering** | High-fidelity host telemetry collector | Event ID 1 (Create), Event ID 8 (Thread), Event ID 10 (Access) |
| **MITRE ATT&CK Enterprise Matrix** | Adversary tactic & technique framework | 14 Enterprise tactics, 291 technique coverage |
| **Process Injection (T1055)** | Telemetry detection for code injection | `CreateRemoteThread`, `NtMapViewOfSection`, APC queuing |
| **Credential Access (T1003)** | LSASS memory handle hunting | Process access masks (`0x1010`, `0x1038`), dump signatures |
| **Command Interpreters (T1059)** | Scripting engine execution tracking | `powershell.exe -enc`, `cmd.exe /c`, `wscript.exe` |
| **Zeek / Suricata IDS Rules** | Network protocol analysis & detection | Bro/Zeek scripts, Suricata HTTP/TLS inspection rules |
| **Windows Event Logs (EVTX)** | Security log auditing & correlation | Event 4688 (Process Creation), Event 4624 (Logon) |

---

## 6. AI Safety, Guardrails & LLM Red Teaming Defense

| Keyword Cluster | Primary Context | Applied `<DDW-X>` Component |
|---|---|---|
| **Prompt Injection Mitigation** | Direct & indirect override defense | Heuristic signature scanner, boundary delimiters |
| **Jailbreak Classification** | Persona override & DAN filter | Roleplay jailbreak detection, unconstrained prompt triage |
| **Delimiter Boundary Defense** | Structured input demarcation | XML isolation tags (`<user_query>`), escape rules |
| **NeMo Guardrails & Llama-Guard** | Programmable LLM dialogue rails | Canonical user intents, secondary safety classifiers |
| **System Prompt Hardening** | Immutable prompt constitutional logic | Core identity protection, leak prevention anchors |
| **Tool Execution Sandboxing** | Autonomous agent permission gating | Filesystem write limits, network egress confirmations |
| **Adversarial Benchmark Testing** | Automated model resilience auditing | Multi-turn red teaming suites, safety regression tests |

---

## 7. Local RAG Architecture & Zero-Copy Memory Mapping

| Keyword Cluster | Primary Context | Applied `<DDW-X>` Component |
|---|---|---|
| **Local RAG Controller Architecture** | Document retrieval without LLM bloat | Active `.md` query engines, `cs_parsed_brains/` |
| **Zero-Copy `mmap` Execution** | Kernel memory-mapped file search | Python `mmap.mmap()`, sub-millisecond query speed |
| **Atomic Red Team Knowledge Base** | 950+ unit tests for MITRE techniques | `art_brain.txt` (108MB uncompressed corpus) |
| **Offline Brain Database** | 160MB+ uncompressed security corpus | 16 plaintext domain brains, zero internet dependency |
| **Regex Chunk Slicing** | Context window chunk extraction | Sliding byte offsets, match-centered windowing |

---

## 8. Low-Level Systems & Concurrency Architecture

| Keyword Cluster | Primary Context | Applied `<DDW-X>` Component |
|---|---|---|
| **Lock-Free Concurrency** | Non-blocking multi-threaded structures | `std::atomic`, atomic compare-and-swap (CAS) |
| **Memory Order Semantics** | CPU instruction ordering constraints | `memory_order_relaxed`, `acquire`, `release` |
| **Cache-Line Alignment** | False-sharing prevention in CPU caches | `alignas(64)` L1 D-Cache alignment |
| **Zero-Allocation Programming** | Predictable real-time memory usage | Ring buffers, static arena allocators, pre-allocated pools |
| **Cross-Platform C/C++ Systems** | High-performance OS systems code | POSIX syscalls, Win32 APIs, compiler intrinsics |

---

## 9. Frontier Model Lineages & System Prompt Archaeology

| Model / Framework Lineage | Specialized Domain | Core Prompt Engineering Focus |
|---|---|---|
| **Anthropic Claude Fable 5** | Deep multi-step reasoning & tool calling | Rigorous verification, recursive self-correction |
| **Anthropic Claude Opus (4.6-5)** | Architectural refactoring & complex plans | High-effort system design, full-stack reasoning |
| **Anthropic Claude Code Engine** | Terminal agent orchestration & IDE subagents | Tool execution loops, bash safety, git integration |
| **OpenAI GPT-5 (5.0-5.6-sol)** | Next-gen reasoning effort & agent mode | Autonomous tool selection, persistent planning |
| **OpenAI o-Series (o3, o4-mini)** | High-compute chain-of-thought logic | Mathematical proofs, low-level binary reasoning |
| **OpenAI Codex Engine** | Code completion & execution synthesis | Python scripting, automated unit test generation |
| **Google Gemini 3 (Pro, Flash)** | Multimodal reasoning & AI Studio builds | Ultra-long context routing, code synthesis |
| **DeepSeek V3 & R1** | Open reasoning & code optimization | Chain-of-thought formatting, cost-efficient logic |
| **xAI Grok (3-4.5)** | Uncensored truthfulness & API workflows | Direct technical explanation, real-time synthesis |
| **Cursor AI & Cline Engine** | IDE-native agentic pair programming | Context rule indexing, multi-file atomic edits |
