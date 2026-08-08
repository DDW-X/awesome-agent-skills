---
name: "<CS>/<DDW-X> Detection Engineering & Threat Hunting"
description: "RAG-driven Master Skill and runtime controller for Sigma rule synthesis, MITRE ATT&CK telemetry mapping, Sysmon/Windows Event Log hunting, and automated SIEM detection pipelines querying cs_parsed_brains/ on-the-fly."
---

# `<CS>/<DDW-X> Detection Engineering & Threat Hunting`

**The RAG-Augmented Detection Engineering & Telemetry Controller**

---

> **CRITICAL:** You must unzip the database archive located in the `cs_parsed_brains/` directory before utilizing this skill. The embedded RAG search scripts require the raw text files to execute successfully.

## 1. The Autonomous RAG Directive

> [!IMPORTANT]
> **STRICT EXECUTION DIRECTIVE FOR IDE AGENTS**:
> Do NOT guess MITRE ATT&CK technique numbers, Sysmon Event IDs, or Sigma query mappings. You MUST search the local `cs_parsed_brains/` database (including the massive `art_brain.txt` and `Anthropic-Cybersecurity-Skills_brain.txt`) to locate exact telemetry schemas and attack-to-defense mappings before generating SIEM rules.

```
 ┌────────────────────────────────────────────────────────────────────────────────────────┐
 │                   RAG DETECTION ENGINEERING & HUNTING ARCHITECTURE                     │
 │                                                                                        │
 │  ┌───────────────────────────┐         mmap/regex           ┌───────────────────────┐  │
 │  │ IDE Agent Context         │ ───────────────────────────► │ cs_parsed_brains/     │  │
 │  │ (Detection & Hunting)     │ ◄─────────────────────────── │ art_brain.txt (108MB) │  │
 │  └─────────────┬─────────────┘         Retrieved Telemetry  └───────────────────────┘  │
 │                │                                                                       │
 │                ▼                                                                       │
 │  ┌───────────────────────────┐                              ┌───────────────────────┐  │
 │  │ Sigma Compiler Engine     │ ───────────────────────────► │ Splunk SPL & Elastic  │  │
 │  │ (MITRE ATT&CK Alignment)  │                              │ Production SIEM Rules │  │
 │  └───────────────────────────┘                              └───────────────────────┘  │
 └────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Knowledge Base Database Mapping

| Target Query Domain | Primary Brain Source | Size | Key Information Retrieved |
|---|---|---|---|
| **MITRE ATT&CK & Atomic Tests** | `cs_parsed_brains/art_brain.txt` | 108.4 MB | 954 Atomic Red Team tests, exact CLI execution logs, EVTX IDs |
| **ATT&CK Coverage & Blue Team** | `cs_parsed_brains/Anthropic-Cybersecurity-Skills_brain.txt` | 22.8 MB | 291 MITRE techniques mapped across 14 enterprise tactics |
| **Adversary Emulation Scripts** | `cs_parsed_brains/Awesome-Redteam_brain.txt` | 24.5 MB | Commandline indicators, PowerShell payloads, C2 beacon traces |

---

## 3. Embedded High-Speed MMap RAG Search Engine

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# [RAG CONTROLLER] MMap Search Utility for Detection Engineering
import mmap
import os
import re
import sys
from typing import List, Dict, Any

WORKSPACE_ROOT = r"c:\Users\sorena\Desktop\ddw-x clone\skillssssssssssssssssssssssss"
BRAIN_DIR = os.path.join(WORKSPACE_ROOT, "cs_parsed_brains")

def search_detection_knowledge(query_regex: str, target_brains: List[str] = None, max_results: int = 5) -> List[Dict[str, Any]]:
    """Searches the massive 108MB Atomic Red Team and MITRE ATT&CK coverage maps in milliseconds."""
    if target_brains is None:
        target_brains = ["art_brain.txt", "Anthropic-Cybersecurity-Skills_brain.txt", "Awesome-Redteam_brain.txt"]
        
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
    query = sys.argv[1] if len(sys.argv) > 1 else "T1055"
    print(f"[*] Executing RAG retrieval for MITRE technique / detection: {query}")
    hits = search_detection_knowledge(query)
    for i, hit in enumerate(hits, 1):
        print(f"\n=== [HIT {i}] Source: {hit['source_brain']} (Offset {hit['match_position']}) ===")
        print(hit["content_chunk"])
```

---

## 4. Production Sigma Rule Synthesis Engine (Python)

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# [SIGMA ENGINE]
import json
import yaml
from typing import Any, Dict

class SigmaCompiler:
    def __init__(self, sigma_yaml: str):
        self.rule = yaml.safe_load(sigma_yaml)
        
    def to_splunk(self) -> str:
        selection = self.rule.get("detection", {}).get("selection", {})
        clauses = []
        for k, v in selection.items():
            if isinstance(v, list):
                clauses.append("(" + " OR ".join([f'{k}="{item}"' for item in v]) + ")")
            else:
                clauses.append(f'{k}="{v}"')
        return "index=windows source=\"XmlWinEventLog:Microsoft-Windows-Sysmon/Operational\" " + " AND ".join(clauses)

if __name__ == "__main__":
    test_rule = """
title: CreateRemoteThread Detection
detection:
    selection:
        EventID: 8
        SourceImage|endswith:
            - '\\powershell.exe'
            - '\\cmd.exe'
    condition: selection
"""
    compiler = SigmaCompiler(test_rule)
    print("[+] Compiled Splunk SPL:", compiler.to_splunk())
```
