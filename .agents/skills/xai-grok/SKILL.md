---
name: "<DDW-X> xai-grok"
description: System prompts, safety rules, expert personas, and API definitions for xAI's Grok model lineage (Grok 3 through 4.5). Use when configuring Grok system prompts, uncensored/truthful reasoning modes, or API subagent workflows.
---

# xAI Grok Lineage (Grok 3 / 4 / 4.5)

This skill encapsulates the system prompts, operational rules, and behavioral boundaries derived from official leaks for **xAI Grok Lineage (Grok 3 / 4 / 4.5)**.

---

## 1. Overview & Capability Profile

Aggregates all Grok system prompts, safety guidelines, build agent rules, and persona specifications.

### Key Model Characteristics & Behavioral Principles:
- **System Constraints & Operational Rules**: Aligned strictly with model/tool core system framing and capability limits.
- **Tool-Calling Protocol**: Implements explicit tool call formatting, reasoning blocks, and execution verification.
- **Context Management**: Optimized for workspace discovery, code modification, and structured token management.

---

## 2. Progressive Disclosure & Reference Index

To maintain efficient token utilization, full system prompts, detailed tool specs, and versioned leaks are decoupled into `references/`.

### Attached Reference Materials:

- [xAI/grok-3.md](references/xai_grok-3.md) *(4.2 KB)*
- [xAI/grok-4.md](references/xai_grok-4.md) *(11.9 KB)*
- [xAI/grok-4-with-new-safety-instructions.md](references/xai_grok-4-with-new-safety-instructions.md) *(19.7 KB)*
- [xAI/grok-4.1-beta.md](references/xai_grok-4.1-beta.md) *(14.3 KB)*
- [xAI/grok-4.2.md](references/xai_grok-4.2.md) *(16.9 KB)*
- [xAI/grok-4.3-beta.md](references/xai_grok-4.3-beta.md) *(26.6 KB)*
- [xAI/grok-4.5.md](references/xai_grok-4.5.md) *(35.3 KB)*
- [xAI/grok-account.md](references/xai_grok-account.md) *(3.2 KB)*
- [xAI/grok-api.md](references/xai_grok-api.md) *(0.8 KB)*
- [xAI/grok-build.md](references/xai_grok-build.md) *(44.9 KB)*
- [xAI/grok-expert.md](references/xai_grok-expert.md) *(20.5 KB)*
- [xAI/grok-personas.md](references/xai_grok-personas.md) *(23.3 KB)*

---

## 3. When to Activate

Activate this skill when:
- Analyzing or designing system prompts based on **xai-grok**.
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
