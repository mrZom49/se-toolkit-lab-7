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
        "/scores <lab_id> - View your scores for a specific lab\n"
        "/labs - List all available labs\n\n"
        "You can also ask natural language questions like:\n"
        "• 'what labs are available'\n"
        "• 'show my scores for lab-04'"
    )
