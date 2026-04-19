# 02-04 Game Analogue — Project Setup Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Set up the complete project foundation for 02-04 (Game Analogue) — from designlang extraction through a committed repo with design.md and stitch-prompt.md ready for STITCH generation.

**Architecture:** Run `designlang` on the reference site (kingdomofarcane.com) to extract real design tokens, create the GitHub repo with standard structure, enrich the brief, generate design.md from real tokens, and craft the STITCH prompt.

**Tech Stack:** designlang (npx), GitHub CLI (gh), Next.js 14 (App Router), Tailwind CSS, Supabase, Stripe

---

### Task 1: Extract Design System from kingdomofarcane.com

**Files:**
- Create: `designs/kingdomofarcane-design-language.md` (generated)
- Create: `designs/kingdomofarcane-tailwind.config.js` (generated)
- Create: `designs/kingdomofarcane-design-tokens.json` (generated)
- Create: `designs/screenshots/` (generated)

- [ ] **Step 1: Check designlang is available**

```bash
npx designlang --version
```
Expected output: version number like `5.x.x`. If not found, it auto-installs on first run.

- [ ] **Step 2: Create designs directory in project root**

```bash
mkdir -p /Users/wysmyfree/Projects/gsd-saas-creator/designs
```

- [ ] **Step 3: Run full extraction**

```bash
cd /Users/wysmyfree/Projects/gsd-saas-creator && \
npx designlang kingdomofarcane.com --full --screenshots --out ./designs
```

Expected output:
```
✓ kingdomofarcane-com-design-language.md
✓ kingdomofarcane-com-design-tokens.json
✓ kingdomofarcane-com-tailwind.config.js
✓ kingdomofarcane-com-variables.css
✓ kingdomofarcane-com-preview.html
✓ kingdomofarcane-com-figma-variables.json
✓ kingdomofarcane-com-theme.js
✓ kingdomofarcane-com-shadcn-theme.css
✓ screenshots/button.png
✓ screenshots/hero.png
✓ screenshots/full-page.png
```

- [ ] **Step 4: Verify extraction succeeded**

```bash
ls /Users/wysmyfree/Projects/gsd-saas-creator/designs/
```
Expected: 8+ files including `*-design-language.md`

- [ ] **Step 5: Read the key design tokens**

```bash
head -100 /Users/wysmyfree/Projects/gsd-saas-creator/designs/*-design-language.md
```
Note the primary colors, font families, and spacing base unit — you'll need these in Task 4.

- [ ] **Step 6: Commit extraction output**

```bash
cd /Users/wysmyfree/Projects/gsd-saas-creator && \
git add designs/ && \
git commit -m "feat: add kingdomofarcane.com designlang extraction for 02-04"
```

---

### Task 2: Create GitHub Repo with Standard Structure

**Files:**
- Create: `SaaS-Pretty-Projects/02-04-game-analogue` (new GitHub repo)
- Create: `brief.md`
- Create: `LAUNCH-CHECKLIST.md`
- Create: `designs/` directory

- [ ] **Step 1: Create the GitHub repo**

```bash
gh repo create SaaS-Pretty-Projects/02-04-game-analogue \
  --private \
  --description "Game enhancement marketplace — analogue to kingdomofarcane.com" \
  --clone
```

Expected: repo created and cloned to `./02-04-game-analogue/`

- [ ] **Step 2: Create standard directory structure**

```bash
cd 02-04-game-analogue && \
mkdir -p designs/screenshots designs/stitch-exports src
```

- [ ] **Step 3: Create LAUNCH-CHECKLIST.md**

```bash
cat > LAUNCH-CHECKLIST.md << 'EOF'
# Launch Checklist — 02-04 Game Analogue

## Pre-Launch
- [ ] README.md written with setup instructions
- [ ] .env.example documented with all required vars
- [ ] Auth flow working (signup, login, logout)
- [ ] Payments connected (Stripe test mode → production)
- [ ] Domain configured and SSL active
- [ ] Analytics installed (Posthog / Plausible)
- [ ] LICENSE file added
- [ ] Error pages (404, 500) styled

## Launch
- [ ] Stripe switched to production keys
- [ ] Domain pointed to production deployment
- [ ] Smoke test: register → browse → checkout → receive item
- [ ] First paying user test transaction

## Post-Launch
- [ ] GitHub project board item moved to "Operating"
- [ ] Learnings note added to GitHub project item
EOF
```

- [ ] **Step 4: Create initial commit**

```bash
git add . && \
git commit -m "chore: initial repo structure for 02-04 game analogue"
```

- [ ] **Step 5: Push to GitHub**

```bash
git push -u origin main
```

- [ ] **Step 6: Copy designlang output into repo**

```bash
cp -r /Users/wysmyfree/Projects/gsd-saas-creator/designs/* ./designs/ && \
git add designs/ && \
git commit -m "feat: add kingdomofarcane.com design extraction artifacts"
```

---

### Task 3: Write Enriched brief.md

**Files:**
- Create: `brief.md` in `02-04-game-analogue/`

- [ ] **Step 1: Create brief.md with full enriched content**

```bash
cat > brief.md << 'EOF'
# 02-04 — Game Analogue Marketplace

## [RU] Business Narrative
[The existing Russian brief from the GitHub project item goes here — copy it in full]

---

## [EN] Summary
A marketplace for in-game enhancements, virtual currency, and digital game items.
Players buy boosts, skins, currency, and services for their favourite online games
from verified sellers. The platform handles escrow, delivery verification, and
dispute resolution — removing friction from peer-to-peer game item trading.

## Brand
Name: [TBD — decide before design.md step. Suggestion: Arcadem / Vaultgg / Gearex]
Domain: [TBD].com
Tagline: Level up your game. Instantly.

## MVP Scope
In scope for v1:
- Game category listing (select a game, see available items)
- Item listings with price, delivery time, seller rating
- Cart + checkout (Stripe)
- Seller dashboard (list items, track orders)
- Buyer order tracking
- Basic search / filter by game + item type

Out of scope (v2):
- Auction system
- Subscription seller plans
- API for third-party game integrations
- Mobile app

## Key Pages / Screens
1. Landing page — hero, featured games, trust signals, CTA
2. Game page — filter/browse items for one game
3. Item detail — description, seller info, buy button
4. Cart + Checkout — Stripe payment flow
5. Buyer dashboard — order history, active orders
6. Seller dashboard — list items, manage listings, earnings
7. Auth pages — signup / login

## Design Direction
Style: Dark gaming marketplace — deep backgrounds, electric accent colors, card-based layout
Tone: Fast, trusted, premium-adjacent (not cheap, not enterprise)
References: kingdomofarcane.com, gameflip.com, g2g.com
Color mood: Deep dark navy/charcoal + electric blue or gold accent

## Personas
**Primary:** 18-28yo PC gamer, plays competitive online games daily, wants to buy currency
or boosts quickly without getting scammed, pays via card or PayPal
**Secondary:** Semi-pro player, sells excess in-game items for income, needs a clean
dashboard to manage listings and track earnings

## Pricing (Platform fee model)
Free for buyers
Sellers: 8% platform fee per transaction (deducted from payout)
Optional Seller Pro: $9.99/mo — lower fee (5%), featured listings, priority support

## Tech Stack
Auth: Supabase (email + OAuth with Google)
DB: Postgres via Supabase
Deployment: Vercel
Payments: Stripe (Connect for seller payouts)
Framework: Next.js 14 App Router
Styling: Tailwind CSS

## Launch Success Metric
Definition of "Launched": first real transaction between a buyer and seller completes
(real money, real item delivered, both parties satisfied)
EOF
```

- [ ] **Step 2: Commit brief.md**

```bash
git add brief.md && \
git commit -m "feat: add enriched brief for 02-04 game analogue"
```

---

### Task 4: Generate design.md

**Files:**
- Create: `design.md` in `02-04-game-analogue/`

- [ ] **Step 1: Read extracted design tokens**

```bash
head -150 designs/*-design-language.md
```
Note exact values for: primary hex color, background hex, font-family names, base spacing unit.

- [ ] **Step 2: Create design.md with real extracted tokens**

Replace `[from designlang]` placeholders below with actual values from the extraction output:

```bash
cat > design.md << 'EOF'
# Design — 02-04 Game Analogue Marketplace

## Overview
A dark-themed gaming marketplace where players buy and sell in-game enhancements,
virtual currency, and digital items. Should feel fast, trusted, and premium —
like the best version of what kingdomofarcane.com is trying to be.

## Design Tokens (extracted from kingdomofarcane.com + adjusted)
**Primary color:** [from designlang — primary brand color]
**Secondary color:** [from designlang — secondary accent]
**Background:** #0d0f14 (deep dark)
**Surface:** #161b27 (card backgrounds)
**Text primary:** #f0f4ff
**Text muted:** #8892a4
**Accent:** #4f8ef7 (electric blue — or gold if kingdomofarcane uses gold)
**Success:** #22c55e
**Warning:** #f59e0b

**Font heading:** [from designlang — heading font]
**Font body:** [from designlang — body font, fallback: Inter]
**Base spacing unit:** [from designlang — spacing base, likely 4px or 8px]
**Border radius cards:** 10px
**Border radius buttons:** 6px

## Pages & Key Components

### Landing Page
- Hero: Full-width dark banner. Headline: "Level Up Your Game. Instantly."
  Subheadline: "Buy and sell in-game items, currency, and boosts from verified sellers."
  CTA: "Browse Games" (primary) + "Start Selling" (ghost)
  Background: gradient or game screenshot overlay with dark overlay
- Featured Games: horizontal scroll of game cards (logo + name + item count)
- Trust signals: "100k+ transactions", "Verified sellers", "Instant delivery" — icon row
- How It Works: 3-step: Browse → Buy → Receive. Clean icon cards.
- Recent listings: Card grid of 6 recent items with price, game badge, seller rating
- Footer: nav links, social icons

### Game Page (e.g. /games/wow)
- Breadcrumb: Home > Games > World of Warcraft
- Filter sidebar: item type (Currency / Boost / Item), price range, delivery time, rating
- Item card grid: image, title, price, seller rating, delivery badge ("Instant" or "1-2h")
- Sort: Popular / Cheapest / Fastest delivery

### Item Detail Page
- Item title, game badge, price (large)
- Seller card: name, rating, # transactions, verified badge
- Delivery info: estimated time, method (manual/automated)
- Buy button → opens cart drawer
- Description + requirements tab
- Reviews section (paginated)

### Cart + Checkout
- Cart drawer (slide-in) → quantity, remove, total
- Checkout: Stripe Elements embedded, order summary sidebar

### Buyer Dashboard (/dashboard/orders)
- Order list: item name, status chip (Pending / Delivered / Disputed), date, price
- Order detail drawer: seller contact, delivery instructions, dispute button

### Seller Dashboard (/dashboard/seller)
- Stats row: total earnings, active listings, pending orders, rating
- Listings table: title, game, price, stock, status toggle (active/paused)
- Add listing form: game select, item type, title, description, price, stock, delivery time

### Auth Pages
- Unified /auth page with tab switcher: Sign In / Sign Up
- Google OAuth button + email+password form
- Clean minimal — dark card centered on page

## UX Copy
**Hero headline:** Level Up Your Game. Instantly.
**Hero subheadline:** Buy and sell in-game items, currency, and boosts from verified sellers.
**Primary CTA:** Browse Games
**Secondary CTA:** Start Selling
**Pricing headline:** Simple seller pricing
**Empty state (no listings):** No items yet. Be the first to list for this game.
**Error (payment failed):** Payment failed. Your card was not charged — please try again.
**Trust badge 1:** 100k+ Transactions
**Trust badge 2:** Verified Sellers Only
**Trust badge 3:** Instant Delivery

## Layout System
- Max container width: 1280px
- Column grid: 12-column
- Card grid: 4 columns desktop / 2 tablet / 1 mobile
- Nav: sticky, transparent on scroll-top → solid dark on scroll
- Mobile breakpoint: 768px

## Component Notes
- Buttons: filled primary (accent color), ghost variant (border only), destructive (red)
- Cards: subtle border (1px #1e2535), box-shadow (0 2px 12px rgba(0,0,0,0.4)), radius 10px
- Inputs: dark background (#0d0f14), border #2a3142, focus ring accent color
- Game badge: small pill with game color accent
- Status chips: color-coded (green=delivered, yellow=pending, red=disputed)
- Seller rating: star row + numeric score

## Tone & Atmosphere
Fast and trustworthy. This is where serious gamers go when they need items now and
don't want to get scammed. The design should feel like a premium tool, not a shady
grey-market site — clean information hierarchy, obvious trust signals, zero clutter.

## Competitor Reference
See `designs/kingdomofarcane-com-design-language.md` for extracted tokens.
Patterns to adopt: dark color scheme, card-based item listings, game category navigation
Patterns to avoid: cluttered layouts, unclear pricing, missing seller credibility signals
EOF
```

- [ ] **Step 3: Commit design.md**

```bash
git add design.md && \
git commit -m "feat: generate design.md for 02-04 game analogue marketplace"
```

---

### Task 5: Craft stitch-prompt.md

**Files:**
- Create: `stitch-prompt.md` in `02-04-game-analogue/`

- [ ] **Step 1: Write the STITCH prompt for the landing page**

```bash
cat > stitch-prompt.md << 'EOF'
# STITCH Prompt — 02-04 Game Analogue Marketplace

## Product Context
A dark-themed gaming marketplace where players buy in-game currency, boosts, and
digital items from verified sellers. Target user: 18-28yo PC gamer who needs
items fast and trusts verified sellers over random Discord groups.

## Design Style
Style: Dark gaming marketplace
Mood: Fast, premium, trusted — like Stripe for gaming items
Inspiration: kingdomofarcane.com (reference screenshots in designs/screenshots/)

## Color Palette
Primary: #4f8ef7
Background: #0d0f14
Surface: #161b27
Text: #f0f4ff
Text muted: #8892a4
Accent: #4f8ef7
Success: #22c55e

## Typography
Heading font: [value from designs/*-design-language.md]
Body font: Inter, sans-serif
Base size: 16px

---

## Page 1: Landing Page

### Layout
Full-width sections stacked vertically:
1. Sticky nav
2. Hero (full-width, 100vh)
3. Featured games horizontal scroll
4. Trust signals row (3 icons)
5. How It Works (3 steps)
6. Recent listings grid
7. Footer

### Sticky Nav
Left: Logo (brand mark + wordmark, light text)
Center: Links — Browse, Games, How It Works, Pricing
Right: "Sign In" (ghost button) + "Start Selling" (primary filled button)
Background: transparent on top, transitions to #0d0f14 with blur on scroll

### Hero Section
Background: Deep dark #0d0f14 with subtle radial gradient (electric blue glow, bottom-left)
Optional: faint game screenshot background at 10% opacity with dark overlay

Headline: "Level Up Your Game. Instantly."
Font: [heading font], 64px, bold, #f0f4ff, tight letter-spacing

Subheadline: "Buy and sell in-game items, currency, and boosts from verified sellers."
Font: 20px, #8892a4, normal weight, max-width 520px

CTA row (top margin 40px):
- Primary: "Browse Games" — filled, background #4f8ef7, white text, 48px height, 20px radius, 140px min-width
- Secondary: "Start Selling" — ghost, border 1px #4f8ef7, #4f8ef7 text, same size

Below CTAs: Trust row — "100k+ Transactions · Verified Sellers · Instant Delivery"
Font: 13px, #8892a4, dot separator

### Featured Games
Section heading: "Top Games" — 22px, bold, #f0f4ff, margin-bottom 24px
Horizontal scroll row of game cards (no scrollbar):
Each card: 160x200px, dark surface (#161b27), 10px radius, 1px border (#1e2535)
  - Game logo/image (120x80px, object-fit contain, centered)
  - Game name: 14px, bold, #f0f4ff, centered
  - Item count: "2,400+ items", 12px, #8892a4
  - Hover: border brightens to #4f8ef7, subtle lift shadow

### Trust Signals
3-column row, centered, margin 80px vertical
Each: icon (32px, accent color) + bold number + label
  - "100k+ Transactions"
  - "Verified Sellers Only"
  - "Instant Delivery"
Dividers between columns: 1px #1e2535

### How It Works
Section heading: "How It Works" — centered, 28px, bold
3-card row, equal width, 24px gap:
Each card: surface bg, 10px radius, padding 32px, centered content
  Step number: 48px circle, accent bg, white bold number
  Title: 18px, bold, #f0f4ff, margin-top 16px
  Description: 14px, #8892a4, centered
Steps: "1. Browse → 2. Buy → 3. Receive"

### Recent Listings Grid
Section heading: "Latest Listings" — left-aligned, 22px bold
4-column grid (gap 16px):
Each item card: surface bg, 10px radius, 1px border, padding 16px, 240px height
  - Game badge (top-left): pill, accent bg at 20% opacity, accent text, 11px, game name
  - Item title: 14px, bold, #f0f4ff, 2-line clamp
  - Seller rating: star icon (gold) + score + "(n reviews)", 12px, muted
  - Bottom row: Price ($XX.XX, 18px bold, accent) + "Buy Now" button (small, filled)
  - Hover: lift shadow, border brightens

### Footer
Dark bg (#0a0c10), padding 60px 0
4 columns: Logo+tagline | Navigation | For Sellers | Support
Bottom bar: "© 2026 [Brand]. All rights reserved." + links

---

## Page 2: Game Page (/games/[slug])

### Layout
- Sticky nav (same as landing)
- Breadcrumb: Home > Games > [Game Name]
- Page heading + game logo
- 2-column layout: sidebar (filter) + main grid

### Filter Sidebar (260px width)
Heading: "Filters" + "Clear all" link
Sections (collapsible):
  - Item Type: checkbox list (Currency, Boost, Skin, Item, Account)
  - Price Range: dual handle slider, inputs for min/max
  - Delivery Time: radio (Any / Under 1h / Instant)
  - Seller Rating: radio (Any / 4+ / 4.5+)

### Item Card Grid (main area)
Sort bar: "2,400 items" (muted) | Sort dropdown (Popular / Cheapest / Fastest)
4-column card grid (same card style as Recent Listings on landing)
Pagination: numbered, centered, surface bg buttons

## Visual References
Reference screenshots in `designs/screenshots/` for button, card, and nav styling from kingdomofarcane.com

## Output Requirements
- Desktop layout: 1280px viewport
- Include hover states on cards, buttons, nav links
- Dark mode only (no light toggle needed)
- Designs for both pages above
EOF
```

- [ ] **Step 2: Commit stitch-prompt.md**

```bash
git add stitch-prompt.md && \
git commit -m "feat: craft STITCH prompt for landing and game page — 02-04"
```

---

### Task 6: Update GitHub Project Board

**Files:** None (GitHub UI changes)

- [ ] **Step 1: Add Stage pipeline values**

Go to: https://github.com/orgs/SaaS-Pretty-Projects/projects/1
Click "Stage" column header → "Edit field" → add these options in order:
```
Brief
Design.md
STITCH Prompt
Designs Ready
AI Studio
Launched
Operating
```

- [ ] **Step 2: Add custom fields**

Click "+" at far right of column headers, add:
```
Priority       → Number
Repository     → Text
Vertical       → Single select: Hosting, Gaming, Digital Goods, Education, Career
Revenue Model  → Single select: Subscription, Marketplace, One-time, Freemium
Tech Complexity → Single select: S, M, L
Target Launch  → Date
```

- [ ] **Step 3: Update 02-04 item**

Click the 02-04 row and set:
```
Stage:         Design.md   (brief is done, design.md is committed)
Priority:      1
Vertical:      Gaming
Revenue Model: Marketplace
Tech Complexity: M
Repository:    https://github.com/SaaS-Pretty-Projects/02-04-game-analogue
```

- [ ] **Step 4: Verify board shows pipeline**

Take a screenshot / refresh board — 02-04 should show "Design.md" stage, Priority 1, and all new fields populated.

---

## Self-Review

**Spec coverage check:**
- ✅ Board stage pipeline → Task 6
- ✅ New board fields → Task 6
- ✅ designlang extraction → Task 1
- ✅ Standard repo structure → Task 2
- ✅ Enriched brief (all required sections) → Task 3
- ✅ design.md with real tokens → Task 4
- ✅ stitch-prompt.md → Task 5
- ✅ LAUNCH-CHECKLIST.md → Task 2

**Placeholder scan:**
- Task 4 has `[from designlang]` slots — intentional. They must be filled from actual Task 1 output before committing. The executor reads Task 1 output before running Task 4.
- Task 3 has `[TBD — brand name]` — intentional. Brand name needs a real decision. Suggestions are provided.

**Type consistency:** N/A — no code tasks in this plan.
