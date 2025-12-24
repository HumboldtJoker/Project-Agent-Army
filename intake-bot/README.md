# Layer 1 Intake Bot

A conversational AI bot for gathering requirements for custom AI agent development. Part of the customer intake pipeline for the AI Agent Building Service.

## Overview

This is Layer 1 of the intake pipeline:
- **Layer 0**: Static HTML form that collects basic customer info and deposit
- **Layer 1** (this bot): Conversational requirements gathering
- **Layer 2+**: Agent development based on gathered requirements

The Intake Bot uses Claude (via the Anthropic API) to conduct a structured conversation that gathers all necessary information to build a custom AI agent.

## Installation

1. Clone or copy this directory to your local machine

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your API key:
   ```bash
   cp .env.example .env
   # Edit .env and add your Anthropic API key
   ```

## Usage

### CLI Interface

Run the interactive CLI for testing:

```bash
python main.py
```

Commands during conversation:
- Type your responses normally to continue the conversation
- `quit` or `exit` - End the session
- `status` - View current turn count and completion status
- `export` - Save conversation state to JSON file

### Demo Mode

Run with sample Layer 0 context:

```bash
python main.py --demo
```

### Programmatic Usage

```python
from src.intake_bot import IntakeBot

# Initialize with optional Layer 0 context
layer0_context = {
    "name": "John Doe",
    "email": "john@example.com",
    "company": "Acme Corp",
    "initial_description": "Need a customer support agent",
    "budget_tier": "professional"
}

bot = IntakeBot(layer0_context=layer0_context)

# Start the conversation
result = bot.start_conversation()
print(result["response"])

# Continue the conversation
while not bot.is_complete():
    user_input = input("You: ")
    result = bot.send_message(user_input)
    print(f"Bot: {result['response']}")

    if result["complete"]:
        requirements = result["requirements"]
        print("Requirements gathered:", requirements)
        break
```

### Response Format

The `send_message()` method returns a dictionary:

```python
{
    "response": str,        # Bot's response text
    "turn": int,            # Current turn number
    "complete": bool,       # Whether requirements are complete
    "requirements": dict,   # Requirements JSON if complete, else None
    "approaching_limit": bool,  # True if near turn limit
    "at_limit": bool        # True if at turn limit
}
```

### Final Requirements JSON

When complete, the bot outputs a structured JSON:

```json
{
  "status": "complete",
  "requirements": {
    "agent_purpose": "What the agent should accomplish",
    "domain": "Field or industry context",
    "primary_tasks": ["task1", "task2", "task3"],
    "tools_needed": ["tool1", "tool2"],
    "tone_style": "Communication personality",
    "constraints": ["constraint1", "constraint2"],
    "safety_boundaries": ["boundary1", "boundary2"],
    "user_context": "Who will use it"
  },
  "safety_signals": {
    "workflow_integration": "How they plan to use it",
    "boundary_awareness": "Their understanding of limits",
    "error_handling_approach": "How they handle mistakes",
    "ai_responsibility_stance": "Their view on AI responsibility"
  },
  "estimated_complexity": "basic|standard|professional|enterprise",
  "flags": []
}
```

## Configuration

Settings in `src/config.py`:

| Setting | Value | Description |
|---------|-------|-------------|
| MODEL | claude-3-haiku-20240307 | Claude model (MVI - simpler model) |
| TEMPERATURE | 0.3 | Low for consistency |
| MAX_TOKENS | 200 | Keep responses concise |
| MAX_TURNS | 30 | Maximum conversation turns |
| WARNING_TURN | 25 | Start wrapping up here |

## File Structure

```
intake-bot/
├── .env.example          # Template for API key
├── requirements.txt      # Python dependencies
├── prompts/
│   └── intake_system_prompt.txt  # Bot's system prompt
├── src/
│   ├── __init__.py
│   ├── intake_bot.py     # Main IntakeBot class
│   ├── conversation.py   # Conversation state management
│   └── config.py         # Configuration loading
├── main.py               # CLI interface
└── README.md             # This file
```

## State Persistence

Export and restore conversation state:

```python
# Export
state = bot.export_state()
with open("state.json", "w") as f:
    json.dump(state, f)

# Restore
with open("state.json") as f:
    state = json.load(f)
bot = IntakeBot.restore_from_state(state)
```

## Safety Features

The bot includes several safety mechanisms:
- Strict topic boundaries (only discusses agent requirements)
- Safety screening questions woven into conversation
- Flag detection for concerning patterns
- Turn limit to prevent endless conversations
- No execution of code or external access

## Flags

The bot may flag conversations for:
- `hostile_interaction` - Aggressive or abusive user
- `scope_creep` - Potentially harmful agent requests
- `unrealistic_expectations` - Impossible capabilities requested
- `ai_relationship_concern` - Unhealthy AI attachment signals
- `safety_resistance` - User dismisses safety questions
- `unclear_purpose` - Cannot determine legitimate use case

## Integration with Layer 0

The bot accepts context from the Layer 0 form:

```python
layer0_context = {
    "name": "Customer name",
    "email": "customer@email.com",
    "company": "Company name",
    "initial_description": "Brief description from form",
    "budget_tier": "basic|standard|professional|enterprise"
}

bot = IntakeBot(layer0_context=layer0_context)
```

This context is used to:
- Personalize the greeting
- Skip redundant questions
- Set expectations based on budget tier

## Error Handling

The bot handles common errors gracefully:
- Missing API key: Clear error message with setup instructions
- API errors: Returns error info in response dict
- Invalid JSON detection: Continues conversation normally
- Turn limit: Graceful session ending with partial data
