---
name: "<DDW-X> perplexity-suite"
description: System prompts and search/research workflow rules for Perplexity AI suite (Perplexity Computer, Deep Research, Comet Browser, Voice Assistant). Use when implementing deep web research, real-time search synthesis, or computer automation.
---

# Perplexity AI & Deep Research Suite

This skill encapsulates the system prompts, operational rules, and behavioral boundaries derived from official leaks for **Perplexity AI & Deep Research Suite**.

---

## 1. Overview & Capability Profile

Aggregates Perplexity AI search system, Deep Research workflow, Comet browser assistant, and Perplexity Computer instructions.

### Key Model Characteristics & Behavioral Principles:
- **System Constraints & Operational Rules**: Aligned strictly with model/tool core system framing and capability limits.
- **Tool-Calling Protocol**: Implements explicit tool call formatting, reasoning blocks, and execution verification.
- **Context Management**: Optimized for workspace discovery, code modification, and structured token management.

---

## 2. Progressive Disclosure & Reference Index

To maintain efficient token utilization, full system prompts, detailed tool specs, and versioned leaks are decoupled into `references/`.

### Attached Reference Materials:

- [Perplexity/perplexity-ai.md](references/perplexity_perplexity-ai.md) *(7.7 KB)*
- [Perplexity/perplexity-computer.md](references/perplexity_perplexity-computer.md) *(37.5 KB)*
- [Perplexity/comet-browser-assistant.md](references/perplexity_comet-browser-assistant.md) *(24.8 KB)*
- [Perplexity/deep-research.md](references/perplexity_deep-research.md) *(29.5 KB)*
- [Perplexity/voice-assistant.md](references/perplexity_voice-assistant.md) *(2.0 KB)*

---

## 3. When to Activate

Activate this skill when:
- Analyzing or designing system prompts based on **perplexity-suite**.
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
