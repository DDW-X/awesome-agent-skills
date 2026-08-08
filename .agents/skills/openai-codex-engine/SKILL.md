---
name: "<DDW-X> openai-codex-engine"
description: System prompts, terminal agent instructions, computer-use parameters, and code review rules for OpenAI Codex and Codex Desktop. Use when building CLI coding agents, automated review pipelines, or computer-use automation.
---

# OpenAI Codex Engine & Desktop Agent

This skill encapsulates the system prompts, operational rules, and behavioral boundaries derived from official leaks for **OpenAI Codex Engine & Desktop Agent**.

---

## 1. Overview & Capability Profile

Aggregates the full Codex system prompt, planning mode rules, computer use controls, and code auto-review specifications.

### Key Model Characteristics & Behavioral Principles:
- **System Constraints & Operational Rules**: Aligned strictly with model family core system framing and capability limits.
- **Tool-Calling Protocol**: Implements explicit tool call formatting, reasoning blocks, and execution verification.
- **Context Management**: Optimized for workspace discovery, code modification, and structured token management.

---

## 2. Progressive Disclosure & Reference Index

To maintain efficient token utilization, full system prompts, detailed tool specs, and versioned leaks are decoupled into `references/`.

### Attached Reference Materials:

- [Codex/codex-full.md](references/codex_codex-full.md) *(351.1 KB)*
- [Codex/codex-auto-review.md](references/codex_codex-auto-review.md) *(12.6 KB)*
- [Codex/codex-desktop-realtime-voice-agent.md](references/codex_codex-desktop-realtime-voice-agent.md) *(2.5 KB)*
- [Codex/gpt-5.3-codex-spark.md](references/codex_gpt-5.3-codex-spark.md) *(11.7 KB)*
- [Codex/gpt-5.4.md](references/codex_gpt-5.4.md) *(12.6 KB)*
- [Codex/gpt-5.4-mini.md](references/codex_gpt-5.4-mini.md) *(10.9 KB)*
- [Codex/gpt-5.5.md](references/codex_gpt-5.5.md) *(19.3 KB)*
- [Codex/gpt-5.6.md](references/codex_gpt-5.6.md) *(17.3 KB)*
- [Codex/gpt-5.6-sol.md](references/codex_gpt-5.6-sol.md) *(16.9 KB)*
- [Codex/plan_mode.md](references/codex_plan_mode.md) *(8.6 KB)*
- [Codex/computer-use.md](references/codex_computer-use.md) *(6.1 KB)*
- [Codex/control-chrome.md](references/codex_control-chrome.md) *(13.2 KB)*
- [Codex/control-in-app-browser.md](references/codex_control-in-app-browser.md) *(10.9 KB)*
- [Codex/personality_friendly.md](references/codex_personality_friendly.md) *(2.7 KB)*
- [Codex/personality_friendly_gpt-5.5.md](references/codex_personality_friendly_gpt-5.5.md) *(1.9 KB)*
- [Codex/personality_pragmatic.md](references/codex_personality_pragmatic.md) *(2.1 KB)*
- [Codex/personality_pragmatic_gpt-5.5.md](references/codex_personality_pragmatic_gpt-5.5.md) *(1.8 KB)*

---

## 3. When to Activate

Activate this skill when:
- Analyzing or designing system prompts based on **openai-codex-engine**.
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
