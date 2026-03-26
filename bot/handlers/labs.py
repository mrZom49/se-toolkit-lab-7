"""Handler for /labs command."""

from services.lms_api import LMSAPIClient


async def handle_labs(api_client: LMSAPIClient) -> str:
    """Handle the /labs command.

    Args:
        api_client: LMS API client instance.

    Returns:
        List of available labs.
    """
    try:
        items = await api_client.get_items()
    except Exception as e:
        return f"❌ Error fetching labs: {str(e)}"

    if not items:
        return "📚 No labs available at the moment."

    # Group items by lab
    labs: dict[str, list[dict]] = {}
    for item in items:
        lab_id = item.get("lab_id", "unknown")
        if lab_id not in labs:
            labs[lab_id] = []
        labs[lab_id].append(item)

    # Format output
    lines = ["📚 Available Labs:\n"]
    for lab_id in sorted(labs.keys()):
        tasks = labs[lab_id]
        task_count = len(tasks)
        # Get lab title from first task
        lab_title = tasks[0].get("title", "")
        if lab_title:
            # Extract main title (before the task number)
            parts = lab_title.split(" Task ")
            main_title = parts[0] if len(parts) > 1 else lab_title
            lines.append(f"• **{lab_id}** – {main_title} ({task_count} tasks)")
        else:
            lines.append(f"• **{lab_id}** ({task_count} tasks)")

    lines.append("\nUse /scores <lab_id> to view scores for a specific lab.")
    lines.append("Or ask: 'show pass rates for lab-04'")

    return "\n".join(lines)
