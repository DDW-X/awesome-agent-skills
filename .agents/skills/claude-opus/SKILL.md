---
name: "<DDW-X> claude-opus"
description: Architectural guidelines, system prompts, and tool usage rules for Anthropic's Claude Opus model lineage (Opus 4.6, 4.7, 4.8, and 5). Use when implementing deep reasoning, complex refactoring, high-effort planning, or Opus-level analysis.
---

# Claude Opus Lineage (4.6 / 4.7 / 4.8 / 5)

This skill encapsulates the system prompts, operational rules, and behavioral boundaries derived from official Anthropic leaks for **Claude Opus Lineage (4.6 / 4.7 / 4.8 / 5)**.

---

## 1. Overview & Capability Profile

Aggregates all Opus series system prompts across versions 4.6 to 5, including tool-enabled and tool-less configurations.

### Key Model Characteristics & Behavioral Principles:
- **Strict Tone & Safety Boundaries**: Adheres strictly to Anthropic's core helpful, honest, and harmless system framing.
- **Tool-Calling Protocol**: Implements explicit tool call formatting, reasoning blocks, and execution verification.
- **Terminal & Workspace Context**: Configured for dynamic workspace discovery, file modification, and context retention.

---

## 2. Progressive Disclosure & Reference Index

To maintain efficient token utilization, full system prompts, detailed tool specs, and versioned leaks are decoupled into `references/`.

### Attached Reference Materials:

- [claude-opus-4.6.md](references/claude-opus-4.6.md) *(175.4 KB)*
- [claude-opus-4.6-no-tools.md](references/claude-opus-4.6-no-tools.md) *(48.5 KB)*
- [claude-opus-4.7.md](references/claude-opus-4.7.md) *(177.9 KB)*
- [claude-opus-4.8.md](references/claude-opus-4.8.md) *(179.2 KB)*
- [claude-opus-5.md](references/claude-opus-5.md) *(219.1 KB)*
- [Claude Code/claude-code-opus-4.6.md](references/claude-code_claude-code-opus-4.6.md) *(166.6 KB)*
- [Claude Code/claude-code-opus-4.7.md](references/claude-code_claude-code-opus-4.7.md) *(166.6 KB)*
- [Claude Code/claude-code-opus-4.8.md](references/claude-code_claude-code-opus-4.8.md) *(129.6 KB)*
- [Claude Code/claude-code-opus-5.md](references/claude-code_claude-code-opus-5.md) *(135.5 KB)*

---

## 3. When to Activate

Activate this skill when:
- Analyzing or designing system prompts based on **claude-opus**.
- Aligning agent behavior with official Anthropic model guidelines.
- Developing tool-calling protocols or terminal agent instructions for this model tier.
- Evaluating model responses against baseline system constraints.

---

## 4. Operational Checklist for AI Agents

When acting under this model profile:
1. [ ] **Verify Context Constraints**: Check file limits and avoid outputting duplicate code blocks.
2. [ ] **Follow Tool Execution Order**: Use grep/glob before file edits; read file contents prior to modification.
3. [ ] **Maintain Concise Technical Output**: Minimize conversational filler, focusing on precise diffs and execution output.
4. [ ] **Adhere to Reference Guidelines**: Refer to specific version files in `references/` for detailed behavior.
