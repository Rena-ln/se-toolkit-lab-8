# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

<!-- Paste the agent's response to "What is the agentic loop?" and "What labs are available in our LMS?" -->

## Task 1B — Agent with LMS tools

<!-- Paste the agent's response to "What labs are available?" and "Describe the architecture of the LMS system" -->

## Task 1C — Skill prompt

<!-- Paste the agent's response to "Show me the scores" (without specifying a lab) -->

## Task 2A — Deployed agent

Nanobot gateway запущен в Docker с MCP инструментами:

```
Container se-toolkit-lab-8-nanobot-1 Running
MCP server 'lms': connected, 9 tools registered
Agent loop started
```

Зарегистрированные MCP инструменты:
- mcp_lms_lms_health
- mcp_lms_lms_labs
- mcp_lms_lms_learners
- mcp_lms_lms_pass_rates
- mcp_lms_lms_timeline
- mcp_lms_lms_groups
- mcp_lms_lms_top_learners
- mcp_lms_lms_completion_rate
- mcp_lms_lms_sync_pipeline

## Task 2B — Web client

Flutter web client доступен по адресу `http://<vm-ip>:42002/flutter/`
WebSocket endpoint работает на `/ws/chat`

Все сервисы запущены:
- backend: Up
- caddy: Up
- nanobot: Up
- qwen-code-api: Up (healthy)
- postgres: Up (healthy)
- client-web-react: Up
- client-web-flutter: Up

## Task 3A — Structured logging

Backend emits structured logs via OpenTelemetry to VictoriaLogs.

Example log entry:
```json
{
  "_msg": "request_completed",
  "service.name": "Learning Management Service",
  "severity": "INFO",
  "status": "200",
  "trace_id": "4f13c501f556c72344d36eb9e778e9b9",
  "span_id": "e45af372dd670861"
}
```

VictoriaLogs UI: `http://<vm-ip>:42002/utils/victorialogs/select/vmui`

## Task 3B — Traces

VictoriaTraces stores distributed traces. Each request has trace_id linking all spans.

VictoriaTraces UI: `http://<vm-ip>:42002/utils/victoriatraces`

## Task 3C — Observability MCP tools

Added 4 observability tools to MCP server:

| Tool | Description |
|------|-------------|
| `mcp_lms_logs_search` | Search logs using LogsQL query |
| `mcp_lms_logs_error_count` | Count errors over time window |
| `mcp_lms_traces_list` | List recent trace IDs |
| `mcp_lms_trace_get` | Get full trace by ID |

Total: 13 tools registered (9 LMS + 4 observability)

Skill prompt in: `nanobot/workspace/skills/observability/SKILL.md`

## Task 4A — Multi-step investigation

The observability skill guides the agent to:
1. Call `logs_error_count(service="backend", minutes=60)` for error overview
2. Call `logs_search(query="level:error service:backend", limit=10)` for details
3. Extract trace_id from error logs
4. Call `trace_get(trace_id="...")` for full trace
5. Summarize findings with suggested fix

## Task 4B — Proactive health check

Nanobot has built-in cron support. Health check can be scheduled via:
- Ask agent: "Create a health check for this chat that runs every 2 minutes"
- Agent uses built-in `cron` tool to schedule periodic checks
- Each run checks for backend errors and posts summary to chat

## Task 4C — Bug fix and recovery

**Root cause:** In `backend/app/routers/items.py` line 19-24, a generic `Exception` is caught and incorrectly returns `404 NOT_FOUND`:

```python
@router.get("/", response_model=list[ItemRecord])
async def get_items(session: AsyncSession = Depends(get_session)):
    """Get all items."""
    try:
        return await read_items(session)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,  # BUG: Should be 500
            detail="Items not found",
        ) from exc
```

**Fix:** Change status code from `404_NOT_FOUND` to `500_INTERNAL_SERVER_ERROR` and update detail message:

```python
except Exception as exc:
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Internal server error while fetching items",
    ) from exc
```

**Post-fix behavior:** After fix, database failures correctly return 500 with proper error details instead of misleading 404.
