# Bot Dockerfile using astral/uv base image
# See: https://docs.astral.sh/uv/guides/integration/docker/

ARG REGISTRY_PREFIX=harbor.pg.innopolis.university/docker-hub-cache/
FROM ${REGISTRY_PREFIX}astral/uv:python3.14-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_NO_DEV=1
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Copy bot pyproject.toml and sync its dependencies
COPY bot/pyproject.toml ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-dev

# Copy bot source code
COPY bot/ ./bot/

# ---
# Stage 2: final image
# ---

ARG REGISTRY_PREFIX=harbor.pg.innopolis.university/docker-hub-cache/
FROM ${REGISTRY_PREFIX}python:3.14.2-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8
ENV PYTHONPATH=/app

# Setup non-root user
RUN groupadd --system --gid 999 nonroot \
    && useradd --system --gid 999 --uid 999 --create-home nonroot

# Copy application from builder
COPY --from=builder --chown=nonroot:nonroot /app /app

# Add venv to PATH
ENV PATH="/app/.venv/bin:$PATH"

USER nonroot
WORKDIR /app

# Run bot with unbuffered output for proper logging
CMD ["python", "-u", "bot/bot.py"]
