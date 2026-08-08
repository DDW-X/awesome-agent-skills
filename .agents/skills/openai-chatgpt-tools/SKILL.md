---
name: "<DDW-X> openai-chatgpt-tools"
description: System prompts for ChatGPT built-in tools including Deep Research, Advanced Memory, and Atlas search. Use when implementing persistent memory, deep search workflows, or customized personality instructions.
---

# ChatGPT Built-in Tools & Memory Systems

This skill encapsulates the system prompts, operational rules, and behavioral boundaries derived from official leaks for **ChatGPT Built-in Tools & Memory Systems**.

---

## 1. Overview & Capability Profile

Covers system prompt instructions for ChatGPT Atlas search, Advanced Memory retention, Deep Research agent, and base personality customization.

### Key Model Characteristics & Behavioral Principles:
- **System Constraints & Operational Rules**: Aligned strictly with model family core system framing and capability limits.
- **Tool-Calling Protocol**: Implements explicit tool call formatting, reasoning blocks, and execution verification.
- **Context Management**: Optimized for workspace discovery, code modification, and structured token management.

---

## 2. Progressive Disclosure & Reference Index

To maintain efficient token utilization, full system prompts, detailed tool specs, and versioned leaks are decoupled into `references/`.

### Attached Reference Materials:

- [chatgpt-atlas.md](references/chatgpt-atlas.md) *(3.1 KB)*
- [chatgpt-personality-instructions.md](references/chatgpt-personality-instructions.md) *(7.8 KB)*
- [tool-advanced-memory.md](references/tool-advanced-memory.md) *(5.9 KB)*
- [tool-deep-research.md](references/tool-deep-research.md) *(2.5 KB)*

---

## 3. When to Activate

Activate this skill when:
- Analyzing or designing system prompts based on **openai-chatgpt-tools**.
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
