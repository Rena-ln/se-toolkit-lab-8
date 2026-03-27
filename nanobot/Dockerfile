# syntax=docker/dockerfile:1

# Multi-stage build for nanobot gateway

# ------------------------------------------------------------------------------
# Builder stage
# ------------------------------------------------------------------------------
FROM astral/uv:python3.14-bookworm-slim AS builder

WORKDIR /app

# Copy dependency files from workspace root
COPY --from=workspace pyproject.toml uv.lock ./

# Sync nanobot-ai and lms-mcp
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

# Copy nanobot source
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

# Add venv to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Create workspace directory
RUN mkdir -p /app/nanobot/workspace && chown nonroot:nonroot /app/nanobot/workspace

WORKDIR /app/nanobot

# Switch to non-root user
USER nonroot

# Run entrypoint
CMD ["python", "/app/nanobot/entrypoint.py"]
