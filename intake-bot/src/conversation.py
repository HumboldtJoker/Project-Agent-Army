"""Conversation state management for the Intake Bot."""

import json
import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ConversationState:
    """
    Manages the state of an intake conversation.

    Tracks turn count, message history, and completion status.
    """

    turn_count: int = 0
    messages: list = field(default_factory=list)
    is_complete: bool = False
    requirements: Optional[dict] = None
    layer0_context: Optional[dict] = None

    # Pattern to detect final JSON output
    JSON_PATTERN = re.compile(
        r'\{\s*"status"\s*:\s*"complete".*?"requirements"\s*:',
        re.DOTALL
    )

    def add_user_message(self, content: str) -> None:
        """
        Add a user message to the conversation.

        Args:
            content: The user's message text.
        """
        self.messages.append({
            "role": "user",
            "content": content
        })
        self.turn_count += 1

    def add_assistant_message(self, content: str) -> None:
        """
        Add an assistant message and check for completion.

        Args:
            content: The assistant's response text.
        """
        self.messages.append({
            "role": "assistant",
            "content": content
        })

        # Check if this response contains the final JSON
        self._check_completion(content)

    def _check_completion(self, content: str) -> None:
        """
        Check if the response contains the final requirements JSON.

        Args:
            content: The assistant's response to check.
        """
        if self.JSON_PATTERN.search(content):
            # Try to extract and parse the JSON
            try:
                # Find the JSON object in the response
                json_match = re.search(r'\{[\s\S]*\}', content)
                if json_match:
                    json_str = json_match.group()
                    parsed = json.loads(json_str)

                    # Validate it has the expected structure
                    if (parsed.get("status") == "complete" and
                            "requirements" in parsed):
                        self.is_complete = True
                        self.requirements = parsed
            except json.JSONDecodeError:
                # Not valid JSON, continue conversation
                pass

    def get_messages_for_api(self) -> list:
        """
        Get the message history formatted for the Anthropic API.

        Returns:
            List of message dictionaries for the API.
        """
        return self.messages.copy()

    def get_turn_info(self) -> dict:
        """
        Get current turn information.

        Returns:
            Dictionary with turn count and limit info.
        """
        from .config import Config
        return {
            "current_turn": self.turn_count,
            "max_turns": Config.MAX_TURNS,
            "warning_turn": Config.WARNING_TURN,
            "approaching_limit": self.turn_count >= Config.WARNING_TURN,
            "at_limit": self.turn_count >= Config.MAX_TURNS
        }

    def build_context_message(self) -> Optional[str]:
        """
        Build a context message from Layer 0 data if available.

        Returns:
            A formatted context string or None if no Layer 0 context.
        """
        if not self.layer0_context:
            return None

        context_parts = ["Context from initial form:"]

        if "name" in self.layer0_context:
            context_parts.append(f"- Customer name: {self.layer0_context['name']}")

        if "email" in self.layer0_context:
            context_parts.append(f"- Email: {self.layer0_context['email']}")

        if "company" in self.layer0_context:
            context_parts.append(f"- Company: {self.layer0_context['company']}")

        if "initial_description" in self.layer0_context:
            context_parts.append(
                f"- Initial description: {self.layer0_context['initial_description']}"
            )

        if "budget_tier" in self.layer0_context:
            context_parts.append(f"- Budget tier: {self.layer0_context['budget_tier']}")

        return "\n".join(context_parts)

    def to_dict(self) -> dict:
        """
        Serialize the conversation state to a dictionary.

        Returns:
            Dictionary representation of the state.
        """
        return {
            "turn_count": self.turn_count,
            "messages": self.messages,
            "is_complete": self.is_complete,
            "requirements": self.requirements,
            "layer0_context": self.layer0_context
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ConversationState":
        """
        Deserialize a conversation state from a dictionary.

        Args:
            data: Dictionary containing state data.

        Returns:
            A new ConversationState instance.
        """
        state = cls(
            turn_count=data.get("turn_count", 0),
            messages=data.get("messages", []),
            is_complete=data.get("is_complete", False),
            requirements=data.get("requirements"),
            layer0_context=data.get("layer0_context")
        )
        return state
