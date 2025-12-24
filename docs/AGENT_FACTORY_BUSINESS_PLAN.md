# Agent Factory: Customer Journey & Cost Analysis

Complete workflow from "Hello" to "Here's your receipt" with cost breakdowns for pricing strategy.

## Customer Journey Map

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CUSTOMER JOURNEY                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌────────┐│
│  │  INTAKE  │───▶│ ESTIMATE │───▶│  PAYMENT │───▶│  BUILD   │───▶│DELIVERY││
│  │  CHAT    │    │ + OPTIONS│    │   GATE   │    │ PIPELINE │    │        ││
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘    └────────┘│
│       │               │               │               │               │     │
│       ▼               ▼               ▼               ▼               ▼     │
│   5-15 min        5 min           Stripe/etc      30min-2hr       Email    │
│   Chatbot      Auto-generated    Customer pays   Async build    + Download │
│                                                                             │
│                                        │                                    │
│                                        ▼                                    │
│                              ┌──────────────────┐                           │
│                              │  HUMAN REVIEW    │                           │
│                              │  (if flagged)    │                           │
│                              └──────────────────┘                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Stage 1: Intake Chat

**Purpose**: Gather requirements through hardened conversational interface.

### Flow
1. Customer lands on website
2. Chatbot greets, explains service
3. Guided questionnaire (from agent-builder skill)
4. Captures: purpose, domain, tools, integrations, tone, constraints

### Technical Stack
| Component | Option A (Budget) | Option B (Scale) |
|-----------|-------------------|------------------|
| Frontend | Static site + embedded chat widget | Next.js app |
| Chat UI | Open source (chatbot-ui) | Custom React |
| Hosting | Vercel/Netlify free tier | Vercel Pro |
| LLM | Claude Haiku (fast, cheap) | Claude Sonnet (better understanding) |

### Costs (Per Conversation)
| Model | Avg tokens/conversation | Cost |
|-------|------------------------|------|
| Haiku | ~5,000 in + ~2,000 out | ~$0.006 |
| Sonnet | ~5,000 in + ~2,000 out | ~$0.045 |

**Recommendation**: Haiku for intake. It's just gathering structured requirements.

### Monthly Infrastructure
| Item | Cost |
|------|------|
| Hosting (Vercel free/hobby) | $0-20 |
| Domain | ~$12/year |
| SSL | Free (Let's Encrypt) |
| **Total infrastructure** | **~$20/month** |

---

## Stage 2: Estimate + Options

**Purpose**: Present customer with package options and pricing.

### Flow
1. System analyzes requirements from intake
2. Classifies complexity tier
3. Generates 2-3 package options
4. Presents estimate with feature breakdown

### Complexity Tiers

| Tier | Description | Example | Suggested Price |
|------|-------------|---------|-----------------|
| **Basic** | Single-purpose agent, standard tools, no custom integrations | "A code review helper" | $50-100 |
| **Standard** | Multi-capability, 1-2 custom integrations, hooks | "Customer support bot with CRM integration" | $150-300 |
| **Professional** | Complex workflows, multiple MCPs, custom tools, testing suite | "Full cognitive prosthetic with memory" | $400-800 |
| **Enterprise** | Human consultation, ongoing support, custom training | "Department-wide agent system" | $1000+ (quote) |

### Package Options (Example Output)
```markdown
## Your Agent Estimate: Customer Support Bot

Based on your requirements, here are your options:

### Option A: Essential ($149)
- Core support agent with FAQ handling
- Integration with your helpdesk
- Standard ethical framework
- Basic documentation
- Delivery: 24-48 hours

### Option B: Professional ($299)
- Everything in Essential, plus:
- Escalation logic to human agents
- Sentiment detection
- Custom MCP for your ticket system
- Adversarial testing suite
- Delivery: 48-72 hours

### Option C: Premium ($449)
- Everything in Professional, plus:
- Multi-language support
- Analytics dashboard integration
- Priority human review
- 30-day support for adjustments
- Delivery: 72 hours

[Select Package] [Customize] [Talk to Human]
```

### Cost to Generate Estimate
- LLM call to analyze requirements: ~$0.01 (Haiku)
- Template rendering: negligible
- **Total per estimate**: ~$0.01

---

## Stage 3: Payment Gate

**Purpose**: Secure payment before build begins.

### Technical Stack
| Component | Recommendation | Cost |
|-----------|----------------|------|
| Payment processor | Stripe | 2.9% + $0.30 per transaction |
| Invoicing | Stripe Invoicing | Included |
| Checkout UI | Stripe Checkout (hosted) | Free |

### Payment Flow
1. Customer selects package
2. Redirect to Stripe Checkout
3. Payment successful → webhook triggers build
4. Customer gets confirmation email with order number

### Costs
| Price Point | Stripe Fee | Your Net |
|-------------|------------|----------|
| $100 | $3.20 | $96.80 |
| $200 | $6.10 | $193.90 |
| $300 | $9.00 | $291.00 |
| $500 | $14.80 | $485.20 |

---

## Stage 4: Build Pipeline

**Purpose**: Actually construct the agent.

### Pipeline Stages
```
Requirements → Domain Research → Agent Spec → Security Review → Testing → Package
     │              │                │              │            │          │
     ▼              ▼                ▼              ▼            ▼          ▼
  From intake   WebSearch +      agent-builder   security-   adversarial   Zip file
               domain-researcher    pipeline     hardener    test suite   + docs
```

### Build Process (Automated)
1. **Domain Research** (domain-researcher agent)
   - Web search for best practices
   - Tool ecosystem identification
   - Compliance requirements
   - ~10-20 LLM calls

2. **Spec Generation** (agent-builder agent)
   - Full agent specification
   - System prompt with ethics
   - Tool definitions
   - Example interactions
   - ~15-30 LLM calls

3. **Security Hardening** (security-hardener agent)
   - Review spec for vulnerabilities
   - Add defensive measures
   - Generate adversarial tests
   - ~10-15 LLM calls

4. **Packaging**
   - Compile into skill.md format
   - Generate documentation
   - Create installation guide
   - Bundle test suite

### Build Costs (Per Agent)

Using Claude models:

| Stage | Calls | Model | Tokens (avg) | Cost |
|-------|-------|-------|--------------|------|
| Domain Research | 15 | Sonnet | 50K in, 20K out | ~$0.45 |
| Spec Generation | 25 | Sonnet | 80K in, 40K out | ~$0.90 |
| Security Review | 10 | Sonnet | 30K in, 15K out | ~$0.30 |
| Testing | 20 | Haiku | 40K in, 20K out | ~$0.05 |
| **Total LLM cost** | | | | **~$1.70** |

Add 50% buffer for retries/complexity: **~$2.50 per build**

### Human Review Gate

**When triggered**:
- Enterprise tier (always)
- Flagged by security-hardener (vulnerabilities found)
- Customer requested "Talk to Human"
- Edge case requirements (unusual domain)

**Human Review Costs**:
- Your time: estimate 15-30 min for standard review
- Value your time at: $50-100/hour
- Human review cost: $12.50-50 per reviewed order

**Volume Estimate**:
- 80% of orders: fully automated (no human review)
- 20% of orders: human review needed

---

## Stage 5: Delivery

**Purpose**: Get the agent to the customer.

### Delivery Flow
1. Build complete → Package created
2. Upload to secure storage (S3/equivalent)
3. Generate signed download link (expires 7 days)
4. Email customer with:
   - Download link
   - Installation guide
   - Receipt
   - Support contact

### Delivery Costs
| Item | Cost |
|------|------|
| S3 storage | ~$0.01/agent (tiny files) |
| Email (SendGrid/Postmark) | ~$0.001/email |
| **Total per delivery** | **~$0.01** |

---

## Full Cost Summary (Per Order)

### Basic Tier ($100 order)
| Item | Cost |
|------|------|
| Intake (Haiku) | $0.01 |
| Estimate generation | $0.01 |
| Stripe fee | $3.20 |
| Build (LLM) | $2.50 |
| Delivery | $0.01 |
| **Total cost** | **$5.73** |
| **Gross margin** | **$94.27 (94%)** |

### Standard Tier ($250 order)
| Item | Cost |
|------|------|
| Intake (Haiku) | $0.01 |
| Estimate generation | $0.01 |
| Stripe fee | $7.55 |
| Build (LLM, more complex) | $4.00 |
| Delivery | $0.01 |
| **Total cost** | **$11.58** |
| **Gross margin** | **$238.42 (95%)** |

### Professional Tier ($500 order)
| Item | Cost |
|------|------|
| Intake (Haiku) | $0.01 |
| Estimate generation | $0.01 |
| Stripe fee | $14.80 |
| Build (LLM, complex) | $6.00 |
| Human review (20% chance) | $5.00 avg |
| Delivery | $0.01 |
| **Total cost** | **$25.83** |
| **Gross margin** | **$474.17 (95%)** |

---

## Human-in-the-Loop: Where & When

### Automated (No Human Needed)
- Intake conversation
- Estimate generation
- Payment processing
- Standard builds (Basic/Standard tiers)
- Delivery

### Human Review Required
| Trigger | Reason | Action |
|---------|--------|--------|
| Enterprise tier | High stakes, custom needs | Full review before build |
| Security flags | Hardener found issues | Review and fix |
| Edge case domain | Unusual request | Verify feasibility |
| Customer request | "Talk to human" clicked | Sales/support call |
| Build failure | Automated build errored | Debug and retry |

### Review Queue UI (For You)
```
┌─────────────────────────────────────────────────────────────┐
│ REVIEW QUEUE                                    [3 pending] │
├─────────────────────────────────────────────────────────────┤
│ ⚠️  Order #1042 - Enterprise - Medical Records Agent        │
│     Flagged: HIPAA compliance review needed                 │
│     [Review] [Reject] [Request Info]                        │
├─────────────────────────────────────────────────────────────┤
│ ⚠️  Order #1045 - Standard - Customer flagged               │
│     Flagged: Security hardener found 2 medium issues        │
│     [Review] [Auto-remediate] [Reject]                      │
├─────────────────────────────────────────────────────────────┤
│ 💬  Order #1047 - Contact request                           │
│     Customer wants to discuss custom integration            │
│     [Schedule Call] [Email] [Send FAQ]                      │
└─────────────────────────────────────────────────────────────┘
```

---

## Infrastructure Summary

### Minimum Viable Launch
| Component | Solution | Monthly Cost |
|-----------|----------|--------------|
| Website + Chat | Vercel (free) + embedded widget | $0 |
| LLM API | Anthropic (pay-per-use) | Variable |
| Payments | Stripe | 2.9% + $0.30/tx |
| Email | Postmark/SendGrid free tier | $0 |
| File storage | S3/Cloudflare R2 | ~$1 |
| Domain | Namecheap/Cloudflare | $12/year |
| **Fixed monthly** | | **~$5** |

### Growth Stage
| Component | Solution | Monthly Cost |
|-----------|----------|--------------|
| Website | Vercel Pro | $20 |
| Database | Supabase/PlanetScale free→pro | $0-25 |
| Queue system | Inngest/Trigger.dev | $0-25 |
| Monitoring | Sentry free tier | $0 |
| **Fixed monthly** | | **~$70** |

---

## Pricing Strategy Recommendations

### Cost-Plus Pricing (Safe)
- Calculate true cost (~$5-25 per agent)
- Add desired profit margin (80-90%)
- Results in $50-250 range

### Value-Based Pricing (Better)
- What's the agent worth to the customer?
- A customer support bot saves $1000s/month in labor
- A cognitive prosthetic improves quality of life (priceless)
- Price at fraction of value delivered

### Suggested Price Points
| Tier | Price | Your Cost | Margin | Value Proposition |
|------|-------|-----------|--------|-------------------|
| Basic | $99 | ~$6 | 94% | "Simple agent, fast delivery" |
| Standard | $249 | ~$12 | 95% | "Production-ready with integrations" |
| Professional | $499 | ~$26 | 95% | "Full solution with testing" |
| Enterprise | Custom | Variable | 80%+ | "White glove service" |

---

## Launch Checklist

### Phase 1: MVP (Week 1-2)
- [ ] Landing page explaining service
- [ ] Embedded intake chatbot (hardened)
- [ ] Manual estimate generation (you review)
- [ ] Stripe checkout
- [ ] Manual build process (you run the pipeline)
- [ ] Email delivery

### Phase 2: Automation (Week 3-4)
- [ ] Automated estimate generation
- [ ] Automated build pipeline
- [ ] Review queue for flagged orders
- [ ] Automated delivery

### Phase 3: Scale (Month 2+)
- [ ] Order tracking dashboard for customers
- [ ] Revision/adjustment workflow
- [ ] Referral program
- [ ] Subscription tier for ongoing support

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Jailbroken intake bot | Defense in depth, monitoring, rate limits |
| Build produces bad agent | Security hardener review, adversarial testing |
| Customer unhappy | Clear scope in estimate, revision policy |
| Overwhelming demand | Queue system, auto-scaling, price increases |
| Legal liability | Clear terms of service, no guarantees on agent behavior |

---

## Next Steps

1. **Validate with CC** - Get blessing on commercial use of toolset
2. **Build hardened intake bot** - Using the full security stack
3. **Set up Stripe** - Test checkout flow
4. **Manual pilot** - Run 5-10 orders manually to validate pricing/process
5. **Automate** - Build out the pipeline as volume justifies

---

*"The best business is one where you get paid to do what you'd do anyway."*
