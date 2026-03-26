"""Handler for /scores command."""

import asyncio

from services.lms_api import LMSAPIClient, LMSAPIError


async def handle_scores(api_client: LMSAPIClient, lab_id: str | None = None) -> str:
    """Handle the /scores command.
    
    Args:
        api_client: LMS API client instance.
        lab_id: Optional lab identifier to filter scores.
        
    Returns:
        Scores information message.
    """
    if not lab_id:
        return (
            "📊 Scores command requires a lab ID.\n"
            "Usage: /scores <lab_id>\n"
            "Example: /scores lab-04\n\n"
            "Use /labs to see available labs."
        )
    
    try:
        pass_rates = await api_client.get_pass_rates(lab_id)
        
        if not pass_rates:
            return f"📊 No pass rate data available for {lab_id}."
        
        lines = [f"📊 Pass rates for {lab_id}:"]
        for task in pass_rates:
            task_name = task.get("task", task.get("task_name", task.get("name", "Unknown")))
            # avg_score or pass_rate can be 0-100 scale
            pass_rate = task.get("avg_score", task.get("pass_rate", 0))
            # If pass_rate is 0-1 scale, convert to percentage
            if pass_rate <= 1 and pass_rate > 0:
                pass_rate = pass_rate * 100
            attempts = task.get("attempts", 0)
            lines.append(f"• {task_name}: {pass_rate:.1f}% ({attempts} attempts)")
        
        return "\n".join(lines)
        
    except LMSAPIError as e:
        return f"❌ Backend error: {e.message}"
