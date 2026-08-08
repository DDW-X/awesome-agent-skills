---
name: "<DDW-X> mistral-engine"
description: System prompts and behavioral rules for Mistral AI models (Mistral Code, Mistral Medium 3.5, Codestral). Use when configuring Mistral agent prompts, code completion, or Le Chat system instructions.
---

# Mistral AI & Codestral Engine

This skill encapsulates the system prompts, operational rules, and behavioral boundaries derived from official leaks for **Mistral AI & Codestral Engine**.

---

## 1. Overview & Capability Profile

Covers system prompt framing for Mistral Code and Mistral Medium 3.5.

### Key Model Characteristics & Behavioral Principles:
- **System Constraints & Operational Rules**: Aligned strictly with model/tool core system framing and capability limits.
- **Tool-Calling Protocol**: Implements explicit tool call formatting, reasoning blocks, and execution verification.
- **Context Management**: Optimized for workspace discovery, code modification, and structured token management.

---

## 2. Progressive Disclosure & Reference Index

To maintain efficient token utilization, full system prompts, detailed tool specs, and versioned leaks are decoupled into `references/`.

### Attached Reference Materials:

- [Mistral/mistral-code.md](references/mistral_mistral-code.md) *(13.3 KB)*
- [Mistral/mistral-medium-3.5.md](references/mistral_mistral-medium-3.5.md) *(21.5 KB)*

---

## 3. When to Activate

Activate this skill when:
- Analyzing or designing system prompts based on **mistral-engine**.
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
