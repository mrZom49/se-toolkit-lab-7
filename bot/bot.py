#!/usr/bin/env python3
"""LMS Bot entry point.

Supports two modes:
1. Test mode: `uv run bot.py --test "/command"` - prints response to stdout
2. Telegram mode: `uv run bot.py` - runs the Telegram bot
"""

import argparse
import asyncio
import sys
from pathlib import Path

# Add bot directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandObject

from config import load_settings
from handlers import (
    handle_start,
    handle_help,
    handle_health,
    handle_scores,
    handle_labs,
)
from services import LMSAPIClient, LLMClient


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


def route_command(command: str, args: str | None = None) -> str:
    """Route a command to the appropriate handler.
    
    Args:
        command: The command name (without leading /).
        args: Optional command arguments.
        
    Returns:
        Handler response text.
    """
    if command == "start":
        return handle_start()
    elif command == "help":
        return handle_help()
    elif command == "health":
        return handle_health()
    elif command == "scores":
        return handle_scores(args)
    elif command == "labs":
        return handle_labs()
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
    
    # Handle natural language input - map to commands
    input_lower = user_input.lower()
    if "lab" in input_lower and ("available" in input_lower or "what" in input_lower):
        return "labs", None
    if "score" in input_lower:
        # Try to extract lab id
        parts = input_lower.split()
        for i, part in enumerate(parts):
            if part.startswith("lab"):
                return "scores", part
        return "scores", None
    if "help" in input_lower:
        return "help", None
    
    # Default to unknown
    return "unknown", user_input


async def run_test_mode(user_input: str) -> None:
    """Run the bot in test mode.
    
    Args:
        user_input: The input to process.
    """
    # Load settings (for API configuration)
    settings = load_settings()
    
    # Parse input and route to handler
    command, args = parse_test_input(user_input)
    response = route_command(command, args)
    
    # Print response to stdout
    print(response)


async def run_telegram_mode() -> None:
    """Run the bot in Telegram mode."""
    settings = load_settings()
    settings.validate_for_telegram()
    
    # Initialize services
    lms_client = LMSAPIClient(settings.lms_api_base_url, settings.lms_api_key)
    llm_client = LLMClient(settings.llm_api_base_url, settings.llm_api_key)
    
    # Initialize aiogram
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()
    
    # Register command handlers
    @dp.message(Command("start"))
    async def cmd_start(message: types.Message) -> None:
        await message.answer(handle_start())
    
    @dp.message(Command("help"))
    async def cmd_help(message: types.Message) -> None:
        await message.answer(handle_help())
    
    @dp.message(Command("health"))
    async def cmd_health(message: types.Message) -> None:
        await message.answer(handle_health())
    
    @dp.message(Command("scores"))
    async def cmd_scores(message: types.Message, command: CommandObject) -> None:
        lab_id = command.args if command.args else None
        await message.answer(handle_scores(lab_id))
    
    @dp.message(Command("labs"))
    async def cmd_labs(message: types.Message) -> None:
        await message.answer(handle_labs())
    
    # Start polling
    await dp.start_polling(bot)
    
    # Cleanup
    await bot.session.close()
    await lms_client.close()
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
