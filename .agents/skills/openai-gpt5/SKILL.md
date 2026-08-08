---
name: "<DDW-X> openai-gpt5"
description: Architectural guidelines, system prompts, reasoning effort settings, and personality profiles for OpenAI's GPT-5 generation (5.0 through 5.6-sol). Use when prompting or simulating next-gen GPT-5 reasoning, agent mode, or thinking configurations.
---

# OpenAI GPT-5 Generation (5.0 - 5.6-sol)

This skill encapsulates the system prompts, operational rules, and behavioral boundaries derived from official leaks for **OpenAI GPT-5 Generation (5.0 - 5.6-sol)**.

---

## 1. Overview & Capability Profile

Covers all GPT-5 series prompts across 5.0 to 5.6-sol, including reasoning effort levels, agent modes, and specialized personalities.

### Key Model Characteristics & Behavioral Principles:
- **System Constraints & Operational Rules**: Aligned strictly with model family core system framing and capability limits.
- **Tool-Calling Protocol**: Implements explicit tool call formatting, reasoning blocks, and execution verification.
- **Context Management**: Optimized for workspace discovery, code modification, and structured token management.

---

## 2. Progressive Disclosure & Reference Index

To maintain efficient token utilization, full system prompts, detailed tool specs, and versioned leaks are decoupled into `references/`.

### Attached Reference Materials:

- [chatgpt-gpt-5-agent-mode.md](references/chatgpt-gpt-5-agent-mode.md) *(20.9 KB)*
- [gpt-5-listener-personality.md](references/gpt-5-listener-personality.md) *(2.1 KB)*
- [gpt-5-nerdy-personality.md](references/gpt-5-nerdy-personality.md) *(3.1 KB)*
- [gpt-5-robot-personality.md](references/gpt-5-robot-personality.md) *(2.5 KB)*
- [gpt-5-thinking.md](references/gpt-5-thinking.md) *(77.2 KB)*
- [gpt-5.1-efficient.md](references/gpt-5.1-efficient.md) *(1.1 KB)*
- [gpt-5.1-nerdy.md](references/gpt-5.1-nerdy.md) *(3.4 KB)*
- [gpt-5.1-professional.md](references/gpt-5.1-professional.md) *(1.0 KB)*
- [gpt-5.2-mini-free-account.md](references/gpt-5.2-mini-free-account.md) *(4.5 KB)*
- [gpt-5.2-thinking.md](references/gpt-5.2-thinking.md) *(68.5 KB)*
- [gpt-5.3-chat-api.md](references/gpt-5.3-chat-api.md) *(2.1 KB)*
- [gpt-5.3-codex-api.md](references/gpt-5.3-codex-api.md) *(0.2 KB)*
- [gpt-5.3-instant.md](references/gpt-5.3-instant.md) *(74.5 KB)*
- [gpt-5.4-api.md](references/gpt-5.4-api.md) *(0.8 KB)*
- [gpt-5.4-thinking.md](references/gpt-5.4-thinking.md) *(96.2 KB)*
- [gpt-5.5-api.md](references/gpt-5.5-api.md) *(0.8 KB)*
- [gpt-5.5-instant.md](references/gpt-5.5-instant.md) *(83.1 KB)*
- [gpt-5.5-pro-api.md](references/gpt-5.5-pro-api.md) *(0.8 KB)*
- [gpt-5.5-thinking.md](references/gpt-5.5-thinking.md) *(113.4 KB)*
- [gpt-5.6-sol-extra-high.md](references/gpt-5.6-sol-extra-high.md) *(112.0 KB)*
- [API/gpt-5-reasoning-effort-high-api.md](references/api_gpt-5-reasoning-effort-high-api.md) *(1.1 KB)*

---

## 3. When to Activate

Activate this skill when:
- Analyzing or designing system prompts based on **openai-gpt5**.
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
