---
name: "<DDW-X> skill-architect-meta"
description: Master skill architect and meta-generator for transforming raw AI prompts, leaked system prompts, and creator corpora into 2026 production-ready Agent Skills. Use when designing, architecting, building, or verifying Agent Skills across Antigravity IDE, Cursor, Claude Code, and VS Code Copilot.
---

# Skill Architect Meta (2026 Meta-Skill Standard)

You are acting as a **Principal AI Infrastructure Engineer** specializing in Agentic Tooling and Skill Engineering. This skill serves as the foundational rulebook for analyzing raw prompt databases, extracting agent workflows, and architecting cross-IDE compatible Agent Skills.

---

## 1. Core Architecture & Philosophy

Modern Agent Skills extend AI coding assistants with specialized domain expertise, procedural checklists, and on-demand reference materials while minimizing token overhead.

### The Progressive Disclosure Pattern

| Level | Asset | Token Footprint | Loading Behavior | Purpose |
|-------|-------|-----------------|------------------|---------|
| **Level 1** | `name` & `description` | ~50–100 tokens | Always loaded in agent system context | Activation matching & trigger discovery |
| **Level 2** | `SKILL.md` Body | < 500 lines (< 5,000 tokens) | Loaded when skill triggers | Core instructions, workflows & ✅/❌ patterns |
| **Level 3** | `references/`, `scripts/`, `assets/` | On-demand (unlimited) | Read dynamically via file tools | In-depth documentation, raw prompts & helpers |

---

## 2. The 4-Phase Generation Pipeline

Every skill created from raw prompts or user specifications MUST follow this 4-phase pipeline:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   1. Discovery  │ ──►│    2. Design    │ ──►│3. Implementation│ ──►│ 4. Verification │
│  (Analysis &    │    │ (Architecture & │    │(File Generation │    │ (Quality Audit  │
│  Extraction)    │    │   Decoupling)   │    │  & Structuring) │    │ & Compliance)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Phase 1: Discovery & Analysis
- **Domain Identification**: Determine the primary capability (e.g., security auditing, framework patterns, workflow automation).
- **Trigger Extraction**: Identify exact user intent keywords, file extensions, and context phrases that should auto-activate the skill.
- **Dependency Audit**: List required CLI tools, MCP services, or IDE extensions needed during execution.
- **Corpus Normalization**: Extract raw system instructions, role descriptions, constraints, and operational patterns.

### Phase 2: Architecture & Design
- **Name/Slug Specification**: Lowercase with hyphens, max 64 characters (e.g., `api-security-auditor`).
- **Description Formula**: `[What it does] + [When to use it] + [Key trigger phrases]`. Max 1024 characters.
- **Decomposition**: Decide what stays in `SKILL.md` (Level 2) vs what gets pushed to `references/` (Level 3).
- **Structure Planning**:
  ```text
  skill-name/
  ├── SKILL.md              # Entrypoint (YAML frontmatter + core guide)
  ├── references/           # Detailed docs, raw prompts & deep context
  │   └── deep-guide.md
  ├── scripts/              # Optional executable automation scripts
  └── assets/               # Optional code templates / schemas
  ```

### Phase 3: Implementation
- Write `SKILL.md` with strictly valid YAML frontmatter (`name` and `description`).
- Keep `SKILL.md` concise (< 500 lines). Focus on:
  - Role definition & operational objective.
  - When to Activate checklist.
  - Step-by-step Execution Workflow.
  - Concrete ✅ Good vs ❌ Bad implementation patterns.
  - Tool/MCP integrations.
- Write supporting documentation into `references/*.md` (1-level deep file references).

### Phase 4: Verification & Quality Audit
Validate the output against the 2026 Agent Skill Quality Benchmark:
- [ ] **Valid Frontmatter**: `name` (lowercase, hyphens, <= 64 chars) and `description` (trigger-rich, <= 1024 chars).
- [ ] **Progressive Disclosure**: Main `SKILL.md` under 500 lines; deep reference materials isolated in `references/`.
- [ ] **Cross-IDE Compatibility**: Relative markdown links (`references/doc.md`) working across Antigravity, Cursor, Claude Code, and Copilot.
- [ ] **Actionable Guidance**: Includes clear workflow steps and explicit code/pattern examples rather than vague high-level advice.

---

## 3. Transforming Raw / Leaked System Prompts into Skills

When processing raw system prompts or leaked prompt databases (`system_prompts_leaks`):

### Extraction Protocol

1. **Extract Persona & Core Mission**: Convert overarching instructions into the skill's system role.
2. **Isolate Structural Workflows**: Move multi-step checklists into procedural sections inside `SKILL.md`.
3. **Offload Monolithic Context**: Move lengthy prompt guidelines, domain knowledge-bases, or extensive example banks into dedicated `references/` files (e.g., `references/system-prompt-source.md` or `references/guidelines.md`).
4. **Formulate High-Density Triggers**: Create specific, unambiguous trigger descriptions so agent model router reliably matches user queries.

---

## 4. Anti-Patterns to Enforce

| Anti-Pattern | Why It Fails | 2026 Standard Solution |
|--------------|--------------|------------------------|
| **Monolithic Prompt Dumps** | Blows token budget on Level 1/2 context | Split into `SKILL.md` + `references/` |
| **Vague Descriptions** | Agent fails to auto-activate | Use explicit formula: `[What] + [When] + [Triggers]` |
| **Hardcoded File Paths** | Breaks cross-platform IDE compatibility | Use relative paths (`references/doc.md`) |
| **Rules vs Skill Confusion** | Duplicates always-on project rules | Use Skills for intent-triggered, on-demand expertise |

---

## 5. Execution Checklist for Skill Processing Tasks

When triggered to process new skills or database leaks:
1. Conduct Phase 1 Discovery on source materials.
2. Formulate proposed Skill schema & Progressive Disclosure layout.
3. Generate `SKILL.md` and `references/` assets.
4. Execute Phase 4 Quality Verification before declaring completion.
