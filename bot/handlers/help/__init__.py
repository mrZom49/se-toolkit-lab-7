"""Handler for /help command."""


def handle_help() -> str:
    """Handle the /help command.
    
    Returns:
        List of available commands and their descriptions.
    """
    return (
        "📖 Available Commands:\n\n"
        "/start - Start the bot and see welcome message\n"
        "/help - Show this help message\n"
        "/health - Check backend service status\n"
        "/labs - List all available labs\n"
        "/scores <lab_id> - View pass rates for a specific lab\n\n"
        "Examples:\n"
        "• /scores lab-04"
    )
