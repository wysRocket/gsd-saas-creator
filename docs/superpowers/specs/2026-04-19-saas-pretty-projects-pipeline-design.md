# SaaS-Pretty-Projects — Pipeline Design Spec
**Date:** 2026-04-19  
**Project:** github.com/orgs/SaaS-Pretty-Projects/projects/1  
**Approach:** Option 2 — Enrich 02-04 first, derive repeatable template from it  
**Scope:** Project board · Brief content · Workflow (Brief → Launch)

---

## Context

23 real SaaS products to launch sequentially, one at a time.  
Currently active: **02-04 Game analogue (kingdomofarcane.com)** — Priority 1.  
All other items remain at Brief stage until they become active.

---

## A. Project Board Changes

### Stage Field — Replace single "Brief" value with full pipeline:

| Stage | Meaning |
|---|---|
| `Brief` | Business narrative written (Russian + structured EN fields) |
| `Design.md` | Enriched brief + designlang extraction + design.md complete |
| `STITCH Prompt` | stitch-prompt.md crafted and committed to repo |
| `Designs Ready` | STITCH artifacts exported to `/designs` folder |
| `AI Studio` | Code generation in progress |
| `Launched` | Live on domain, LAUNCH-CHECKLIST.md complete |
| `Operating` | Running, feedback loop active, learnings noted |

### New Custom Fields to Add:

| Field | Type | Values |
|---|---|---|
| `Priority` | Number | Launch order (1 = active now) |
| `Repository` | Text | GitHub repo URL |
| `Vertical` | Single select | Hosting / Gaming / Digital Goods / Education / Career |
| `Revenue Model` | Single select | Subscription / Marketplace / One-time / Freemium |
| `Tech Complexity` | Single select | S / M / L |
| `Target Launch` | Date | Rough milestone per project |

### Immediate action on 02-04:
- Set `Priority = 1`
- Advance `Stage` to `Design.md` once brief enrichment is done
- Link `Repository` once repo is created

---

## B. Enriched Brief Structure

Every GitHub project item must contain the existing Russian business narrative **plus** this structured block appended below it:

```markdown
---

## [EN] Summary
One paragraph in English. Seed for design.md and STITCH prompts.

## Brand
Name: [Brand name]
Domain: [domain.com]
Tagline: [One-line hook]

## MVP Scope
In scope for v1:
- [Feature A]
- [Feature B]
Out of scope:
- [Feature C] (v2)

## Key Pages / Screens
1. Landing page
2. [Page name]
3. [Page name]

## Design Direction
Style: [Dark luxury / Clean minimal / Bold gaming / etc.]
Tone: [Trusted / Playful / Premium / etc.]
References: [competitor.com, competitor2.com]
Color mood: [Deep dark + gold / Light + electric blue / etc.]

## Personas
**Primary:** [Name], [role], [pain point]
**Secondary:** [Name], [role], [pain point]

## Pricing
Plan A: $X/mo — [what's included]
Plan B: $Y/mo — [what's included]

## Tech Stack
Auth: [Supabase / Clerk / Firebase]
DB: [Postgres / Firestore]
Deployment: [Vercel / Railway / Cloudflare]
Payments: [Stripe / LiqPay]

## Launch Success Metric
Definition of "Launched": [first paying user / site live / etc.]
```

**Rule:** Only enrich a brief when it becomes Priority 1. Don't front-load all 22.

---

## C. Repo Structure Per Project

Each SaaS gets its own GitHub repo under `SaaS-Pretty-Projects`. Standard layout:

```
{id}-{slug}/                        e.g. 02-04-game-analogue/
├── brief.md                        Copy of enriched GitHub issue content
├── design.md                       Generated from brief + designlang output
├── stitch-prompt.md                Crafted STITCH prompt, versioned
├── handoff.md                      AI Studio bundle: brief + design + tech hints
├── LAUNCH-CHECKLIST.md             Auth ✓ Payments ✓ Domain ✓ Analytics ✓ README ✓
├── designs/
│   ├── {competitor}-design-language.md    designlang extraction output
│   ├── {competitor}-tailwind.config.js
│   ├── {competitor}-design-tokens.json
│   ├── screenshots/                       Component screenshots from designlang
│   │   ├── button.png
│   │   ├── hero.png
│   │   └── full-page.png
│   └── stitch-exports/                    STITCH-generated design artifacts
│       ├── landing.png
│       └── dashboard.png
├── src/                            AI Studio generated code
├── .env.example
└── README.md
```

---

## D. Full Workflow — Brief to Launch

### Step 1 — Enrich Brief
Fill in all structured fields in the GitHub project item (EN summary, MVP scope, key screens, design direction, pricing, tech stack). This is the only step that requires human judgment — everything downstream is templated.

### Step 2 — designlang Extraction
Run on every competitor/reference URL from the brief's Design Direction section:

```bash
npx designlang <competitor-url> --full --screenshots --out ./designs
```

Commit outputs to `/designs`. These are the ground truth tokens for design.md and STITCH.

**For 02-04:** `npx designlang kingdomofarcane.com --full --screenshots`

### Step 3 — Generate design.md
Using `templates/design-template.md` as scaffold, populate from:
- Brief structured fields (screens, tone, personas, pricing)
- designlang `*-design-language.md` (real colors, fonts, spacing, components)

Commit as `design.md` in repo root.

### Step 4 — Craft stitch-prompt.md
Using `templates/stitch-template.md` as scaffold, build the STITCH prompt from design.md.
Reference extracted component screenshots as visual anchors.
Commit as `stitch-prompt.md`.

### Step 5 — Run STITCH, Export Designs
Run STITCH skill with stitch-prompt.md as input.
Export generated artifacts to `designs/stitch-exports/`.
Advance board item to `Designs Ready`.

### Step 6 — Build handoff.md, Run AI Studio
Assemble `handoff.md` from:
- [EN] Summary from brief
- Full design.md content
- Tech stack from brief
- Key screens list
- Relevant designlang tokens

Paste into aistudio.google.com. Generate codebase into `src/`.

### Step 7 — Launch
Complete `LAUNCH-CHECKLIST.md`:
- [ ] README written
- [ ] .env.example documented
- [ ] Auth working
- [ ] Payments connected
- [ ] Domain configured
- [ ] Analytics installed
- [ ] LICENSE added

Advance board to `Launched`. Update Priority — next item becomes Priority 1.

### Step 8 — Operating + Retrospective
Add "Learnings" comment to GitHub project item:
- 3 things that went well
- 3 things to fix before next project
- Time taken (Brief → Launched)

Advance board to `Operating`. Move to next project.

---

## E. Templates (this repo)

Four template files live in `templates/` and are copied into each new project repo:

| File | Purpose |
|---|---|
| `templates/brief-template.md` | Structured fields block to paste into GitHub issue |
| `templates/design-template.md` | Blank design.md scaffold with all required sections |
| `templates/stitch-template.md` | STITCH prompt scaffold with fill-in slots |
| `templates/handoff-template.md` | AI Studio bundle template |

---

## F. Repeatability Principle

By project 3, the pipeline runs as: enrich brief → run designlang → fill templates → STITCH → AI Studio → launch checklist. Each project benefits from the previous one's learnings note. The templates evolve in this repo; individual project repos only consume them.

---

## Immediate Next Actions (02-04)

1. **Enrich 02-04 brief** on GitHub — add EN summary, MVP scope, key screens, design direction
2. **Run** `npx designlang kingdomofarcane.com --full --screenshots`
3. **Create** `SaaS-Pretty-Projects/02-04-game-analogue` repo with standard structure
4. **Update board** — add Stage pipeline values + Priority/Vertical/Repo fields
5. **Generate** design.md from brief + designlang output
6. **Craft** stitch-prompt.md
