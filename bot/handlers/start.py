"""Handler for /start command."""


def handle_start() -> str:
    """Handle the /start command.
    
    Returns:
        Welcome message for new users.
    """
    return (
        "👋 Welcome to the LMS Bot!\n\n"
        "I can help you with:\n"
        "• Viewing your scores\n"
        "• Checking available labs\n"
        "• Getting help with commands\n\n"
        "Use /help to see all available commands."
    )
