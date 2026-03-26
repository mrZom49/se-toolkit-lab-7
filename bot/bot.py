#!/usr/bin/env python3
"""LMS Bot entry point.

Supports two modes:
1) Test mode: `uv run bot.py --test "/command"` - prints response to stdout
2) Telegram mode: `uv run bot.py` - runs the Telegram bot
"""

import argparse
import asyncio
import sys
from pathlib import Path

# Add bot directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandObject
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import load_settings
from handlers.start import handle_start
from handlers.help import handle_help
from handlers.health import handle_health
from handlers.scores import handle_scores
from handlers.labs import handle_labs
from services.lms_api import LMSAPIClient, LMSAPIError
from services.llm_client import LLMClient
from services.intent_router import IntentRouter


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="LMS Telegram Bot")
    parser.add_argument(
        "--test",
        type=str,
        metavar="INPUT",
        help="Test mode: process input and print response to stdout",
    )
    return parser.parse_args()


async def route_command(
    command: str,
    api_client: LMSAPIClient,
    llm_client: LLMClient | None = None,
    args: str | None = None,
) -> str:
    """Route a command to the appropriate handler.

    Args:
        command: The command name (without leading /).
        api_client: LMS API client instance.
        llm_client: Optional LLM client for natural language routing.
        args: Optional command arguments.

    Returns:
        Handler response text.
    """
    if command == "start":
        return handle_start()
    elif command == "help":
        return handle_help()
    elif command == "health":
        return await handle_health(api_client)
    elif command == "scores":
        return await handle_scores(api_client, args)
    elif command == "labs":
        return await handle_labs(api_client)
    elif command == "unknown" and llm_client:
        # Use LLM-based intent routing for natural language queries
        router = IntentRouter(llm_client, api_client)
        return await router.route(args or "", debug=True)
    else:
        return f"❓ Unknown command: /{command}\nUse /help to see available commands."


def parse_test_input(user_input: str) -> tuple[str, str | None]:
    """Parse test input into command and arguments.

    Args:
        user_input: The test input string (e.g., "/scores lab-04" or "what labs are available")

    Returns:
        Tuple of (command, args)
    """
    user_input = user_input.strip()

    # Handle command-style input
    if user_input.startswith("/"):
        parts = user_input[1:].split(maxsplit=1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else None
        return command, args

    # Handle natural language input - route to LLM
    return "unknown", user_input


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


async def run_test_mode(user_input: str) -> None:
    """Run the bot in test mode.

    Args:
        user_input: The input to process.
    """
    # Load settings (for API configuration)
    settings = load_settings()

    # Initialize API client
    api_client = LMSAPIClient(
        settings.lms_api_base_url or "http://localhost:42002",
        settings.lms_api_key or "test-key",
    )

    # Initialize LLM client
    llm_client = LLMClient(
        settings.llm_api_base_url or "http://localhost:42005",
        settings.llm_api_key or "test-key",
        settings.llm_api_model or "coder-model",
    )

    try:
        # Parse input and route to handler
        command, args = parse_test_input(user_input)
        response = await route_command(command, api_client, llm_client, args)

        # Print response to stdout
        print(response)
    finally:
        await api_client.close()
        await llm_client.close()


async def run_telegram_mode() -> None:
    """Run the bot in Telegram mode."""
    settings = load_settings()
    settings.validate_for_telegram()

    # Initialize services
    api_client = LMSAPIClient(settings.lms_api_base_url, settings.lms_api_key)
    llm_client = LLMClient(settings.llm_api_base_url, settings.llm_api_key, settings.llm_api_model)
    router = IntentRouter(llm_client, api_client)

    # Initialize aiogram
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()

    # Register command handlers
    @dp.message(Command("start"))
    async def cmd_start(message: types.Message) -> None:
        await message.answer(
            handle_start(),
            reply_markup=get_start_keyboard(),
        )

    @dp.message(Command("help"))
    async def cmd_help(message: types.Message) -> None:
        await message.answer(handle_help())

    @dp.message(Command("health"))
    async def cmd_health(message: types.Message) -> None:
        response = await handle_health(api_client)
        await message.answer(response)

    @dp.message(Command("scores"))
    async def cmd_scores(message: types.Message, command: CommandObject) -> None:
        lab_id = command.args if command.args else None
        response = await handle_scores(api_client, lab_id)
        await message.answer(response)

    @dp.message(Command("labs"))
    async def cmd_labs(message: types.Message) -> None:
        response = await handle_labs(api_client)
        await message.answer(response)

    # Register callback query handler for inline buttons
    @dp.callback_query()
    async def handle_callback(callback: types.CallbackQuery) -> None:
        """Handle inline button callbacks."""
        data = callback.data
        response = ""

        if data == "labs":
            response = await handle_labs(api_client)
        elif data == "help":
            response = handle_help()
        elif data.startswith("scores_"):
            lab_id = data.replace("scores_", "")
            response = await handle_scores(api_client, lab_id)
        elif data.startswith("pass_rates_"):
            lab_id = data.replace("pass_rates_", "")
            response = await handle_scores(api_client, lab_id)  # Reuse scores handler for now
        elif data.startswith("top_"):
            lab_id = data.replace("top_", "")
            response = await handle_scores(api_client, lab_id)  # Will be updated
        elif data == "lowest_pass_rate":
            # Use LLM router for this complex query
            response = await router.route("which lab has the lowest pass rate?")

        if response:
            await callback.message.answer(response)

        await callback.answer()

    # Register message handler for natural language queries
    @dp.message()
    async def handle_message(message: types.Message) -> None:
        """Handle natural language messages."""
        if not message.text:
            return

        user_text = message.text.strip()

        # Use the intent router for natural language processing
        response = await router.route(user_text)
        await message.answer(response)

    # Start polling
    await dp.start_polling(bot)

    # Cleanup
    await bot.session.close()
    await api_client.close()
    await llm_client.close()


async def main() -> None:
    """Main entry point."""
    args = parse_args()

    if args.test:
        await run_test_mode(args.test)
    else:
        await run_telegram_mode()


if __name__ == "__main__":
    asyncio.run(main())
