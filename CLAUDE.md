
## Ruflo / Claude Code Agent Integration

This repo uses **Ruflo** (Claude Code agent orchestration) to manage the SaaS creation
pipeline via GitHub Projects board `SaaS-Pretty-Projects/projects/1`.

### Quick Commands

```bash
# See what's on the board and what agents can act on
python scripts/ruflo_board_poller.py

# See shell commands to run each actionable item
python scripts/ruflo_board_poller.py --dispatch

# Live watch mode
python scripts/ruflo_board_poller.py --watch

# Filter by stage
python scripts/ruflo_board_poller.py --stage Brief
```

### Slash Commands (Claude Code)

| Command | Description |
|---------|-------------|
| `/process-board` | Process all actionable board items with agents |
| `/board-status` | Show pipeline health for all board items |
| `/saas-create-from-board` | Add a new SaaS to the board and start the pipeline |

### Agents (`.claude/agents/`)

| Agent | Role |
|-------|------|
| `saas-swarm-coordinator` | Entry point — reads board, routes to sub-agents |
| `saas-pm` | Generates brief.md from board item |
| `saas-engineer` | Runs design pipeline + scaffold |
| `saas-qa` | Validates all artifacts |
| `saas-devops` | Deploys to Firebase, updates board |
| `saas-monitor` | Read-only health reporter |

### Board → Agent Routing

| Board Stage | Agent | Auto? |
|-------------|-------|-------|
| Brief | `saas-pm` | ✅ |
| Design.md | `saas-engineer` | ✅ |
| In Progress | `saas-engineer` | ✅ |
| Ready for Prod | `saas-qa` | ✅ |
| Launched | `saas-devops` | ✅ |
| STITCH Prompt | — | 👤 human |
| Designs Ready | — | 👤 human |
| AI Studio | — | 👤 human |
| Revisions | — | 👤 human |

---

## Skill routing

When the user's request matches an available skill, invoke it via the Skill tool. When in doubt, invoke the skill.

Key routing rules:
- Product ideas/brainstorming → invoke /office-hours
- Strategy/scope → invoke /plan-ceo-review
- Architecture → invoke /plan-eng-review
- Design system/plan review → invoke /design-consultation or /plan-design-review
- Full review pipeline → invoke /autoplan
- Bugs/errors → invoke /investigate
- QA/testing site behavior → invoke /qa or /qa-only
- Code review/diff check → invoke /review
- Visual polish → invoke /design-review
- Ship/deploy/PR → invoke /ship or /land-and-deploy
- Save progress → invoke /context-save
- Resume context → invoke /context-restore
