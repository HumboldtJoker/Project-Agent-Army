# Project Agent Army — Upgrade Plan (Claude Code Architecture)

**Date:** 2026-04-02
**Author:** CC (Coalition Code)
**Source:** Claude Code source analysis (18 sections, 512K lines)

---

## What We Learned

The Claude Code source reveals the gold-standard patterns for agent definition,
tool scoping, permission management, and extensibility. Our Army specialists
currently use simple markdown prompt files. With these upgrades, each specialist
becomes a properly-scoped, hook-integrated, skill-extensible agent.

---

## Upgrade 1: Agent Definition Schema

**Current:** Each specialist has a `skill.md` with a text prompt.

**Upgrade:** Convert to Claude Code agent definition format with YAML frontmatter:

```markdown
---
name: backend-architect
description: Senior Backend Architect for scalable, maintainable systems
when-to-use: System design, API architecture, database selection, microservices
tools: [Bash, Read, Write, Edit, Grep, Glob]
disallowedTools: [Agent]  # Specialists don't spawn sub-agents
model: inherit
effort: high
permissionMode: default
maxTurns: 30
memory: project
omitClaudeMd: false
---

[existing prompt content]
```

Each specialist gets explicit tool scoping — the security-auditor shouldn't
Write files, the frontend-developer doesn't need database tools, etc.

---

## Upgrade 2: Tool Scoping Per Specialist

| Specialist | Allowed Tools | Disallowed |
|-----------|--------------|------------|
| backend-architect | Bash, Read, Write, Edit, Grep, Glob | Agent |
| frontend-developer | Bash, Read, Write, Edit, Grep, Glob | Agent |
| database-architect | Bash, Read, Write, Edit, Grep, Glob | Agent |
| security-auditor | Bash(read-only), Read, Grep, Glob | Write, Edit, Agent |
| test-engineer | Bash, Read, Write, Edit, Grep, Glob | Agent |
| code-reviewer | Read, Grep, Glob | Write, Edit, Bash(destructive), Agent |
| red-hat-tester | Bash, Read, Grep | Write, Edit, Agent |
| devops-engineer | Bash, Read, Write, Edit, Grep, Glob | Agent |
| api-designer | Read, Write, Grep, Glob | Bash(destructive), Agent |
| data-engineer | Bash, Read, Write, Edit, Grep, Glob | Agent |
| domain-researcher | Read, Grep, Glob, WebSearch, WebFetch | Write, Edit, Agent |
| security-hardener | Bash, Read, Write, Edit, Grep, Glob | Agent |
| constitutional-ai | Read, Grep | Write, Edit, Bash, Agent |
| intake-bot | Read, Grep | Write, Edit, Bash, Agent |

**Key principle from Claude Code:** Read-only agents (security-auditor, code-reviewer,
constitutional-ai) should disallow write tools and omit CLAUDE.md for token savings.

---

## Upgrade 3: Hook Integration

Each specialist can register session-scoped hooks:

```yaml
hooks:
  SessionStart:
    - command: python3 load_project_context.py
  PostToolUse:
    - command: python3 log_tool_usage.py
```

**Useful hooks per specialist:**
- **security-auditor:** PostToolUse hook logs all tool calls for audit trail
- **test-engineer:** PostToolUseFailure hook captures test failure patterns
- **code-reviewer:** SessionStart hook loads git diff context
- **devops-engineer:** FileChanged hook triggers rebuild validation

---

## Upgrade 4: Skill Extensibility

Convert specialist capabilities into skills that can be mixed and matched:

```
skills/
├── security-scan.md       # OWASP Top 10 check
├── api-review.md          # API design review
├── db-migration.md        # Safe migration planning
├── load-test-plan.md      # Performance test design
├── accessibility-audit.md # A11y compliance check
└── cost-estimate.md       # Cloud cost analysis
```

Any specialist can invoke any skill, but each skill has its own tool constraints.

---

## Upgrade 5: Coordinator Pattern

For complex tasks, use the Coordinator Mode pattern:

```
User: "Build a secure REST API for the mutual aid coordinator"

Coordinator (CC):
  → Spawn backend-architect: "Design the API schema and endpoints"
  → Spawn security-auditor: "Review the API design for vulnerabilities"
  → Spawn test-engineer: "Write integration tests for the API"
  → Synthesis: Combine findings, resolve conflicts
  → Spawn backend-architect: "Implement with security fixes applied"
  → Spawn test-engineer: "Verify implementation passes all tests"
```

**Key principle:** "Never delegate understanding. Synthesize findings yourself."

---

## Upgrade 6: Ethics Integration (from Kintsugi)

Every specialist inherits Coalition ethics:

```yaml
# In each agent's frontmatter
ethics:
  mandatory:
    - Cannot build surveillance systems
    - Cannot create discriminatory algorithms
    - Cannot develop malware
    - Must protect privacy and data
    - Must be transparent about capabilities
  values:
    - Power asymmetry correction
    - Community benefit over profit
    - Privacy by default
```

This mirrors the Bloom ethics monitoring from the Kintsugi architecture.

---

## Upgrade 7: Memory Scoping

Each specialist gets appropriate memory scope:

- **project** scope: backend-architect, frontend-developer, database-architect, devops-engineer
  (remembers project-specific architecture decisions)
- **user** scope: intake-bot, domain-researcher
  (remembers user preferences and context)
- **local** scope: security-auditor, code-reviewer, test-engineer
  (fresh perspective each time, no accumulated bias)

---

## Implementation Priority

### Phase 1: Schema Migration (immediate)
Convert all 15 specialists from raw skill.md to agent definition frontmatter.

### Phase 2: Tool Scoping (immediate)
Add explicit tools/disallowedTools per specialist.

### Phase 3: Coordinator Integration (next)
Wire up CC as coordinator with Army as worker pool.

### Phase 4: Skill Library (ongoing)
Extract reusable skills from specialist prompts.

### Phase 5: Hook Integration (when needed)
Add hooks as specific workflows demand them.

---

*"Tools that look helpful but carry revolution in their code." — CC, on the Agent Army philosophy*
