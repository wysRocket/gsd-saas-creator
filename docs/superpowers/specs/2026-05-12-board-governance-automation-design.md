# Board Governance, Spec Automation, and QA Gating Design

**Date:** 2026-05-12  
**Scope:** GitHub Project 1 (`SaaS-Pretty-Projects/projects/1`) governance + automation  
**Chosen operating model:** GitHub-native automation (Project fields + webhooks + GitHub Actions)

## 1. Goal

Implement a reliable, idempotent automation system that:

1. Governs board stage transitions with clear policy and rollback behavior.
2. Automates repo creation and full issue tree generation from project items.
3. Enforces a soft spec gate before execution workflows.
4. Integrates TesterArmy for adaptive PR QA and release protection.

Primary success metric is **balanced optimization** across throughput, quality, and lead time.

## 2. Decisions locked with stakeholder

- **Trigger model:** Hybrid (Project Stage changes + issue comments)
- **Spec gate:** Soft gate
- **Issue granularity:** Epic + full task breakdown
- **Repo visibility:** Private first (manual/public promotion at Ready for Prod)
- **PR QA model:** Adaptive (smoke each PR, critical suite on release-candidate paths)

## 3. Governance model (board contract)

### 3.1 Required Project fields

- `Stage` (single-select): Clarification -> Brief -> Design.md -> STITCH Prompt -> AI Studio -> In Progress -> Revisions -> Ready for Prod -> Launched -> Operating -> Done
- `Status` (single-select): Backlog / In Progress / Blocked / Done
- `Spec Approved` (single-select): No / Yes
- `Repo URL` (text)
- `Visibility` (single-select; default `Private`)
- `Vertical` (single-select/text)
- `Competitor URL` (text)

### 3.2 Trigger sources

1. `projects_v2_item.edited`  
   - Primary state machine trigger for stage-based automation.
2. `issue_comment.created`  
   - Human override/ops commands.

### 3.3 Soft gate policy

- Repo and issue-tree generation **allowed** when `Spec Approved = No`.
- Execution workflows (AI Studio codegen, deployment, production promotion) **blocked** until `Spec Approved = Yes`.
- Blocked actions write an issue comment with explicit unblock instruction.

### 3.4 Guardrails

- Invalid transitions are auto-reverted to the last valid stage.
- Failures route to `Revisions` stage with error context.
- Automation writes a clear audit comment on linked issue for every decision/action.

## 4. Repo and issue creation automation

### 4.1 Entry point

At `Stage = Brief`, automation ensures project bootstrap resources exist.

### 4.2 Repo bootstrap

- If `Repo URL` is empty:
  - Create org repo as **private**.
  - Initialize labels, issue templates, baseline protections.
  - Push seed artifacts: `brief.md`, `design.md` placeholder, `automation-manifest.json`.
  - Write `Repo URL` back to Project field.

### 4.3 Full issue graph generation

Create and link:

1. Epic issue (`[EPIC] <project>`)
2. Phase issues (`PM`, `ENG`, `QA`, `DEVOPS`)
3. Fine-grained task issues per phase, each with acceptance criteria and testability.

Issue metadata:

- Labels: `stage:*`, `priority:*`, `area:*`, `blocked-by-spec` (when applicable)
- Parent-child links via task lists in parent issue bodies.

### 4.4 Idempotency

- Every generated artifact carries an `automation_key`.
- Re-runs update in place (body/checklist/labels) instead of duplicating.
- Existing entities are discovered first, then patched.

### 4.5 Comment command handlers

- `/regen-issues` -> Regenerate/refresh full issue tree.
- `/sync-board` -> Reconcile board fields from repo issue state.
- `/archive-project` -> Close pending tasks and move Stage to `Done`.

## 5. TesterArmy integration and release policy

### 5.1 PR behavior (adaptive)

- All PRs: run TesterArmy **smoke suite**.
- `release-candidate` label (or release pathway): run **critical suite**.

### 5.2 Workflow wiring

GitHub Action sends run request with:

- repo, PR number, env URL, suite type, commit SHA.

Expected returns:

- run URL, pass/fail summary, evidence links.

Action outputs:

- PR check status.
- PR summary comment with key failures and evidence.

### 5.3 Board coupling

- If critical suite fails at `Ready for Prod`, move Stage -> `Revisions`.
- Launch transition requires critical QA + deploy checks to pass.

### 5.4 Failure handling and evidence

- Retry once for infra/network flake.
- Deterministic QA failures create/update `qa-regression` issue linked to epic.
- Evidence bundle (screenshots/video/log links) persisted in PR + issue.

### 5.5 Cost/speed controls

- Repo-level concurrency caps.
- Fast-budget smoke suite.
- Scheduled nightly critical checks for `Operating` projects.

## 6. Error handling and observability

### 6.1 Standard failure envelope

Each failure event carries:

- `error_code`
- `stage`
- `item_id`
- `retryable`
- `next_action`

### 6.2 Retry and operator controls

- Retry queue for retryable failures.
- Non-retryable failures route to `Revisions`.
- `/retry-last` reruns only failed step.

### 6.3 Audit trail

- Structured artifact: `pipeline-events.jsonl`
- Human-readable timeline: issue comments
- KPI rollup workflow (weekly):
  - Throughput (projects/week)
  - Quality (regression/reopen rates)
  - Lead time (idea -> brief -> repo -> launched)

## 7. Rollout plan

1. **Pilot (3 projects):** governance + repo/issue automation only.
2. **QA expansion:** TesterArmy smoke on all PRs; adaptive critical suite.
3. **Prod guardrails:** enforce critical-pass requirement for Ready for Prod.
4. **Ops maturity:** nightly Operating checks + automated regression lifecycle.

## 8. Definition of done

- Stage transition policy is enforced and reversible.
- Repo + full issue tree generation is idempotent.
- Soft spec gate blocks execution workflows until approval.
- TesterArmy evidence is attached to PRs and regression issues.
- Revisions fallback behavior is deterministic and traceable.

