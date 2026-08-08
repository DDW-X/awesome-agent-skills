---
name: "<DDW-X> claude-fable-5"
description: Behavioral guidelines, persona instructions, and operational boundaries for Anthropic's Claude Fable 5 model family. Use when simulating Fable 5 reasoning, evaluating prompt architecture, or adapting Fable 5 behavior for agent workflows.
---

# Claude Fable 5 Engine & System Prompts

This skill encapsulates the system prompts, operational rules, and behavioral boundaries derived from official Anthropic leaks for **Claude Fable 5 Engine & System Prompts**.

---

## 1. Overview & Capability Profile

Covers Claude Fable 5 core system prompt, desktop environment parameters, and command execution guidelines.

### Key Model Characteristics & Behavioral Principles:
- **Strict Tone & Safety Boundaries**: Adheres strictly to Anthropic's core helpful, honest, and harmless system framing.
- **Tool-Calling Protocol**: Implements explicit tool call formatting, reasoning blocks, and execution verification.
- **Terminal & Workspace Context**: Configured for dynamic workspace discovery, file modification, and context retention.

---

## 2. Progressive Disclosure & Reference Index

To maintain efficient token utilization, full system prompts, detailed tool specs, and versioned leaks are decoupled into `references/`.

### Attached Reference Materials:

- [claude-fable-5.md](references/claude-fable-5.md) *(227.0 KB)*
- [Claude Code/claude-code-fable-5.md](references/claude-code_claude-code-fable-5.md) *(136.6 KB)*
- [Claude Code/claude-code-desktop-fable-5.md](references/claude-code_claude-code-desktop-fable-5.md) *(304.4 KB)*

---

## 3. When to Activate

Activate this skill when:
- Analyzing or designing system prompts based on **claude-fable-5**.
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
