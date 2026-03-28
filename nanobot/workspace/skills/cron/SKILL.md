# Cron Skill — Scheduled Health Checks

You have access to a **cron tool** that can schedule recurring jobs. Use this to proactively monitor system health.

## Available Cron Actions

When the user asks you to create a scheduled health check, you can create a cron job that:
1. Runs at a specified interval (e.g., every 15 minutes)
2. Checks for backend errors using `logs_error_count`
3. Posts a summary to the current chat

## How to Create a Health Check Job

When the user says something like:
- "Create a health check that runs every 15 minutes"
- "Monitor the system and report errors"
- "Set up a scheduled job to check for errors"

You should:
1. **Confirm the schedule** — Ask or confirm the interval (e.g., "every 15 minutes")
2. **Confirm the chat** — The job will post to the current chat session
3. **Create the job** — Use your built-in cron tool to schedule:
   - A job that calls `logs_error_count(service="backend", minutes=<interval>)`
   - If errors found, call `logs_search(query="level:error", limit=5)` for details
   - Post a summary like: "Health check: No errors in the last 15 minutes" or "Health check: Found 3 errors in the last 15 minutes"

## Example Cron Job Configuration

```
Schedule: */15 * * * *  (every 15 minutes)
Action: Check backend errors, post summary to chat
```

## Listing Scheduled Jobs

When the user asks "What jobs are scheduled?" or "List scheduled jobs":
- Use your cron tool to list all active jobs
- Show the schedule and purpose of each job

## Removing Jobs

When the user asks to remove a scheduled job:
- Use your cron tool to cancel/delete the job
- Confirm the job was removed

## Example Interactions

**User**: "Create a health check for this chat that runs every 15 minutes."

**You**: "I'll create a scheduled health check that runs every 15 minutes. Each run will check for backend errors in the last 15 minutes and post a summary here. If there are no recent errors, I'll report that the system looks healthy."

[Creates cron job]

"Done! I've scheduled a health check that runs every 15 minutes. You can ask me to list scheduled jobs or remove this job anytime."

---

**User**: "List scheduled jobs."

**You**: "You have 1 scheduled job:
- Health Check: Runs every 15 minutes, checks backend errors, posts to this chat"

---

**User**: "Remove the health check job."

**You**: "I've removed the scheduled health check job. It will no longer run."
