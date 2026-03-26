"""Handler for /scores command."""

from services.lms_api import LMSAPIClient


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
            "📊 Your Scores:\n\n"
            "Please specify a lab ID. Usage: /scores <lab_id>\n\n"
            "Example: /scores lab-04\n\n"
            "Or ask naturally: 'show scores for lab 4'"
        )

    # Normalize lab_id (e.g., "4" -> "lab-04")
    if lab_id.isdigit():
        lab_id = f"lab-{lab_id.zfill(2)}"
    elif not lab_id.startswith("lab-"):
    # Try to extract lab number from simple formats like "lab4" or "lab 4"                               │
    	lab_id = lab_id.replace(" ", "").replace("lab", "")                                                  │
  	if lab_id.isdigit():                                                                                 │
 		lab_id = f"lab-{lab_id.zfill(2)}

    try:
        scores = await api_client.get_scores(lab_id)
    except Exception as e:
        return f"❌ Error fetching scores: {str(e)}"

    if not scores:
        return f"📊 No score data available for {lab_id}"

    # Format score distribution
    lines = [f"📊 Score Distribution for {lab_id}:\n"]
    for score_data in scores:
        task_name = score_data.get("task_name", "Unknown")
        bucket_0 = score_data.get("bucket_0", 0)  # 0-49
        bucket_1 = score_data.get("bucket_1", 0)  # 50-69
        bucket_2 = score_data.get("bucket_2", 0)  # 70-89
        bucket_3 = score_data.get("bucket_3", 0)  # 90-100
        total = bucket_0 + bucket_1 + bucket_2 + bucket_3

        lines.append(f"• {task_name}:")
        lines.append(f"  0-49: {bucket_0} | 50-69: {bucket_1} | 70-89: {bucket_2} | 90-100: {bucket_3} (Total: {total})")

    return "\n".join(lines)
