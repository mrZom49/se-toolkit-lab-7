"""Handler for /start command."""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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
        "Use /help to see all available commands.\n\n"
        "Or just ask me a question like:\n"
        "• 'what labs are available?'\n"
        "• 'show scores for lab 4'\n"
        "• 'which lab has the lowest pass rate?'"
    )


def get_start_keyboard() -> InlineKeyboardMarkup:
    """Create inline keyboard for common queries.

    Returns:
        InlineKeyboardMarkup with common action buttons.
    """
    keyboard = [
        [
            InlineKeyboardButton(text="📚 Available Labs", callback_data="labs"),
            InlineKeyboardButton(text="❓ Help", callback_data="help"),
        ],
        [
            InlineKeyboardButton(text="📊 Scores Lab 04", callback_data="scores_lab-04"),
            InlineKeyboardButton(text="📈 Pass Rates Lab 04", callback_data="pass_rates_lab-04"),
        ],
        [
            InlineKeyboardButton(text="🏆 Top Students Lab 04", callback_data="top_lab-04"),
            InlineKeyboardButton(text="📉 Lowest Pass Rate", callback_data="lowest_pass_rate"),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
