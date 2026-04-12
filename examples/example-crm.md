# Example: Freelancer CRM

A complete walkthrough of using `/saas-create` to build a CRM SaaS for freelancers.

---

## 1. Trigger

```
/saas-create A lightweight CRM for freelancers to track clients, projects, invoices, and follow-ups — with a dashboard showing revenue at a glance
```

---

## 2. What @pm Produces (`REQUIREMENTS.md`)

```markdown
# Requirements: FreelanceCRM

## Product Vision
A lightweight CRM that helps independent freelancers manage their entire client lifecycle — from first contact to paid invoice — without the overhead of enterprise tools.

## User Stories
- As a freelancer, I want to add clients with contact info, so that I can keep all my leads organized.
- As a freelancer, I want to create projects linked to clients, so that I can track deliverables and deadlines.
- As a freelancer, I want to generate and send invoices, so that I get paid on time.
- As a freelancer, I want to set follow-up reminders, so that I never let a lead go cold.
- As a freelancer, I want a revenue dashboard, so that I can see my monthly earnings at a glance.

## Technical Stack
- Frontend: React / Next.js with Tailwind CSS
- Backend: Firebase Functions (Node.js)
- Database: Cloud Firestore

## Key Features
- Client list with search and status tags (lead, active, archived)
- Project tracker with status, deadline, and linked client
- Invoice generator with PDF export
- Follow-up reminder system with email notifications
- Revenue dashboard with monthly/yearly charts

## Success Metrics
- User can add a client, create a project, and send an invoice in under 3 minutes
```

> **HALT GATE**: User types `approve`

---

## 3. What @engineer Produces (`DESIGN.md`)

After running `extract_dna.py` against a Stitch project (or using defaults):

```markdown
# Design DNA: FreelanceCRM

## Color Palette
- **Primary**: `#4F46E5` (buttons, links, highlights)
- **Surface**: `#F9FAFB` (page background)
- **Text**: `#111827` (body copy)
- **Muted**: `#6B7280` (secondary labels)
- **Danger**: `#EF4444` (errors, overdue invoices)

## Typography
- **Heading**: Inter, 24px–36px, 700
- **Body**: Inter, 14px–16px, 400
- **Label**: Inter, 12px, 500 uppercase

## Component Library Mapping
- Stitch ID: `btn-primary` → React Component: `<PrimaryButton>`
- Stitch ID: `card-base` → React Component: `<Card>`
- Stitch ID: `input-text` → React Component: `<TextInput>`
- Stitch ID: `table-row` → React Component: `<TableRow>`
- Stitch ID: `badge-status` → React Component: `<StatusBadge>`

## Layout Tokens
- Container Max-Width: 1280px
- Grid Gutter: 24px
```

---

## 4. What @engineer Produces (`ARCHITECTURE.md`)

```markdown
# Architecture: FreelanceCRM

## Firestore Schema
- /users/{uid} — profile, settings
- /clients/{clientId} — name, email, phone, status, tags, ownerId
- /projects/{projectId} — title, clientId, status, deadline, ownerId
- /invoices/{invoiceId} — clientId, projectId, amount, status, dueDate, pdfUrl
- /reminders/{reminderId} — clientId, message, dueDate, sent

## Auth
- Provider: Firebase Email/Password + Google OAuth

## Firebase Functions
- POST /api/invoices/generate — renders PDF, stores in Storage, updates invoice doc
- POST /api/reminders/send — sends reminder email via SendGrid
- GET  /api/dashboard/revenue — aggregates invoice data by month
```

---

## 5. Scaffolded Project Structure

```
freelancecrm/
├── src/
│   ├── pages/
│   │   ├── index.tsx          ← Dashboard
│   │   ├── clients/index.tsx  ← Client list
│   │   ├── projects/index.tsx ← Project tracker
│   │   └── invoices/index.tsx ← Invoice list
│   ├── components/
│   │   ├── PrimaryButton.tsx
│   │   ├── Card.tsx
│   │   ├── StatusBadge.tsx
│   │   └── TableRow.tsx
│   ├── lib/
│   │   └── firebase.ts
│   └── styles/
│       └── globals.css
├── functions/
│   ├── src/
│   │   ├── invoices.ts
│   │   ├── reminders.ts
│   │   └── dashboard.ts
│   └── package.json
├── .github/workflows/deploy.yml
├── firestore.rules
├── package.json
└── .env.local.example
```

---

## 6. Deployment

After tests pass, user types `deploy`.

```
@devops running deploy.py...
  [1/5] Firestore rules applied
  [2/5] Firebase Functions deployed
  [3/5] Next.js build complete
  [4/5] Pushed to GitHub — Actions triggered
  [5/5] Hostinger skipped (not configured)

Live URL: https://freelancecrm-abc12.web.app
```

**Total time: ~23 minutes**
