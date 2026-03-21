"""LMS API client service."""

import httpx


class LMSAPIClient:
    """Client for interacting with the LMS API."""

    def __init__(self, base_url: str, api_key: str):
        """Initialize the LMS API client.
        
        Args:
            base_url: Base URL of the LMS API.
            api_key: API key for authentication.
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={"Authorization": f"Bearer {self.api_key}"},
        )

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()

    async def get_scores(self, lab_id: str) -> dict:
        """Fetch scores for a specific lab.
        
        Args:
            lab_id: The lab identifier.
            
        Returns:
            Scores data from the LMS API.
        """
        response = await self._client.get(f"/scores/{lab_id}")
        response.raise_for_status()
        return response.json()

    async def get_labs(self) -> list[dict]:
        """Fetch all available labs.
        
        Returns:
            List of lab data.
        """
        response = await self._client.get("/labs")
        response.raise_for_status()
        return response.json()

    async def health_check(self) -> bool:
        """Check if the LMS API is healthy.
        
        Returns:
            True if the API is healthy, False otherwise.
        """
        try:
            response = await self._client.get("/health")
            return response.status_code == 200
        except httpx.HTTPError:
            return False
