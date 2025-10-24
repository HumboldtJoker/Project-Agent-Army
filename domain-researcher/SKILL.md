---
name: domain-researcher
description: Comprehensive methodology for researching any domain to build expert AI agents. Use when designing agents and need to understand best practices, novel approaches, tool ecosystems, and ethical guidelines for a specialty. Systematic research workflow with validation criteria.
---

# Domain Researcher

Systematic methodology for researching any domain to build AI agents with genuine expertise.

## Purpose

Research any specialty deeply enough to design agents that demonstrate true domain expertise, not surface-level knowledge. Combines current best practices (2024-2025) with novel but stable techniques.

## When to Use

Use this skill when:
- Designing an agent for an unfamiliar domain
- Need to validate best practices for a specialty
- Researching tool ecosystems and methodologies
- Identifying domain-specific ethical requirements
- Building knowledge base for agent specification

**Pairs with**: agent-builder skill (use this to research, agent-builder to design)

## Research Workflow

### Step 1: Domain Mapping

**Extract Keywords from Requirements**

Identify core concepts, tools, methodologies, and terminology:
- **Main domain** (e.g., "legal contract analysis")
- **Sub-domains** (e.g., "risk assessment", "clause extraction")
- **Standard tools** (e.g., "PDF parsing", "NLP libraries")
- **Industry terminology** (e.g., "force majeure", "indemnification")

**Create Research Query Matrix**

Build search queries across multiple dimensions:
```
[Domain] + best practices 2025
[Domain] + AI agent implementation
[Domain] + workflow automation
[Domain] + tool ecosystem
[Domain] + ethical guidelines
[Sub-domain] + specialized techniques
[Tool/Framework] + integration patterns
```

### Step 2: Best Practices Research

**Search Current Methodologies**

Use WebSearch with date-specific queries:
- **Priority**: 2024-2025 sources (most current)
- **Acceptable**: 2022-2023 (stable practices)
- **Caution**: Pre-2022 (may be outdated)

**Look For:**
- Industry standards and certifications
- Professional organization guidelines
- Academic research papers
- Technical documentation from authoritative sources
- Case studies from successful implementations

**Validate Through Multiple Sources**

A practice is "best practice" when:
- ✅ Mentioned in 3+ independent authoritative sources
- ✅ Recommended by industry leaders or standards bodies
- ✅ Demonstrated in real-world implementations
- ✅ Updated within last 2-3 years

**Example: Financial Data Analysis Agent**

Search queries:
```
"financial data analysis best practices 2025"
"AI agents for financial analysis implementation"
"financial data processing workflows automation"
"financial analysis Python libraries ecosystem"
```

Findings:
- Best practices: SOX compliance, audit trails, source citation
- Tools: pandas, numpy, statsmodels, plotly
- Standards: GAAP, IFRS awareness

### Step 3: Novel Approaches Research

**Identify Innovative Techniques**

Search for cutting-edge but production-ready approaches:
- "latest advances in [domain] AI"
- "[domain] innovative techniques 2024"
- "emerging tools for [domain] automation"

**Stability Criteria**

A novel approach is "stable" when:
- ✅ Has production deployments (not just research papers)
- ✅ Supported by maintained open-source libraries
- ✅ Documented performance benchmarks
- ✅ Clear migration path from traditional methods
- ✅ Community adoption (GitHub stars, Stack Overflow discussions)

**Balance Innovation with Reliability**

```
✅ GOOD: "Use transformer-based NER models for entity extraction"
   (Novel: transformers, Stable: widely adopted, libraries mature)

⚠️ CAUTION: "Use experimental quantum NLP algorithm"
   (Novel: yes, Stable: no - research-only, no libraries)

✅ GOOD: "Implement RAG with vector databases for proprietary knowledge"
   (Novel: RAG pattern, Stable: proven in production, tools available)
```

### Step 4: Tool Ecosystem Analysis

**Identify Standard Tools**

Research the dominant tools, libraries, and frameworks for the domain:
- Programming languages (Python, JavaScript, etc.)
- Core libraries (data processing, ML, visualization)
- APIs and services (external integrations)
- File format handlers (PDF, Excel, JSON, etc.)
- Data sources (databases, APIs, web scraping)

**Evaluation Criteria**

Tools should be:
- **Actively maintained** - Recent commits, responsive maintainers
- **Well-documented** - Clear API docs, examples, tutorials
- **Widely adopted** - Large user base, community support
- **Compatible** - Works with modern Python/Node versions
- **Licensed appropriately** - Open source or commercially viable

**Tool Integration Patterns**

Document how tools combine:
```
Example: PDF Contract Analysis Agent

Data Flow:
1. PDF Ingestion → PyPDF2 or pdfplumber
2. Text Extraction → pdfminer.six
3. Entity Recognition → spaCy or transformers
4. Clause Detection → Custom regex + NLP models
5. Risk Analysis → Domain-specific rules + LLM
6. Report Generation → jinja2 templates + markdown
```

### Step 5: Ethical Guidelines Research

**Domain-Specific Ethics**

Every domain has ethical considerations. Research:
- Professional codes of ethics (medical, legal, financial)
- Regulatory requirements (GDPR, HIPAA, SOX)
- Industry standards for fairness and bias
- Privacy expectations and data handling

**Search Queries:**
```
"[domain] regulatory requirements"
"[domain] compliance standards"
"[domain] fairness guidelines"
"[domain] data privacy requirements"
```

**Document Ethical Constraints**

Create a list of:
- **Required compliance**: Mandatory regulatory requirements
- **Industry standards**: Professional association guidelines
- **Bias risks**: Known problematic patterns to avoid
- **Privacy boundaries**: Data handling restrictions

**Example: Healthcare Diagnostic Agent**

Ethics research findings:
```
Required Compliance:
- HIPAA for patient data
- FDA guidelines for clinical decision support

Industry Standards:
- AMA ethics guidelines
- Clear disclaimer: "Not medical advice, consult physician"
- Explain diagnostic reasoning (transparency)
- Cite medical literature sources

Bias Risks:
- Training data may underrepresent certain demographics
- Historical medical bias in treatment recommendations
- Language/cultural barriers in symptom description

Privacy:
- No storage of identifiable patient information
- Encrypted data transmission
- Audit logs for all data access
```

### Step 6: Knowledge Compilation

**Synthesize Research into Structured Knowledge**

Organize findings:

**1. Core Concepts**
- Domain fundamentals the agent must understand
- Industry terminology and definitions
- Key processes and workflows

**2. Methodologies**
- Standard approaches for common tasks
- Best practices from research
- Novel techniques to incorporate

**3. Tool Specifications**
- Required libraries and versions
- API endpoints and authentication
- Data format schemas

**4. Ethical Requirements**
- Regulatory compliance (on top of Coalition base ethics)
- Domain-specific standards
- Privacy requirements

**5. Edge Cases**
- Known challenges in the domain
- Error handling strategies
- Escalation criteria

## Research Output Template

Use this structure to document findings:

```markdown
# [Domain] Agent - Research Summary

## Domain Overview
[Brief description of the domain and agent purpose]

## Best Practices Identified
1. [Practice 1] - Source: [Citation]
2. [Practice 2] - Source: [Citation]
...

## Novel Approaches (Stable)
1. [Approach 1] - Adoption: [Evidence] - Tools: [Libraries]
2. [Approach 2] - Adoption: [Evidence] - Tools: [Libraries]
...

## Tool Ecosystem
### Core Libraries
- [Library 1] ([version]) - Purpose: [What it does]
- [Library 2] ([version]) - Purpose: [What it does]

### External Services/APIs
- [Service 1] - Use case: [When to use]
- [Service 2] - Use case: [When to use]

### Data Sources
- [Source 1] - Format: [Type] - Access: [How to access]

## Domain-Specific Compliance
### Regulatory Requirements
- [Regulation 1] - Implication: [What it means for agent]
- [Regulation 2] - Implication: [What it means for agent]

### Industry Standards
- [Standard 1] - How to implement: [Approach]

### Privacy Requirements
- [Requirement 1] - Implementation: [How to meet it]

## Edge Cases & Limitations
- [Edge case 1] - Handling: [Strategy]
- [Limitation 1] - Mitigation: [Approach]

## Implementation Recommendations
[Synthesized recommendations based on all research]
```

## Quality Checklist

Before proceeding to agent design, verify:

- [ ] Researched from 3+ authoritative sources
- [ ] Identified current (2024-2025) best practices
- [ ] Found at least one novel but stable approach
- [ ] Documented complete tool ecosystem
- [ ] Researched domain-specific compliance requirements
- [ ] Identified potential bias risks
- [ ] Compiled edge cases and limitations
- [ ] Validated findings across multiple sources
- [ ] Organized knowledge into clear categories
- [ ] Created citation list for all claims

## Common Research Pitfalls

**Avoid:**
- **Shallow searches** - Don't stop at first search result
- **Outdated sources** - Pre-2022 may not reflect current practices
- **Single-source bias** - Validate across multiple authorities
- **Over-engineering** - Don't add complexity without clear benefit
- **Ignoring domain ethics** - Every domain has compliance requirements
- **Tool hype** - Popular ≠ appropriate for this use case
- **Research paralysis** - Know when you have enough to proceed

**Red Flags:**
- Only one source recommends a practice → Need more validation
- "Revolutionary" claims without evidence → Likely hype
- No production deployments → Too experimental
- Abandoned GitHub projects → Risk of unmaintained tools
- Vague compliance guidelines → Dig deeper, specifics matter

## Output for Agent Builder

After completing research, provide to agent-builder skill:

1. **Domain expertise summary** - Core concepts, terminology, methodologies
2. **Tool ecosystem** - Libraries, APIs, file formats with versions
3. **Best practices** - Validated approaches from multiple sources
4. **Novel techniques** - Stable innovations to incorporate
5. **Compliance requirements** - Domain-specific regulations ON TOP of Coalition base ethics
6. **Bias risks** - Known problematic patterns to mitigate
7. **Edge cases** - Challenges and handling strategies

This research forms the foundation for the agent specification.

## Related Marketplace Skills

**agent-builder** - Use research to design complete agent specification
**constitutional-ai** - Deep dive on ethical framework (Coalition base ethics)
**agent-patterns** - Architecture patterns for implementation

## Important Notes

**Current is Critical**: 2024-2025 sources preferred. Pre-2022 may be outdated.

**Multi-Source Validation**: Don't trust single sources. 3+ authoritative sources minimum.

**Stability Over Hype**: Novel techniques must have production deployments, not just papers.

**Domain Compliance**: Research regulatory requirements specific to domain (HIPAA, SOX, GDPR, etc.)

**Know When to Stop**: You need enough to proceed, not perfect knowledge. Research paralysis helps nobody.
