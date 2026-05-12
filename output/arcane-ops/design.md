# DESIGN.md for GuidEnza

> **Source:** Generated from `design-language.md` (designlang extraction of the competitor reference) and `brief.md`. Re-run `scripts/generate_design_md.py --repo-dir output/ --force` to regenerate.

## 1. Overview / Visual Theme & Atmosphere

-   **Mood:** The visual atmosphere is **Trusted, Innovative, and Empowering**. It's a sophisticated, dark-themed environment designed for focus and clarity. The aesthetic is clean and modern, evoking a sense of premium, intelligent technology that educators can rely on. The interface feels calm and controlled, reducing cognitive load during complex tasks like curriculum building.
-   **Density:** **Comfortably Dense.** The UI is designed to handle rich information and complex data sets, such as learner analytics and content libraries, without feeling cluttered. Spacing is generous enough to allow elements to breathe, but efficient enough to keep critical information accessible without excessive scrolling.
-   **Visual Philosophy:** **Intelligent Focus.** The design prioritizes user workflow and efficiency. The dark background minimizes eye strain for long sessions, while a deliberate use of color and light guides the user’s attention to key actions, insights, and interactive elements. The overall goal is to create a seamless and intuitive experience that empowers educators, making powerful AI tools feel approachable and easy to control.
-   **Who this is for:** This design system is for educators, instructional designers, and academic administrators who are passionate about leveraging technology to create personalized learning experiences. They are professionals who value efficiency, data-driven insights, and high-quality tools that support their pedagogical goals.

## 2. Color Palette & Roles

The color system is built on a dark foundation, using a warm yellow and a vibrant blue to create clear calls to action and a focused hierarchy.

| Token | Hex | Role/Usage |
| :--- | :--- | :--- |
| **Brand/Accent** | | |
| `brand-primary` | `#fff0c5` | Primary CTAs, key highlights, active state indicators. |
| `brand-secondary` | `#7684ff` | Interactive elements, links, focus rings, secondary actions. |
| `brand-accent` | `#9db1ff` | Subtle highlights, hover states for interactive text, decorative accents. |
| **Surface/Background** | | |
| `surface-primary` | `#050505` | Main application background, the darkest layer. |
| `surface-secondary` | `#141414` | Cards, modals, side panels, and other elevated surfaces. |
| `surface-tertiary` | `#1c1c22` | Hover states on list items, nested components. |
| `surface-interactive` | `#252b39` | Default state for input fields and text areas. |
| **Text** | | |
| `text-primary` | `#ffffff` | Main headings and titles. |
| `text-secondary` | `#e7e7e7` | Body copy, paragraphs, and standard text. |
| `text-tertiary` | `#c8ccd4` | Helper text, labels, metadata, and disabled text. |
| `text-interactive` | `#9db1ff` | Links and interactive text elements. |
| `text-on-brand` | `#141414` | Text used on top of `brand-primary` backgrounds for contrast. |
| **Border** | | |
| `border-primary` | `#252b39` | Subtle borders for cards, inputs, and layout containers. |
| `border-divider` | `#1c1c22` | Separators between sections or list items. |
| `border-interactive` | `#7684ff` | Border for focused inputs and selected components. |
| **Semantic** | | |
| `semantic-success` | `#34D399` | Success messages, validation, and positive indicators. |
| `semantic-warning` | `#FBBF24` | Warnings, pending states, and cautionary notices. |
| `semantic-error` | `#F87171` | Error messages, destructive actions, and critical alerts. |

## 3. Typography Rules

The typography system uses `Inter` for its clean, modern feel in headings and `Segoe UI` for its high readability in body and UI text.

**Font Families:**
**Font heading:** Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif
**Font body:** "Segoe UI", -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif

**Full Type Scale:**

| Role | Font | Size | Weight | Line Height | Letter Spacing | Use |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Display | Inter | 60px | 500 | 72px | -1.5% | Hero/Marketing Titles |
| H1 | Inter | 48px | 500 | 56px | -1% | Primary Page Titles |
| H2 | Inter | 36px | 400 | 44px | -0.5% | Section Headers |
| H3 | Inter | 24px | 400 | 32px | 0% | Sub-section Headers, Card Titles |
| H4 | Inter | 20px | 400 | 28px | 0% | Minor Headers |
| Body L | Segoe UI | 18px | 400 | 28px | 0% | Long-form readable content |
| Body M | Segoe UI | 16px | 400 | 24px | 0% | Default body text, paragraphs |
| Label | Segoe UI | 14px | 500 | 20px | 0.5% | Form labels, UI controls, buttons |
| Caption | Segoe UI | 12px | 400 | 16px | 0.5% | Helper text, metadata, legal |

## 4. Component Stylings

Component styles are designed to be clear, interactive, and consistent with the dark, modern aesthetic.

**Buttons:**
-   **Primary:**
    -   `background`: `brand-primary` (`#fff0c5`)
    -   `text-color`: `text-on-brand` (`#141414`)
    -   `border`: `none`
    -   `padding`: `12px 24px`
    -   `radius`: `8px`
    -   `shadow`: `shadow-sm`
    -   `hover`: `transform: scale(1.03)`
    -   `active`: `transform: scale(0.98)`
-   **Secondary:**
    -   `background`: `surface-interactive` (`#252b39`)
    -   `text-color`: `text-primary` (`#ffffff`)
    -   `border`: `1px solid #252b39`
    -   `padding`: `12px 24px`
    -   `radius`: `8px`
    -   `shadow`: `none`
    -   `hover`: `background: #343c50`
    -   `active`: `background: #1f2531`
-   **Ghost:**
    -   `background`: `transparent`
    -   `text-color`: `text-interactive` (`#9db1ff`)
    -   `border`: `1px solid border-primary` (`#252b39`)
    -   `padding`: `12px 24px`
    -   `radius`: `8px`
    -   `shadow`: `none`
    -   `hover`: `background: rgba(157, 177, 255, 0.1)`
    -   `active`: `background: rgba(157, 177, 255, 0.2)`
-   **Disabled:**
    -   `background`: `surface-tertiary` (`#1c1c22`)
    -   `text-color`: `text-tertiary` (`#c8ccd4` with 50% opacity)
    -   `border`: `none`
    -   `cursor`: `not-allowed`

**Cards:**
-   `background`: `surface-secondary` (`#141414`)
-   `text-color`: `text-secondary` (`#e7e7e7`)
-   `border`: `1px solid border-primary` (`#252b39`)
-   `padding`: `24px`
-   `radius`: `12px`
-   `shadow`: `shadow-md`

**Inputs (Text Fields):**
-   `background`: `surface-interactive` (`#252b39`)
-   `text-color`: `text-secondary` (`#e7e7e7`)
-   `border`: `1px solid border-primary` (`#252b39`)
-   `padding`: `12px 16px`
-   `radius`: `8px`
-   `shadow`: `none`
-   `hover`: `border-color: #343c50`
-   `focus`: `border-color: border-interactive` (`#7684ff`), `box-shadow: 0 0 0 3px rgba(118, 132, 255, 0.2)`

**Navigation (Sidebar):**
-   `background`: `surface-primary` (`#050505`)
-   `padding`: `16px`
-   **Nav Item:**
    -   `text-color`: `text-tertiary` (`#c8ccd4`)
    -   `hover`: `background: surface-tertiary` (`#1c1c22`), `text-color: text-primary` (`#ffffff`)
    -   `active`: `background: surface-secondary` (`#141414`), `text-color: text-primary` (`#ffffff`), `border-left: 3px solid brand-secondary` (`#7684ff`)

## 5. Spacing System

The spacing system is based on an 8px base unit to ensure consistent and rhythmic layouts.

| Token | Value | Use |
| :--- | :--- | :--- |
| `space-1` | 4px | Micro-spacing within components (e.g., between icon and text). |
| `space-2` | 8px | Base unit. Small gaps between inline elements. |
| `space-3` | 12px | Gaps inside compact components like small buttons. |
| `space-4` | 16px | Standard padding for components like inputs and list items. |
| `space-5` | 20px | - |
| `space-6` | 24px | Standard padding for larger components like cards. |
| `space-8` | 32px | Gaps between medium-sized components or content sections. |
| `space-10` | 40px | - |
| `space-12` | 48px | Gaps between major layout sections. |
| `space-16` | 64px | Large gaps for page-level separation. |

## 6. Layout Principles

-   **Grid:** A 12-column, flexible grid system with a 24px gutter is used for all primary layouts. This provides structure and adaptability across different screen sizes.
-   **Max-width:** The main content container has a maximum width of `1440px`, centered on the screen. This ensures comfortable line lengths and prevents the layout from becoming too wide on large monitors.
-   **Section Rhythm:** Vertical spacing between major page sections should use `space-12` (48px) or `space-16` (64px) to create a clear visual hierarchy and rhythm.
-   **Responsive Collapsing:** The primary layout consists of a main content area and a persistent sidebar. On tablet (`md`) and smaller breakpoints, the sidebar collapses into an icon-only rail or is hidden behind a hamburger menu icon to maximize content visibility.

## 7. Depth & Elevation

Depth is created using a combination of subtle shadows and soft glows, optimized for a dark UI.

-   **Formula:** Shadows are composed of a dark, diffuse layer for depth and a subtle colored glow from `brand-secondary` to add a "tech" feel.
-   **Use Cases:**
    -   `shadow-sm`: `0px 2px 4px rgba(0, 0, 0, 0.2)`
        -   Used for small, interactive elements on hover/focus, like buttons.
    -   `shadow-md`: `0px 4px 12px rgba(0, 0, 0, 0.3), 0px 0px 2px rgba(118, 132, 255, 0.1)`
        -   The default elevation for cards, side panels, and other primary surfaces.
    -   `shadow-lg`: `0px 10px 25px rgba(0, 0, 0, 0.4), 0px 0px 8px rgba(118, 132, 255, 0.15)`
        -   Used for elements that need to appear prominently above all other content, such as modals, dialogs, and dropdown menus.

## 8. Do's and Don'ts

**Do's:**
1.  **Do use `brand-primary` (`#fff0c5`) exclusively for primary calls-to-action.** This preserves its visual weight and ensures users can always identify the most important action on a page.
2.  **Do maintain consistent vertical rhythm.** Use the defined spacing tokens (`space-4`, `space-6`, `space-12`, etc.) for all margins and padding to create a harmonious and predictable layout.
3.  **Do leverage the full text hierarchy.** Use `text-primary`, `text-secondary`, and `text-tertiary` correctly to guide the user's focus and improve content scannability.

**Don'ts:**
1.  **Don't use pure black (`#000000`).** Stick to the defined surface colors (`#050505`, `#141414`) to maintain a softer, more premium aesthetic and avoid harsh contrast.
2.  **Don't create one-off colors or spacing values.** Adherence to the design system's tokens is critical for maintaining visual consistency and scalability.
3.  **Don't overuse shadows or glows.** Depth should be used purposefully to indicate elevation and interactivity, not for decoration. Most elements should remain flat on their respective surfaces.

## 9. Responsive Behavior

-   **Breakpoints:**
    -   `sm`: `640px` (Mobile devices)
    -   `md`: `768px` (Tablets)
    -   `lg`: `1024px` (Laptops / Small desktops)
    -   `xl`: `1280px` (Standard desktops)
    -   `2xl`: `1536px` (Large desktops)
-   **Touch Targets:** All interactive elements, including buttons, links, and form controls, must have a minimum touch target size of `44px` by `44px` to ensure usability on touch devices.
-   **Collapsing Behavior:**
    -   **Navigation:** The main sidebar navigation collapses to an icon-only rail on `md` screens (tablets) and is hidden behind a hamburger menu on `sm` screens (mobile).
    -   **Data Tables:** On `sm` screens, complex data tables will become horizontally scrollable or reflow into a vertical list of cards to prevent content overflow and maintain readability.
    -   **Grids:** Multi-column layouts (e.g., 3-column card grids) will stack vertically on smaller screens, typically collapsing to a 2-column layout on tablets and a single-column layout on mobile.