# SPEC.md — SaaS Pipeline Orchestrator

**Version:** 1.0.0
**Kind:** System Specification
**Status:** Active

> This is the **source of truth** for the SaaS Pipeline multi-agent system.
> Agent instructions in `.md` files are generated from this spec.
> Changes to agent behavior MUST be reflected here first.

---

## 1. System Overview

The SaaS Pipeline transforms a GitHub Projects board item into a deployed Next.js + Firebase SaaS application through five automated stages. Each stage is owned by a named agent.

### Pipeline Architecture

```
GitHub Projects Board (Stage change webhook)
    │
    ▼
@pm_agent          ──→ brief.md
    │
    ▼
@stitch_agent     ──→ design DNA / designlang artifacts
    │
    ▼
@engineer_agent    ──→ design.md → stitch-prompt.md → src/ (scaffold)
    │
    ▼
@qa_agent          ──→ pipeline-events.jsonl (validation log)
    │
    ▼
@devops_agent      ──→ Firebase deploy → board advanced to 'launched'
```

### Agents Directory

| Agent | File | Owns |
|-------|------|------|
| `@pm` | `app/pm_agent.py` | `brief` stage |
| `@stitch` | `app/stitch_agent.py` | `design_dna` stage |
| `@engineer` | `app/engineer_agent.py` | `design_md`, `stitch_prompt`, `code` stages |
| `@qa` | `app/qa_agent.py` | `qa` stage |
| `@devops` | `app/devops_agent.py` | `deploy` stage |
| `@monitor` | `app/monitor_agent.py` | Board polling |

---

## 2. Stage Contracts

Each stage has:
- **Inputs**: files or data required to start
- **Outputs**: files produced
- **Gates**: validation checks that must pass before advancing
- **Halts**: conditions that stop the pipeline

### Stage: `brief`

| Field | Value |
|-------|-------|
| Owner | `@pm` |
| Trigger | Board item moved to `Brief` |
| Inputs | `brief.md`, competitor design-language.md |
| Outputs | `brief.md` |
| Gate | `agent_workflow.py validate-stage brief` |

**Gates (must all pass):**
- `brief_present` — brief.md ≥ 200 chars
- `no_template_placeholders` — no `[...]` or `{{...}}` remaining

**Artifact contract (`brief.md`):**
```
# {project_name}

## Overview
One paragraph description of the SaaS.

## Target User
Who uses this, and why now.

## Core Value
The single most important benefit.

## Core Feature Set
- Feature 1
- Feature 2
- Feature 3

## Positioning
How this differs from {competitor_url}

## Pricing
Free / $X/mo / Enterprise

## Technical Stack
Next.js 14, Firebase, shadcn/ui
```

---

### Stage: `design_dna`

| Field | Value |
|-------|-------|
| Owner | `@stitch` |
| Trigger | `brief.md` exists |
| Inputs | `brief.md`, competitor URL |
| Outputs | `design/competitor-design-language.md`, `design/design-tokens.json` |

**Gates:**
- `design_language_md` ≥ 500 chars
- At least 3 hex colors present
- At least 2 font families present

---

### Stage: `design_md`

| Field | Value |
|-------|-------|
| Owner | `@engineer` |
| Trigger | `design_dna` complete |
| Inputs | `brief.md`, `design/competitor-design-language.md`, `templates/design-template.md` |
| Outputs | `design.md` |
| Gate | `agent_workflow.py validate-stage design_md` |

**Gates:**
- `design_md_present` — design.md ≥ 600 chars
- `no_template_placeholders` — no `[...]` or `{{...}}` remaining
- `real_design_tokens` — ≥ 3 hex colors, ≥ 1 font, no empty token values
- `designlang_reference_present` — design.md mentions design-language.md source

**Artifact contract (`design.md`):**
```
# Design.md — {project_name}

## Design Language
Colors, typography, spacing system

## Layout & Structure
Page hierarchy and responsive strategy

## Features & Interactions
Core user flows with behavior specs

## Component Inventory
Named components with visual and interaction specs

## Technical Approach
Next.js 14 + Firebase + shadcn/ui + Tailwind
```

---

### Stage: `stitch_prompt`

| Field | Value |
|-------|-------|
| Owner | `@engineer` |
| Trigger | `design_md` gate passes |
| Inputs | `brief.md`, `design.md`, `design/competitor-design-language.md`, `templates/stitch-template.md` |
| Outputs | `stitch-prompt.md` |
| Gate | `agent_workflow.py validate-stage stitch_prompt` |

**Gates:**
- `stitch_prompt_present` — stitch-prompt.md ≥ 600 chars
- `no_template_placeholders`
- `stitch_uses_design_md` — stitch-prompt.md references design.md

**Idempotency:** Supports `--force` to regenerate. Without `--force`, skips if output exists.

---

### Stage: `qa`

| Field | Value |
|-------|-------|
| Owner | `@qa` |
| Trigger | `stitch_prompt` gate passes |
| Inputs | `brief.md`, `design.md`, `stitch-prompt.md` |
| Outputs | `pipeline-events.jsonl` |
| Gate | All three artifact checks pass |

**Gates:**
- `artifact_set_complete` — all three files exist
- `run_npm_tests` — `npm test` passes (non-blocking, logged)

**QA failure behavior:**
- Post ❌ comment on GitHub issue with failure details
- Do NOT advance board stage
- Board stays in `qa` until human moves to `revisions`

---

### Stage: `deploy`

| Field | Value |
|-------|-------|
| Owner | `@devops` |
| Trigger | `qa` gate passes |
| Inputs | `brief.md`, `design.md`, `stitch-prompt.md`, `src/` |
| Outputs | Live Firebase URL, board `Deploy URL` field set |
| Gate | Firebase deploy succeeds |

**Behavior:**
1. Create GitHub repo if not exists (`SaaS-Pretty-Projects/{repo_name}`)
2. Clone repo
3. Run `scaffold.py` with design tokens
4. Commit and push
5. Set `Repo URL` field on board item
6. Deploy to Firebase
7. Set `Deploy URL` field on board item
8. Advance board to `In Progress`

---

## 3. Agent Specifications

### A. `@pm_agent`

**Role:** Product Manager
**File:** `app/pm_agent.py`
**Model:** `gemini-flash-latest` (configurable via `GEMINI_MODEL` env)

**Responsibility:** Translate a GitHub Projects board item into a structured `brief.md`.

**Inputs (from payload):**
- `project_name` — board item title or explicit field
- `competitor_url` — `Competitor URL` board field
- `vertical` — `Vertical` board field (Hosting, Gaming, Digital Goods, Education, Career)
- `repo_dir` — computed as `PIPELINE_OUTPUT_DIR/<project_name>`

**Tools:**
- `generate_brief` — calls `scripts/generate_brief.py`
- `validate_stage` — calls `agent_workflow.py validate-stage brief`
- `get_board_item_fields` — reads board item via GraphQL

**Behavior:**
1. Extract board item fields
2. Call `generate_brief(project_name, competitor_url, vertical, repo_dir)`
3. Call `validate_stage(brief, repo_dir)`
4. If either fails: report error and HALT
5. Report brief.md path, word count, key decisions made

**Halts on:**
- `generate_brief` subprocess error
- `validate_stage` returns failures
- `competitor_url` is empty

---

### B. `@stitch_agent`

**Role:** Design DNA Extractor
**File:** `app/stitch_agent.py`
**Model:** `gemini-flash-latest`

**Responsibility:** Run Stitch MCP to extract visual design tokens from a competitor URL.

**Tools:**
- `run_designlang` — runs `npx designlang <url> --full --screenshots --out ./design`
- `extract_stitch_dna` — calls Stitch MCP for token extraction

**Behavior:**
1. Run designlang on competitor URL
2. Save output to `repo_dir/design/`
3. Validate at least 3 colors + 2 fonts extracted
4. Report artifacts produced

**Halts on:** designlang produces < 3 colors or < 500 chars total

---

### C. `@engineer_agent`

**Role:** Software Engineer
**File:** `app/engineer_agent.py`
**Model:** `gemini-flash-latest`

**Responsibility:** Translate brief + design tokens into `design.md`, `stitch-prompt.md`, and full application scaffold.

**Tools:**
- `generate_design_md` — calls `scripts/generate_design_md.py`
- `generate_stitch_prompt` — calls `scripts/generate_stitch_prompt.py` (supports `--force`)
- `scaffold_project` — calls `scripts/scaffold.py`
- `validate_stage` — calls `agent_workflow.py validate-stage <stage>`

**Behavior (enforced order):**
1. `generate_design_md` → `validate_stage(design_md)`
2. IF design_md validation fails → HALT, report failures
3. `generate_stitch_prompt [--force]` → `validate_stage(stitch_prompt)`
4. IF stitch_prompt validation fails → HALT
5. `scaffold_project(project_name, repo_dir, design_tokens_path)`
6. Report scaffold summary: files created, colors, fonts, component count

**Halts on:**
- Any `validate_stage` failure with specific error details
- `scaffold_project` error (best-effort scaffold, continue anyway but log)

**Idempotency:** `generate_stitch_prompt` MUST be called with `--force` only when human explicitly requests regeneration. Without `--force`, the script skips if `stitch-prompt.md` exists and is non-empty.

---

### D. `@qa_agent`

**Role:** Quality Assurance
**File:** `app/qa_agent.py`
**Model:** `gemini-flash-latest`

**Responsibility:** Validate all pipeline artifacts before deployment.

**Tools:**
- `validate_all_stages` — calls `agent_workflow.py status --repo-dir <repo_dir>`
- `run_npm_tests` — runs `npm test` in the scaffolded project
- `post_github_issue_comment` — posts comment on GitHub issue

**Behavior:**
1. Call `validate_all_stages`
2. Call `run_npm_tests` (non-blocking — failures logged but don't halt)
3. If any critical validation fails:
   - Post ❌ comment on GitHub issue with failure details
   - Do NOT advance board stage
   - HALT pipeline
4. If all pass: post ✅ comment, report "QA PASSED"

**Critical failures (must halt):**
- Any `required_inputs` file missing
- Any `required_outputs` file missing
- `no_template_placeholders` check fails
- `real_design_tokens` check fails

**Non-critical (logged, reported, but don't halt):**
- `run_npm_tests` failures (scaffold tests may be stubs)

---

### E. `@devops_agent`

**Role:** DevOps Engineer
**File:** `app/devops_agent.py`
**Model:** `gemini-flash-latest`

**Responsibility:** Create the GitHub repo, push scaffold, deploy to Firebase, update board.

**Tools:**
- `create_and_push_repo` — creates GitHub repo, clones, copies scaffold, commits, pushes
- `deploy_to_firebase` — runs Firebase deploy
- `update_board_field` — sets `Repo URL` and `Deploy URL` fields on board
- `advance_board_stage` — moves board item to next stage

**Behavior (in order):**
1. `create_and_push_repo(org, repo_name, project_name, repo_dir)`
   - `gh repo create SaaS-Pretty-Projects/{repo_name} --public`
   - Clone into temp dir
   - Copy scaffold output to clone
   - `git add -A && git commit && git push origin main`
2. `update_board_field(Repo URL, https://github.com/SaaS-Pretty-Projects/{repo_name})`
3. `deploy_to_firebase(repo_name)` — triggers GitHub Actions workflow
4. `update_board_field(Deploy URL, <firebase_url>)`
5. `advance_board_stage(In Progress)`
6. Post ✅ comment: live URL + next steps

**Repo creation:** Always use `--public`. If repo exists, `gh repo create` silently succeeds (idempotent).

**Halts on:** GitHub repo creation/push failure (cannot proceed without a repo).

---

## 4. Data Contracts

### Board Item Fields (Project v2)

| Field | ID | Type |
|-------|-----|------|
| Stage | `PVTSSF_lADOEHzfoM4BU-0MzhQD56k` | Single-select |
| Vertical | `PVTSSF_lADOEHzfoM4BU-0MzhQhuNE` | Single-select |
| Competitor URL | `PVTF_lADOEHzfoM4BU-0MzhQv9f8` | Text |
| Repo URL | `PVTF_lADOEHzfoM4BU-0MzhQhuOI` | Text |
| AI Studio | `PVTF_lADOEHzfoM4BU-0MzhQtV7M` | Text |
| Deploy URL | `PVTF_lADOEHzfoM4BU-0MzhQv9gA` | Text |

### Stage Option IDs

| Stage | Option ID |
|-------|-----------|
| Brief | `cddac2f5` |
| Clarification | `0d90f5af` |
| Design.md | `67a099a3` |
| STITCH Prompt | `e471f317` |
| Designs Ready | `5339ae55` |
| AI Studio | `cda08427` |
| In Progress | `58cac058` |
| Revisions | `e7d47d45` |
| Ready for Prod | `5198760c` |
| Launched | `f01a3972` |
| Operating | `79fb3f03` |
| Done | `c15f4a82` |

### Vertical Option IDs

| Vertical | Option ID |
|----------|-----------|
| Hosting | `56a9c75a` |
| Gaming | `a263f297` |
| Digital Goods | `9bdacda3` |
| Education | `817d2a42` |
| Career | `79fc421b` |

---

## 5. Error Handling

### Transient Failures (retry automatically)
- GitHub API rate-limit (429) — webhook `dispatchStageChange` retries 3x with backoff
- Network timeouts — each generator retries once

### Permanent Failures (halt, human intervenes)
- `validate_stage` returns failures — board stays at current stage, human moves to `revisions`
- Missing required inputs — halt before generation attempt
- GitHub repo creation fails (auth error) — halt, report

### Human-Gate Stages (pipeline halts, waits for human)
- `STITCH Prompt` — human completes STITCH work in Figma, moves to `Designs Ready`
- `Designs Ready` — human reviews Figma board, moves to `AI Studio`
- `AI Studio` — human runs AI Studio, moves to `In Progress`
- `In Progress` — human reviews scaffold, moves to `Ready for Prod`
- `Revisions` — human edits files, moves back to the appropriate stage

---

## 6. Observability

### Pipeline Event Log

Each stage writes a JSONL entry to `<repo_dir>/pipeline-events.jsonl`:
```json
{"timestamp": "2026-05-04T12:00:00Z", "stage": "brief", "status": "completed", "message": "brief.md generated"}
{"timestamp": "2026-05-04T12:01:00Z", "stage": "design_md", "status": "failed", "message": "validation failed", "details": {"failures": ["..."]}}
```

### Board Status Script

```bash
python3 scripts/board_status.py              # snapshot
python3 scripts/board_status.py --stuck        # stuck items
python3 scripts/board_status.py --by-stage    # pipeline view
python3 scripts/board_status.py --watch       # 60s polling
```

### Nudge Cron

`stitch-prompt-nudge` runs every 24h — posts reminder comment on items stuck at `STITCH Prompt`.

### Contract Drift Checker

```bash
python3 scripts/contract_drift_check.py -v    # verify spec vs implementation
```

---

## 7. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-05-03 | Initial spec. 5 agents (pm, stitch, engineer, qa, devops). Stage contracts defined. Gap #6 (scaffold wiring) implemented. |
