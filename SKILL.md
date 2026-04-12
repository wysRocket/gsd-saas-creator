---
name: saas-creator
description: "An end-to-end pipeline to move from a natural language 'vibe' to a deployed SaaS product. Orchestrates design DNA extraction via Google Stitch, code generation via Google AI Studio, and deployment via Firebase + GitHub Actions."
version: "1.0.0"
trigger: "/saas-create"
agents: ["@pm", "@engineer", "@qa", "@devops"]
halt_gates:
  - "User approval of REQUIREMENTS.md before design extraction"
  - "User approval before any cloud resource provisioning"
tools:
  - stitch_api
  - firebase_cli
  - github_cli
  - python_scripts
---

# GSD SaaS Creator

Portable Agent Skill for the **Design-to-Deployed** autonomous pipeline.

## Overview

Orchestrates a specialized team of AI agents to transform a single natural language product intent into a live, production-ready SaaS application in as little as 23 minutes.

**Pipeline**: `Vibe Prompt → Requirements → Stitch Design DNA → Architecture → Code → Tests → Deploy`

**Integrations**: Google Stitch (design) · Google AI Studio (logic) · Firebase (backend/hosting) · GitHub Actions (CI/CD)

---

## Orchestration Logic

### Phase 1: Intent & Requirements
- **Goal**: Translate user intent into a signed-off technical specification.
- **Agent**: `@pm`
- **Steps**:
  1. Interview user: capture product name, target user, core problem, key features.
  2. Generate `REQUIREMENTS.md` using `templates/REQUIREMENTS.md.j2`.
  3. Present to user for review.
- **HALT GATE**: User must explicitly approve `REQUIREMENTS.md` before proceeding.

### Phase 2: Visual DNA (Google Stitch)
- **Goal**: Extract the design system tokens and component map from Stitch.
- **Agent**: `@engineer`
- **Steps**:
  1. Run `scripts/extract_dna.py <stitch_project_id>` — produces `design_tokens.json`.
  2. Run `scripts/render_templates.py DESIGN.md` — maps tokens into `DESIGN.md`.
  3. Validate color palette, typography, and component completeness.

### Phase 3: System Architecture
- **Goal**: Define the full technical stack and data contracts.
- **Agent**: `@engineer`
- **Steps**:
  1. Define Firestore data schema (collections, documents, fields).
  2. Define Firebase Authentication flow (email/password, OAuth providers).
  3. Define API surface: Firebase Functions endpoints and payload schemas.
  4. Confirm tech stack: React/Next.js · Tailwind · Firebase · GitHub Actions.

### Phase 4: Code Generation & Testing
- **Goal**: Scaffold and validate a production-quality application.
- **Agents**: `@engineer`, `@qa`
- **Steps**:
  1. `@engineer`: Run `scripts/scaffold.py` to generate project skeleton from `DESIGN.md`.
  2. `@engineer`: Implement Firebase Functions and Firestore integration.
  3. `@qa`: Run unit tests (`npm test`) and visual regression checks.
  4. `@qa`: Verify auth flows, CRUD operations, and API error handling.
  5. Fix any blocking issues before proceeding.

### Phase 5: Deployment to Production
- **Goal**: Deliver a live URL.
- **Agent**: `@devops`
- **Steps**:
  1. Render `templates/deploy.yml.j2` into `.github/workflows/deploy.yml`.
  2. Push code to GitHub repository.
- **HALT GATE**: User must approve before cloud resource provisioning.
  3. Run `scripts/deploy.py` to provision Firebase project and Hostinger webhook.
  4. Trigger GitHub Actions — confirm green deploy.
  5. Return live URL to user.

---

## Tooling

| Tool | Purpose |
|---|---|
| `scripts/extract_dna.py` | Pull design tokens from Stitch API |
| `scripts/render_templates.py` | Render Jinja2 templates with extracted data |
| `scripts/scaffold.py` | Generate project skeleton from DESIGN.md |
| `scripts/deploy.py` | Provision Firebase + trigger deployment |
| `templates/DESIGN.md.j2` | Design DNA document template |
| `templates/REQUIREMENTS.md.j2` | Requirements document template |
| `templates/deploy.yml.j2` | GitHub Actions CI/CD workflow template |
| `reference/firebase_security_rules.txt` | Baseline Firestore security rules |
| `reference/stitch_schema.json` | Stitch token schema for validation |

## Environment

All credentials must be set as environment variables (see `.env.example`). No secrets are stored in code.

```
STITCH_API_KEY       — Google Stitch API key
FIREBASE_TOKEN       — Firebase CLI auth token
GITHUB_TOKEN         — GitHub personal access token
HOSTINGER_WEBHOOK_URL — Hostinger deploy webhook (optional)
```
