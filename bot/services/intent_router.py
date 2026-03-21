"""Intent router for natural language queries."""

from __future__ import annotations

import re
from typing import Any

from services.lms_api import LMSAPIClient
from services.llm_client import LLMClient


class IntentRouter:
    """Routes natural language queries to appropriate API calls via LLM."""

    def __init__(self, llm_client: LLMClient, api_client: LMSAPIClient):
        """Initialize the intent router.

        Args:
            llm_client: The LLM client for intent classification.
            api_client: The LMS API client for data fetching.
        """
        self.llm_client = llm_client
        self.api_client = api_client

    async def route(self, user_message: str, debug: bool = False) -> str:
        """Route a user message and generate a response.

        Args:
            user_message: The user's input message.
            debug: If True, print debug output to stderr.

        Returns:
            The bot's response.
        """
        # Check for simple greetings/fallbacks first (fast path)
        simple_response = self._check_simple_cases(user_message)
        if simple_response:
            return simple_response

        # Use LLM for intent-based routing with tool calling
        response = await self.llm_client.generate_completion(
            user_message=user_message,
            api_client=self.api_client,
            debug=debug,
        )

        return response

    def _check_simple_cases(self, message: str) -> str | None:
        """Check for simple cases that don't need LLM processing.

        Args:
            message: The user's input message.

        Returns:
            A response string if this is a simple case, None otherwise.
        """
        message_lower = message.strip().lower()

        # Greeting patterns
        greeting_patterns = [
            r"^hi$",
            r"^hello$",
            r"^hey$",
            r"^greetings",
            r"^good (morning|afternoon|evening)",
        ]

        for pattern in greeting_patterns:
            if re.match(pattern, message_lower):
                return (
                    "👋 Hello! I'm the LMS Bot. I can help you with:\n\n"
                    "• Viewing labs and tasks\n"
                    "• Checking scores and pass rates\n"
                    "• Finding top learners\n"
                    "• Comparing groups\n\n"
                    "Just ask me a question like:\n"
                    "• 'what labs are available?'\n"
                    "• 'show me scores for lab 4'\n"
                    "• 'which lab has the lowest pass rate?'"
                )

        # Gibberish/unclear input (very short or no recognizable words)
        words = message_lower.split()
        if len(words) == 1 and len(words[0]) <= 3 and not words[0] in ["lab", "api", "bot", "lms"]:
            # Check if it's mostly non-alphabetic
            alpha_count = sum(1 for c in words[0] if c.isalpha())
            if alpha_count < len(words[0]) * 0.5:
                return (
                    "I didn't understand that. Here's what I can help you with:\n\n"
                    "• List available labs: 'what labs are available?'\n"
                    "• Show scores: 'show scores for lab 4'\n"
                    "• Compare labs: 'which lab has the lowest pass rate?'\n"
                    "• Top students: 'who are the top 5 students in lab 4'\n\n"
                    "Use /help for all commands."
                )

        # Single lab reference without clear intent
        lab_only_pattern = r"^lab[- ]?\d+$"
        if re.match(lab_only_pattern, message_lower):
            lab_id = self._extract_lab_id(message_lower)
            return (
                f"What about {lab_id}? I can help you with:\n\n"
                f"• 'show scores for {lab_id}'\n"
                f"• 'show pass rates for {lab_id}'\n"
                f"• 'who are the top students in {lab_id}'\n"
                f"• 'show groups for {lab_id}'"
            )

        return None

    def _extract_lab_id(self, text: str) -> str | None:
        """Extract a lab ID from text.

        Args:
            text: Text that may contain a lab ID.

        Returns:
            Lab ID if found, None otherwise.
        """
        # Match patterns like "lab-04", "lab 4", "lab04"
        match = re.search(r"lab[- ]?(\d+)", text, re.IGNORECASE)
        if match:
            return f"lab-{match.group(1).zfill(2)}"
        return None


def get_capabilities_hint() -> str:
    """Get a hint message about bot capabilities.

    Returns:
        String describing what the bot can do.
    """
    return (
        "I can help you with:\n\n"
        "• 'what labs are available?' - List all labs\n"
        "• 'show scores for lab X' - Score distribution\n"
        "• 'show pass rates for lab X' - Pass rates per task\n"
        "• 'which lab has the lowest pass rate?' - Compare labs\n"
        "• 'who are the top students in lab X?' - Top learners\n"
        "• 'compare groups in lab X' - Group performance"
    )
