#!/usr/bin/env python3
"""CLI interface for testing the Layer 1 Intake Bot."""

import sys
import json
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.intake_bot import IntakeBot
from src.config import Config


def print_separator():
    """Print a visual separator."""
    print("-" * 60)


def print_status(turn: int, complete: bool, approaching_limit: bool):
    """Print the current conversation status."""
    status_parts = [f"Turn: {turn}/{Config.MAX_TURNS}"]

    if complete:
        status_parts.append("STATUS: COMPLETE")
    elif approaching_limit:
        status_parts.append("WARNING: Approaching turn limit")

    print(f"[{' | '.join(status_parts)}]")


def main():
    """Run the interactive CLI for the Intake Bot."""
    print("=" * 60)
    print("Layer 1 Intake Bot - Requirements Gathering")
    print("=" * 60)
    print()
    print("This bot will gather requirements for your custom AI agent.")
    print("Type 'quit' or 'exit' to end the session.")
    print("Type 'status' to see current progress.")
    print("Type 'export' to save the conversation state.")
    print()
    print_separator()

    # Optional: simulate Layer 0 context
    # In production, this would come from the intake form
    layer0_context = None

    # Check for --demo flag to use sample context
    if "--demo" in sys.argv:
        layer0_context = {
            "name": "Demo User",
            "email": "demo@example.com",
            "company": "Demo Corp",
            "initial_description": "I need a customer support agent",
            "budget_tier": "professional"
        }
        print("Running in demo mode with sample Layer 0 context.")
        print_separator()

    try:
        bot = IntakeBot(layer0_context=layer0_context)
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print()
        print("Please ensure you have set up your .env file with:")
        print("  ANTHROPIC_API_KEY=your-api-key-here")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"File Error: {e}")
        sys.exit(1)

    print()
    print("Starting conversation...")
    print_separator()

    # Get the initial greeting
    result = bot.start_conversation()
    print()
    print(f"Bot: {result['response']}")
    print()
    print_status(result["turn"], result["complete"], result["approaching_limit"])
    print_separator()

    # Main conversation loop
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nSession ended by user.")
            break

        if not user_input:
            continue

        # Handle special commands
        if user_input.lower() in ("quit", "exit"):
            print("\nEnding session...")
            break

        if user_input.lower() == "status":
            turn_info = bot.state.get_turn_info()
            print()
            print(f"Current turn: {turn_info['current_turn']}")
            print(f"Max turns: {turn_info['max_turns']}")
            print(f"Complete: {bot.is_complete()}")
            if bot.is_complete():
                print("Requirements have been gathered successfully!")
            print_separator()
            continue

        if user_input.lower() == "export":
            state = bot.export_state()
            filename = "intake_state.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2)
            print(f"\nState exported to {filename}")
            print_separator()
            continue

        # Send message to bot
        result = bot.send_message(user_input)

        print()
        print(f"Bot: {result['response']}")
        print()
        print_status(result["turn"], result["complete"], result["approaching_limit"])
        print_separator()

        # Check if complete
        if result["complete"]:
            print()
            print("=" * 60)
            print("REQUIREMENTS GATHERING COMPLETE")
            print("=" * 60)
            print()
            print("Final Requirements:")
            print(json.dumps(result["requirements"], indent=2))
            print()

            # Offer to save
            try:
                save = input("Save requirements to file? (y/n): ").strip().lower()
                if save == "y":
                    filename = "requirements_output.json"
                    with open(filename, "w", encoding="utf-8") as f:
                        json.dump(result["requirements"], f, indent=2)
                    print(f"Requirements saved to {filename}")
            except (EOFError, KeyboardInterrupt):
                pass

            break

        # Check if at turn limit
        if result.get("at_limit"):
            print()
            print("Turn limit reached. Session ending.")
            if bot.get_requirements():
                print("Partial requirements gathered:")
                print(json.dumps(bot.get_requirements(), indent=2))
            break

    print()
    print("Thank you for using the Intake Bot.")
    print(f"Total turns: {bot.get_turn_count()}")


if __name__ == "__main__":
    main()
