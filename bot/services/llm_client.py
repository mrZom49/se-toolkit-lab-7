"""LLM client service for intent routing."""

import httpx


class LLMClient:
    """Client for interacting with the LLM API."""

    def __init__(self, base_url: str, api_key: str, model: str = "coder-model"):
        """Initialize the LLM client.
        
        Args:
            base_url: Base URL of the LLM API.
            api_key: API key for authentication.
            model: Model name to use for completions.
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={"Authorization": f"Bearer {self.api_key}"},
        )

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()

    async def classify_intent(self, user_message: str) -> str:
        """Classify the user's intent from their message.
        
        Args:
            user_message: The user's input message.
            
        Returns:
            The classified intent (e.g., 'start', 'help', 'health', 'scores', 'labs').
        """
        # Placeholder implementation - will be implemented in Phase 3
        # This would call the LLM API to classify the intent
        return "unknown"

    async def generate_response(self, prompt: str) -> str:
        """Generate a response using the LLM.
        
        Args:
            prompt: The prompt to send to the LLM.
            
        Returns:
            Generated response text.
        """
        # Placeholder implementation
        return "I understand your query, but I'm still learning how to help with that."
