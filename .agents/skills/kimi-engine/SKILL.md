---
name: "<DDW-X> kimi-engine"
description: System prompts and long-context processing rules for Moonshot AI's Kimi assistant (Kimi 2.6 and Kimi 3). Use when configuring Kimi long-context retrieval, document analysis, or agent prompts.
---

# Moonshot AI Kimi Long-Context Engine (Kimi 2.6 / 3)

This skill encapsulates the system prompts, operational rules, and behavioral boundaries derived from official leaks for **Moonshot AI Kimi Long-Context Engine (Kimi 2.6 / 3)**.

---

## 1. Overview & Capability Profile

Covers system instructions and long-context retrieval rules for Kimi 2.6 and Kimi 3.

### Key Model Characteristics & Behavioral Principles:
- **System Constraints & Operational Rules**: Aligned strictly with model/tool core system framing and capability limits.
- **Tool-Calling Protocol**: Implements explicit tool call formatting, reasoning blocks, and execution verification.
- **Context Management**: Optimized for workspace discovery, code modification, and structured token management.

---

## 2. Progressive Disclosure & Reference Index

To maintain efficient token utilization, full system prompts, detailed tool specs, and versioned leaks are decoupled into `references/`.

### Attached Reference Materials:

- [Kimi/kimi-2.6.md](references/kimi_kimi-2.6.md) *(12.9 KB)*
- [Kimi/kimi-3.md](references/kimi_kimi-3.md) *(35.2 KB)*

---

## 3. When to Activate

Activate this skill when:
- Analyzing or designing system prompts based on **kimi-engine**.
- Aligning agent behavior with official model/tool guidelines.
- Developing tool-calling protocols or terminal agent instructions for this environment.
- Evaluating model responses against baseline system constraints.

---

## 4. Operational Checklist for AI Agents

When acting under this model profile:
1. [ ] **Verify Context Constraints**: Check file limits and avoid outputting duplicate code blocks.
2. [ ] **Follow Tool Execution Order**: Use grep/glob before file edits; read file contents prior to modification.
3. [ ] **Maintain Concise Technical Output**: Minimize conversational filler, focusing on precise diffs and execution output.
4. [ ] **Adhere to Reference Guidelines**: Refer to specific version files in `references/` for detailed behavior.
