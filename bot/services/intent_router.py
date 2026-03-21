"""Intent router for natural language queries."""

from __future__ import annotations

from services.lms_api import LMSAPIClient
from services.llm_client import LLMClient


class IntentRouter:
    """Routes natural language queries to appropriate API calls via LLM.

    This router uses the LLM exclusively for intent classification and tool selection.
    No regex or keyword-based routing is used - the LLM decides which tool to call.
    """

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
        # Use LLM for intent-based routing with tool calling
        # The LLM handles greetings, clarifications, and all tool selection
        response = await self.llm_client.generate_completion(
            user_message=user_message,
            api_client=self.api_client,
            debug=debug,
        )

        return response
