# /saas-create Workflow

Orchestrates the full SaaS Creator pipeline from a single vibe prompt to a live URL.

## Trigger

```
/saas-create [vibe prompt]
```

**Example:**
```
/saas-create A project management tool for freelancers with time tracking, invoicing, and a client portal
```

---

## Execution Steps

### Step 1 — Requirements (Agent: @pm)

**Trigger**: `/saas-create` received with vibe prompt.

1. `@pm` parses the vibe prompt to extract:
   - Product name (inferred or asked)
   - Target user persona
   - Core problem being solved
   - 3–5 key features
   - Success metric (what does "done" look like?)
2. `@pm` renders `templates/REQUIREMENTS.md.j2` with extracted data → writes `REQUIREMENTS.md`.
3. `@pm` presents `REQUIREMENTS.md` to the user.

> **HALT GATE**: The pipeline pauses. User must type `approve` or provide corrections.
> If corrections are given, `@pm` revises and re-presents. Loop until approved.

---

### Step 2 — Visual DNA (Agent: @engineer)

**Trigger**: User approved `REQUIREMENTS.md`.

1. `@engineer` asks: "Do you have a Google Stitch project ID? (Enter ID or `skip`)"
   - **If ID provided**: Run `python scripts/extract_dna.py <project_id>` → `design_tokens.json`
   - **If skipped**: Use default design tokens from `reference/stitch_schema.json`
2. Run `python scripts/render_templates.py DESIGN.md` → writes `DESIGN.md`.
3. `@engineer` validates DESIGN.md for completeness (colors, typography, components).
4. Report: "Design DNA extracted. X color tokens, Y typography styles, Z components mapped."

---

### Step 3 — Architecture (Agent: @engineer)

**Trigger**: `DESIGN.md` validated.

1. `@engineer` defines:
   - Firestore schema (collections and document shapes)
   - Firebase Auth providers (email, Google OAuth, etc.)
   - Firebase Functions endpoints (list: method, path, purpose)
2. Writes `ARCHITECTURE.md` summarizing all decisions.
3. Reports architecture summary to user (non-blocking, informational only).

---

### Step 4 — Code Generation & QA (Agents: @engineer → @qa)

**Trigger**: `ARCHITECTURE.md` written.

1. `@engineer` runs `python scripts/scaffold.py` with `DESIGN.md` + `ARCHITECTURE.md` as inputs.
   - Generates: `src/` (React/Next.js), `functions/` (Firebase), `firestore.rules`, `package.json`
2. `@engineer` implements Firebase Functions from ARCHITECTURE.md endpoint list.
3. `@engineer` wires Firestore collections to frontend data layer.
4. `@qa` runs: `npm install && npm test`
5. `@qa` checks: auth flows, CRUD operations, API error states.
6. If tests fail: `@engineer` fixes, `@qa` re-runs. Max 3 retry cycles before halting for user input.
7. Report: "All tests passing. App ready for deployment review."

---

### Step 5 — Deploy to Production (Agent: @devops)

**Trigger**: All tests passing.

1. `@devops` renders `templates/deploy.yml.j2` → `.github/workflows/deploy.yml`.
2. `@devops` summarizes deployment plan:
   - Firebase project: `<project_id>`
   - GitHub repo: `<repo_url>`
   - Hosting target: Firebase Hosting + (optional) Hostinger

> **HALT GATE**: The pipeline pauses. User must type `deploy` to authorize.
> Cloud resources will be provisioned and real costs may be incurred.

3. `@devops` runs `python scripts/deploy.py` to:
   - Initialize Firebase project
   - Apply `firestore.rules` from `reference/firebase_security_rules.txt`
   - Push code to GitHub
   - Trigger GitHub Actions workflow
4. `@devops` monitors GitHub Actions until green.
5. `@devops` returns: **"Live URL: https://<project_id>.web.app"**

---

## Abort / Recovery

At any step, the user can type:
- `abort` — Stop the pipeline entirely.
- `pause` — Halt after the current step completes; resume with `/saas-create resume`.
- `retry` — Re-run the current step from the beginning.
- `skip` — Skip the current step (use with caution, may cause downstream failures).

## Output Artifacts

| File | Description |
|---|---|
| `REQUIREMENTS.md` | Approved product specification |
| `design_tokens.json` | Raw Stitch design tokens |
| `DESIGN.md` | Rendered design DNA document |
| `ARCHITECTURE.md` | Technical stack and data model |
| `src/` | React/Next.js frontend source |
| `functions/` | Firebase Functions backend |
| `.github/workflows/deploy.yml` | CI/CD pipeline |
| `firestore.rules` | Firestore security rules |
