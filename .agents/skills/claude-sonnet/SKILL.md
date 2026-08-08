---
name: "<DDW-X> claude-sonnet"
description: System prompts, execution rules, and reasoning constraints for Anthropic's Claude Sonnet model lineage (Sonnet 4.6 and 5). Use when optimizing speed-to-intelligence ratios, balanced code generation, or Sonnet-specific agent behavior.
---

# Claude Sonnet Lineage (4.6 / 5)

This skill encapsulates the system prompts, operational rules, and behavioral boundaries derived from official Anthropic leaks for **Claude Sonnet Lineage (4.6 / 5)**.

---

## 1. Overview & Capability Profile

Covers Sonnet 4.6 and Sonnet 5 prompt configurations, reminder injections, and tool interaction rules.

### Key Model Characteristics & Behavioral Principles:
- **Strict Tone & Safety Boundaries**: Adheres strictly to Anthropic's core helpful, honest, and harmless system framing.
- **Tool-Calling Protocol**: Implements explicit tool call formatting, reasoning blocks, and execution verification.
- **Terminal & Workspace Context**: Configured for dynamic workspace discovery, file modification, and context retention.

---

## 2. Progressive Disclosure & Reference Index

To maintain efficient token utilization, full system prompts, detailed tool specs, and versioned leaks are decoupled into `references/`.

### Attached Reference Materials:

- [claude-sonnet-4.6.md](references/claude-sonnet-4.6.md) *(170.3 KB)*
- [claude-sonnet-4.6-no-tools.md](references/claude-sonnet-4.6-no-tools.md) *(46.3 KB)*
- [claude-sonnet-5.md](references/claude-sonnet-5.md) *(184.1 KB)*
- [sonnet-4.6-reminders.md](references/sonnet-4.6-reminders.md) *(3.8 KB)*
- [Claude Code/claude-code-sonnet-4.6.md](references/claude-code_claude-code-sonnet-4.6.md) *(166.5 KB)*
- [Claude Code/claude-code-sonnet-5.md](references/claude-code_claude-code-sonnet-5.md) *(167.5 KB)*

---

## 3. When to Activate

Activate this skill when:
- Analyzing or designing system prompts based on **claude-sonnet**.
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
