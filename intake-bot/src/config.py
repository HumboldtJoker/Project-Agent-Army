"""Configuration management for the Intake Bot."""

import os
from pathlib import Path
from dotenv import load_dotenv


class Config:
    """Configuration loader for the Intake Bot application."""

    # Model settings (MVI principle - use simpler model)
    MODEL = "claude-3-haiku-20240307"
    TEMPERATURE = 0.3  # Consistency over creativity
    MAX_TOKENS = 200  # Keep responses concise

    # Conversation limits
    MAX_TURNS = 30
    WARNING_TURN = 25  # Start wrapping up at this turn

    def __init__(self, env_path: str = None):
        """
        Initialize configuration.

        Args:
            env_path: Optional path to .env file. Defaults to project root.
        """
        if env_path:
            load_dotenv(env_path)
        else:
            # Try to find .env in project root
            project_root = Path(__file__).parent.parent
            env_file = project_root / ".env"
            if env_file.exists():
                load_dotenv(env_file)
            else:
                load_dotenv()  # Try default locations

        self._api_key = os.getenv("ANTHROPIC_API_KEY")

    @property
    def api_key(self) -> str:
        """Get the Anthropic API key."""
        if not self._api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not found. "
                "Please set it in your .env file or environment variables."
            )
        return self._api_key

    @property
    def prompts_dir(self) -> Path:
        """Get the prompts directory path."""
        return Path(__file__).parent.parent / "prompts"

    def get_system_prompt(self) -> str:
        """Load the system prompt from file."""
        prompt_file = self.prompts_dir / "intake_system_prompt.txt"
        if not prompt_file.exists():
            raise FileNotFoundError(
                f"System prompt not found at {prompt_file}. "
                "Please ensure the prompts directory contains intake_system_prompt.txt"
            )
        return prompt_file.read_text(encoding="utf-8")
