---
name: "<DDW-X> openai-gpt4o"
description: System prompts, voice mode instructions, and behavioral rules for OpenAI's GPT-4o and GPT-4.5 model family. Use when configuring GPT-4o/4.5 agent personalities, voice interaction rules, or multimodal prompt constraints.
---

# OpenAI GPT-4o & GPT-4.5 Model Family

This skill encapsulates the system prompts, operational rules, and behavioral boundaries derived from official leaks for **OpenAI GPT-4o & GPT-4.5 Model Family**.

---

## 1. Overview & Capability Profile

Aggregates system prompts for GPT-4o, GPT-4.5, Advanced Voice Mode, legacy voice, and deprecation preparedness.

### Key Model Characteristics & Behavioral Principles:
- **System Constraints & Operational Rules**: Aligned strictly with model family core system framing and capability limits.
- **Tool-Calling Protocol**: Implements explicit tool call formatting, reasoning blocks, and execution verification.
- **Context Management**: Optimized for workspace discovery, code modification, and structured token management.

---

## 2. Progressive Disclosure & Reference Index

To maintain efficient token utilization, full system prompts, detailed tool specs, and versioned leaks are decoupled into `references/`.

### Attached Reference Materials:

- [gpt-4o.md](references/gpt-4o.md) *(30.9 KB)*
- [4o-2025-09-03-new-personality.md](references/4o-2025-09-03-new-personality.md) *(2.6 KB)*
- [chatgpt-4.5.md](references/chatgpt-4.5.md) *(30.6 KB)*
- [gpt-4.1.md](references/gpt-4.1.md) *(12.6 KB)*
- [gpt-4.1-mini.md](references/gpt-4.1-mini.md) *(4.8 KB)*
- [gpt-4.5.md](references/gpt-4.5.md) *(10.8 KB)*
- [gpt-4o-advanced-voice-mode.md](references/gpt-4o-advanced-voice-mode.md) *(2.2 KB)*
- [gpt-4o-legacy-voice-mode.md](references/gpt-4o-legacy-voice-mode.md) *(5.7 KB)*
- [ChatGPT/chatgpt-4o-deprecation-preparedness-prompt.md](references/chatgpt_chatgpt-4o-deprecation-preparedness-prompt.md) *(2.0 KB)*

---

## 3. When to Activate

Activate this skill when:
- Analyzing or designing system prompts based on **openai-gpt4o**.
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
