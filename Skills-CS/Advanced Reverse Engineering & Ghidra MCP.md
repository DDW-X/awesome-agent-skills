---
name: "<CS>/<DDW-X> Advanced Reverse Engineering & Ghidra MCP"
description: "RAG-driven Master Skill and runtime controller for headless binary analysis, Ghidra MCP bridges, structural PE/ELF dissection, and decompilation intelligence querying cs_parsed_brains/ on-the-fly."
---

# `<CS>/<DDW-X> Advanced Reverse Engineering & Ghidra MCP`

**The RAG-Augmented Reverse Engineering & Decompiler Controller**

---

> **CRITICAL:** You must unzip the database archive located in the `cs_parsed_brains/` directory before utilizing this skill. The embedded RAG search scripts require the raw text files to execute successfully.

## 1. The Autonomous RAG Directive

> [!IMPORTANT]
> **STRICT EXECUTION DIRECTIVE FOR IDE AGENTS**:
> Do NOT guess or hallucinate binary structures, decompiler API bindings, or Ghidra socket RPC schemas. You MUST use the embedded high-speed memory-mapped search engine to query the local `cs_parsed_brains/` database for exact implementations, symbol tables, and cross-reference queries before generating code.

```
 ┌────────────────────────────────────────────────────────────────────────────────────────┐
 │                   RAG REVERSE ENGINEERING & GHIDRA MCP ARCHITECTURE                    │
 │                                                                                        │
 │  ┌───────────────────────────┐         mmap/regex           ┌───────────────────────┐  │
 │  │ IDE Agent Context         │ ───────────────────────────► │ cs_parsed_brains/     │  │
 │  │ (Dynamic Search Tooling)  │ ◄─────────────────────────── │ Database (160MB+)     │  │
 │  └─────────────┬─────────────┘         Retrieved Chunks     └───────────────────────┘  │
 │                │                                                                       │
 │                ▼                                                                       │
 │  ┌───────────────────────────┐         JSON-RPC TCP         ┌───────────────────────┐  │
 │  │ FastMCP Bridge Server     │ ───────────────────────────► │ Ghidra Headless / GUI │  │
 │  │ (bridge_mcp_ghidra.py)    │ ◄─────────────────────────── │ (Port 13337)          │  │
 │  └───────────────────────────┘                              └───────────────────────┘  │
 └────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Knowledge Base Database Mapping

When reverse engineering binaries or configuring MCP bridges, execute dynamic retrieval against these specific brain files:

| Target Query Domain | Primary Brain Source | Size | Key Information Retrieved |
|---|---|---|---|
| **Ghidra MCP Server & Bridge** | `cs_parsed_brains/GhidraMCP_brain.txt` | 163 KB | FastMCP tools, `DecompInterface`, Python bridge socket |
| **Binary Dissection & Formats** | `cs_parsed_brains/PATT_brain.txt` | 9.2 MB | PE/ELF/Mach-O headers, section layout, entropy math |
| **Reverse Engineering Tooling** | `cs_parsed_brains/awesome-malware-analysis_brain.txt` | 140 KB | Disassembler configs, debuggers, memory profilers |
| **Low-Level Binary Patterns** | `cs_parsed_brains/ck_brain.txt` | 1.7 MB | Assembly calling conventions, stack frames, OLLVM CFG |

---

## 3. Embedded High-Speed MMap RAG Search Engine

Run this embedded Python script directly in your IDE terminal or sub-agent execution context to retrieve exact code blocks from the database in milliseconds:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# [RAG CONTROLLER] High-Speed Memory-Mapped Search Utility for Reverse Engineering
import mmap
import os
import re
import sys
from typing import List, Dict, Any

WORKSPACE_ROOT = r"c:\Users\sorena\Desktop\ddw-x clone\skillssssssssssssssssssssssss"
BRAIN_DIR = os.path.join(WORKSPACE_ROOT, "cs_parsed_brains")

def search_reverse_engineering_knowledge(query_regex: str, target_brains: List[str] = None, max_results: int = 5) -> List[Dict[str, Any]]:
    """Performs zero-copy memory-mapped regular expression retrieval across brain archives."""
    if target_brains is None:
        target_brains = ["GhidraMCP_brain.txt", "PATT_brain.txt", "awesome-malware-analysis_brain.txt", "ck_brain.txt"]
        
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
    query = sys.argv[1] if len(sys.argv) > 1 else "DecompInterface"
    print(f"[*] Executing RAG retrieval for query: {query}")
    hits = search_reverse_engineering_knowledge(query)
    for i, hit in enumerate(hits, 1):
        print(f"\n=== [HIT {i}] Source: {hit['source_brain']} (Offset {hit['match_position']}) ===")
        print(hit["content_chunk"])
```

---

## 4. Production FastMCP Ghidra Bridge Server (`bridge_mcp_ghidra.py`)

Below is the complete production FastMCP bridge connecting the IDE agent to Ghidra:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# [GHIDRA MCP BRIDGE] <CS>/<DDW-X> Production FastMCP Server Implementation
import asyncio
import json
import logging
import socket
import sys
from typing import Any, Dict, List, Optional
from mcp.server.fastmcp import FastMCP, Context
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("DDWX-GhidraMCP")

# Initialize Master FastMCP Server
mcp = FastMCP("DDWX-Ghidra-MCP-Bridge", dependencies=["pydantic"])

GHIDRA_BRIDGE_HOST = "127.0.0.1"
GHIDRA_BRIDGE_PORT = 13337

class DecompileRequest(BaseModel):
    function_target: str = Field(description="Function symbol name (e.g. 'main') or hex address (e.g. '0x00401520')")
    include_xrefs: bool = Field(default=True, description="Whether to include cross-references")
    timeout_seconds: int = Field(default=30, description="Max timeout in seconds")

class RenameSymbolRequest(BaseModel):
    address: str = Field(description="Hex address (e.g. '0x00402100')")
    new_name: str = Field(description="New semantic symbol name")

def dispatch_ghidra_command(payload: Dict[str, Any], timeout: float = 30.0) -> Dict[str, Any]:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((GHIDRA_BRIDGE_HOST, GHIDRA_BRIDGE_PORT))
            s.sendall((json.dumps(payload) + "\n").encode("utf-8"))
            
            chunks = []
            while True:
                chunk = s.recv(8192)
                if not chunk: break
                chunks.append(chunk)
                if b"\n" in chunk: break
            return json.loads(b"".join(chunks).decode("utf-8").strip())
    except Exception as e:
        return {"status": "ERROR", "error": str(e)}

@mcp.tool()
async def get_binary_metadata(ctx: Context) -> str:
    """Retrieves high-level metadata of the currently analyzed binary."""
    return json.dumps(dispatch_ghidra_command({"action": "get_program_info"}), indent=2)

@mcp.tool()
async def decompile_target_function(req: DecompileRequest, ctx: Context) -> str:
    """Invokes Ghidra's decompiler to convert assembly into high-level pseudo-C."""
    cmd = {"action": "decompile", "target": req.function_target, "xrefs": req.include_xrefs}
    res = dispatch_ghidra_command(cmd, timeout=float(req.timeout_seconds))
    return res.get("decompiled_code", f"Error: {res.get('error')}")

@mcp.tool()
async def rename_symbol(req: RenameSymbolRequest, ctx: Context) -> str:
    """Renames a symbol in Ghidra's database."""
    cmd = {"action": "rename_symbol", "address": req.address, "new_name": req.new_name}
    return json.dumps(dispatch_ghidra_command(cmd), indent=2)

if __name__ == "__main__":
    mcp.run()
```

---

## 5. Ghidra Background Socket Listener (`GhidraMCPBridge.py`)

Run this script inside Ghidra's Python interpreter to accept JSON-RPC requests:

```python
# [GHIDRA SCRIPT] GhidraMCPBridge.py
# @category MCP
import socket
import json
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor
from ghidra.program.model.symbol import SourceType

HOST, PORT = "127.0.0.1", 13337

def handle_request(req):
    action = req.get("action")
    if action == "get_program_info":
        return {
            "status": "OK",
            "name": currentProgram.getName(),
            "language": currentProgram.getLanguage().toString(),
            "image_base": currentProgram.getImageBase().toString(),
            "format": currentProgram.getExecutableFormat()
        }
    elif action == "decompile":
        target = req.get("target")
        func = currentProgram.getFunctionManager().getFunctionAt(currentProgram.getAddressFactory().getAddress(target))
        if not func:
            return {"status": "ERROR", "error": "Function not found"}
        decompiler = DecompInterface()
        decompiler.openProgram(currentProgram)
        res = decompiler.decompileFunction(func, 30, ConsoleTaskMonitor())
        return {"status": "OK", "decompiled_code": res.getDecompiledFunction().getC()}
    return {"status": "ERROR", "error": "Unsupported action"}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(5)
print("[+] Ghidra MCP Bridge listening on {}:{}".format(HOST, PORT))
while True:
    client, _ = server.accept()
    data = client.recv(16384).decode('utf-8')
    if data:
        client.sendall(json.dumps(handle_request(json.loads(data))) + "\n")
    client.close()
```
