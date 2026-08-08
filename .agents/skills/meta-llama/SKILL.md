---
name: "<DDW-X> meta-llama"
description: System prompts and creative assistant instructions for Meta AI and Llama model applications (Meta Spark, Muse Spark). Use when architecting Llama 3 system prompts or open-weights agent instructions.
---

# Meta Llama & Spark Assistant Suite

This skill encapsulates the system prompts, operational rules, and behavioral boundaries derived from official leaks for **Meta Llama & Spark Assistant Suite**.

---

## 1. Overview & Capability Profile

Defines system framing and assistant rules for Meta Spark and Muse Spark 1.1.

### Key Model Characteristics & Behavioral Principles:
- **System Constraints & Operational Rules**: Aligned strictly with model/tool core system framing and capability limits.
- **Tool-Calling Protocol**: Implements explicit tool call formatting, reasoning blocks, and execution verification.
- **Context Management**: Optimized for workspace discovery, code modification, and structured token management.

---

## 2. Progressive Disclosure & Reference Index

To maintain efficient token utilization, full system prompts, detailed tool specs, and versioned leaks are decoupled into `references/`.

### Attached Reference Materials:

- [Meta/meta-spark.md](references/meta_meta-spark.md) *(55.8 KB)*
- [Meta/muse-spark-1.1.md](references/meta_muse-spark-1.1.md) *(70.7 KB)*

---

## 3. When to Activate

Activate this skill when:
- Analyzing or designing system prompts based on **meta-llama**.
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
