"""LMS API client service."""

import httpx


<<<<<<< HEAD
class LMSAPIError(Exception):
    """Exception raised when LMS API call fails."""

    def __init__(self, message: str, original_error: Exception | None = None):
        self.message = message
        self.original_error = original_error
        super().__init__(self.message)


=======
>>>>>>> 0947f564f882f44003aa916622e2324e44228fbb
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
<<<<<<< HEAD
            timeout=10.0,
=======
>>>>>>> 0947f564f882f44003aa916622e2324e44228fbb
        )

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()

<<<<<<< HEAD
    async def get_items(self) -> list[dict]:
        """Fetch all items (labs and tasks).
        
        Returns:
            List of items from the LMS API.
            
        Raises:
            LMSAPIError: If the API call fails.
        """
        try:
            response = await self._client.get("/items/")
            response.raise_for_status()
            return response.json()
        except httpx.ConnectError as e:
            raise LMSAPIError(f"connection refused ({self.base_url}). Check that the services are running.", e)
        except httpx.HTTPStatusError as e:
            raise LMSAPIError(f"HTTP {e.response.status_code} {e.response.reason_phrase}. The backend service may be down.", e)
        except httpx.HTTPError as e:
            raise LMSAPIError(f"request failed: {str(e)}", e)

    async def get_pass_rates(self, lab: str) -> list[dict]:
        """Fetch pass rates for a specific lab.
        
        Args:
            lab: The lab identifier (e.g., 'lab-04').
            
        Returns:
            List of pass rate data per task.
            
        Raises:
            LMSAPIError: If the API call fails.
        """
        try:
            response = await self._client.get(
                "/analytics/pass-rates",
                params={"lab": lab},
            )
            response.raise_for_status()
            return response.json()
        except httpx.ConnectError as e:
            raise LMSAPIError(f"connection refused ({self.base_url}). Check that the services are running.", e)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise LMSAPIError(f"lab '{lab}' not found. Use /labs to see available labs.", e)
            raise LMSAPIError(f"HTTP {e.response.status_code} {e.response.reason_phrase}. The backend service may be down.", e)
        except httpx.HTTPError as e:
            raise LMSAPIError(f"request failed: {str(e)}", e)

    async def health_check(self) -> dict:
        """Check if the LMS API is healthy and get item count.
        
        Returns:
            Dict with 'healthy' status and 'item_count'.
            
        Raises:
            LMSAPIError: If the API call fails.
        """
        try:
            response = await self._client.get("/items/")
            response.raise_for_status()
            items = response.json()
            return {"healthy": True, "item_count": len(items)}
        except httpx.ConnectError as e:
            raise LMSAPIError(f"connection refused ({self.base_url}). Check that the services are running.", e)
        except httpx.HTTPStatusError as e:
            raise LMSAPIError(f"HTTP {e.response.status_code} {e.response.reason_phrase}. The backend service may be down.", e)
        except httpx.HTTPError as e:
            raise LMSAPIError(f"request failed: {str(e)}", e)
=======
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
>>>>>>> 0947f564f882f44003aa916622e2324e44228fbb
