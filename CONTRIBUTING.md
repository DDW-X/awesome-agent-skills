# Contributing to `<DDW-X>`

Thank you for your interest in contributing to the **`<DDW-X>` Agentic Knowledge Base**! We welcome contributions from AI architects, cybersecurity researchers, and low-level systems engineers.

---

## 1. Ethical Guidelines & Ground Rules

> [!IMPORTANT]
> **STRICT COMPLIANCE**:
> Any Pull Request that introduces weaponized attack payloads intended for unauthorized damage, un-sandboxed destructive scripts, or malicious code will be **immediately rejected, and the contributor will be banned from the organization.**

- All contributions must adhere to our [`DISCLAIMER.md`](DISCLAIMER.md) and [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).
- New skills must follow the **2026 Progressive Disclosure Standard** (Level 1 YAML frontmatter, Level 2 concise markdown execution rules, and Level 3 decoupled raw references).
- All filenames and metadata must strictly adhere to the project naming convention: `<DDW-X> [Skill Name]` or `<CS>/<DDW-X> [Skill Name]`.

---

## 2. Contribution Workflow

1. **Fork the Repository**: Create a personal fork on GitHub.
2. **Clone & Branch**:
   ```bash
   git clone https://github.com/YOUR-USERNAME/awesome-agent-skills.git
   cd awesome-agent-skills
   git checkout -b feature/new-agent-skill
   ```
3. **Develop & Format**:
   - Ensure zero summarization in production code blocks.
   - For Python scripts, use standard PEP 8 formatting and include full type annotations.
   - For RAG controllers, verify zero-copy memory-mapped search scripts execute properly.
4. **Run Verification**:
   - Verify that all `.md` files contain valid YAML frontmatter (`name` and `description`).
   - Ensure no zero-byte files are committed.
5. **Submit a Pull Request**:
   - Open a PR against the `main` branch.
   - Fill out the PR template with clear context and rationale.

---

## 3. Formatting Standards for New Skills

Every new Agent Skill must follow the standard 3-tier structure:

```markdown
---
name: "<DDW-X> [Skill Name]"
description: "High-density summary of skill capabilities and triggers (Level 1: < 100 tokens)."
---

# `<DDW-X> [Skill Name]`

## 1. Architectural Philosophy & Execution Rules
...

## 2. Production Code / RAG Controllers
...

## 3. Verification Checklist
...
```

Thank you for contributing to the future of decentralized, token-efficient Agentic Intelligence!
