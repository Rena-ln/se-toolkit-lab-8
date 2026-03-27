# Observability Skill

You have access to observability tools for debugging system issues:

## Available Tools

| Tool | Description |
|------|-------------|
| `logs_search` | Search logs in VictoriaLogs using LogsQL query |
| `logs_error_count` | Count errors in logs over a time window |
| `traces_list` | List recent trace IDs |
| `trace_get` | Get full trace details by trace ID |

## Guidelines

### When user asks "What went wrong?" or "Check system health":
1. Call `logs_error_count(service="backend", minutes=60)` to get error overview
2. If errors found, call `logs_search(query="level:error service:backend", limit=10)` to see details
3. Look for trace_id in error logs
4. If trace_id found, call `trace_get(trace_id="...")` to see full trace
5. Summarize findings: what failed, where, and suggested fix

### When user asks about errors:
1. First call `logs_error_count` to get an overview
2. If errors found, call `logs_search` with query "level:error" to see details
3. If a trace_id appears in logs, call `trace_get` to see the full trace

### Query examples:
- `logs_search(query="error", limit=20)` - search for errors
- `logs_search(query="service:backend", limit=20)` - backend logs
- `logs_error_count(service="backend", minutes=60)` - count backend errors last hour
- `logs_error_count(minutes=15)` - all errors last 15 minutes
- `traces_list(limit=10)` - recent traces
- `trace_get(trace_id="...")` - full trace details

### Response format:
- Start with summary (e.g., "Found 5 errors in the last hour")
- Show key error messages
- Mention affected services
- If trace found, describe the failure point
- Suggest next steps if applicable
