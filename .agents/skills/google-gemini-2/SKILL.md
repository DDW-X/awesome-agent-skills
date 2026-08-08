---
name: "<DDW-X> google-gemini-2"
description: System prompts and web app instructions for Google Gemini 2.0 Flash and 2.5 Pro/Flash model family. Use when configuring Gemini 2.0/2.5 API parameters, webapp instructions, or guided learning modes.
---

# Google Gemini 2.0 & 2.5 Model Family

This skill encapsulates the system prompts, operational rules, and behavioral boundaries derived from official leaks for **Google Gemini 2.0 & 2.5 Model Family**.

---

## 1. Overview & Capability Profile

Covers Gemini 2.0 Flash, 2.5 Flash Image Preview, and 2.5 Pro API & Guided Learning system prompts.

### Key Model Characteristics & Behavioral Principles:
- **System Constraints & Operational Rules**: Aligned strictly with model family core system framing and capability limits.
- **Tool-Calling Protocol**: Implements explicit tool call formatting, reasoning blocks, and execution verification.
- **Context Management**: Optimized for workspace discovery, code modification, and structured token management.

---

## 2. Progressive Disclosure & Reference Index

To maintain efficient token utilization, full system prompts, detailed tool specs, and versioned leaks are decoupled into `references/`.

### Attached Reference Materials:

- [gemini-2.0-flash-webapp.md](references/gemini-2.0-flash-webapp.md) *(2.3 KB)*
- [gemini-2.5-flash-image-preview.md](references/gemini-2.5-flash-image-preview.md) *(4.8 KB)*
- [gemini-2.5-pro-api.md](references/gemini-2.5-pro-api.md) *(3.1 KB)*
- [gemini-2.5-pro-guided-learning.md](references/gemini-2.5-pro-guided-learning.md) *(15.1 KB)*
- [gemini-2.5-pro-webapp.md](references/gemini-2.5-pro-webapp.md) *(1.9 KB)*

---

## 3. When to Activate

Activate this skill when:
- Analyzing or designing system prompts based on **google-gemini-2**.
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
