"""Handler for /labs command."""

import asyncio

from services.lms_api import LMSAPIClient, LMSAPIError


async def handle_labs(api_client: LMSAPIClient) -> str:
    """Handle the /labs command.
    
    Args:
        api_client: LMS API client instance.
        
    Returns:
        List of available labs.
    """
    try:
        items = await api_client.get_items()
        
        # Filter for labs (type == "lab" or items that have children)
        labs = [item for item in items if item.get("type") == "lab" or item.get("parent_id") is None]
        
        if not labs:
            return "📚 No labs available at the moment."
        
        lab_lines = []
        for lab in labs:
            name = lab.get("name", "Unknown")
            description = lab.get("description", "")
            lab_lines.append(f"• {name} — {description}" if description else f"• {name}")
        
        return "📚 Available Labs:\n" + "\n".join(lab_lines)
        
    except LMSAPIError as e:
        return f"❌ Backend error: {e.message}"
