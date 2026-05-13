# /process-board

Reads the GitHub Projects board at `SaaS-Pretty-Projects/projects/1`, identifies
actionable items, and runs the SaaS pipeline agents on each one.

## Usage

```
/process-board [--item "<project name or item ID>"] [--dry-run] [--stage <stage_name>]
```

**Examples:**
```
/process-board                            # Process all actionable items
/process-board --item "FreelancePay"      # Process one specific item
/process-board --dry-run                  # Preview what would run, no changes
/process-board --stage Brief              # Process only items at Brief stage
```

## What This Does

1. Invoke the `saas-swarm-coordinator` agent.
2. The coordinator fetches all board items via GraphQL.
3. For each item at an actionable stage (Brief, Design.md, In Progress, Ready for Prod):
   - Extracts: project_name, competitor_url, vertical, stage, item_node_id
   - Dispatches to the appropriate sub-agent
4. Reports results: ✅ advanced / ❌ failed / ⏸ skipped (human-gate stage)

## Actionable vs Human-Gate Stages

| Stage | Handler |
|-------|---------|
| `Brief` | `@saas-pm` generates brief.md |
| `Design.md` | `@saas-engineer` runs design pipeline |
| `In Progress` | `@saas-engineer` generates scaffold |
| `Ready for Prod` | `@saas-qa` validates artifacts |
| `Launched` | `@saas-devops` deploys to Firebase |
| `STITCH Prompt` | ⏸ Human gate — skip, post reminder |
| `Designs Ready` | ⏸ Human gate — skip |
| `AI Studio` | ⏸ Human gate — skip |
| `Revisions` | ⏸ Human gate — skip |

## Board GraphQL Query

The coordinator uses this query to read the board:

```graphql
query {
  node(id: "PVT_kwDOEHzfoM4BU-0M") {
    ... on ProjectV2 {
      items(first: 50) {
        nodes {
          id
          content {
            ... on Issue {
              title
              number
              url
              repository { name }
            }
          }
          fieldValues(first: 10) {
            nodes {
              ... on ProjectV2ItemFieldTextValue {
                text
                field { ... on ProjectV2Field { name } }
              }
              ... on ProjectV2ItemFieldSingleSelectValue {
                name
                optionId
                field { ... on ProjectV2SingleSelectField { name } }
              }
            }
          }
        }
      }
    }
  }
}
```
