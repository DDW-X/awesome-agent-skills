---
name: "<CS>/<DDW-X> IDE Security & Code Auditing Architect"
description: "RAG-driven Master Skill and runtime controller for Static Application Security Testing (SAST), AST-level vulnerability auditing, Cursor/Cline rule enforcement, and OWASP Top 10 remediation querying cs_parsed_brains/ on-the-fly."
---

# `<CS>/<DDW-X> IDE Security & Code Auditing Architect`

**The RAG-Augmented IDE Security & Secure Code Auditing Controller**

---

> **CRITICAL:** You must unzip the database archive located in the `cs_parsed_brains/` directory before utilizing this skill. The embedded RAG search scripts require the raw text files to execute successfully.

## 1. The Autonomous RAG Directive

> [!IMPORTANT]
> **STRICT EXECUTION DIRECTIVE FOR IDE AGENTS**:
> Do NOT guess AST node types, regex taint patterns, or secure coding directives. You MUST query the local `cs_parsed_brains/` database for existing `.cursorrules`, `.clinerules`, and SAST linters before establishing project security policies or refactoring source code.

```
 ┌────────────────────────────────────────────────────────────────────────────────────────┐
 │                      RAG IDE SECURITY & AST AUDIT ARCHITECTURE                         │
 │                                                                                        │
 │  ┌───────────────────────────┐         mmap/regex           ┌───────────────────────┐  │
 │  │ IDE Agent Context         │ ───────────────────────────► │ cs_parsed_brains/     │  │
 │  │ (SAST / PR Review Tasks)  │ ◄─────────────────────────── │ Database (160MB+)     │  │
 │  └─────────────┬─────────────┘         Retrieved Chunks     └───────────────────────┘  │
 │                │                                                                       │
 │                ▼                                                                       │
 │  ┌───────────────────────────┐                              ┌───────────────────────┐  │
 │  │ Python AST Linter         │ ───────────────────────────► │ OWASP Top 10          │  │
 │  │ (ast.NodeVisitor SAST)    │                              │ Remediated Diffs      │  │
 │  └───────────────────────────┘                              └───────────────────────┘  │
 └────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Knowledge Base Database Mapping

| Target Query Domain | Primary Brain Source | Size | Key Information Retrieved |
|---|---|---|---|
| **Cursor IDE Security Rules** | `cs_parsed_brains/cursor-security-rules_brain.txt` | 65 KB | Multi-language `.cursorrules` parameters, secrets defense |
| **Cline Security Directives** | `cs_parsed_brains/awesome-clinerules_brain.txt` | 881 KB | System instructions, safe bash execution, linters |
| **Secure Coding & Taint Rules** | `cs_parsed_brains/Anthropic-Cybersecurity-Skills_brain.txt` | 22.8 MB | OWASP Top 10 remediation, parameterized queries, SSRF filters |

---

## 3. Embedded High-Speed MMap RAG Search Engine

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# [RAG CONTROLLER] MMap Search Utility for IDE Security & Rules
import mmap
import os
import re
import sys
from typing import List, Dict, Any

WORKSPACE_ROOT = r"c:\Users\sorena\Desktop\ddw-x clone\skillssssssssssssssssssssssss"
BRAIN_DIR = os.path.join(WORKSPACE_ROOT, "cs_parsed_brains")

def search_security_rules(query_regex: str, target_brains: List[str] = None, max_results: int = 5) -> List[Dict[str, Any]]:
    """Searches .cursorrules, .clinerules, and secure coding guardrails."""
    if target_brains is None:
        target_brains = ["cursor-security-rules_brain.txt", "awesome-clinerules_brain.txt", "Anthropic-Cybersecurity-Skills_brain.txt"]
        
    compiled_query = re.compile(query_regex.encode("utf-8"), re.IGNORECASE)
    results = []
    
    for brain_filename in target_brains:
        brain_path = os.path.join(BRAIN_DIR, brain_filename)
        if not os.path.exists(brain_path):
            continue
            
        with open(brain_path, "rb") as f:
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                for match in compiled_query.finditer(mm):
                    start = max(0, match.start() - 300)
                    end = min(len(mm), match.end() + 700)
                    chunk = mm[start:end].decode("utf-8", errors="ignore")
                    
                    results.append({
                        "source_brain": brain_filename,
                        "match_position": match.start(),
                        "content_chunk": chunk
                    })
                    if len(results) >= max_results:
                        return results
    return results

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "cursorrules"
    print(f"[*] Executing RAG retrieval for security rules: {query}")
    hits = search_security_rules(query)
    for i, hit in enumerate(hits, 1):
        print(f"\n=== [HIT {i}] Source: {hit['source_brain']} (Offset {hit['match_position']}) ===")
        print(hit["content_chunk"])
```

---

## 4. Production AST Vulnerability Scanner (Python)

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# [AST SECURITY SCANNER]
import ast
import json
import os
import sys
from typing import Any, Dict, List

class ASTSecurityAuditor(ast.NodeVisitor):
    def __init__(self, filename: str = "snippet.py"):
        self.filename = filename
        self.findings: List[Dict[str, Any]] = []

    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Name) and node.func.id in ("eval", "exec"):
            self.findings.append({
                "severity": "CRITICAL", "category": "CODE_INJECTION",
                "file": self.filename, "line": node.lineno,
                "description": f"Dangerous '{node.func.id}()' invocation."
            })
        elif isinstance(node.func, ast.Attribute) and getattr(node.func.value, "id", None) == "subprocess":
            for kw in node.keywords:
                if kw.arg == "shell" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                    self.findings.append({
                        "severity": "HIGH", "category": "COMMAND_INJECTION",
                        "file": self.filename, "line": node.lineno,
                        "description": "Subprocess executed with 'shell=True'."
                    })
        self.generic_visit(node)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8", errors="ignore") as f:
            tree = ast.parse(f.read(), filename=sys.argv[1])
        auditor = ASTSecurityAuditor(sys.argv[1])
        auditor.visit(tree)
        print(json.dumps(auditor.findings, indent=2))
```
