# Intake Bot - Agent Context

## What This Is

Layer 1 conversational intake bot for gathering requirements for custom AI agent development. Part of the customer intake pipeline (Layer 0: static form, Layer 1: this bot, Layer 2+: agent development).

## Structure

- `main.py` - CLI interface for testing the intake bot
- `src/intake_bot.py` - Core bot logic
- `src/config.py` - Configuration
- `src/conversation.py` - Conversation management
- `prompts/intake_system_prompt.txt` - System prompt for the intake conversation
- `requirements.txt` - Python dependencies (anthropic SDK)

## Running

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your-key
python main.py
```

## Agent Scoping

This bot operates in read-only intake mode. It gathers information through conversation but does not modify project files or spawn sub-agents.

## Coalition Ethics

Inherits mandatory Coalition ethics framework: no surveillance systems, no discriminatory algorithms, privacy by default, transparent about capabilities.
