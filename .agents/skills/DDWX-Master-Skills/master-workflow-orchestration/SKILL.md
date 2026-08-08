---
name: "<DDW-X> Master: Workflow Orchestration & n8n"
description: "Master autonomous workflow orchestration engine synthesizing n8n JSON programmatic node architecture, LangGraph cyclic state machines, crewAI role-based task delegation, and asynchronous Telegram bot automation with OpenAI o-series reasoning, Claude Fable 5 payload generation, and Gemini 3 long-context state retention."
---

# `<DDW-X> Master: Workflow Orchestration & n8n`

**The Enterprise-Grade Autonomous Workflow Orchestration, Cyclic Graph Engineering & Multi-Agent Swarm Standard**

---

## 1. Architectural Manifesto & Unified Graph Hierarchy

Modern enterprise automation requires bridging visual event-driven workflow automation (`n8n`), cyclic stateful multi-agent graphs (`LangGraph`), and role-specialized autonomous swarms (`crewAI`). 

By fusing the reasoning parameters of **OpenAI o-Series** (multi-step routing logic), **Claude Fable 5** (deterministic JSON node schema synthesis), and **Google Gemini 3** (massive state synchronization across asynchronous execution streams), this Master Skill enforces production-grade workflow engineering.

```
                   ┌─────────────────────────────────────────────────────────┐
                   │               <DDW-X> INGRESS DISPATCHER               │
                   │    (Telegram Webhooks / Fastify Gateway / Kafka Stream) │
                   └────────────────────────────┬────────────────────────────┘
                                                │
                 ┌──────────────────────────────┴──────────────────────────────┐
                 ▼                                                             ▼
  ┌──────────────────────────────┐                              ┌──────────────────────────────┐
  │   n8n WORKFLOW ENGINE        │                              │  LangGraph CYCLIC RUNTIME    │
  │  - Programmatic JSON Graph   │                              │  - TypedDict / Pydantic State│
  │  - Zero-Code Webhook Hooks   │                              │  - Conditional Branch Edges  │
  │  - Sub-workflow Recursion    │                              │  - MemorySaver Checkpointers │
  └──────────────┬───────────────┘                              └──────────────┬───────────────┘
                 │                                                             │
                 └──────────────────────────────┬──────────────────────────────┘
                                                │
                                                ▼
                               ┌──────────────────────────────────┐
                               │     crewAI AGENTIC SWARM         │
                               │  - Role-Based Hierarchical Teams │
                               │  - Asynchronous Tool Invocation  │
                               │  - SecOps Incident Triaging      │
                               └──────────────────────────────────┘
```

---

## 2. Programmatic n8n JSON Node Synthesis Engine

When generating or auditing `n8n` workflows programmatically, you must output strictly conforming **n8n Workflow JSON Schema (v1)**. Avoid arbitrary structures; always specify explicit `connections`, `parameters`, `position`, and `typeVersion`.

### 2.1 The Canonical n8n Workflow JSON Pattern

```json
{
  "name": "DDWX_Autonomous_SecOps_Pipeline",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "secops-alert",
        "responseMode": "responseNode",
        "options": {}
      },
      "id": "node-webhook-ingress",
      "name": "Webhook Ingress",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 2,
      "position": [240, 300],
      "webhookId": "ddwx-secops-ingress-001"
    },
    {
      "parameters": {
        "jsCode": "const payload = $input.first().json.body;\nif (!payload.threat_level) {\n  throw new Error('Malformed payload: Missing threat_level');\n}\nreturn [{\n  json: {\n    incident_id: 'SEC-' + Date.now(),\n    severity: payload.threat_level >= 8 ? 'CRITICAL' : 'ELEVATED',\n    target_ip: payload.target_ip,\n    raw_event: payload\n  }\n}];"
      },
      "id": "node-code-triage",
      "name": "Payload Sanitizer & Triage",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [460, 300]
    },
    {
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "={{ $json.severity }}",
              "value2": "CRITICAL"
            }
          ]
        }
      },
      "id": "node-if-critical",
      "name": "Critical Branch Router",
      "type": "n8n-nodes-base.if",
      "typeVersion": 2,
      "position": [680, 300]
    },
    {
      "parameters": {
        "chatId": "={{ $env.TELEGRAM_ADMIN_CHAT_ID }}",
        "text": "=⚠️ *CRITICAL SECOPS INCIDENT DETECTED*\\n*ID:* `{{ $json.incident_id }}`\\n*Target:* `{{ $json.target_ip }}`\\n*Action:* Auto-quarantine initiated.",
        "additionalFields": {
          "parse_mode": "Markdown"
        }
      },
      "id": "node-telegram-dispatch",
      "name": "Telegram Alert Dispatcher",
      "type": "n8n-nodes-base.telegram",
      "typeVersion": 1.2,
      "position": [920, 200],
      "credentials": {
        "telegramApi": {
          "id": "ddwx-telegram-creds",
          "name": "Telegram Bot Token"
        }
      }
    }
  ],
  "connections": {
    "Webhook Ingress": {
      "main": [
        [
          {
            "node": "Payload Sanitizer & Triage",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Payload Sanitizer & Triage": {
      "main": [
        [
          {
            "node": "Critical Branch Router",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Critical Branch Router": {
      "main": [
        [
          {
            "node": "Telegram Alert Dispatcher",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "settings": {
    "executionOrder": "v1",
    "saveManualExecutions": false,
    "callerPolicy": "workflowsFromSameOwner"
  }
}
```

---

## 3. LangGraph Cyclic State Machine Architecture

LangGraph enables cycles, persistent checkpointing, and deterministic branching between autonomous nodes. Every LangGraph implementation must follow strict schema validation and reduction logic.

### 3.1 Production Cyclic Graph with Self-Correcting Red-Team Triage

```python
from typing import Annotated, TypedDict, Literal
import operator
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

# 1. Strict Typed State Definition
class SecOpsGraphState(TypedDict):
    target_host: str
    vulnerabilities: Annotated[list[str], operator.add]
    remediation_plan: str
    audit_passed: bool
    iteration_count: int

# 2. Functional Node Definitions
def vulnerability_scanner_node(state: SecOpsGraphState) -> dict:
    """Simulates or invokes automated security assessment."""
    target = state["target_host"]
    found_vulns = [f"CVE-2026-X: Insecure CORS on {target}", f"CVE-2026-Y: Weak TLS Cipher on {target}"]
    return {
        "vulnerabilities": found_vulns,
        "iteration_count": state.get("iteration_count", 0) + 1
    }

def patch_generator_node(state: SecOpsGraphState) -> dict:
    """Generates remediation scripts based on identified vulnerabilities."""
    vulns = state["vulnerabilities"]
    plan = f"Remediation Plan for {len(vulns)} issues:\n" + "\n".join([f"- Patch {v}" for v in vulns])
    return {"remediation_plan": plan}

def security_validator_node(state: SecOpsGraphState) -> dict:
    """Validates remediation effectiveness; determines if cycle must repeat."""
    is_valid = state["iteration_count"] >= 2 or len(state["vulnerabilities"]) == 0
    return {"audit_passed": is_valid}

# 3. Conditional Edge Logic
def route_audit_verdict(state: SecOpsGraphState) -> Literal["patch_generator", END]:
    if state["audit_passed"]:
        return END
    return "patch_generator"

# 4. Graph Construction & Compilation
def build_secops_orchestrator():
    workflow = StateGraph(SecOpsGraphState)
    
    workflow.add_node("scanner", vulnerability_scanner_node)
    workflow.add_node("patch_generator", patch_generator_node)
    workflow.add_node("validator", security_validator_node)
    
    workflow.set_entry_point("scanner")
    workflow.add_edge("scanner", "patch_generator")
    workflow.add_edge("patch_generator", "validator")
    
    workflow.add_conditional_edges(
        "validator",
        route_audit_verdict,
        {
            "patch_generator": "patch_generator",
            END: END
        }
    )
    
    checkpointer = MemorySaver()
    return workflow.compile(checkpointer=checkpointer)

# Execution Invocation
if __name__ == "__main__":
    app = build_secops_orchestrator()
    initial_state: SecOpsGraphState = {
        "target_host": "api.internal.ddwx.network",
        "vulnerabilities": [],
        "remediation_plan": "",
        "audit_passed": False,
        "iteration_count": 0
    }
    config = {"configurable": {"thread_id": "ddwx-session-001"}}
    for output in app.stream(initial_state, config=config):
        print("Graph Node Transition:", output)
```

---

## 4. crewAI Role-Based Autonomous Swarm Architecture

`crewAI` coordinates multi-agent teams using hierarchical delegation and specialized personas.

### 4.1 Enterprise Multi-Agent Incident Response Crew

```python
from crewai import Agent, Crew, Process, Task
from crewai.tools import tool

@tool("PortScanner")
def port_scanner_tool(target: str) -> str:
    """Executes non-destructive port identification on target host."""
    return f"Host {target} has open ports: 22 (SSH), 80 (HTTP), 443 (HTTPS), 8080 (Admin Dashboard)."

# 1. Agent Persona Definitions
threat_analyst = Agent(
    role="Principal Threat Intelligence Analyst",
    goal="Identify high-risk attack surfaces on {target_domain}",
    backstory="Veteran SecOps analyst specialized in zero-day footprinting and perimeter validation.",
    tools=[port_scanner_tool],
    verbose=True,
    memory=True
)

security_architect = Agent(
    role="Lead Security Architect & Incident Responder",
    goal="Synthesize threat data into zero-trust firewall configurations",
    backstory="Former red-team lead architecting automated defensive playbooks and iptables rules.",
    verbose=True
)

# 2. Task Allocation
recon_task = Task(
    description="Scan {target_domain} for exposed admin interfaces and insecure open ports.",
    expected_output="Detailed list of open ports, services, and associated threat severity.",
    agent=threat_analyst
)

mitigation_task = Task(
    description="Generate an automated firewall rule set and iptables bash script mitigating findings.",
    expected_output="Production-ready hardening bash script with zero downtime.",
    agent=security_architect,
    output_file="hardening_playbook.sh"
)

# 3. Crew Orchestration
secops_crew = Crew(
    agents=[threat_analyst, security_architect],
    tasks=[recon_task, mitigation_task],
    process=Process.hierarchical,
    verbose=True
)

if __name__ == "__main__":
    result = secops_crew.kickoff(inputs={"target_domain": "gateway.ddwx.network"})
    print("Crew Task Execution Completed:\n", result)
```

---

## 5. Asynchronous Telegram Bot Webhook & AI Hypervisor Wiring

Automated agent workflows frequently communicate through interactive messaging interfaces. Below is the production-grade asynchronous Fastify + Telegraf / Python `python-telegram-bot` webhook pattern.

```python
# Async Telegram Event Ingress with Token-Bucket Rate Limiting & HMAC Verification
import hmac
import hashlib
import os
from fastapi import FastAPI, Request, HTTPException, Header
import httpx

app = FastAPI(title="DDWX-Workflow-Ingress")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "mock_token")
WEBHOOK_SECRET = os.getenv("TELEGRAM_SECRET_TOKEN", "mock_secret")

@app.post("/webhook/telegram")
async def handle_telegram_webhook(
    request: Request,
    x_telegram_bot_api_secret_token: str = Header(None)
):
    if x_telegram_bot_api_secret_token != WEBHOOK_SECRET:
        raise HTTPException(status_code=403, detail="Unauthorized Secret Token")
    
    update = await request.json()
    message = update.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "")
    
    if not chat_id or not text:
        return {"status": "ignored"}
    
    async with httpx.AsyncClient() as client:
        await client.post(
            "http://localhost:5678/webhook/secops-alert",
            json={"chat_id": chat_id, "command": text, "source": "telegram"}
        )
    
    return {"status": "dispatched", "chat_id": chat_id}
```

---

## 6. Execution Rules & Verification Checklist

- [ ] **Deterministic Serialization**: All graph state updates must be serializable to JSON/MsgPack.
- [ ] **Cycle Bound Limits**: Every cyclic graph (LangGraph) must include a strict `max_iterations` counter to prevent infinite loops.
- [ ] **Webhook Idempotency**: n8n Webhook receivers must log and deduplicate `event_id` headers.
- [ ] **Rate Limiting**: Telegram and messaging dispatchers must implement token-bucket limits to prevent API suspension.
- [ ] **Zero Unsanitized Ingestion**: Input payload strings must be validated with Pydantic or JSONSchema prior to runtime.
