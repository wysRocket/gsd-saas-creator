---

## [EN] Summary
GuidEnza is an AI-powered platform designed to help educators and institutions create, manage, and deliver personalized learning pathways and adaptive curriculum content. It streamlines the process of tailoring educational experiences to individual student needs, improving engagement, and optimizing learning outcomes through intelligent content generation and progress tracking.

## Brand
Name: GuidEnza
Domain: guid-enza.com
Tagline: Your AI Guide to Personalized Education.

## MVP Scope
In scope for v1:
- AI-assisted curriculum and lesson plan generation based on learning objectives and student profiles.
- Centralized content library for storing, organizing, and reusing educational materials.
- Basic learner progress tracking and performance analytics for individual students.
- User management for educators to create and manage their classes/groups.
Out of scope:
- Real-time collaborative curriculum editing for multiple educators.
- Integrations with third-party Learning Management Systems (LMS) like Canvas or Moodle.
- Advanced predictive analytics for student performance or intervention recommendations.
- Mobile applications for educators or learners.

## Key Pages / Screens
1. Landing page
2. Educator Dashboard (overview of classes, students, and curriculum)
3. Curriculum Builder (interface for AI generation and content organization)
4. Learner Profile & Progress View (detailed student performance and pathway visualization)
5. Content Library Management (upload, categorize, and search educational resources)

## Design Direction
Style: Modern Tech with a Premium feel, leaning towards a sophisticated dark mode aesthetic.
Tone: Trusted, Innovative, Empowering, Intelligent.
References: neuform.ai (for overall aesthetic inspiration)
Color mood:
- Primary: `#fff0c5` (a soft, warm yellow for highlights and calls to action)
- Secondary: `#7684ff` (a vibrant, engaging blue for interactive elements and accents)
- Accent: `#9db1ff` (a lighter blue for subtle emphasis)
- Background: Predominantly dark, using `#050505` or `#141414` with subtle gradients like `radial-gradient(circle, rgba(255, 255, 255, 0.02), rgba(0, 0, 0, 0) 58%)` for depth.
- Text: `#ffffff` for primary text, `#e7e7e7` and `#c8ccd4` for secondary text and descriptions.
- Typography: Headings will use `Inter` (light weight, e.g., 300-500) for a modern, clean look. Body text will use `Segoe UI` or `Arial` for readability, with a standard weight (400).
- Spacing: A consistent base unit of 2px, with common increments like 4px, 16px, 20px.
- Border Radii: `6px` (md) for general elements and `999px` (full) for buttons or profile images.

## Personas
**Primary:** Dr. Anya Sharma, High School Curriculum Coordinator at Progressive Academy, overwhelmed by the manual effort required to adapt lesson plans for diverse student needs and learning styles, leading to inconsistent student engagement and outcomes.
**Secondary:** Mr. David Chen, Director of Educational Technology at Horizon University, struggling to implement scalable solutions for personalized learning across multiple departments, leading to fragmented educational experiences and high operational costs.

## Pricing
Plan A: Educator Pro: $49/mo — Ideal for individual teachers. Includes 1 educator seat, unlimited classes, 50 AI curriculum generations/month, basic learner progress tracking, and access to the core content library.
Plan B: Department Plus: $199/mo — Tailored for small departments or schools. Includes up to 10 educator seats, unlimited AI curriculum generations, advanced analytics & reporting, and priority support.
Plan C: Institution Elite: $499/mo — Designed for larger institutions. Includes unlimited educator seats, full AI capabilities, custom branding, API access for future LMS integrations, dedicated account manager, and enterprise-grade security.

## Tech Stack
Auth: Supabase
DB: Postgres
Deployment: Vercel
Payments: Stripe

## Launch Success Metric
Definition of "Launched": The GuidEnza platform is publicly accessible via guid-enza.com, all core MVP features (AI curriculum generation, content library, basic learner tracking, educator dashboard) are stable and functional