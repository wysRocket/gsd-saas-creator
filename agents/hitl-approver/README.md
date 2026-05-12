# hitl-approver

Human-in-the-Loop (HITL) review service for the gsd-saas-creator pipeline.

Uses the [OpenRouter HITL tools API](https://openrouter.ai/announcements/human-in-the-loop-tools)
to give an AI reviewer the ability to either **auto-approve** routine cases or
**pause and wait for a human** on high-stakes decisions.

## How it works

1. A pipeline agent (PM, QA, DevOps) calls the `/review` endpoint with a
   review type and payload.
2. The service starts an OpenRouter model session with the appropriate HITL tool.
3. The model inspects the payload and either:
   - **Auto-resolves**: the `onToolCalled` hook returns a value → session
     completes immediately with `status: completed`.
   - **Pauses for human**: the hook returns `null` → session stays at
     `status: awaiting_hitl` and the pending tool call is surfaced.
4. A human POSTs their decision to `/review/:id/respond`.
5. The service resumes the model session via `callModel` with the human's
   response as a `function_call_output`, completing the session.

## Review types

| Type | Auto-approve condition | Always escalates? |
|------|----------------------|-------------------|
| `brief` | quality_score ≥ 80 AND word_count ≥ 300 AND no template placeholders | No |
| `deployment` | — | **Yes** (every deploy requires sign-off) |
| `qa_failure` | failures are non-critical npm test stubs only | No |

## Setup

```bash
cd agents/hitl-approver
cp .env.example .env
# Fill in OPENROUTER_API_KEY and optionally HITL_API_SECRET
npm install
npm run dev
```

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENROUTER_API_KEY` | — | **Required.** Your OpenRouter API key. |
| `HITL_MODEL` | `openai/gpt-4o-mini` | Model used by the reviewer agent. |
| `PORT` | `3456` | HTTP port to listen on. |
| `HITL_API_SECRET` | *(empty)* | If set, all requests must include `Authorization: Bearer <secret>`. |

## API

### `POST /review`

Start a new review session.

```bash
curl -X POST http://localhost:3456/review \
  -H "Content-Type: application/json" \
  -d '{
    "type": "brief",
    "payload": {
      "project_name": "TaskFlow Pro",
      "brief_content": "## Overview\n...",
      "competitor_url": "https://asana.com",
      "word_count": 450
    }
  }'
```

Response:
```json
{
  "session_id": "abc123",
  "status": "completed",
  "result": { "approved": true, "feedback": "", "quality_score": 87 }
}
```

Or if human review needed:
```json
{
  "session_id": "abc123",
  "status": "awaiting_hitl",
  "pending_calls": [{ "call_id": "call_xyz", "name": "review_brief", "arguments": {...} }]
}
```

### `GET /review/:id`

Get session status. Same response shape as POST.

### `POST /review/:id/respond`

Submit a human decision to resume the paused session.

```bash
# Approve
curl -X POST http://localhost:3456/review/abc123/respond \
  -H "Content-Type: application/json" \
  -d '{ "call_id": "call_xyz", "decision": { "approved": true, "feedback": "LGTM", "quality_score": 85 } }'

# Reject
curl -X POST http://localhost:3456/review/abc123/respond \
  -H "Content-Type: application/json" \
  -d '{ "call_id": "call_xyz", "decision": { "approved": false, "feedback": "Needs more competitor analysis", "quality_score": 55 } }'
```

## Pipeline integration

The Python pipeline agents call this service via three tool functions in
`agents/saas-pipeline/app/tools/pipeline_tools.py`:

- `request_brief_review(project_name, brief_content, competitor_url, word_count)`
- `request_deployment_approval(repo_name, project_name, firebase_project, qa_summary)`
- `request_qa_review(repo_name, stage, failures, qa_output)`

These functions block until a decision is available (polling at
`HITL_POLL_INTERVAL_SECONDS`, up to `HITL_POLL_TIMEOUT_SECONDS`).

Configure the pipeline to reach this service:

```env
# agents/saas-pipeline/.env
HITL_APPROVER_URL=http://localhost:3456
HITL_API_SECRET=your-secret-here
```

## Development

```bash
npm run dev      # ts-node watch mode
npm run build    # compile to dist/
npm run typecheck # type-check only
```
