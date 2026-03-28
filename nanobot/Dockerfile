# syntax=docker/dockerfile:1

# Multi-stage build for nanobot gateway

# ------------------------------------------------------------------------------
# Builder stage
# ------------------------------------------------------------------------------
FROM astral/uv:python3.14-bookworm-slim AS builder

WORKDIR /app

# Copy dependency files from workspace root
COPY --from=workspace pyproject.toml uv.lock ./

# Copy mcp source for lms-mcp dependency
COPY --from=workspace mcp /app/mcp

# Copy nanobot-websocket-channel packages
COPY --from=workspace nanobot-websocket-channel/nanobot-channel-protocol /app/nanobot-websocket-channel/nanobot-channel-protocol
COPY --from=workspace nanobot-websocket-channel/nanobot-webchat /app/nanobot-websocket-channel/nanobot-webchat

# Copy nanobot source
COPY pyproject.toml /app/nanobot/pyproject.toml

# Sync all dependencies including nanobot-webchat and lms-mcp
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-dev

# Copy rest of nanobot source
COPY . /app/nanobot/

# ------------------------------------------------------------------------------
# Runtime stage
# ------------------------------------------------------------------------------
FROM python:3.14.2-slim-bookworm

# Create non-root user
RUN groupadd --system --gid 999 nonroot \
    && useradd --system --gid 999 --uid 999 --create-home nonroot

# Copy everything from builder
COPY --from=builder --chown=nonroot:nonroot /app/.venv /app/.venv
COPY --from=builder --chown=nonroot:nonroot /app/nanobot /app/nanobot
# Copy mcp and nanobot-websocket-channel for editable installs
COPY --from=builder --chown=nonroot:nonroot /app/mcp /app/mcp
COPY --from=builder --chown=nonroot:nonroot /app/nanobot-websocket-channel /app/nanobot-websocket-channel

# Add venv to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Create workspace directory
RUN mkdir -p /app/nanobot/workspace && chown nonroot:nonroot /app/nanobot/workspace

WORKDIR /app/nanobot

# Switch to non-root user
USER nonroot

# Run entrypoint
CMD ["python", "/app/nanobot/entrypoint.py"]
