# /saas-create-from-board

Create a new SaaS product by adding it to the GitHub Projects board and starting the pipeline.

## Usage

```
/saas-create-from-board "<project name>" --competitor "<url>" --vertical "<vertical>"
```

**Verticals:** Hosting / Gaming / Digital Goods / Education / Career

**Example:**
```
/saas-create-from-board "FreelancePay" --competitor "https://stripe.com" --vertical "Digital Goods"
```

## What This Does

1. Creates a GitHub issue in `SaaS-Pretty-Projects` org:
   ```bash
   gh issue create \
     --repo SaaS-Pretty-Projects/pipeline \
     --title "<project name>" \
     --body "Competitor: <url>\nVertical: <vertical>\n\nAuto-created by SaaS Creator pipeline."
   ```

2. Adds the issue to the project board at `Brief` stage:
   ```bash
   # Get issue node ID, then add to project
   gh api graphql -f query='
     mutation($projectId: ID!, $contentId: ID!) {
       addProjectV2ItemById(input: { projectId: $projectId, contentId: $contentId }) {
         item { id }
       }
     }
   ' -f projectId="PVT_kwDOEHzfoM4BU-0M" -f contentId="<issue_node_id>"
   ```

3. Sets the board fields (Competitor URL, Vertical, Stage=Brief):
   ```bash
   # Set Competitor URL
   gh api graphql -f query='mutation { updateProjectV2ItemFieldValue(input: {
     projectId: "PVT_kwDOEHzfoM4BU-0M"
     itemId: "<item_node_id>"
     fieldId: "PVTF_lADOEHzfoM4BU-0MzhQv9f8"
     value: { text: "<competitor_url>" }
   }) { projectV2Item { id } } }'

   # Set Vertical
   # Hosting: 56a9c75a | Gaming: a263f297 | Digital Goods: 9bdacda3 | Education: 817d2a42 | Career: 79fc421b
   gh api graphql -f query='mutation { updateProjectV2ItemFieldValue(input: {
     projectId: "PVT_kwDOEHzfoM4BU-0M"
     itemId: "<item_node_id>"
     fieldId: "PVTSSF_lADOEHzfoM4BU-0MzhQhuNE"
     value: { singleSelectOptionId: "<vertical_option_id>" }
   }) { projectV2Item { id } } }'
   ```

4. Immediately kicks off `/process-board --item "<project name>"` to start the Brief stage.

## Vertical → Option ID Map

| Vertical | Option ID |
|----------|-----------|
| Hosting | `56a9c75a` |
| Gaming | `a263f297` |
| Digital Goods | `9bdacda3` |
| Education | `817d2a42` |
| Career | `79fc421b` |
