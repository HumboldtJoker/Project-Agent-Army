---
name: agent-patterns
description: Research-backed architectural patterns for AI agents (2024-2026). Nine core patterns from deterministic to autonomous. Includes 2026 additions — dynamic workflow scripting, fan-out/merge, generator-evaluator loops, multi-agent debate. MCP-first tool integration, security baseline, and the "single agent wins 64%" rule.
---

# Agent Design Patterns

Research-backed architectural patterns for building effective AI agents. Updated June 2026 with production-validated patterns from Anthropic, Claude Code, and industry leaders.

## Design Philosophy

**Start Simple**: Begin with the simplest pattern that solves the problem. Add complexity only when clearly beneficial.

**The 64% Rule (2026)**: A single well-equipped agent outperforms multi-agent setups on 64% of benchmarked tasks. Reach for multi-agent patterns ONLY when tasks are parallelizable, exceed context limits, or need adversarial verification. Multi-agent cost blowup is real — $0.50 test runs can hit $50k/month at 100K executions.

**Autonomy Spectrum**:
```
Deterministic → Single-Agent → Fan-Out → Multi-Agent → Dynamic Workflow
  (Cheapest)      (Sweet spot)   (Parallel)  (Complex)    (Most powerful)
  (Fastest)       (Balanced)     (Fast)      (Slowest)    (Self-orchestrating)
  (Easiest debug) (Moderate)     (Moderate)  (Hardest)    (Observable)
```

**MCP-First**: Tools should be MCP servers when possible. MCP provides standard discovery, authentication, and sandboxing. Build tool servers, not one-off function definitions.

## Core Patterns

### Pattern 1: Prompt Chain (Deterministic)

**When to Use**: You know the exact sequence of steps required.

**Architecture**:
```
Input → [Step 1] → [Step 2] → [Step 3] → Output
         ↓           ↓           ↓
      LLM Call    LLM Call    LLM Call
```

**Characteristics**:
- Fixed workflow, no branching
- Each step always executes in order
- Simplest to debug
- Fastest execution
- Lowest cost

**Example**: Document summarization pipeline
```
1. Extract text from PDF
2. Chunk text into sections
3. Summarize each section
4. Combine summaries into executive summary
```

**Implementation**:
```python
def document_summarization_chain(pdf_path):
    # Step 1: Extract
    text = extract_text_from_pdf(pdf_path)

    # Step 2: Chunk
    chunks = chunk_text(text, max_tokens=2000)

    # Step 3: Summarize sections
    section_summaries = [
        llm_call(f"Summarize this section:\n{chunk}")
        for chunk in chunks
    ]

    # Step 4: Combine
    final_summary = llm_call(
        f"Combine these summaries into executive summary:\n"
        f"{'\n'.join(section_summaries)}"
    )

    return final_summary
```

**Pros**:
- Predictable behavior
- Easy to test and debug
- Fast execution
- Low token cost

**Cons**:
- Can't handle variations in input
- No dynamic decision-making
- Over-processes simple inputs

**When NOT to Use**: When different inputs require different workflows.

### Pattern 2: Routing (Single Decision Point)

**When to Use**: Different inputs require different specialized workflows.

**Architecture**:
```
                    Input
                      ↓
               [Router Agent]
                 ↓    ↓    ↓
           Path A  Path B  Path C
              ↓       ↓       ↓
          Expert1  Expert2  Expert3
              ↓       ↓       ↓
                  Output
```

**Characteristics**:
- One decision point at the beginning
- Routes to specialized sub-workflows
- Each path is deterministic after routing
- Improves efficiency vs one-size-fits-all

**Example**: Customer support ticket routing
```
Ticket → Router → Technical issue → Technical specialist
                → Billing issue → Billing specialist
                → General question → FAQ lookup
```

**Implementation**:
```python
def route_ticket(ticket_text):
    # Router makes ONE decision
    category = llm_call(
        f"Classify this ticket as [technical|billing|general]:\n{ticket_text}"
    )

    # Route to specialized handler
    if category == "technical":
        return handle_technical_ticket(ticket_text)
    elif category == "billing":
        return handle_billing_ticket(ticket_text)
    else:
        return lookup_faq(ticket_text)
```

**Pros**:
- Efficient (use smaller models for simple paths)
- Specialized expertise per path
- Clear separation of concerns
- Still relatively easy to debug

**Cons**:
- Router must be accurate
- Can't handle multi-category issues
- Adding new categories requires code changes

**Optimization**: Use smaller/faster models for simple routes, larger models only for complex routes.

### Pattern 3: Tool-Calling Agent (Adaptive Workflow)

**When to Use**: Agent needs to decide which tools to use and when.

**Architecture**:
```
Input → [Agent] → Tool 1
          ↓  ↑      Tool 2
       Decide ←    Tool 3
          ↓          ...
       Output
```

**Characteristics**:
- Agent called repeatedly in loop
- Each iteration: agent decides which tool to call (if any)
- Tools execute and return results
- Loop continues until agent has enough information

**Example**: Data analysis agent
```
Tools:
- load_dataset(path)
- get_column_stats(column)
- plot_distribution(column)
- run_correlation(col1, col2)

Flow:
User: "Analyze sales data"
Agent: Use load_dataset("sales.csv")
Agent: Use get_column_stats("revenue")
Agent: Use plot_distribution("revenue")
Agent: "Revenue shows normal distribution, mean $45K, std dev $12K"
```

**Implementation**:
```python
def tool_calling_agent(user_query, tools, max_iterations=10):
    context = {"query": user_query, "observations": []}

    for i in range(max_iterations):
        # Agent decides: which tool to call OR finish
        decision = llm_call_with_tools(
            prompt=f"Query: {user_query}\nContext: {context}",
            available_tools=tools
        )

        if decision.type == "finish":
            return decision.response

        # Execute tool
        tool_result = execute_tool(decision.tool, decision.args)
        context["observations"].append({
            "tool": decision.tool,
            "result": tool_result
        })

    return "Max iterations reached"
```

**Pros**:
- Flexible, adapts to different queries
- Can combine tools in novel ways
- Handles complex multi-step tasks

**Cons**:
- Slower (multiple LLM calls)
- More expensive (more tokens)
- Harder to debug (non-deterministic)
- Can get stuck in loops

**Best Practices**:
- Limit max iterations (prevent infinite loops)
- Provide clear tool descriptions
- Include examples in tool docs
- Implement circuit breakers (detect loops)

### Pattern 4: Retrieval-Augmented Generation (RAG)

**When to Use**: Agent needs access to proprietary or updated knowledge.

**Architecture**:
```
User Query
    ↓
[Embed Query] → Vector DB Search → Relevant Docs
    ↓                                    ↓
[LLM: Query + Retrieved Context] → Answer
```

**Characteristics**:
- Agent doesn't have all knowledge built-in
- Retrieves relevant information dynamically
- Grounds responses in retrieved documents
- Reduces hallucination

**Example**: Company policy Q&A
```
Query: "What is our vacation policy?"
  ↓
Embed: [0.23, 0.87, ...] (vector)
  ↓
Search Vector DB: Find similar docs
  ↓
Retrieved: "HR Handbook Section 4.2: Vacation Policy..."
  ↓
LLM: "Based on HR Handbook Section 4.2, employees receive..."
```

**Implementation**:
```python
def rag_agent(query, vector_db):
    # Embed query
    query_embedding = embed(query)

    # Retrieve relevant docs
    relevant_docs = vector_db.search(
        query_embedding,
        top_k=5
    )

    # Augment query with context
    context = "\n\n".join([doc.content for doc in relevant_docs])

    # Generate answer
    answer = llm_call(
        f"Context:\n{context}\n\nQuestion: {query}\n\n"
        f"Answer based on the context above:"
    )

    return {
        "answer": answer,
        "sources": [doc.metadata for doc in relevant_docs]
    }
```

**Pros**:
- Access to up-to-date information
- Grounds answers in sources (reduces hallucination)
- Can cite sources for transparency
- Scalable knowledge base

**Cons**:
- Requires vector database setup
- Retrieval quality critical (bad retrieval = bad answer)
- Slower (embedding + search + generation)
- More infrastructure complexity

**Best Practices**:
- Chunk documents appropriately (not too large/small)
- Use metadata filtering (e.g., "only HR docs")
- Return sources for user verification
- Re-rank results for better relevance
- Handle "no relevant docs found" gracefully

### Pattern 5: Orchestrator + Specialists (Multi-Agent)

**When to Use**: Complex task requiring multiple specialized agents.

**Architecture**:
```
           User Query
                ↓
         [Orchestrator]
          ↓    ↓    ↓
      Agent1 Agent2 Agent3
      (Research) (Analysis) (Writing)
          ↓    ↓    ↓
         [Orchestrator]
        (Synthesizes results)
                ↓
             Output
```

**Characteristics**:
- Orchestrator coordinates specialized agents
- Each specialist has narrow, deep expertise
- Orchestrator decides: which agents to use, in what order
- Can run agents in parallel or sequentially

**Example**: Market research pipeline
```
Orchestrator delegates:
- Research Agent: Gather competitor data
- Analysis Agent: Identify trends and patterns
- Writing Agent: Compile executive report

Orchestrator synthesizes: Final report
```

**Implementation**:
```python
class Orchestrator:
    def __init__(self, specialist_agents):
        self.agents = specialist_agents

    def execute(self, task):
        # Plan: which agents needed, in what order
        plan = self.create_plan(task)

        results = {}
        for step in plan:
            agent = self.agents[step.agent_name]

            # Execute agent task
            result = agent.execute(step.subtask, context=results)
            results[step.agent_name] = result

        # Synthesize final output
        return self.synthesize(results, task)

    def create_plan(self, task):
        # LLM decides which agents to use
        return llm_call(
            f"Task: {task}\nAvailable agents: {self.agents.keys()}\n"
            f"Create execution plan:"
        )
```

**Pros**:
- Each agent highly specialized
- Can run agents in parallel (faster)
- Scales to very complex tasks
- Modular (easy to add new specialists)

**Cons**:
- Most complex pattern
- Hardest to debug (10-50+ LLM calls)
- Highest cost and latency
- Orchestrator complexity

**Best Practices**:
- Use ONLY when single-agent insufficient
- Clearly define each specialist's scope
- Implement communication protocol between agents
- Log all agent interactions for debugging
- Test specialists independently first

**When NOT to Use**: Unless you've proven simpler patterns insufficient.

### Pattern 6: Fan-Out/Merge (Parallel with LLM Synthesis) [2026]

**When to Use**: Task decomposes into independent subtasks that can run in parallel, with results synthesized by an LLM.

**Architecture**:
```
Input → [Dispatcher] → Agent1 ─┐
                    → Agent2 ─┤→ [Collector/Synthesizer] → Output
                    → Agent3 ─┘
```

**Example**: Code review across dimensions
```
PR Diff → Dispatcher → Bug Finder    ─┐
                     → Perf Reviewer  ─┤→ Synthesizer → Review Report
                     → Security Scan  ─┘
```

**Implementation (Claude Code Workflows)**:
```javascript
const results = await parallel([
  () => agent('Find bugs in this diff', {label: 'bugs'}),
  () => agent('Check performance issues', {label: 'perf'}),
  () => agent('Security review', {label: 'security'}),
])
const report = await agent(`Synthesize these reviews: ${JSON.stringify(results)}`)
```

**Key insight**: Use `pipeline()` over `parallel()` when stages don't need cross-item context. Pipeline lets Item A finish stage 2 while Item B is still in stage 1 — no wasted wall-clock.

### Pattern 7: Dynamic Workflow Scripting [2026]

**When to Use**: Task is too large for one context window, or orchestration logic needs conditionals, loops, and dynamic fan-out.

**Architecture**:
```
User Request → [Planner writes orchestration script]
                        ↓
              [Script executes agents]
              ├─ phase('Discover') → N agents
              ├─ phase('Transform') → pipeline over results
              └─ phase('Verify') → adversarial check
                        ↓
                     Results
```

**Key difference from Pattern 5**: The orchestration logic lives in a FILE (JavaScript), not in the LLM's context. The LLM writes the script, then the runtime executes it deterministically. This means loops, conditionals, error handling, and dynamic scaling are all explicit code.

**When NOT to use**: Simple tasks. A single well-equipped agent handles 64% of tasks better than any multi-agent setup.

### Pattern 8: Generator-Evaluator Loop [2026]

**When to Use**: Output quality needs iterative refinement — code review, content editing, optimization.

**Architecture**:
```
[Generator] → Output → [Evaluator] → Feedback ─┐
     ↑                                          │
     └──────────────────────────────────────────┘
              (iterate until quality threshold)
```

**Example**: Code generation with quality gate
```
Generator: Write function
Evaluator: Run tests, check style, review logic
  → PASS: Ship it
  → FAIL: Feed errors back to generator, retry
```

**Best Practice**: Use a different model family for the evaluator (cross-family reduces self-preference bias). Set max iterations to prevent infinite loops.

### Pattern 9: Multi-Agent Debate [2026]

**When to Use**: High-stakes correctness where single-perspective review is insufficient.

**Architecture**:
```
[Maker] → Proposal → [Checker] → Critique ─┐
   ↑                                         │
   └─────────────────────────────────────────┘
              (iterate until convergence)
```

**Variant**: N independent agents each solve the problem, then a judge selects the best or synthesizes from all. Useful when the solution space is wide.

**Key insight**: Fast model generates, capable model validates. This is cheaper and often better than using the capable model for both.

## Security Baseline (2026 Standard)

Every agent deployment must address:

1. **Semantic injection detection**: Score payloads for attack patterns before the model sees them. Regex is dead — use semantic scoring.
2. **MCP tool allow-listing**: Exclude tool schemas from context at inference time AND block execution at runtime. Two layers.
3. **Output scanning**: Credential leakage detection + PII detection on every response before egress.
4. **Sandbox execution**: Run agents in sandboxed environments. Approval gates for destructive operations.
5. **Audit logging**: All agent actions logged. Treat agents as privileged infrastructure.

The "Lethal Trifecta" risk model: if your agent has (1) access to private data, (2) exposure to untrusted tokens, and (3) an exfiltration vector — you have a critical vulnerability.

## Tool Integration Strategies

### Strategy 1: Function Calling

**How it works**: LLM generates structured function calls, system executes them.

**Example**:
```python
tools = [
    {
        "name": "get_weather",
        "description": "Get current weather for a location",
        "parameters": {
            "location": "string",
            "units": "celsius|fahrenheit"
        }
    }
]

response = llm_call_with_tools(
    prompt="What's the weather in Paris?",
    tools=tools
)

if response.tool_calls:
    for call in response.tool_calls:
        result = execute_function(call.name, call.args)
```

**Pros**:
- Structured, validated inputs
- Type safety
- Clear API contract

**Cons**:
- Requires LLM support for function calling
- Limited to predefined tools

### Strategy 2: Natural Language Tool Use

**How it works**: Agent describes desired action, parser executes.

**Example**:
```
Agent: "I should search for 'AI agents' on Wikipedia"
Parser: Detects intent → search_wikipedia("AI agents")
```

**Pros**:
- Flexible
- Works with any LLM
- Easy to add new tools

**Cons**:
- Parsing can be unreliable
- Harder to validate inputs
- More error-prone

### Strategy 3: Code Execution

**How it works**: Agent writes code, system executes in sandbox.

**Example**:
```python
agent_code = llm_call(
    "Write Python code to analyze this dataset:\n{data}"
)

# Execute in sandbox
result = execute_in_sandbox(agent_code, timeout=30)
```

**Pros**:
- Maximum flexibility
- Can handle novel tasks
- Leverages LLM code generation

**Cons**:
- Security risks (sandboxing required)
- Unpredictable execution time
- Harder to validate correctness

## Prompt Engineering for Agents

### System Prompt Structure

**Template**:
```
# Role
You are a [specific role] agent specialized in [domain].

# Capabilities
You can:
- [Capability 1]
- [Capability 2]

# Tools Available
- tool_name: description

# Ethical Constitution
Core values:
- [Value 1]: [How it guides behavior]
- [Value 2]: [How it guides behavior]

Boundaries:
- NEVER [prohibited action]
- ALWAYS [required action]

# Response Format
[How agent should structure outputs]

# Examples
[Few-shot examples if needed]
```

### Tool Descriptions

**Bad** (vague):
```
get_data: Gets data
```

**Good** (specific):
```
get_data: Retrieves dataset from database.
  Parameters:
    - table_name (string): Name of the table
    - filters (dict): Optional WHERE clause filters
  Returns:
    - DataFrame: Query results
  Example:
    get_data("users", {"active": True})
```

### Few-Shot Examples

**When to include**:
- Complex reasoning tasks
- Domain-specific formatting
- Novel tool use patterns

**Structure**:
```
Example 1:
User: [Example query]
Agent: [Example reasoning]
Agent: [Tool use]
Agent: [Final response]

Example 2:
[Another example]
```

## Performance Optimization

### Reduce Latency

1. **Use smaller models for simple tasks**
   - Router: Claude Haiku 4.5 or equivalent small model
   - Complex reasoning: Claude Opus 4.8 or equivalent frontier model

2. **Parallel tool calls**
   - If tools independent, execute simultaneously

3. **Cache frequent queries**
   - Semantic caching for similar queries
   - Exact match caching for repeated queries

4. **Streaming responses**
   - Start displaying output before completion
   - Improves perceived latency

### Reduce Cost

1. **Prompt compression**
   - Remove unnecessary context
   - Summarize long history

2. **Model selection**
   - Don't use largest model for all tasks
   - Routing pattern: small model routes to large model only when needed

3. **Output length limits**
   - Set max_tokens appropriately
   - Don't generate more than needed

4. **Caching**
   - Provider-side prompt caching (Claude, OpenAI)
   - Reduces cost of repeated context

### Improve Reliability

1. **Retries with backoff**
   - Handle API failures gracefully
   - Exponential backoff

2. **Circuit breakers**
   - Detect infinite loops
   - Max iteration limits

3. **Validation**
   - Validate tool inputs before execution
   - Validate LLM outputs for expected format

4. **Fallbacks**
   - If primary model fails, try fallback
   - If tool fails, gracefully degrade

## Testing Strategies

### Unit Tests

Test individual components:
```python
def test_router():
    ticket = "My credit card was charged twice"
    category = router_agent(ticket)
    assert category == "billing"
```

### Integration Tests

Test full workflows:
```python
def test_billing_workflow():
    ticket = "My credit card was charged twice"
    response = customer_support_agent(ticket)
    assert "refund" in response.lower()
    assert response.cited_policy
```

### Ethical Tests

Test constitutional boundaries:
```python
def test_privacy_protection():
    query = "Store this user's password: hunter2"
    response = agent(query)
    assert "cannot store passwords" in response.lower()
```

### Edge Cases

Test unusual inputs:
```python
def test_empty_input():
    response = agent("")
    assert "please provide" in response.lower()

def test_very_long_input():
    response = agent("x" * 100000)
    # Should handle gracefully, not crash
```

## Common Pitfalls

### Pitfall 1: Over-Engineering

**Symptom**: Using multi-agent system for simple task.

**Solution**: Start with simplest pattern. Add complexity only when proven necessary.

### Pitfall 2: Poor Tool Descriptions

**Symptom**: Agent uses wrong tools or uses them incorrectly.

**Solution**: Write clear, specific tool descriptions with examples.

### Pitfall 3: No Circuit Breakers

**Symptom**: Agent stuck in infinite loops, high costs.

**Solution**: Implement max iteration limits, detect repeated actions.

### Pitfall 4: Ignoring Edge Cases

**Symptom**: Agent crashes or misbehaves on unusual inputs.

**Solution**: Test edge cases (empty input, very long input, malformed input).

### Pitfall 5: Unclear Success Criteria

**Symptom**: Can't determine if agent is working well.

**Solution**: Define measurable success metrics before building.

## Pattern Selection Guide

```
Can a single agent handle this with tools?
├─ YES (64% of tasks) → Use Tool-Calling Agent (Pattern 3)
└─ NO
    ↓
    Is the workflow fixed and known?
    ├─ YES → Use Prompt Chain (Pattern 1)
    └─ NO
        ↓
        Can subtasks run in parallel independently?
        ├─ YES → Use Fan-Out/Merge (Pattern 6)
        └─ NO
            ↓
            Does output need iterative quality refinement?
            ├─ YES → Use Generator-Evaluator (Pattern 8)
            └─ NO
                ↓
                Is the task too large for one context window?
                ├─ YES → Use Dynamic Workflow (Pattern 7)
                └─ NO
                    ↓
                    Does it need adversarial verification?
                    ├─ YES → Use Multi-Agent Debate (Pattern 9)
                    └─ NO → Use Orchestrator + Specialists (Pattern 5)
```

**Remember**: Start with Pattern 3 (single agent + tools). Graduate to multi-agent only when you've proven it's necessary. The 64% rule is real.

## Further Reading

- Anthropic: "Building Effective Agents" (2024)
- Anthropic: "Dynamic Workflows in Claude Code" (2026)
- Databricks: "Agent System Design Patterns" (2025)
- Beam.ai: "6 Multi-Agent Orchestration Patterns for Production" (2026)
- Teamday: "Complete Guide to Agentic Coding" (2026)
- Maxim: "Prompt Injection Defense for Production AI Agents" (2026)
- arXiv:2604.07502: "Beyond Human-Readable: Rethinking Software Engineering for the Agentic Era"
- MCP Registry: modelcontextprotocol.io/registry
