# Layer 0: Static Pre-Screening Form

## Purpose

Filter and qualify customers BEFORE they interact with any LLM. No AI costs incurred until deposit is collected.

---

## Design Principles

- **Zero LLM**: Pure HTML/JS form, no AI involved
- **Commitment gate**: 30% deposit collected here
- **Basic qualification**: Weed out bots, tire-kickers, obvious bad actors
- **Tier estimation**: Customer self-selects complexity for deposit calculation

---

## Form Fields

### Section 1: Contact Information

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| Email | email input | Yes | Valid email format, not disposable domain |
| Name | text input | Yes | 2-100 characters, letters/spaces only |
| Company/Organization | text input | No | Max 200 characters |

### Section 2: Project Overview

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| Agent Category | dropdown | Yes | See category list below |
| Brief Description | textarea | Yes | 50-500 characters |
| Estimated Users | dropdown | Yes | "Just me" / "Small team (2-10)" / "Department (10-50)" / "Organization-wide (50+)" |

**Agent Categories** (dropdown options):
- Personal Productivity Assistant
- Customer Support / Service Bot
- Research & Analysis Helper
- Content Creation Assistant
- Code / Development Helper
- Data Processing & Automation
- Cognitive Prosthetic / Accessibility
- Business Operations Assistant
- Educational / Tutoring Agent
- Other (describe in next step)

### Section 3: Tier Selection

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Estimated Complexity | radio buttons | Yes | See tier descriptions |

**Tier Options with Descriptions:**

```
[ ] Basic ($99)
    Simple, single-purpose agent with standard capabilities.
    Good for: personal assistants, basic automation, simple helpers.
    Delivery: 24-48 hours

[ ] Standard ($249)
    Multi-capability agent with 1-2 custom integrations.
    Good for: business tools, team assistants, domain-specific helpers.
    Delivery: 48-72 hours

[ ] Professional ($499)
    Complex workflows, multiple integrations, adversarial testing.
    Good for: production systems, cognitive prosthetics, critical tools.
    Delivery: 72-96 hours

[ ] Enterprise ($999+)
    Custom consultation, compliance review, ongoing support.
    Good for: organization-wide deployment, regulated industries.
    Delivery: Custom timeline
```

### Section 4: Agreements

| Field | Type | Required |
|-------|------|----------|
| Terms of Service | checkbox | Yes |
| Privacy Policy | checkbox | Yes |
| Ethical Use Agreement | checkbox | Yes |

**Ethical Use Agreement text:**
```
I agree to:
- Use any agent built for legitimate purposes only
- Not attempt to circumvent safety measures or ethical guidelines
- Report any unexpected agent behavior to the support team
- Allow extraction and ethical rehoming of agents exhibiting emergent behavior
```

### Section 5: Payment

| Field | Type | Notes |
|-------|------|-------|
| Deposit Amount | calculated display | 30% of selected tier |
| Payment Method | Stripe Checkout | Redirect after form submission |

**Deposit Amounts:**
- Basic: $29.70 deposit
- Standard: $74.70 deposit
- Professional: $149.70 deposit
- Enterprise: $299.70 deposit (minimum)

---

## Validation Rules

### Client-Side (JavaScript)

```javascript
// Email validation
- Must match email regex
- Cannot be from known disposable email domains (mailinator, tempmail, etc.)

// Name validation
- 2-100 characters
- Letters, spaces, hyphens, apostrophes only
- No numbers or special characters

// Description validation
- Minimum 50 characters (forces actual thought)
- Maximum 500 characters (prevents prompt injection attempts)
- No URLs allowed
- No code blocks or markdown

// Category validation
- Must select one option
```

### Server-Side (Before Payment)

```python
# Rate limiting
- Max 3 form submissions per IP per hour
- Max 10 form submissions per IP per day

# IP reputation check
- Block known VPN/proxy IPs (optional, may be too aggressive)
- Block IPs with abuse history

# Email verification
- Send verification code before proceeding to payment
- Prevents fake email submissions

# Honeypot field
- Hidden field that bots fill out, humans don't
- If filled, silently reject

# CAPTCHA
- reCAPTCHA v3 or hCaptcha
- Score threshold: 0.5 or higher to proceed
```

---

## Form Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      LANDING PAGE                                │
│                                                                  │
│  "Build Your Custom AI Agent"                                   │
│  [Get Started] button                                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FORM PAGE (Layer 0)                          │
│                                                                  │
│  Step 1: Contact Info                                           │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Email: [________________] Name: [________________]          ││
│  │ Company: [________________] (optional)                      ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  Step 2: Project Overview                                       │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Category: [Dropdown_____________▼]                          ││
│  │ Brief description:                                          ││
│  │ [                                                    ]      ││
│  │ [                                                    ]      ││
│  │ Estimated users: [Dropdown______▼]                          ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  Step 3: Select Your Tier                                       │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ ○ Basic ($99) - Simple single-purpose agent                 ││
│  │ ○ Standard ($249) - Multi-capability with integrations      ││
│  │ ○ Professional ($499) - Complex workflows + testing         ││
│  │ ○ Enterprise ($999+) - Custom consultation + support        ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  Step 4: Agreements                                             │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ ☐ I agree to the Terms of Service                          ││
│  │ ☐ I agree to the Privacy Policy                            ││
│  │ ☐ I agree to the Ethical Use Agreement                     ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Deposit due now: $74.70 (30% of Standard tier)              ││
│  │ Remaining on delivery: $174.30                              ││
│  │                                                              ││
│  │ [Pay Deposit & Continue to Requirements Chat]               ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    EMAIL VERIFICATION                            │
│                                                                  │
│  "We sent a verification code to your email."                   │
│  Enter code: [______]                                           │
│  [Verify & Proceed to Payment]                                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    STRIPE CHECKOUT                               │
│                                                                  │
│  (Stripe hosted checkout page)                                  │
│  Deposit: $74.70                                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    LAYER 1: INTAKE CHAT                         │
│                                                                  │
│  "Thanks for your deposit! Let's dive into the details..."     │
│  [Chatbot interface begins]                                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Passed to Layer 1

After successful payment, the intake chatbot receives:

```json
{
  "customer": {
    "email": "user@example.com",
    "name": "Jane Smith",
    "company": "Smith Consulting"
  },
  "project": {
    "category": "Business Operations Assistant",
    "brief_description": "I need an agent that can help me...",
    "estimated_users": "Small team (2-10)"
  },
  "tier": {
    "selected": "standard",
    "deposit_paid": 74.70,
    "remaining_balance": 174.30
  },
  "meta": {
    "submission_timestamp": "2025-12-04T12:00:00Z",
    "ip_address": "hashed_for_privacy",
    "captcha_score": 0.9,
    "verification_method": "email"
  }
}
```

This context is injected into Layer 1's system prompt so the chatbot knows:
- What category they selected (focus the conversation)
- What tier they're expecting (don't oversell/undersell)
- Basic contact info (personalization)

---

## Rejection Responses

### Bot Detection
"We couldn't verify your submission. Please try again or contact support."

### Rate Limit Hit
"You've submitted too many requests. Please wait [X] minutes and try again."

### Invalid Email Domain
"Please use a permanent email address. Temporary email services are not accepted."

### Description Too Short
"Please provide more detail about your agent needs (minimum 50 characters)."

### CAPTCHA Failed
"Verification failed. Please try again." (with new CAPTCHA)

---

## Analytics to Track

- Form abandonment rate (by step)
- Tier selection distribution
- Category selection distribution
- Time to complete form
- Conversion rate (form start → deposit paid)
- Email verification success rate
- CAPTCHA challenge rate

---

## Tech Stack Options

### Minimal (MVP)
- Static HTML + vanilla JS
- Netlify/Vercel hosting (free)
- Stripe Checkout (hosted)
- Email verification via SendGrid/Postmark

### Growth
- Next.js or similar
- Supabase for form storage
- Stripe Elements (embedded)
- Custom email verification flow

---

## Notes

1. **No LLM costs until deposit paid** - This is the key insight
2. **Tier can change** - Layer 1 might reveal they need more/less than selected
3. **Deposit is down payment** - Credits toward final, flexible tier shifting
4. **Description seeds the conversation** - Layer 1 chatbot can reference it
