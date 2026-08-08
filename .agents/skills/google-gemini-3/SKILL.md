---
name: "<DDW-X> google-gemini-3"
description: System prompts and reasoning boundaries for Google Gemini 3 (Flash, Pro, 3.1 Pro, and 3.5 Flash). Use when architecting Gemini 3 agent prompts, AI Studio build instructions, or multi-modal reasoning workflows.
---

# Google Gemini 3 & 3.5 Model Lineage

This skill encapsulates the system prompts, operational rules, and behavioral boundaries derived from official leaks for **Google Gemini 3 & 3.5 Model Lineage**.

---

## 1. Overview & Capability Profile

Aggregates Gemini 3.0, 3.1, and 3.5 Pro/Flash system prompts across API, Webapp, and AI Studio environments.

### Key Model Characteristics & Behavioral Principles:
- **System Constraints & Operational Rules**: Aligned strictly with model family core system framing and capability limits.
- **Tool-Calling Protocol**: Implements explicit tool call formatting, reasoning blocks, and execution verification.
- **Context Management**: Optimized for workspace discovery, code modification, and structured token management.

---

## 2. Progressive Disclosure & Reference Index

To maintain efficient token utilization, full system prompts, detailed tool specs, and versioned leaks are decoupled into `references/`.

### Attached Reference Materials:

- [gemini-3-flash.md](references/gemini-3-flash.md) *(15.3 KB)*
- [gemini-3-pro.md](references/gemini-3-pro.md) *(13.9 KB)*
- [gemini-3.1-pro.md](references/gemini-3.1-pro.md) *(25.8 KB)*
- [gemini-3.1-pro-api.md](references/gemini-3.1-pro-api.md) *(2.6 KB)*
- [gemini-3.5-flash.md](references/gemini-3.5-flash.md) *(15.7 KB)*
- [gemini-3.5-flash-ai-studio.md](references/gemini-3.5-flash-ai-studio.md) *(2.3 KB)*

---

## 3. When to Activate

Activate this skill when:
- Analyzing or designing system prompts based on **google-gemini-3**.
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
