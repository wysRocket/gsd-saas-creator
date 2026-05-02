# Agent Workflow

This repo uses Google Agents CLI as a lifecycle reference, not as a generated
ADK app. The installed CLI and skills provide the pattern:

```bash
uvx google-agents-cli setup
agents-cli --version
agents-cli info
```

`agents-cli info` currently reports that this directory is not an ADK agent
project. That is expected: `gsd-saas-creator` generates SaaS product repos and
orchestrates Design.md automation. The repo-native implementation lives in:

- `templates/agent-contracts.json` — executable contracts for `@pm`,
  `@engineer`, `@qa`, and `@devops`.
- `scripts/agent_workflow.py` — contract router, eval gate runner, and JSONL
  event logger.
- `.github/workflows/stage-trigger.yml` — calls the workflow runner before and
  after generated artifacts.

## Commands

Print the contract for a stage:

```bash
python scripts/agent_workflow.py route design_md
```

Validate one generated stage:

```bash
python scripts/agent_workflow.py validate-stage design_md --repo-dir output/my-saas --log
```

Append an observability event:

```bash
python scripts/agent_workflow.py record-stage stitch_prompt \
  --repo-dir output/my-saas \
  --status started \
  --message "Generating stitch-prompt.md"
```

Check all stages:

```bash
python scripts/agent_workflow.py status --repo-dir output/my-saas
```

Run a full local dry run:

```bash
python scripts/dry_run_design_pipeline.py --repo-dir output/design-pipeline-dry-run
```

If `GEMINI_API_KEY` is not available, test the same validation gates with
deterministic fixture artifacts:

```bash
python scripts/dry_run_design_pipeline.py --repo-dir /tmp/gsd-design-dry-run --offline-fixture
```

## Design.md Automation

When a GitHub Projects item moves to `Design.md`, the action now runs:

1. designlang extraction into `output/<repo>/design/`
2. `generate_brief.py`
3. `agent_workflow.py validate-stage brief --log`
4. `generate_design_md.py`
5. `agent_workflow.py validate-stage design_md --log`
6. `generate_stitch_prompt.py`
7. `agent_workflow.py validate-stage stitch_prompt --log`
8. push `brief.md`, `design.md`, `stitch-prompt.md`, designlang artifacts, and
   `pipeline-events.jsonl`

The validation gates block stage advancement when generated files are missing,
too short, still contain template placeholders, lack real design tokens, or
drop the required `design.md` contract reference.
