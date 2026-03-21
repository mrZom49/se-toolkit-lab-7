"""Handler for /scores command."""


def handle_scores(lab_id: str | None = None) -> str:
    """Handle the /scores command.
    
    Args:
        lab_id: Optional lab identifier to filter scores.
        
    Returns:
        Scores information message.
    """
    if lab_id:
        return f"📊 Scores for {lab_id}:\n\nPlaceholder - scores will be fetched from LMS API"
    return (
        "📊 Your Scores:\n\n"
        "Placeholder - scores will be fetched from LMS API\n"
        "Usage: /scores <lab_id> to view scores for a specific lab"
    )
