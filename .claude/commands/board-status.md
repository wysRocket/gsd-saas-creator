# /board-status

Show the current state of all SaaS projects on the GitHub Projects board.

## Usage

```
/board-status [--stuck] [--by-stage] [--watch]
```

**Examples:**
```
/board-status               # Snapshot of all items
/board-status --stuck       # Only items stuck for > 30 minutes
/board-status --by-stage    # Group by pipeline stage
/board-status --watch       # Live-refresh every 60 seconds
```

## What This Does

Invokes the `saas-monitor` agent, which runs:

```bash
python scripts/board_status.py [--stuck | --by-stage | --watch]
```

And returns a health report:
- Items per stage
- Stuck pipelines (no progress in > 30 min)
- Failed stages (from pipeline-events.jsonl)
- Recently completed items

## Output Format

```
🟢 Pipeline Health — SaaS-Pretty-Projects/projects/1

📋 Brief:           2 items
🎨 Design.md:       1 item  
⚙️  In Progress:     1 item
✅ Launched:         3 items
🔴 Stuck:           1 item  → "FreelancePay" (stuck at Design.md for 45m)
```
