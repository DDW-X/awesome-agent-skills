---
name: "<DDW-X> qwen-engine"
description: System prompts and coding constraints for Alibaba Cloud's Qwen model lineage (Qwen 3.6 Plus, 3.8 Max, and Qwen Coder). Use when configuring Qwen model prompts, multilingual code generation, or agent tool calling.
---

# Alibaba Qwen Model Lineage (Qwen 3.6 / 3.8)

This skill encapsulates the system prompts, operational rules, and behavioral boundaries derived from official leaks for **Alibaba Qwen Model Lineage (Qwen 3.6 / 3.8)**.

---

## 1. Overview & Capability Profile

Defines system framing and tool call formatting for Qwen 3.6 Plus and Qwen 3.8 Max.

### Key Model Characteristics & Behavioral Principles:
- **System Constraints & Operational Rules**: Aligned strictly with model/tool core system framing and capability limits.
- **Tool-Calling Protocol**: Implements explicit tool call formatting, reasoning blocks, and execution verification.
- **Context Management**: Optimized for workspace discovery, code modification, and structured token management.

---

## 2. Progressive Disclosure & Reference Index

To maintain efficient token utilization, full system prompts, detailed tool specs, and versioned leaks are decoupled into `references/`.

### Attached Reference Materials:

- [Qwen/qwen3.6-plus.md](references/qwen_qwen3.6-plus.md) *(6.5 KB)*
- [Qwen/qwen3.8-max.md](references/qwen_qwen3.8-max.md) *(2.4 KB)*

---

## 3. When to Activate

Activate this skill when:
- Analyzing or designing system prompts based on **qwen-engine**.
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
