---
name: "<DDW-X> claude-integrations"
description: System prompts and behavioral constraints for Claude product integrations (Cowork, Chrome, Office Apps, iOS, Voice, Design). Use when building or auditing platform-specific AI extensions for Excel, Word, PowerPoint, Chrome, or Mobile.
---

# Claude Enterprise & Application Integrations

This skill encapsulates the system prompts, operational rules, and behavioral boundaries derived from official Anthropic leaks for **Claude Enterprise & Application Integrations**.

---

## 1. Overview & Capability Profile

Covers specialized product integrations including Cowork dispatch, MS Office plugins, Chrome extension, iOS mobile app, voice mode, and artifact visualization.

### Key Model Characteristics & Behavioral Principles:
- **Strict Tone & Safety Boundaries**: Adheres strictly to Anthropic's core helpful, honest, and harmless system framing.
- **Tool-Calling Protocol**: Implements explicit tool call formatting, reasoning blocks, and execution verification.
- **Terminal & Workspace Context**: Configured for dynamic workspace discovery, file modification, and context retention.

---

## 2. Progressive Disclosure & Reference Index

To maintain efficient token utilization, full system prompts, detailed tool specs, and versioned leaks are decoupled into `references/`.

### Attached Reference Materials:

- [claude-cowork.md](references/claude-cowork.md) *(273.6 KB)*
- [claude-cowork-dispatch.md](references/claude-cowork-dispatch.md) *(69.9 KB)*
- [claude-design.md](references/claude-design.md) *(198.9 KB)*
- [claude-for-excel.md](references/claude-for-excel.md) *(16.6 KB)*
- [claude-for-word.md](references/claude-for-word.md) *(27.4 KB)*
- [claude-in-chrome.md](references/claude-in-chrome.md) *(72.3 KB)*
- [claude-in-powerpoint.md](references/claude-in-powerpoint.md) *(6.0 KB)*
- [claude-mobile-ios.md](references/claude-mobile-ios.md) *(52.2 KB)*
- [claude-voice-mode.md](references/claude-voice-mode.md) *(1.1 KB)*
- [anthropic-interviewer.md](references/anthropic-interviewer.md) *(11.4 KB)*
- [anthropic_reminders.md](references/anthropic_reminders.md) *(10.3 KB)*
- [research_instructions.md](references/research_instructions.md) *(20.3 KB)*
- [visualize.md](references/visualize.md) *(69.0 KB)*

---

## 3. When to Activate

Activate this skill when:
- Analyzing or designing system prompts based on **claude-integrations**.
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
