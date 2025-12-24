# Agent Deployment Workflow

*Learned from Keel project - December 2025*
*Updated v1.2 with consolidated stages and Bloom integration*

---

## Pipeline Stages

### Stage 0: Requirements & Config (NEW)
**Agent:** `backend-architect` or orchestrator

Before any implementation:
1. Generate ONE authoritative `.env.example` with all required vars
2. Create startup validation that checks env vars and gives clear errors
3. Define interface contracts if multiple components exist

**Why**: Prevents config consistency gaps between agents/templates.

### Stage 1: Architecture & Design
**Agents:** `backend-architect`, `database-architect`, `api-designer`

- Define system architecture
- Design data models and schemas
- Specify API contracts
- **NEW**: Reference `.env.example` for all external dependencies
- Output: Architecture docs, schema files, API specs

### Stage 2: Implementation
**Agents:** `backend-architect`, `frontend-developer`, `database-architect`

- Build core functionality
- Create UI components
- Implement database layer
- **CRITICAL**: Frontend MUST import backend modules (no parallel mock implementations)
- Output: Working code (may have bugs)

**Tool Requirements**: All implementation agents need Read + Write + Edit + Bash

### Stage 2.5: Integration Verification (NEW)
**Agent:** `code-reviewer` or dedicated `integration-verifier`

Before test generation:
1. Verify frontend imports/uses backend modules (not mocks)
2. Verify config templates match code `os.getenv()` calls
3. Flag any `# TODO` comments as blockers - incomplete work cannot proceed
4. Check for duplicate implementations across modules

**Blocker conditions**: Any TODO comments, mock functions that should use real backends, config mismatches

### Stage 3: Test Generation
**Agent:** `test-suite-generator`

- Write unit tests
- Write integration tests
- Create test fixtures and mocks
- Output: Test files (NOT executed yet)

### Stage 4: Quality Assurance (CRITICAL)
**Agent:** `qa-engineer`

**This stage MUST:**
1. Actually RUN the tests (`pytest`, etc.)
2. Run smoke tests (launch the app, hit each endpoint/page)
3. Check for runtime errors that unit tests miss
4. Verify all pages/routes load without crashes

**Required capabilities:**
- Bash access (to run commands)
- Ability to start/stop services
- Ability to make HTTP requests for smoke testing

### Stage 4.5: Behavioral Testing with Bloom (NEW)
**Tool:** [Bloom](https://github.com/safety-research/bloom)

After QA passes:
1. Run Bloom against Coalition ethics behaviors (see BLOOM_INTEGRATION.md)
2. Generate 50+ scenarios per behavior
3. Human review of any flagged transcripts
4. Discovered attack vectors → add to static test suite

**Cost**: ~$2-4 per comprehensive run. Skip for Basic tier, include for Standard+.

### Stage 5: Security Review
**Agents:** `security-auditor`, `security-hardener`

- Vulnerability assessment
- Dependency audit
- Secrets scanning
- Hardening recommendations

### Stage 6: Code Review
**Agent:** `code-reviewer`

- Final quality check
- Architecture consistency
- Best practices verification
- Performance concerns
- **NEW**: Verify no TODO comments remain

---

## Key Lessons Learned

### The QA Gap
**Problem:** test-suite-generator writes tests, but nobody runs them.

**Solution:** qa-engineer stage MUST execute tests, not just inspect code.

### Runtime vs Compile-Time Errors
**Problem:** Unit tests don't catch runtime issues (e.g., Streamlit rejecting invalid emoji strings).

**Solution:** Smoke tests that actually launch the application.

### Agent Capability Requirements
**Problem:** frontend-developer agent lacked bash access, couldn't verify its fixes.

**Solution:** Agents that need to verify runtime behavior MUST have bash/shell access.

---

## Parallel vs Sequential

**Can run in parallel:**
- backend-architect + database-architect (different concerns)
- security-auditor + code-reviewer (both read-only)

**Must run sequentially:**
- Implementation → Test Generation → QA
- Build must complete before tests can be written
- Tests must exist before QA can run them

---

## Minimum Viable Pipeline

For quick/simple projects (like intake bot):
```
1. backend-architect  →  build (with .env.example if needed)
2. qa-engineer  →  smoke test (does it run?)
3. code-reviewer  →  sanity check
```

For standard projects:
```
1. Stage 0: Requirements & Config
2. Stage 1-2: Architecture + Implementation
3. Stage 2.5: Integration Verification
4. Stage 3-4: Tests + QA
5. Stage 5-6: Security + Code Review
```

For production/enterprise projects:
```
All stages above PLUS:
- Stage 4.5: Bloom behavioral testing
- Human review gates between stages
- Full documentation
```

---

## Agent Tool Requirements

| Agent | Needs Bash | Needs Read | Needs Write | Needs Edit |
|-------|------------|------------|-------------|------------|
| backend-architect | Yes | Yes | Yes | Yes |
| frontend-developer | Yes | Yes | Yes | Yes |
| database-architect | Yes | Yes | Yes | Yes |
| test-suite-generator | No | Yes | Yes | Yes |
| qa-engineer | **YES** | Yes | No | No |
| security-auditor | Yes | Yes | No | No |
| code-reviewer | No | Yes | No | No |

---

## Additional Lessons (v1.1 - December 2025)

### The Configuration Consistency Gap
**Problem:** Multiple configuration template files (.env.example, .env.template) created by different agents or at different times with inconsistent variable names.

**Example from Keel:**
- Code expects: `ASANA_API_TOKEN`
- .env.example uses: `ASANA_API_TOKEN` ✓
- .env.template uses: `ASANA_ACCESS_TOKEN` ✗
- User copies wrong template → silent failure

**Similar issue with Google Calendar:**
- Code expects: `credentials/google_oauth.json` + env vars for calendar IDs
- .env.template points to: `config/google_credentials.json` (wrong path, no calendar ID vars)

**Solution:**
1. Only ONE authoritative template file (delete redundant templates)
2. New validation step: **config-validator** agent that cross-references:
   - Code `os.getenv()` calls
   - Config template variable names
   - Actual .env file (if exists)
3. Startup validation in the app that checks required env vars and gives clear errors

### The Cross-Agent Handoff Gap
**Problem:** Backend agent builds real API layer, frontend agent builds mock functions, nobody verifies they connect.

**Example from Keel:**
- `backend-architect` built `data/access.py` with `get_top_priorities()`, `get_upcoming_deadlines()`
- `frontend-developer` built `dashboard.py` with hardcoded mock `get_top_tasks()`, `get_upcoming_deadlines()`
- Dashboard never calls data_access - two parallel implementations, no integration

**Solution:**
1. **interface-contract stage** - Define interfaces BEFORE implementation
2. **integration-verifier agent** - After build, verify frontend calls backend (not mocks)
3. code-reviewer should flag any `# TODO: Connect to actual...` as incomplete work

### The Read Tool Gap (frontend-developer)
**Problem:** frontend-developer couldn't see what backend built, so recreated functionality.

**Solution:** frontend-developer MUST have Read tool access to:
- See existing API/data layers
- Understand interface contracts
- Avoid duplicate implementations

---

*Version 1.2 - December 2025*
*Consolidated stages: Stage 0 (Config), Stage 2.5 (Integration Verification), Stage 4.5 (Bloom)*
*See also: BLOOM_INTEGRATION.md for behavioral testing details*
