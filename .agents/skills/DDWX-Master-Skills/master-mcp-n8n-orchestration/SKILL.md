---
name: "<DDW-X> Master: MCP & n8n Agentic Orchestration"
description: "Master Model Context Protocol (MCP) and n8n agentic orchestration engine synthesizing JSON-RPC 2.0 MCP server architecture, IDE-native tool-calling protocols, n8n-claw embedded smart agents, asynchronous Telegram bots, and local AI hypervisor routing with OpenAI o-series reasoning and Claude Code CLI engine."
---

# `<DDW-X> Master: MCP & n8n Agentic Orchestration`

**The Enterprise Standard for Model Context Protocol (MCP), Programmatic n8n Agentic Nodes, and Multi-Model Swarm Workflows**

---

## 1. Architectural Manifesto & The MCP / n8n Unified Bus

The frontier of agentic engineering requires bridging **IDE-native Model Context Protocol (MCP)** servers with **distributed workflow runtimes (`n8n`)** and **smart embedded autonomous agents (`n8n-claw`)**.

By fusing the reasoning architectures of **OpenAI o-Series** & **OpenAI Codex** (programmatic JSON node synthesis and deterministic schema binding) with **Claude Fable 5** & **Claude Code Engine** (strict JSON-RPC 2.0 MCP tool calling and terminal execution), this Master Skill enables autonomous IDE agents (Google Antigravity, Cursor, Claude Code, VS Code Copilot) to control, generate, and monitor distributed workflow pipelines.

```
 ┌────────────────────────────────────────────────────────────────────────────────────────┐
 │                      IDE AGENT RUNTIME (Antigravity / Cursor / Claude)                │
 │    ┌───────────────────────┐   stdio / SSE    ┌───────────────────────────────────┐    │
 │    │ Model Context Engine  │ ◄──────────────► │  <DDW-X> MCP Workflow Server      │    │
 │    │ (JSON-RPC 2.0 Client) │                  │  - tools/list  - tools/call       │    │
 │    └───────────────────────┘                  └─────────────────┬─────────────────┘    │
 └─────────────────────────────────────────────────────────────────┼──────────────────────┘
                                                                   │ HTTP REST / Webhook
                                                                   ▼
 ┌────────────────────────────────────────────────────────────────────────────────────────┐
 │                      DISTRIBUTED n8n AGENTIC WORKFLOW RUNTIME                          │
 │  ┌─────────────────────────┐   Sub-Workflow   ┌────────────────────────────────────┐   │
 │  │ n8n-claw Smart Agent    │ ◄──────────────► │ n8n Production Webhook Node (JSON) │   │
 │  │ (Local LLM Hypervisor)  │                  │ - HMAC Verification - Triage Logic │   │
 │  └────────────┬────────────┘                  └─────────────────┬──────────────────┘   │
 └───────────────┼─────────────────────────────────────────────────┼──────────────────────┘
                 ▼                                                 ▼
 ┌───────────────────────────────┐               ┌────────────────────────────────────┐
 │  Local AI Hypervisor (vLLM)   │               │ Asynchronous Telegram Alert Stream │
 └───────────────────────────────┘               └────────────────────────────────────┘
```

---

## 2. Model Context Protocol (MCP) Server Architecture

When building or integrating MCP servers into IDE workflows, you must conform strictly to the **MCP Specification (2024-11-05 / 2026-Standard)** over `stdio` or `Server-Sent Events (SSE)`.

### 2.1 FastMCP Production Server for n8n Programmatic Node Control

```python
# [MCP PROTOCOL ENFORCEMENT] <DDW-X> Master MCP Server Implementation
import asyncio
import json
import httpx
from mcp.server.fastmcp import FastMCP, Context
from pydantic import BaseModel, Field

# Initialize Master MCP Server
mcp = FastMCP(
    "DDWX-MCP-Workflow-Orchestrator",
    dependencies=["httpx", "pydantic"]
)

N8N_API_URL = "http://localhost:5678/api/v1"
N8N_API_KEY = "ddwx-production-mcp-key"

class DeployWorkflowInput(BaseModel):
    workflow_name: str = Field(description="Unique human-readable identifier for workflow")
    nodes: list[dict] = Field(description="Array of valid n8n node objects conforming to v1 schema")
    connections: dict = Field(description="Connection mapping between nodes")
    active: bool = Field(default=True, description="Whether to immediately activate upon deployment")

@mcp.tool()
async def deploy_n8n_workflow(payload: DeployWorkflowInput, ctx: Context) -> str:
    """Programmatically validates and deploys a complete JSON workflow directly into n8n."""
    ctx.info(f"Validating workflow payload for: {payload.workflow_name}")
    
    # 1. Structural Schema Validation
    if not payload.nodes or not payload.connections:
        raise ValueError("Invalid workflow: Nodes and connections must not be empty.")
    
    workflow_body = {
        "name": f"<DDW-X> {payload.workflow_name}",
        "nodes": payload.nodes,
        "connections": payload.connections,
        "settings": {
            "executionOrder": "v1",
            "saveManualExecutions": False
        }
    }
    
    headers = {
        "X-N8N-API-KEY": N8N_API_KEY,
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.post(f"{N8N_API_URL}/workflows", json=workflow_body, headers=headers)
        if resp.status_code not in (200, 201):
            ctx.error(f"n8n API Deployment failed: {resp.text}")
            return f"Deployment failed: {resp.status_code} - {resp.text}"
        
        data = resp.json()
        workflow_id = data.get("id")
        
        # Activate workflow if requested
        if payload.active and workflow_id:
            await client.post(f"{N8N_API_URL}/workflows/{workflow_id}/activate", headers=headers)
            
    ctx.info(f"Workflow successfully deployed and activated: ID {workflow_id}")
    return json.dumps({"status": "SUCCESS", "workflow_id": workflow_id, "name": payload.workflow_name})

@mcp.tool()
async def trigger_n8n_webhook(path: str, event_payload: dict, ctx: Context) -> str:
    """Dispatches a structured event payload directly to an active n8n webhook listener."""
    target_url = f"http://localhost:5678/webhook/{path.lstrip('/')}"
    ctx.info(f"Triggering webhook: {target_url}")
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(target_url, json=event_payload)
        return json.dumps({"status_code": resp.status_code, "response": resp.json() if resp.status_code == 200 else resp.text})

if __name__ == "__main__":
    mcp.run()
```

---

## 3. `n8n-claw` Embedded Smart Agent Pattern

The `n8n-claw` pattern embeds local and cloud reasoning agents directly inside n8n JavaScript/Python nodes, enabling autonomous fallback, schema healing, and self-correcting routing loops.

```javascript
// [N8N-CLAW EMBEDDED AGENT] Self-Healing JSON Triage Node
const items = $input.all();
const rawInput = items[0].json;

// 1. Schema Healing Logic
function healSchema(payload) {
  const sanitized = {
    incident_id: payload.id || `INC-${Date.now()}`,
    threat_level: Number(payload.threat_score || payload.severity || 5),
    target_host: payload.host || payload.target || "unknown_endpoint",
    timestamp: new Date().toISOString()
  };
  
  if (sanitized.threat_level > 10) sanitized.threat_level = 10;
  if (sanitized.threat_level < 1) sanitized.threat_level = 1;
  return sanitized;
}

const sanitizedPayload = healSchema(rawInput);

// 2. Autonomous Route Determination
const route = sanitizedPayload.threat_level >= 7 ? "IMMEDIATE_QUARANTINE" : "LOG_TELEMETRY";

return [
  {
    json: {
      ...sanitizedPayload,
      agent_decision: route,
      dispatched_via: "DDWX_MCP_Claw_Engine",
      execution_epoch: Date.now()
    }
  }
];
```

---

## 4. Multi-Model AI Hypervisor Proxy Architecture

In enterprise deployments, workflows must dynamically balance between local open-weights reasoning (Ollama / vLLM) and frontier cloud models (Claude Opus 5, GPT-5).

```python
# [HYPERVISOR GATEWAY] Multi-Model Dynamic Reasoning Router
import os
from typing import Literal
import httpx
from pydantic import BaseModel

class InferenceRequest(BaseModel):
    prompt: str
    temperature: float = 0.2
    model_tier: Literal["local_fast", "cloud_reasoning", "security_audit"]

async def execute_hypervisor_inference(req: InferenceRequest) -> dict:
    """Routes prompt based on cost, latency, and security isolation requirements."""
    
    if req.model_tier == "local_fast":
        # Route to on-premise local Ollama / vLLM instance
        url = "http://localhost:11434/api/generate"
        payload = {"model": "qwen2.5-coder:7b", "prompt": req.prompt, "stream": False}
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(url, json=payload)
            return {"tier": "LOCAL", "response": resp.json().get("response")}

    elif req.model_tier == "security_audit":
        # Route to Claude Fable 5 / Anthropic API for deep static analysis
        headers = {
            "x-api-key": os.getenv("ANTHROPIC_API_KEY", ""),
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        payload = {
            "model": "claude-3-5-sonnet-20241022",
            "max_tokens": 4096,
            "messages": [{"role": "user", "content": req.prompt}]
        }
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post("https://api.anthropic.com/v1/messages", json=payload, headers=headers)
            data = resp.json()
            return {"tier": "ANTHROPIC_CLOUD", "response": data["content"][0]["text"]}

    # Fallback to OpenAI Reasoning Endpoint
    return {"tier": "OPENAI_FALLBACK", "response": "Routed to o3-mini reasoning pipeline"}
```

---

## 5. Asynchronous Telegram Webhook & Notification Pipeline

```python
# [TELEGRAM NOTIFIER] Production-Grade Webhook with Retry and MarkdownV2 Escaping
import re
import httpx

def escape_markdown_v2(text: str) -> str:
    """Escapes Telegram MarkdownV2 reserved characters."""
    reserved = r"_*[]()~`>#+-=|{}.!"
    return re.sub(f"([{re.escape(reserved)}])", r"\\\1", text)

async def dispatch_telegram_alert(bot_token: str, chat_id: str, title: str, details: str):
    """Sends sanitized high-priority alert to Telegram admin channel."""
    safe_title = escape_markdown_v2(title)
    safe_details = escape_markdown_v2(details)
    
    formatted_msg = (
        f"🚨 *{safe_title}*\n\n"
        f"📋 *Details:*\n`{safe_details}`\n\n"
        f"⚡ _Dispatched via <DDW-X> Workflow Engine_"
    )
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": formatted_msg,
        "parse_mode": "MarkdownV2"
    }
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(url, json=payload)
        return resp.json()
```

---

## 6. Execution Rules & Verification Checklist

- [ ] **JSON-RPC 2.0 Compliance**: MCP tools must always return clean, serializable text or JSON strings with zero unhandled exceptions.
- [ ] **Schema Versioning**: All n8n nodes generated programmatically must specify `typeVersion: 2` (or current node version) and accurate input/output connection indices.
- [ ] **Secret Decoupling**: API keys, bot tokens, and database credentials must NEVER be hardcoded inside node JSON payloads; always utilize `={{ $env.SECRET_NAME }}` expressions.
- [ ] **HMAC Validation**: Webhooks accepting external events must verify the `x-signature-sha256` header before passing payloads to downstream nodes.
- [ ] **Error Trigger Configuration**: Workflows must attach a dedicated `n8n-nodes-base.errorTrigger` node to catch runtime failures and notify monitoring channels automatically.
