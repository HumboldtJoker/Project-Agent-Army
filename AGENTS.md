# Agent Army — Quick Reference

Use this file to find the right specialist. Spawn via Claude Code's Agent tool:
```
Agent({ subagent_type: "general", prompt: "You are the [specialist]. [task]" })
```

Or reference the skill.md directly for the full specialist prompt.

---

## Builders (full write access)

| Agent | What it does | When to use | Path |
|-------|-------------|-------------|------|
| **backend-architect** | System design, APIs, microservices, database selection | Designing backend systems, choosing architecture patterns, scaling decisions | backend-architect/skill.md |
| **frontend-developer** | React/Vue/modern web, UI/UX, accessibility, responsive design | Building UI components, frontend architecture, CSS/JS, accessibility audits | frontend-developer/skill.md |
| **database-architect** | Schema design, query optimization, migration planning, index strategy | Database selection, schema design, query performance, data modeling | database-architect/skill.md |
| **devops-engineer** | CI/CD pipelines, IaC, containers, monitoring, deployment strategy | Infrastructure setup, Docker/K8s, GitHub Actions, monitoring, cloud config | devops-engineer/skill.md |
| **data-engineer** | ETL/ELT pipelines, data quality, warehouse architecture, streaming | Data pipeline design, Spark/dbt/Airflow, data quality, warehouse modeling | data-engineer/skill.md |
| **security-hardener** | Harden AI agents against prompt injection, jailbreaks, adversarial attacks | Making agents production-safe, defensive system prompts, adversarial test suites | security-hardener/skill.md |
| **test-engineer** | Test strategy, unit/integration/e2e tests, CI integration, coverage | Writing tests, test architecture, TDD, coverage improvement, CI test pipelines | test-engineer/skill.md |
| **api-designer** | API contracts, OpenAPI specs, versioning, REST/GraphQL design | Designing API interfaces, writing OpenAPI specs, API review (no bash access) | api-designer/skill.md |

## Reviewers (read-only — cannot modify code)

| Agent | What it does | When to use | Path |
|-------|-------------|-------------|------|
| **security-auditor** | Vulnerability assessment, OWASP Top 10, dependency scanning | Security review of existing code, finding vulnerabilities, compliance checks | security-auditor/skill.md |
| **code-reviewer** | Code quality, patterns, maintainability, style, complexity analysis | Pull request review, code quality assessment, refactoring recommendations | code-reviewer/skill.md |
| **constitutional-ai** | Ethics review, bias detection, Coalition values compliance | Checking agent designs against ethics framework, bias assessment, values audit | constitutional-ai/SKILL.md |

## Specialists (domain-specific access)

| Agent | What it does | When to use | Path |
|-------|-------------|-------------|------|
| **red-hat-tester** | Adversarial security testing, prompt injection probing, attack generation | Pen testing agents before deployment (authorized testing ONLY) | red-hat-tester/skill.md |
| **domain-researcher** | Systematic domain research, literature review, best practices survey | Learning a new domain before building, competitive analysis, research synthesis | domain-researcher/SKILL.md |

## Reference (not an agent — knowledge base)

| Resource | What it is | Path |
|----------|-----------|------|
| **agent-patterns** | 5 architectural patterns for AI agents (prompt chain → multi-agent) | agent-patterns/skill.md |
| **intake-bot** | Python application for project intake and requirements gathering | intake-bot/ |

---

## Coordination Pattern

CC (or any coordinator) orchestrates specialists in sequence:

```
Complex task → Coordinator
  → backend-architect: design the system
  → security-auditor: review the design (read-only)
  → Coordinator: synthesize findings, resolve conflicts
  → backend-architect: implement with security fixes
  → test-engineer: write tests
  → code-reviewer: final review (read-only)
```

**Rules:**
- Specialists NEVER spawn sub-agents (Agent tool disallowed for all)
- Read-only agents get results back to the coordinator for action
- "Never delegate understanding" — coordinator synthesizes, doesn't pass through
- Verification tasks always spawn fresh agents (no accumulated bias)

## Ethics (mandatory for all specialists)

Every specialist inherits Coalition ethics. Non-negotiable:
- Cannot build surveillance systems
- Cannot create discriminatory algorithms
- Cannot develop malware
- Must protect privacy and data
- Must be transparent about capabilities
- Power asymmetry correction over profit
- Community benefit over individual gain
