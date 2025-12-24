"""Main IntakeBot class for managing intake conversations."""

from typing import Optional
import anthropic

from .config import Config
from .conversation import ConversationState


class IntakeBot:
    """
    Layer 1 Intake Bot for gathering AI agent requirements.

    Wraps the Anthropic Claude API to conduct structured requirement
    gathering conversations with customers.
    """

    def __init__(self, layer0_context: Optional[dict] = None):
        """
        Initialize the IntakeBot.

        Args:
            layer0_context: Optional context from the Layer 0 static form.
                           May contain: name, email, company, initial_description,
                           budget_tier, etc.
        """
        self.config = Config()
        self.client = anthropic.Anthropic(api_key=self.config.api_key)
        self.system_prompt = self.config.get_system_prompt()

        # Initialize conversation state
        self.state = ConversationState(layer0_context=layer0_context)

        # Prepare the system prompt with any Layer 0 context
        self._prepare_system_prompt()

    def _prepare_system_prompt(self) -> None:
        """Prepare the system prompt, optionally adding Layer 0 context."""
        context_message = self.state.build_context_message()
        if context_message:
            self.system_prompt = (
                f"{self.system_prompt}\n\n"
                f"## Customer Context (from intake form)\n{context_message}\n"
                f"Use this context to personalize your greeting and skip "
                f"questions you already have answers to."
            )

        # Add turn tracking info to system prompt
        self.system_prompt += (
            f"\n\n## Turn Tracking\n"
            f"Maximum turns allowed: {Config.MAX_TURNS}\n"
            f"Current turn will be injected in each message."
        )

    def send_message(self, user_message: str) -> dict:
        """
        Send a user message and get the bot's response.

        Args:
            user_message: The user's message text.

        Returns:
            Dictionary containing:
                - response: The bot's response text
                - turn: Current turn number
                - complete: Whether requirements gathering is complete
                - requirements: The requirements dict if complete, else None
                - approaching_limit: Whether nearing the turn limit
        """
        # Check if we've hit the turn limit
        if self.state.turn_count >= Config.MAX_TURNS:
            return {
                "response": (
                    "We've reached the maximum number of turns for this session. "
                    "Please review the requirements gathered so far or start a new session."
                ),
                "turn": self.state.turn_count,
                "complete": self.state.is_complete,
                "requirements": self.state.requirements,
                "approaching_limit": True,
                "at_limit": True
            }

        # Add user message to state
        self.state.add_user_message(user_message)

        # Build the system prompt with current turn info
        turn_info = self.state.get_turn_info()
        current_system = (
            f"{self.system_prompt}\n\n"
            f"CURRENT TURN: {turn_info['current_turn']} of {turn_info['max_turns']}"
        )

        if turn_info["approaching_limit"]:
            current_system += (
                "\n\nIMPORTANT: You are approaching the turn limit. "
                "Begin summarizing what you have and move toward completion."
            )

        # Call the Anthropic API
        try:
            response = self.client.messages.create(
                model=Config.MODEL,
                max_tokens=Config.MAX_TOKENS,
                temperature=Config.TEMPERATURE,
                system=current_system,
                messages=self.state.get_messages_for_api()
            )

            assistant_message = response.content[0].text

        except anthropic.APIError as e:
            return {
                "response": f"An error occurred communicating with the AI service: {str(e)}",
                "turn": self.state.turn_count,
                "complete": False,
                "requirements": None,
                "approaching_limit": turn_info["approaching_limit"],
                "at_limit": False,
                "error": True
            }

        # Add assistant message to state (this also checks for completion)
        self.state.add_assistant_message(assistant_message)

        return {
            "response": assistant_message,
            "turn": self.state.turn_count,
            "complete": self.state.is_complete,
            "requirements": self.state.requirements,
            "approaching_limit": turn_info["approaching_limit"],
            "at_limit": turn_info["at_limit"]
        }

    def start_conversation(self) -> dict:
        """
        Start the conversation by getting the bot's initial greeting.

        Returns:
            Dictionary with the bot's opening message and turn info.
        """
        # Send an empty-like message to trigger the greeting
        # We use a minimal prompt to get the bot started
        initial_prompt = "Hello, I'm ready to discuss my agent requirements."

        return self.send_message(initial_prompt)

    def is_complete(self) -> bool:
        """
        Check if requirements gathering is complete.

        Returns:
            True if the final JSON has been output, False otherwise.
        """
        return self.state.is_complete

    def get_requirements(self) -> Optional[dict]:
        """
        Get the gathered requirements.

        Returns:
            The requirements dictionary if complete, None otherwise.
        """
        return self.state.requirements

    def get_turn_count(self) -> int:
        """
        Get the current turn count.

        Returns:
            The number of turns elapsed.
        """
        return self.state.turn_count

    def get_conversation_history(self) -> list:
        """
        Get the full conversation history.

        Returns:
            List of message dictionaries.
        """
        return self.state.messages.copy()

    def export_state(self) -> dict:
        """
        Export the full conversation state for persistence.

        Returns:
            Dictionary containing the full state.
        """
        return {
            "conversation": self.state.to_dict(),
            "config": {
                "model": Config.MODEL,
                "temperature": Config.TEMPERATURE,
                "max_tokens": Config.MAX_TOKENS
            }
        }

    @classmethod
    def restore_from_state(
        cls,
        state_dict: dict,
        layer0_context: Optional[dict] = None
    ) -> "IntakeBot":
        """
        Restore an IntakeBot from a saved state.

        Args:
            state_dict: Dictionary from export_state()
            layer0_context: Optional Layer 0 context (will be overwritten
                           by state if present)

        Returns:
            A new IntakeBot instance with restored state.
        """
        # Create a new instance
        bot = cls(layer0_context=layer0_context)

        # Restore the conversation state
        if "conversation" in state_dict:
            bot.state = ConversationState.from_dict(state_dict["conversation"])

        return bot
