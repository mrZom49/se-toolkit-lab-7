# LMS Bot Development Plan

## Overview

This document outlines the development plan for the LMS (Learning Management System) Telegram Bot. The bot provides students with quick access to their academic information, lab assignments, scores, and course-related queries through a natural language interface powered by an LLM.

## Architecture

### Testable Handler Architecture (P0.1)

The core principle is **separation of concerns**: command handlers are pure functions that take input and return text responses. They have no knowledge of Telegram or any other transport layer. This allows:

- Unit testing handlers without mocking Telegram
- CLI test mode via `--test` flag
- Easy migration to other platforms (Discord, web chat) in the future

### Directory Structure

```
bot/
├── bot.py              # Entry point: Telegram startup + --test mode
├── handlers/           # Command handlers (transport-agnostic)
│   ├── __init__.py
│   ├── start.py        # /start command
│   ├── help.py         # /help command
│   ├── health.py       # /health command
│   ├── scores.py       # /scores command
│   └── labs.py         # /labs command
├── services/           # External API clients
│   ├── __init__.py
│   ├── lms_api.py      # LMS API client
│   └── llm_client.py   # LLM API client for intent routing
├── config.py           # Environment variable loading
├── pyproject.toml      # Dependencies
└── PLAN.md             # This file
```

## Development Phases

### Phase 1: Scaffold (Current Task)

Create the basic project structure with:
- `pyproject.toml` with dependencies (aiogram, httpx, pydantic-settings)
- `config.py` for loading environment variables
- Empty handler modules with placeholder responses
- `bot.py` entry point with `--test` mode support
- `.env.bot.example` template

### Phase 2: Backend Integration

Implement real handler logic:
- `/scores` handler calls LMS API to fetch student scores
- `/labs` handler retrieves available lab assignments
- `/health` handler checks backend service status
- Error handling for API failures

### Phase 3: Intent Routing with LLM

Add natural language understanding:
- LLM client service for intent classification
- Route user queries to appropriate handlers
- Support queries like "what labs are available" → `/labs` handler

### Phase 4: Deployment

- Docker configuration for bot container
- Environment setup on VM
- Logging and monitoring
- Graceful shutdown handling

## Test Mode

The `--test` flag enables offline verification:

```bash
cd bot
uv run bot.py --test "/start"        # Prints welcome message
uv run bot.py --test "/help"         # Prints command list
uv run bot.py --test "/health"       # Prints backend status
uv run bot.py --test "/scores lab-04"
```

This reads config from `.env.bot.secret` but does NOT connect to Telegram.

## Dependencies

- **aiogram**: Async Telegram Bot API framework
- **httpx**: Async HTTP client for API calls
- **pydantic-settings**: Type-safe configuration loading

## Environment Variables

Required in `.env.bot.secret`:
- `BOT_TOKEN`: Telegram bot authentication
- `LMS_API_BASE_URL`: LMS API endpoint
- `LMS_API_KEY`: LMS API authentication
- `LLM_API_KEY`: LLM service authentication
- `LLM_API_BASE_URL`: LLM service endpoint
