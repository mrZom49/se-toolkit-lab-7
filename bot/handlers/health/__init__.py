"""Handler for /health command."""

import asyncio

from services.lms_api import LMSAPIClient, LMSAPIError


async def handle_health(api_client: LMSAPIClient) -> str:
    """Handle the /health command.
    
    Args:
        api_client: LMS API client instance.
        
    Returns:
        Backend service status message.
    """
    try:
        result = await api_client.health_check()
        return f"✅ Backend is healthy. {result['item_count']} items available."
    except LMSAPIError as e:
        return f"❌ Backend error: {e.message}"
