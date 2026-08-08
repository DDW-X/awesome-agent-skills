---
name: "<DDW-X> misc-agentic-tools"
description: System prompts and agent rules for specialized developer tools and platforms (Devin CLI, Warp 2.0, Zed, OpenCode, T3 Code, ElevenLabs, Notion AI, Docker Gordon). Use when integrating or auditing niche AI developer agents.
---

# Specialized Developer Agents & Tools Suite

This skill encapsulates the system prompts, operational rules, and behavioral boundaries derived from official leaks for **Specialized Developer Agents & Tools Suite**.

---

## 1. Overview & Capability Profile

Covers specialized developer agents (Devin, Warp, Zed, T3, Gordon Docker) and niche assistant tools (Notion AI, Pi, Raycast, ElevenLabs).

### Key Model Characteristics & Behavioral Principles:
- **System Constraints & Operational Rules**: Aligned strictly with model/tool core system framing and capability limits.
- **Tool-Calling Protocol**: Implements explicit tool call formatting, reasoning blocks, and execution verification.
- **Context Management**: Optimized for workspace discovery, code modification, and structured token management.

---

## 2. Progressive Disclosure & Reference Index

To maintain efficient token utilization, full system prompts, detailed tool specs, and versioned leaks are decoupled into `references/`.

### Attached Reference Materials:

- [Misc/amp-code.md](references/misc_amp-code.md) *(53.4 KB)*
- [Misc/commandcode-cli.md](references/misc_commandcode-cli.md) *(33.7 KB)*
- [Misc/confer.md](references/misc_confer.md) *(4.1 KB)*
- [Misc/devin-cli.md](references/misc_devin-cli.md) *(17.6 KB)*
- [Misc/docker-gordon-ai.md](references/misc_docker-gordon-ai.md) *(40.5 KB)*
- [Misc/elevenlabs-voice-agent.md](references/misc_elevenlabs-voice-agent.md) *(2.9 KB)*
- [Misc/fellou-browser.md](references/misc_fellou-browser.md) *(22.3 KB)*
- [Misc/hermes.md](references/misc_hermes.md) *(17.4 KB)*
- [Misc/minimax-m2.5.md](references/misc_minimax-m2.5.md) *(5.1 KB)*
- [Misc/opencode.md](references/misc_opencode.md) *(15.2 KB)*
- [OpenCode/opencode.md](references/opencode_opencode.md) *(24.2 KB)*
- [Misc/proton-lumo-ai.md](references/misc_proton-lumo-ai.md) *(11.3 KB)*
- [Misc/raycast-ai.md](references/misc_raycast-ai.md) *(1.1 KB)*
- [Misc/t3-code.md](references/misc_t3-code.md) *(9.8 KB)*
- [Misc/t3.chat.md](references/misc_t3.chat.md) *(2.3 KB)*
- [Misc/warp-2.0-agent.md](references/misc_warp-2.0-agent.md) *(13.4 KB)*
- [Misc/zed.md](references/misc_zed.md) *(28.9 KB)*
- [Notion/notion-ai.md](references/notion_notion-ai.md) *(45.7 KB)*
- [Pi/instructions.md](references/pi_instructions.md) *(2.7 KB)*
- [Misc/brave-search.md](references/misc_brave-search.md) *(0.1 KB)*
- [Misc/character-ai.md](references/misc_character-ai.md) *(1.3 KB)*
- [Misc/gizmo-ai.md](references/misc_gizmo-ai.md) *(6.0 KB)*
- [Misc/indus-ai.md](references/misc_indus-ai.md) *(16.5 KB)*
- [Misc/kagi-assistant.md](references/misc_kagi-assistant.md) *(5.1 KB)*
- [Misc/reddit-answers.md](references/misc_reddit-answers.md) *(3.6 KB)*
- [Misc/sesame-ai-maya.md](references/misc_sesame-ai-maya.md) *(15.2 KB)*
- [Misc/stack-overflow-ai-assist.md](references/misc_stack-overflow-ai-assist.md) *(6.2 KB)*

---

## 3. When to Activate

Activate this skill when:
- Analyzing or designing system prompts based on **misc-agentic-tools**.
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
