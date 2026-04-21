# Cloudflare Worker — SaaS Pipeline Webhook Receiver

Receives `projects_v2_item.edited` GitHub webhook events and fires a
`repository_dispatch` to `gsd-saas-creator` when a board item moves to
the **Design.md** stage. This triggers the full pipeline:
designlang → `generate_brief.py` → `generate_stitch_prompt.py`.

## Quick deploy

```bash
cd webhook-receiver
npm install

# Set secrets (one-time)
npx wrangler secret put GITHUB_WEBHOOK_SECRET
npx wrangler secret put GH_TOKEN              # PAT: repo + project + workflow scopes
npx wrangler secret put REPO_OWNER            # wysRocket
npx wrangler secret put REPO_NAME             # gsd-saas-creator

# Deploy
npm run deploy
# → prints: https://saas-pipeline-webhook.<subdomain>.workers.dev
```

## GitHub Webhook setup

1. Go to `github.com/orgs/SaaS-Pretty-Projects/settings/hooks`
2. **Add webhook**
   - **Payload URL**: `https://saas-pipeline-webhook.<subdomain>.workers.dev/webhook`
   - **Content type**: `application/json`
   - **Secret**: same value you put in `GITHUB_WEBHOOK_SECRET`
   - **Events**: Custom → tick **Projects v2 item events**
3. Save

## What it does

```
GitHub Projects board
  │  Stage field changed to "Design.md"
  │  → sends webhook to Cloudflare Worker
  ▼
Worker (this file)
  │  verifies HMAC signature
  │  fetches item fields (Competitor URL, Vertical, Repo URL…)
  │  fires repository_dispatch → gsd-saas-creator
  ▼
GitHub Action (stage-trigger.yml)
  │  runs designlang on Competitor URL
  │  runs generate_brief.py    (Gemini)
  │  runs generate_stitch_prompt.py (Gemini)
  │  pushes brief.md + stitch-prompt.md to product repo
  │  advances Stage → "STITCH Prompt" on board
```

## Local dev

```bash
npm run dev
# Use ngrok or cloudflared tunnel to expose localhost for webhook testing
```

## Required board fields

| Field | Purpose |
|---|---|
| `Competitor URL` | Triggers designlang extraction |
| `Repo URL` | Determines target org repo name |
| `Vertical` | Passed to generate_brief.py |
| `Stage` | Must include "Design.md" option |
