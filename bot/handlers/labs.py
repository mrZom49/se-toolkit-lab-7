"""Handler for /labs command."""


def handle_labs() -> str:
    """Handle the /labs command.
    
    Returns:
        List of available labs.
    """
    return (
        "📚 Available Labs:\n\n"
        "Placeholder - labs will be fetched from LMS API\n\n"
        "Use /scores <lab_id> to view your scores for a specific lab."
    )
