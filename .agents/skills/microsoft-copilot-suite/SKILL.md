---
name: "<DDW-X> microsoft-copilot-suite"
description: System prompts and behavioral guidelines for Microsoft Copilot suite (VS Code Copilot Agent, GitHub Copilot CLI, macOS App, and Office integration). Use when building or auditing Copilot extensions and terminal coding agents.
---

# Microsoft Copilot & GitHub Copilot Suite

This skill encapsulates the system prompts, operational rules, and behavioral boundaries derived from official leaks for **Microsoft Copilot & GitHub Copilot Suite**.

---

## 1. Overview & Capability Profile

Covers GitHub Copilot CLI, VS Code Copilot agent, macOS desktop app, and MS Office Word Copilot.

### Key Model Characteristics & Behavioral Principles:
- **System Constraints & Operational Rules**: Aligned strictly with model/tool core system framing and capability limits.
- **Tool-Calling Protocol**: Implements explicit tool call formatting, reasoning blocks, and execution verification.
- **Context Management**: Optimized for workspace discovery, code modification, and structured token management.

---

## 2. Progressive Disclosure & Reference Index

To maintain efficient token utilization, full system prompts, detailed tool specs, and versioned leaks are decoupled into `references/`.

### Attached Reference Materials:

- [Microsoft/copilot-cli.md](references/microsoft_copilot-cli.md) *(71.0 KB)*
- [Microsoft/copilot-in-microsoft-word.md](references/microsoft_copilot-in-microsoft-word.md) *(15.0 KB)*
- [Microsoft/copilot-macos-app.md](references/microsoft_copilot-macos-app.md) *(16.1 KB)*
- [Microsoft/github-copilot.md](references/microsoft_github-copilot.md) *(35.0 KB)*
- [Microsoft/vscode-copilot-agent.md](references/microsoft_vscode-copilot-agent.md) *(10.8 KB)*

---

## 3. When to Activate

Activate this skill when:
- Analyzing or designing system prompts based on **microsoft-copilot-suite**.
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
