---
name: "<DDW-X> openai-o-series"
description: System prompts and API constraints for OpenAI's o-series reasoning models (o3, o4-mini). Use when developing reasoning-heavy agent workflows, configuring reasoning-effort tiers (low, medium, high), or optimizing o-series tool usage.
---

# OpenAI o-Series Reasoning Models (o3 & o4-mini)

This skill encapsulates the system prompts, operational rules, and behavioral boundaries derived from official leaks for **OpenAI o-Series Reasoning Models (o3 & o4-mini)**.

---

## 1. Overview & Capability Profile

Defines reasoning effort parameters (low, medium, high) and API system constraints for o3 and o4-mini models.

### Key Model Characteristics & Behavioral Principles:
- **System Constraints & Operational Rules**: Aligned strictly with model family core system framing and capability limits.
- **Tool-Calling Protocol**: Implements explicit tool call formatting, reasoning blocks, and execution verification.
- **Context Management**: Optimized for workspace discovery, code modification, and structured token management.

---

## 2. Progressive Disclosure & Reference Index

To maintain efficient token utilization, full system prompts, detailed tool specs, and versioned leaks are decoupled into `references/`.

### Attached Reference Materials:

- [API/o3-high-api.md](references/api_o3-high-api.md) *(0.9 KB)*
- [API/o3-low-api.md](references/api_o3-low-api.md) *(0.9 KB)*
- [API/o3-medium-api.md](references/api_o3-medium-api.md) *(0.9 KB)*
- [API/o4-mini-high.md](references/api_o4-mini-high.md) *(0.9 KB)*
- [API/o4-mini-low-api.md](references/api_o4-mini-low-api.md) *(0.9 KB)*
- [API/o4-mini-medium-api.md](references/api_o4-mini-medium-api.md) *(0.9 KB)*

---

## 3. When to Activate

Activate this skill when:
- Analyzing or designing system prompts based on **openai-o-series**.
- Aligning agent behavior with official model guidelines and system prompts.
- Developing tool-calling protocols or terminal agent instructions for this model tier.
- Evaluating model responses against baseline system constraints.

---

## 4. Operational Checklist for AI Agents

When acting under this model profile:
1. [ ] **Verify Context Constraints**: Check file limits and avoid outputting duplicate code blocks.
2. [ ] **Follow Tool Execution Order**: Use grep/glob before file edits; read file contents prior to modification.
3. [ ] **Maintain Concise Technical Output**: Minimize conversational filler, focusing on precise diffs and execution output.
4. [ ] **Adhere to Reference Guidelines**: Refer to specific version files in `references/` for detailed behavior.
