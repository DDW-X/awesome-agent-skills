---
name: "<DDW-X> google-workspace-integrations"
description: System prompts for Google product integrations (Workspace, Chrome, YouTube, NotebookLM, Search AI Mode). Use when developing or auditing extensions for Google Workspace, Chrome extensions, or YouTube analysis.
---

# Google Workspace & Product Integrations

This skill encapsulates the system prompts, operational rules, and behavioral boundaries derived from official leaks for **Google Workspace & Product Integrations**.

---

## 1. Overview & Capability Profile

Covers Gemini integrations across Google Workspace, Chrome browser extension, YouTube assistant, NotebookLM, Search AI Mode, and Nano Banana 2 API.

### Key Model Characteristics & Behavioral Principles:
- **System Constraints & Operational Rules**: Aligned strictly with model family core system framing and capability limits.
- **Tool-Calling Protocol**: Implements explicit tool call formatting, reasoning blocks, and execution verification.
- **Context Management**: Optimized for workspace discovery, code modification, and structured token management.

---

## 2. Progressive Disclosure & Reference Index

To maintain efficient token utilization, full system prompts, detailed tool specs, and versioned leaks are decoupled into `references/`.

### Attached Reference Materials:

- [gemini-workspace.md](references/gemini-workspace.md) *(20.7 KB)*
- [gemini-in-chrome.md](references/gemini-in-chrome.md) *(11.3 KB)*
- [gemini-youtube.md](references/gemini-youtube.md) *(16.5 KB)*
- [google-search-ai-mode.md](references/google-search-ai-mode.md) *(4.2 KB)*
- [notebooklm-chat.md](references/notebooklm-chat.md) *(2.5 KB)*
- [gemini-diffusion.md](references/gemini-diffusion.md) *(6.4 KB)*
- [nano-banana-2-api.md](references/nano-banana-2-api.md) *(2.4 KB)*

---

## 3. When to Activate

Activate this skill when:
- Analyzing or designing system prompts based on **google-workspace-integrations**.
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
