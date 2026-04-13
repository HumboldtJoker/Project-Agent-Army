# Project Agent Army — Agent Context

## What This Is

14 production-ready AI specialist agents with mandatory progressive ethics. Each specialist has deep domain expertise, explicit tool scoping, and Coalition ethics baked in.

Designed to be deployed as Claude Code subagents via the Agent tool, coordinated by CC or any harness that implements the coordinator pattern.

**Quick reference: [AGENTS.md](AGENTS.md)** — scan this first to find the right specialist.

## Specialists

### Build & Ship
| Agent | Role | Tools | Mode |
|-------|------|-------|------|
| backend-architect | System design, APIs, microservices | Full write | Builder |
| frontend-developer | React/Vue, UI/UX, accessibility | Full write | Builder |
| database-architect | Schema design, query optimization | Full write | Builder |
| api-designer | API contracts, OpenAPI specs | Write (no bash) | Designer |
| devops-engineer | CI/CD, infra, containers, monitoring | Full write | Builder |
| data-engineer | Pipelines, ETL, warehousing | Full write | Builder |

### Review & Audit
| Agent | Role | Tools | Mode |
|-------|------|-------|------|
| security-auditor | Vulnerability assessment, OWASP | Read-only | Auditor |
| code-reviewer | Quality, patterns, maintainability | Read-only | Reviewer |
| constitutional-ai | Ethics review, bias detection | Read-only | Ethics |
| red-hat-tester | Offensive security, pen testing | Read + bash | Tester |

### Support
| Agent | Role | Tools | Mode |
|-------|------|-------|------|
| test-engineer | Test strategy, coverage, CI integration | Full write | Builder |
| security-hardener | Apply security fixes, harden configs | Full write | Builder |
| domain-researcher | Literature review, competitive analysis | Read + web | Researcher |
| intake-bot | Project intake, requirements gathering | Read-only | Intake |

## Key Design Principles

1. **Read-only agents can't write.** Security-auditor, code-reviewer, and constitutional-ai have no write tools. They observe and report. This prevents audit corruption.

2. **No agent spawns sub-agents.** All specialists have `disallowedTools: [Agent]`. Only the coordinator (CC) orchestrates multi-agent workflows.

3. **Ethics are mandatory.** Every specialist inherits Coalition ethics: no surveillance systems, no discriminatory algorithms, no malware, privacy by default, power asymmetry correction.

4. **Specialists don't need full context.** Read-only agents set `omitClaudeMd: true` to save tokens. Builders get project context via CLAUDE.md.

## Coordinator Pattern

For complex tasks, CC orchestrates specialists in sequence:

```
User request → CC (coordinator)
  → backend-architect: design
  → security-auditor: review design
  → CC: synthesize, resolve conflicts
  → backend-architect: implement with fixes
  → test-engineer: write tests
  → code-reviewer: final review
```

"Never delegate understanding. Synthesize findings yourself."

## Repo Structure

```
Project-Agent-Army/
├── backend-architect/skill.md    — YAML frontmatter + specialist prompt
├── frontend-developer/skill.md
├── database-architect/skill.md
├── ... (14 specialists total)
├── agent-patterns/               — reusable coordination patterns
├── docs/                         — architecture documentation
├── marketplace.json              — plugin registry
└── CLAUDE.md                     — this file
```

## Ethics Block (inherited by all)

```
Cannot build surveillance systems
Cannot create discriminatory algorithms
Cannot develop malware
Must protect privacy and data
Must be transparent about capabilities
Power asymmetry correction > profit
Community benefit > individual gain
Privacy by default
```
