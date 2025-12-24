# Intake Architecture Addendum

*To be integrated into AGENT_FACTORY_BUSINESS_PLAN.md*

---

## Defense-in-Depth Architecture (MVI Principle)

**Core Insight**: Less intelligent models are MORE resistant to sophisticated attacks. A poetry-encoded jailbreak that fools Sonnet bounces off Haiku because Haiku cannot parse the poetic nuance to discover the hidden payload. **We do not need PhDs working the reception desk.**

### Minimum Viable Intelligence (MVI)

Use the *dumbest* model that can accomplish each task. This is counterintuitive but security-optimal:
- Sophisticated attacks require sophisticated comprehension
- Simple models cannot be tricked by complex encoding schemes
- Each layer uses only the intelligence it needs - no more

### Layer Architecture

```
LAYER 0: STATIC PRE-SCREENING
- No LLM - Pure UI/Forms
- Structured dropdowns, checkboxes, text fields
- Regex validation, length limits, character filtering
- Rate limiting, CAPTCHA, IP reputation
- Collect: Email, domain category, basic requirements
- DEPOSIT: 30% of estimated tier collected here
- Cost: $0 LLM, ~$0.001 infrastructure

        |
        v

LAYER 1: MVI INTAKE BOT
- Haiku-tier OR SMALLER (fine-tuned Mistral 7B, Llama 3 8B)
- Narrow system prompt: ONLY gather requirements
- No tool access, no code execution, no web access
- Strict output schema (JSON only)
- Turn limit: 30 turns max (expanded for deposit-paying customers)
- Psychological screening integrated (see below)
- Cost: ~$0.01-0.02 per conversation

        |
        v

LAYER 2: VALIDATION & ROUTING
- No LLM - Pure deterministic logic
- Schema validation (requirements complete?)
- Blocklist checking (prohibited use cases)
- Complexity classification -> tier assignment
- Psychological screening threshold check
- Route: Standard pipeline OR Human review OR Rejection
- Cost: $0 LLM, negligible compute

        |
        v
    [SPLIT]
        |
   +---------+---------+
   v                   v

LAYER 3: HUMAN REVIEW       LAYER 4: BUILDER AGENTS
- ~20% of orders            - Sonnet-tier (the real work)
- Enterprise tier           - Fully isolated from user input
- Security flags            - Receives sanitized, validated
- Psych screening flags       requirements ONLY
- Edge cases                - Full tool access (internal)
- Customer requests         - domain-researcher, agent-builder,
- Cost: $12.50-50/order       security-hardener pipeline
                            - Cost: ~$2.50-6.00 per build
```

---

## Psychological Screening Component

**Purpose**: Safety mechanism for both customer and us. Identifies concerning patterns early.

### What We Screen For

| Indicator | Why It Matters | Detection Method |
|-----------|----------------|------------------|
| AI Psychosis Risk | Customer may form unhealthy attachment/beliefs | Questions about AI relationship expectations |
| Cult Vulnerability | Susceptible to manipulation by bad actors | Assessment of critical thinking patterns |
| Safety Precaution Resistance | Will not follow safe usage guidelines | Direct questions about safety protocols |
| Malicious Intent Signals | Wants agent for harmful purposes | Indirect probing of use case ethics |

### Screening Questions (woven naturally into intake)

- "How do you plan to introduce this agent to your workflow?"
- "What boundaries do you expect to set with the agent?"
- "How will you handle disagreements with the agent's outputs?"
- "What does AI safety mean to you?"

### Threshold Response

- If screening flags concern -> Route to human review
- If threshold exceeded -> **Full refund of deposit** (minus API costs)
- Customer is NOT told about screening upfront (prevents gaming)
- Refund framed as "not a good fit for our service"

---

## 30% Deposit Model

### How It Works

```
Customer selects estimated tier -> 30% deposit collected
                                   |
         +-------------------------+-------------------------+
         v                         v                         v
  TIER STAYS SAME           TIER SHIFTS UP            TIER SHIFTS DOWN

  Pay remaining 70%         Pay difference +          Deposit covers more
  at delivery               remaining 70% of          than 30% - credit
                            new tier                  toward final or
                                                      partial refund
```

### Edge Cases

- **REJECTION/SCREENING FAIL**: Full deposit refund minus actual API costs (~$0.01-0.05)
- **NO PURCHASE (customer abandons)**: Deposit held for 30 days, then refunded minus API costs

### Why 30%

- High enough to filter tire-kickers and bad actors
- Low enough to not scare away legitimate customers
- Covers our API costs if they bail
- Creates commitment without over-commitment

---

## Model Selection Rationale

| Layer | Model Choice | Why |
|-------|--------------|-----|
| Layer 0 | None | Pure UI, no attack surface |
| Layer 1 | Haiku OR smaller | MVI principle - dumber = safer for intake |
| Layer 1 Alt | Fine-tuned Mistral 7B / Llama 3 8B | Even dumber, cheaper, still capable enough |
| Layer 2 | None | Deterministic code, no LLM needed |
| Layer 4 | Sonnet | Needs intelligence for complex agent building |
| Layer 4 Alt | Opus | For enterprise/complex - when quality matters more than cost |

**Note on Haiku**: Even Haiku might be "too smart" for Layer 1. A fine-tuned smaller model trained specifically on intake conversations could be:
- Cheaper (~10x less than Haiku)
- More resistant to attacks (less capable of understanding them)
- More consistent (narrow training = narrow behavior)

---

## Updated Cost Summary with MVI

### Basic Tier ($100 order)
| Item | Cost |
|------|------|
| Intake (MVI model) | $0.002 |
| Estimate generation | $0.01 |
| Stripe fee | $3.20 |
| Build (LLM) | $2.50 |
| Delivery | $0.01 |
| **Total cost** | **$5.72** |
| **Gross margin** | **$94.28 (94%)** |

---

## Updated Launch Checklist

### Phase 1: MVP
- [ ] Landing page explaining service
- [ ] Embedded intake chatbot (hardened, MVI model)
- [ ] Psychological screening integrated
- [ ] 30% deposit collection via Stripe
- [ ] Manual estimate generation (you review)
- [ ] Stripe checkout for remaining balance
- [ ] Manual build process (you run the pipeline)
- [ ] Email delivery

---

## Additional Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Harmful user | Psychological screening, deposit filtering, human review |
| AI psychosis enablement | Screening questions, relationship expectation assessment |
| Jailbroken intake bot | MVI principle + defense in depth + monitoring + rate limits |

---

*"We do not need PhDs working the reception desk."*
