"""Command handlers for the LMS bot.

Handlers are pure functions that take input and return text responses.
They have no knowledge of Telegram or any other transport layer.
"""

from .start import handle_start
from .help import handle_help
from .health import handle_health
from .scores import handle_scores
from .labs import handle_labs

__all__ = [
    "handle_start",
    "handle_help",
    "handle_health",
    "handle_scores",
    "handle_labs",
]
