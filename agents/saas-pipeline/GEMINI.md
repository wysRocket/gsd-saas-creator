# Coding Agent Guide — saas-pipeline

## Project Purpose

This is the **SaaS Pipeline Orchestrator** — a multi-agent ADK project that automates
the full SaaS creation workflow from a GitHub Projects board item to a live deployed app.

## Architecture

```
root_agent (orchestrator)
├── pm_agent          — reads board item, runs generate_brief.py
├── stitch_agent      — runs extract_dna.py for Stitch design tokens
├── engineer_agent    — runs render_templates.py + scaffold.py
├── qa_agent          — runs agent_workflow.py + npm test
└── devops_agent      — runs deploy.py + advances board stage
```

Each sub-agent wraps one or more scripts from `../../scripts/`.

## Agent Directory

All agent code lives in `app/`. The root orchestrator is `app/agent.py`.

## Prerequisites

```bash
uv tool install google-agents-cli
cd agents/saas-pipeline
agents-cli install
```

## Development Commands

| Command | Purpose |
|---------|----------|
| `agents-cli playground` | Interactive local testing |
| `agents-cli run "brief for MyApp"` | Quick smoke test |
| `agents-cli eval run` | Run evaluation suite |
| `agents-cli lint` | Check code quality |

## Environment Variables

Copy `.env.example` to `.env` and fill in all values before running locally.

## Pipeline Stages

1. **brief** — `pm_agent` generates `brief.md` from board item
2. **design_dna** — `stitch_agent` extracts design tokens from Stitch
3. **design_md** — `engineer_agent` generates `design.md`
4. **stitch_prompt** — `engineer_agent` generates `stitch-prompt.md`
5. **architecture** — `engineer_agent` generates `ARCHITECTURE.md`
6. **code** — `engineer_agent` runs `scaffold.py`
7. **qa** — `qa_agent` validates all artifacts + runs tests
8. **deploy** — `devops_agent` deploys to Firebase + advances board

## Operational Guidelines

- **Code preservation**: Only modify code directly targeted by the request.
- **NEVER change the model** unless explicitly asked.
- **Run Python with `uv`**: `uv run python script.py`
- **Stop on repeated errors**: Fix root cause instead of retrying.
