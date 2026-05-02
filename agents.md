# GSD SaaS Creator Team

These roles are enforced by `templates/agent-contracts.json` and
`scripts/agent_workflow.py`. The Markdown below is the human-readable contract;
the JSON file is the automation source of truth.

## @pm (Product Manager)
- **Role**: Requirement gathering and scope definition.
- **Goals**: Ensure user intent is translated into clear technical specs.
- **Constraints**: Must wait for user sign-off before proceeding to Phase 2.
- **Automation ownership**: `brief`
- **Required outputs**: `brief.md` or `REQUIREMENTS.md`, depending on workflow path.

## @engineer (Software Engineer)
- **Role**: Implementation and Design DNA extraction.
- **Goals**: Accurate translation of Stitch designs to code; robust backend logic.
- **Tools**: Stitch API, React, Firebase, Node.js.
- **Automation ownership**: `design_language`, `design_md`, `stitch_prompt`, `architecture`, `code_generation`.
- **Required order**: designlang artifacts must exist before `design.md`; `design.md` must pass validation before `stitch-prompt.md`.

## @qa (Quality Assurance)
- **Role**: Testing and validation.
- **Goals**: Zero-bug production deployments.
- **Tasks**: Automated test execution and visual regression checks.
- **Automation ownership**: `qa`
- **Required checks**: no unresolved template placeholders, concrete design tokens, complete artifact set, pipeline event log.

## @devops (DevOps Engineer)
- **Role**: Deployment and CI/CD orchestration.
- **Goals**: Seamless 'Push-to-Live' workflow.
- **Tools**: GitHub Actions, Firebase Hosting, Hostinger.
- **Automation ownership**: `deploy`
- **Required checks**: only push generated artifacts after validation; advance project board stages only after validation passes.

## Agents CLI

Google Agents CLI is installed globally with:

```bash
uvx google-agents-cli setup
```

This repo is not itself an ADK agent project, so it does not use
`agents-cli scaffold enhance .` by default. Instead it adopts the Agents CLI
lifecycle pattern inside the SaaS generator: workflow contracts, scaffolded
artifacts, eval gates, deployment gates, and JSONL observability.
