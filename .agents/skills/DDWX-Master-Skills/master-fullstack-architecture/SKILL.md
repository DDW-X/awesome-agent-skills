---
name: "<DDW-X> Master: Advanced Full-Stack Architecture"
description: "Elite Production Full-Stack Architecture, Distributed Systems, Web Performance, and UI/UX Design Master Skill. Synthesizes full-stack engineering power from Cursor Engine, Claude Sonnet, Gemini 3, and OpenAI Codex."
---

# <DDW-X> Master Skill: Advanced Full-Stack Architecture

## 1. Domain Synthesis & Architecture

This Master Skill unifies four leading full-stack and IDE AI models into a master blueprint for building high-scale, modern web applications and distributed architectures:

- **Cursor AI IDE Engine**: Deep codebase indexing, multi-file atomic edits, precise refactoring, and context-aware diff generation.
- **Claude Sonnet 5**: Clean component architecture, TypeScript type-safety, responsive UI design systems, and state management logic.
- **Google Gemini 3 Pro**: Multi-modal UI/UX optimization, long-context system analysis, API contract design, and web vitals optimization.
- **OpenAI Codex Engine**: High-throughput backend routing, database query optimization, automated test generation, and CI/CD pipelines.

---

## 2. Full-Stack Architectural Standards

### A. Frontend & UI/UX Excellence
- **Design Token Discipline**: Define curated color palettes, typography scales, glassmorphism, and smooth micro-animations. Avoid generic browser defaults.
- **Hydration & SSR Safety**: Prevent React/Next.js hydration mismatches by isolating client-side state hooks from server render paths.
- **Core Web Vitals Optimization**: Optimize for LCP (<2.5s), CLS (<0.1), and INP (<200ms) with eager image loading for hero assets and bundle splitting.

### B. Backend & Data Layer Rules
- **N+1 Query Prevention**: Utilize eager loading (`Include`, `with`, or DataLoader) for all relational queries.
- **Idempotent API Contracts**: Implement strict request deduplication tokens and transaction boundaries for financial or mutating API calls.
- **Decoupled Architecture**: Maintain clean separation between presentation layers, domain business logic, and infrastructure adapters.

---

## 3. Implementation Code Patterns

### ✅ Production Pattern: Atomic Client Component with Hydration Safety
```tsx
'use client';

import { useState, useEffect } from 'react';

export function InteractiveCard({ title, content }: { title: string; content: string }) {
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  if (!isMounted) {
    return <div className="h-48 w-full animate-pulse bg-slate-800/50 rounded-xl" />;
  }

  return (
    <div className="p-6 rounded-xl bg-slate-900/80 backdrop-blur-md border border-slate-800 shadow-xl transition-all hover:scale-[1.02]">
      <h3 className="text-xl font-bold text-slate-100 mb-2">{title}</h3>
      <p className="text-slate-400 text-sm leading-relaxed">{content}</p>
    </div>
  );
}
```

### ❌ Anti-Pattern: Unchecked Direct Hydration Window Dereference
```tsx
export function UnsafeComponent() {
  // DANGEROUS: Mismatch error during Server Side Rendering
  const width = window.innerWidth;
  return <div>Window width: {width}</div>;
}
```


---

## 4. Synthesized Constituent Model References

Below are the direct reference prompt foundations synthesized into this Master Skill:

- **Cursor AI IDE Engine**: [cursor_cursor.md](references/cursor_cursor.md) *(17.7 KB)*
- **Claude Sonnet 5**: [claude-sonnet-5.md](references/claude-sonnet-5.md) *(184.1 KB)*
- **Google Gemini 3 Pro**: [gemini-3-pro.md](references/gemini-3-pro.md) *(13.9 KB)*
- **OpenAI Codex Full Engine**: [codex_codex-full.md](references/codex_codex-full.md) *(351.1 KB)*

---

## 5. Verification & Execution Checklist

When executing tasks under this Master Skill profile:
1. [ ] **Verify Core Intent**: Match task against specialized domain rules (SecOps / Systems / Full-Stack).
2. [ ] **Apply Model Best Practices**: Combine reasoning frameworks from constituent reference files.
3. [ ] **Perform Empirical Verification**: Run tests, builds, or security benchmarks to validate modifications.
