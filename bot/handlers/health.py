"""Handler for /health command."""

from services.lms_api import LMSAPIClient, LMSAPIError


async def handle_health(api_client: LMSAPIClient) -> str:
    """Handle the /health command.

    Args:
        api_client: LMS API client instance.

    Returns:
        Health status message.
    """
    try:
        health = await api_client.health_check()
        if health.get("healthy"):
            return (
                "✅ Backend is healthy!\n\n"
                f"📦 Items in database: {health.get('item_count', 0)}"
            )
        else:
            return "⚠️ Backend returned unhealthy status."
    except LMSAPIError as e:
        return f"❌ Backend health check failed:\n{e.message}"
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"
