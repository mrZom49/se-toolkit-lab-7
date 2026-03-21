"""Handler for /start command."""

from config import BotSettings


def handle_start(settings: BotSettings | None = None) -> str:
    """Handle the /start command.
    
    Args:
        settings: Optional bot settings to get bot name.
        
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
