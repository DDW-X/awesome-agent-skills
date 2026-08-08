---
name: "<DDW-X> claude-code-engine"
description: System instructions, slash commands, agent sub-systems, and tool definitions for the Claude Code CLI and IDE environment. Use when configuring terminal coding agents, subagent orchestration, or inspecting official Claude Code prompts.
---

# Claude Code Engine & Terminal Agent

This skill encapsulates the system prompts, operational rules, and behavioral boundaries derived from official Anthropic leaks for **Claude Code Engine & Terminal Agent**.

---

## 1. Overview & Capability Profile

Defines the environment rules, tool definitions (glob, grep), docs assistant, and Haiku 4.5 coding prompt.

### Key Model Characteristics & Behavioral Principles:
- **Strict Tone & Safety Boundaries**: Adheres strictly to Anthropic's core helpful, honest, and harmless system framing.
- **Tool-Calling Protocol**: Implements explicit tool call formatting, reasoning blocks, and execution verification.
- **Terminal & Workspace Context**: Configured for dynamic workspace discovery, file modification, and context retention.

---

## 2. Progressive Disclosure & Reference Index

To maintain efficient token utilization, full system prompts, detailed tool specs, and versioned leaks are decoupled into `references/`.

### Attached Reference Materials:

- [Claude Code/claude-code-docs-assistant.md](references/claude-code_claude-code-docs-assistant.md) *(18.2 KB)*
- [Claude Code/claude-code-haiku-4.5.md](references/claude-code_claude-code-haiku-4.5.md) *(167.4 KB)*
- [Claude Code/glob-tool.md](references/claude-code_glob-tool.md) *(1.2 KB)*
- [Claude Code/grep-tool.md](references/claude-code_grep-tool.md) *(4.0 KB)*
- [Claude Code/prompt-suggestion.md](references/claude-code_prompt-suggestion.md) *(1.3 KB)*

---

## 3. When to Activate

Activate this skill when:
- Analyzing or designing system prompts based on **claude-code-engine**.
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
