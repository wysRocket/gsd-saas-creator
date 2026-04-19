# Design Language: Dark Fantasy Strategy Card Game | Kingdom of Arcane

> Extracted from `https://kingdomofarcane.com` on April 19, 2026
> 197 elements analyzed

This document describes the complete design language of the website. It is structured for AI/LLM consumption — use it to faithfully recreate the visual design in any framework.

## Color Palette

### Primary Colors

| Role | Hex | RGB | HSL | Usage Count |
|------|-----|-----|-----|-------------|
| Primary | `#00d9ff` | rgb(0, 217, 255) | hsl(189, 100%, 50%) | 201 |
| Secondary | `#e8e8f0` | rgb(232, 232, 240) | hsl(240, 21%, 93%) | 92 |
| Accent | `#00b1ff` | rgb(0, 177, 255) | hsl(198, 100%, 50%) | 13 |

### Neutral Colors

| Hex | HSL | Usage Count |
|-----|-----|-------------|
| `#000000` | hsl(0, 0%, 0%) | 76 |
| `#ffffff` | hsl(0, 0%, 100%) | 2 |

### Background Colors

Used on large-area elements: `#0a0a0f`, `#0d0d18`, `#4a08d2`, `#00b1ff`, `#010103`

### Text Colors

Text color palette: `#000000`, `#e8e8f0`, `#00d9ff`, `#9ca3af`, `#c8c8d8`, `#00b1ff`, `#4b5563`

### Gradients

```css
background-image: linear-gradient(to right in oklab, rgb(0, 217, 255) 0%, rgb(147, 51, 234) 100%);
```

```css
background-image: linear-gradient(rgba(45, 27, 61, 0.9), rgba(29, 21, 45, 0.95) 45%, rgb(19, 13, 30));
```

```css
background-image: linear-gradient(to right bottom, oklab(0.147333 0.00278564 -0.010363 / 0.95) 0%, oklab(0.16649 0.00612255 -0.0263443 / 0.85) 50%, oklab(0.192889 0.0350394 -0.0596025 / 0.9) 100%);
```

```css
background-image: repeating-linear-gradient(0deg, rgb(0, 217, 255) 0px, rgba(0, 0, 0, 0) 1px, rgba(0, 0, 0, 0) 60px), repeating-linear-gradient(90deg, rgb(0, 217, 255) 0px, rgba(0, 0, 0, 0) 1px, rgba(0, 0, 0, 0) 60px);
```

```css
background-image: linear-gradient(to right bottom, oklab(0.815954 -0.116777 -0.0864277 / 0.5) 0%, oklab(0.815954 -0.116777 -0.0864277 / 0.2) 50%, oklab(0.557523 0.135022 -0.213353 / 0.5) 100%);
```

```css
background-image: linear-gradient(to right, rgba(0, 0, 0, 0) 0%, oklab(0.815954 -0.116777 -0.0864277 / 0.6) 50%, rgba(0, 0, 0, 0) 100%);
```

```css
background-image: linear-gradient(to right, oklab(0.815954 -0.116777 -0.0864277 / 0.2) 0%, oklab(0.815954 -0.116777 -0.0864277 / 0.05) 100%);
```

```css
background-image: linear-gradient(to right, rgba(0, 0, 0, 0) 0%, oklab(0.815954 -0.116777 -0.0864277 / 0.15) 50%, rgba(0, 0, 0, 0) 100%);
```

```css
background-image: linear-gradient(to right, rgba(0, 0, 0, 0) 0%, oklab(0.557523 0.135022 -0.213353 / 0.6) 50%, rgba(0, 0, 0, 0) 100%);
```

### Full Color Inventory

| Hex | Contexts | Count |
|-----|----------|-------|
| `#00d9ff` | border, text, background | 201 |
| `#e8e8f0` | text | 92 |
| `#000000` | text, background | 76 |
| `#9ca3af` | text | 14 |
| `#00b1ff` | border, background, text | 13 |
| `#9333ea` | background | 10 |
| `#4a90e2` | background | 10 |
| `#00b4d8` | background | 10 |
| `#0a0a0f` | background | 5 |
| `#daa520` | border | 5 |
| `#ffffff` | background | 2 |
| `#c8c8d8` | text | 2 |
| `#ffb800` | border | 1 |
| `#4a08d2` | background | 1 |
| `#1a1a2e` | border | 1 |
| `#4b5563` | text | 1 |

## Typography

### Font Families

- **Inter** — used for body (101 elements)
- **ui-sans-serif** — used for body (73 elements)
- **Cinzel** — used for all (23 elements)

### Type Scale

| Size (px) | Size (rem) | Weight | Line Height | Letter Spacing | Used On |
|-----------|------------|--------|-------------|----------------|---------|
| 28px | 1.75rem | 600 | 39.2px | 0.42px | h3 |
| 20px | 1.25rem | 700 | 28px | normal | span |
| 16px | 1rem | 400 | 24px | normal | html, head, meta, title |
| 14.4px | 0.9rem | 500 | 21.6px | 1.152px | button, a, svg, path |
| 14px | 0.875rem | 500 | 20px | 1.152px | span, input |
| 12px | 0.75rem | 400 | 16px | 0.72px | p, button, span |
| 11.2px | 0.7rem | 500 | 16.8px | 0.56px | label |

### Heading Scale

```css
h3 { font-size: 28px; font-weight: 600; line-height: 39.2px; }
```

### Body Text

```css
body { font-size: 12px; font-weight: 400; line-height: 16px; }
```

### Font Weights in Use

`400` (174x), `500` (19x), `600` (3x), `700` (1x)

## Spacing

| Token | Value | Rem |
|-------|-------|-----|
| spacing-4 | 4px | 0.25rem |
| spacing-112 | 112px | 7rem |

## Border Radii

| Label | Value | Count |
|-------|-------|-------|
| md | 6px | 3 |
| lg | 12px | 4 |
| lg | 16px | 2 |

## Box Shadows

**sm (inset)** — blur: 0px
```css
box-shadow: rgba(255, 184, 0, 0.8) 0px 0px 0px 2px, rgba(0, 0, 0, 0.8) 0px 0px 0px 3px, rgba(255, 255, 255, 0.25) 0px 2px 4px 0px inset, rgba(0, 0, 0, 0.5) 0px -2px 4px 0px inset, rgba(0, 217, 255, 0.4) 0px 0px 20px 0px, rgba(0, 0, 0, 0.8) 0px 8px 16px 0px;
```

**sm** — blur: 0px
```css
box-shadow: rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 217, 255, 0.15) 0px 0px 12px 0px;
```

**sm (inset)** — blur: 0px
```css
box-shadow: rgba(139, 92, 46, 0.6) 0px 0px 0px 2px, rgba(0, 0, 0, 0.8) 0px 0px 0px 3px, rgba(255, 255, 255, 0.15) 0px 2px 4px 0px inset, rgba(0, 0, 0, 0.4) 0px -2px 4px 0px inset, rgba(0, 0, 0, 0.6) 0px 6px 12px 0px;
```

**sm** — blur: 4px
```css
box-shadow: rgb(0, 180, 216) 0px 0px 4px 0px;
```

**sm** — blur: 4px
```css
box-shadow: rgb(0, 217, 255) 0px 0px 4px 0px;
```

**sm** — blur: 4px
```css
box-shadow: rgb(74, 144, 226) 0px 0px 4px 0px;
```

**sm** — blur: 4px
```css
box-shadow: rgb(147, 51, 234) 0px 0px 4px 0px;
```

**sm** — blur: 4.3428px
```css
box-shadow: rgb(147, 51, 234) 0px 0px 4.3428px 0px;
```

**sm** — blur: 4.4109px
```css
box-shadow: rgb(0, 217, 255) 0px 0px 4.4109px 0px;
```

**sm** — blur: 4.4616px
```css
box-shadow: rgb(147, 51, 234) 0px 0px 4.4616px 0px;
```

**sm** — blur: 4.5549px
```css
box-shadow: rgb(0, 180, 216) 0px 0px 4.5549px 0px;
```

**sm** — blur: 4.6926px
```css
box-shadow: rgb(147, 51, 234) 0px 0px 4.6926px 0px;
```

**sm** — blur: 4.6968px
```css
box-shadow: rgb(0, 180, 216) 0px 0px 4.6968px 0px;
```

**sm** — blur: 4.7025px
```css
box-shadow: rgb(0, 217, 255) 0px 0px 4.7025px 0px;
```

**sm** — blur: 4.7088px
```css
box-shadow: rgb(74, 144, 226) 0px 0px 4.7088px 0px;
```

**sm** — blur: 5.0541px
```css
box-shadow: rgb(74, 144, 226) 0px 0px 5.0541px 0px;
```

**sm** — blur: 5.1021px
```css
box-shadow: rgb(147, 51, 234) 0px 0px 5.1021px 0px;
```

**sm** — blur: 5.2863px
```css
box-shadow: rgb(0, 180, 216) 0px 0px 5.2863px 0px;
```

**sm** — blur: 5.3634px
```css
box-shadow: rgb(147, 51, 234) 0px 0px 5.3634px 0px;
```

**sm** — blur: 5.3904px
```css
box-shadow: rgb(74, 144, 226) 0px 0px 5.3904px 0px;
```

**sm** — blur: 5.6583px
```css
box-shadow: rgb(0, 180, 216) 0px 0px 5.6583px 0px;
```

**sm** — blur: 5.6553px
```css
box-shadow: rgb(147, 51, 234) 0px 0px 5.6553px 0px;
```

**sm** — blur: 5.7015px
```css
box-shadow: rgb(0, 217, 255) 0px 0px 5.7015px 0px;
```

**sm** — blur: 5.808px
```css
box-shadow: rgb(0, 217, 255) 0px 0px 5.808px 0px;
```

**sm** — blur: 5.8257px
```css
box-shadow: rgb(147, 51, 234) 0px 0px 5.8257px 0px;
```

**sm** — blur: 6.405px
```css
box-shadow: rgb(74, 144, 226) 0px 0px 6.405px 0px;
```

**sm** — blur: 6.4074px
```css
box-shadow: rgb(74, 144, 226) 0px 0px 6.4074px 0px;
```

**sm** — blur: 6.5274px
```css
box-shadow: rgb(74, 144, 226) 0px 0px 6.5274px 0px;
```

**sm** — blur: 6.6078px
```css
box-shadow: rgb(0, 180, 216) 0px 0px 6.6078px 0px;
```

**sm** — blur: 6.6609px
```css
box-shadow: rgb(74, 144, 226) 0px 0px 6.6609px 0px;
```

**sm** — blur: 7.2351px
```css
box-shadow: rgb(0, 180, 216) 0px 0px 7.2351px 0px;
```

**sm** — blur: 7.4082px
```css
box-shadow: rgb(147, 51, 234) 0px 0px 7.4082px 0px;
```

**sm** — blur: 7.5705px
```css
box-shadow: rgb(0, 217, 255) 0px 0px 7.5705px 0px;
```

**sm** — blur: 7.8234px
```css
box-shadow: rgb(0, 217, 255) 0px 0px 7.8234px 0px;
```

**md** — blur: 8.0178px
```css
box-shadow: rgb(0, 180, 216) 0px 0px 8.0178px 0px;
```

**md** — blur: 8.1627px
```css
box-shadow: rgb(0, 217, 255) 0px 0px 8.1627px 0px;
```

**md** — blur: 8.2005px
```css
box-shadow: rgb(0, 217, 255) 0px 0px 8.2005px 0px;
```

**md** — blur: 8.421px
```css
box-shadow: rgb(0, 180, 216) 0px 0px 8.421px 0px;
```

**md** — blur: 8.5518px
```css
box-shadow: rgb(0, 180, 216) 0px 0px 8.5518px 0px;
```

**md** — blur: 8.7015px
```css
box-shadow: rgb(147, 51, 234) 0px 0px 8.7015px 0px;
```

**md** — blur: 8.874px
```css
box-shadow: rgb(0, 217, 255) 0px 0px 8.874px 0px;
```

**md** — blur: 8.9496px
```css
box-shadow: rgb(74, 144, 226) 0px 0px 8.9496px 0px;
```

## CSS Custom Properties

### Colors

```css
--gold-accent: #ffb800;
--warm-accent: #ff8c00;
--warm-accent-deep: #ff6b00;
--auth-input-bg: #0d0d1a;
--auth-tab-bg: #0a0a14;
--foreground: #e8e8f0;
--card: #13131a;
--card-foreground: #e8e8f0;
--popover: #1a1a2e;
--popover-foreground: #e8e8f0;
--primary: #00d9ff;
--primary-foreground: #0a0a0f;
--secondary: #2d1b3d;
--secondary-foreground: #e8e8f0;
--muted: #1f1f2e;
--muted-foreground: #9ca3af;
--accent: #9333ea;
--accent-foreground: #fff;
--destructive: #ef4444;
--destructive-foreground: #fff;
--border: #00d9ff26;
--ring: #00d9ff;
--chart-1: #00d9ff;
--chart-2: #9333ea;
--chart-3: #ffb800;
--chart-4: #4a90e2;
--chart-5: #06b6d4;
--sidebar-foreground: #e8e8f0;
--sidebar-primary: #00d9ff;
--sidebar-primary-foreground: #0a0a0f;
--sidebar-accent: #2d1b3d;
--sidebar-accent-foreground: #e8e8f0;
--sidebar-border: #00d9ff26;
--sidebar-ring: #00d9ff;
--color-amber-400: oklch(82.8% .189 84.429);
--tw-ring-shadow: 0 0 #0000;
--color-slate-700: oklch(37.2% .044 257.287);
--tw-inset-ring-shadow: 0 0 #0000;
--color-red-200: oklch(88.5% .062 18.334);
--color-yellow-400: oklch(85.2% .199 91.936);
--color-slate-300: oklch(86.9% .022 252.894);
--tw-ring-offset-color: #fff;
--color-red-400: oklch(70.4% .191 22.216);
--color-white: #fff;
--color-gray-400: oklch(70.7% .022 261.325);
--color-gray-100: oklch(96.7% .003 264.542);
--color-red-500: oklch(63.7% .237 25.331);
--tw-ring-offset-width: 0px;
--tw-ring-offset-shadow: 0 0 #0000;
--color-red-300: oklch(80.8% .114 19.571);
--color-orange-400: oklch(75% .183 55.934);
--tw-border-style: solid;
--color-gray-200: oklch(92.8% .006 264.531);
--color-black: #000;
```

### Spacing

```css
--font-size: 16px;
--spacing: .25rem;
--tw-space-y-reverse: 0;
```

### Typography

```css
--font-display: "Cinzel",serif;
--font-body: "Inter",sans-serif;
--font-weight-medium: 500;
--font-weight-normal: 400;
--tracking-tight: -.025em;
--text-2xl: 1.5rem;
--text-lg: 1.125rem;
--text-5xl--line-height: 1;
--text-base--line-height: 1.5;
--tracking-wider: .05em;
--font-mono: ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,"Liberation Mono","Courier New",monospace;
--text-lg--line-height: 1.55556;
--font-sans: ui-sans-serif,system-ui,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji";
--font-weight-bold: 700;
--default-font-family: ui-sans-serif,system-ui,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji";
--text-xs--line-height: 1.33333;
--text-xl: 1.25rem;
--leading-relaxed: 1.625;
--leading-snug: 1.375;
--tracking-tighter: -.05em;
--font-weight-black: 900;
--text-2xl--line-height: 1.33333;
--tracking-wide: .025em;
--text-xl--line-height: 1.4;
--font-weight-semibold: 600;
--text-sm: .875rem;
--leading-tight: 1.25;
--text-4xl: 2.25rem;
--text-sm--line-height: 1.42857;
--text-5xl: 3rem;
--text-3xl--line-height: 1.2;
--text-xs: .75rem;
--tracking-widest: .1em;
--text-3xl: 1.875rem;
--font-serif: ui-serif,Georgia,Cambria,"Times New Roman",Times,serif;
--text-4xl--line-height: 1.11111;
--text-base: 1rem;
--default-mono-font-family: ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,"Liberation Mono","Courier New",monospace;
```

### Shadows

```css
--tw-inset-shadow-alpha: 100%;
--tw-drop-shadow-alpha: 100%;
--tw-inset-shadow: 0 0 #0000;
--tw-shadow-alpha: 100%;
--drop-shadow-md: 0 3px 3px #0000001f;
--tw-shadow: 0 0 #0000;
```

### Radii

```css
--radius: .5rem;
--radius-2xl: 1rem;
```

### Other

```css
--arcane-black: #0a0a0f;
--deep-charcoal: #13131a;
--midnight-blue: #1a1a2e;
--dark-violet: #2d1b3d;
--arcane-cyan: #00d9ff;
--arcane-blue: #4a90e2;
--purple-glow: #9333ea;
--cyan-glow: #06b6d4;
--warm-dark: #1a0f00;
--warm-dark-deep: #2e1a0a;
--cool-dark: #1a0a2e;
--light-purple: #c4b5fd;
--gold-bright: gold;
--cyan-alt: #00b4d8;
--background: #0a0a0f;
--input: #00d9ff1a;
--input-background: #13131a;
--switch-background: #2d1b3d;
--sidebar: #13131a;
--container-md: 28rem;
--blur-lg: 16px;
--tw-animation-delay: 0s;
--tw-outline-style: solid;
--ease-in: cubic-bezier(.4,0,1,1);
--tw-animation-direction: normal;
--tw-enter-scale: 1;
--blur-xl: 24px;
--tw-gradient-from: rgba(0, 0, 0, 0);
--tw-gradient-to: rgba(0, 0, 0, 0);
--blur-3xl: 64px;
--tw-exit-rotate: 0;
--tw-scale-z: 1;
--blur-2xl: 40px;
--container-sm: 24rem;
--tw-exit-translate-y: 0;
--tw-gradient-via-position: 50%;
--container-lg: 32rem;
--tw-gradient-to-position: 100%;
--default-transition-duration: .15s;
--animate-pulse: pulse 2s cubic-bezier(.4,0,.6,1) infinite;
--tw-gradient-from-position: 0%;
--ease-in-out: cubic-bezier(.4,0,.2,1);
--default-transition-timing-function: cubic-bezier(.4,0,.2,1);
--tw-animation-iteration-count: 1;
--tw-exit-opacity: 1;
--tw-animation-fill-mode: none;
--tw-exit-blur: 0;
--tw-translate-z: 0;
--tw-gradient-via: rgba(0, 0, 0, 0);
--tw-scale-y: 1;
--container-6xl: 72rem;
--tw-exit-translate-x: 0;
--container-3xl: 48rem;
--tw-translate-y: 0;
--blur-md: 12px;
--ease-out: cubic-bezier(0,0,.2,1);
--animate-spin: spin 1s linear infinite;
--tw-enter-translate-x: 0;
--container-4xl: 56rem;
--container-2xl: 42rem;
--tw-exit-scale: 1;
--tw-translate-x: 0;
--tw-enter-rotate: 0;
--tw-scale-x: 1;
--tw-enter-translate-y: 0;
--tw-enter-blur: 0;
--container-xl: 36rem;
--tw-enter-opacity: 1;
--blur-sm: 8px;
```

### Semantic

```css
success: [object Object];
warning: [object Object];
error: [object Object];
info: [object Object];
```

## Breakpoints

| Name | Value | Type |
|------|-------|------|
| sm | 639px | max-width |
| md | 768px | min-width |
| lg | 1024px | min-width |

## Transitions & Animations

**Easing functions:** `[object Object]`, `[object Object]`

**Durations:** `0.3s`, `0.15s`, `0.7s`, `0.5s`

### Common Transitions

```css
transition: all;
transition: box-shadow 0.3s cubic-bezier(0.4, 0, 0.2, 1);
transition: color 0.15s cubic-bezier(0.4, 0, 0.2, 1), background-color 0.15s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.15s cubic-bezier(0.4, 0, 0.2, 1), outline-color 0.15s cubic-bezier(0.4, 0, 0.2, 1), text-decoration-color 0.15s cubic-bezier(0.4, 0, 0.2, 1), fill 0.15s cubic-bezier(0.4, 0, 0.2, 1), stroke 0.15s cubic-bezier(0.4, 0, 0.2, 1), --tw-gradient-from 0.15s cubic-bezier(0.4, 0, 0.2, 1), --tw-gradient-via 0.15s cubic-bezier(0.4, 0, 0.2, 1), --tw-gradient-to 0.15s cubic-bezier(0.4, 0, 0.2, 1);
transition: opacity 0.15s cubic-bezier(0.4, 0, 0.2, 1);
transition: 0.7s cubic-bezier(0.4, 0, 0.2, 1);
transition: opacity 0.7s cubic-bezier(0.4, 0, 0.2, 1);
transition: background 0.7s, box-shadow 0.7s;
transition: 0.5s cubic-bezier(0.4, 0, 0.2, 1);
transition: color 0.5s cubic-bezier(0.4, 0, 0.2, 1), background-color 0.5s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.5s cubic-bezier(0.4, 0, 0.2, 1), outline-color 0.5s cubic-bezier(0.4, 0, 0.2, 1), text-decoration-color 0.5s cubic-bezier(0.4, 0, 0.2, 1), fill 0.5s cubic-bezier(0.4, 0, 0.2, 1), stroke 0.5s cubic-bezier(0.4, 0, 0.2, 1), --tw-gradient-from 0.5s cubic-bezier(0.4, 0, 0.2, 1), --tw-gradient-via 0.5s cubic-bezier(0.4, 0, 0.2, 1), --tw-gradient-to 0.5s cubic-bezier(0.4, 0, 0.2, 1);
transition: 0.3s cubic-bezier(0, 0, 0.2, 1);
```

### Keyframe Animations

**accordion-down**
```css
@keyframes accordion-down {
  0% { height: 0px; }
  100% { height: var(--radix-accordion-content-height,var(--bits-accordion-content-height,var(--reka-accordion-content-height,var(--kb-accordion-content-height,var(--ngp-accordion-content-height,auto))))); }
}
```

**accordion-up**
```css
@keyframes accordion-up {
  0% { height: var(--radix-accordion-content-height,var(--bits-accordion-content-height,var(--reka-accordion-content-height,var(--kb-accordion-content-height,var(--ngp-accordion-content-height,auto))))); }
  100% { height: 0px; }
}
```

**spin**
```css
@keyframes spin {
  100% { transform: rotate(1turn); }
}
```

**pulse**
```css
@keyframes pulse {
  50% { opacity: 0.5; }
}
```

**spin-4da313db**
```css
@keyframes spin-4da313db {
  100% { transform: rotate(1turn); }
}
```

## Component Patterns

Detected UI component patterns and their most common styles:

### Buttons (6 instances)

```css
.button {
  background-color: oklab(0.999994 0.0000455678 0.0000200868 / 0.05);
  color: rgb(0, 217, 255);
  font-size: 14.4px;
  font-weight: 500;
  padding-top: 10px;
  padding-right: 0px;
  border-radius: 0px;
}
```

### Cards (40 instances)

```css
.card {
  background-color: rgb(0, 217, 255);
  border-radius: 3.35544e+07px;
  box-shadow: rgb(74, 144, 226) 0px 0px 4px 0px;
  padding-top: 0px;
  padding-right: 0px;
}
```

### Inputs (2 instances)

```css
.input {
  background-color: oklab(0.16649 0.00612255 -0.0263443 / 0.8);
  color: rgb(232, 232, 240);
  border-color: oklab(0.815954 -0.116777 -0.0864277 / 0.15);
  border-radius: 8px;
  font-size: 14px;
  padding-top: 12px;
  padding-right: 16px;
}
```

### Links (1 instances)

```css
.link {
  color: rgb(232, 232, 240);
  font-size: 14.4px;
  font-weight: 500;
}
```

### Dropdowns (1 instances)

```css
.dropdown {
  border-radius: 0px;
  border-color: rgba(0, 217, 255, 0.15);
  padding-top: 0px;
}
```

### Tabs (1 instances)

```css
.tab {
  background-color: rgb(10, 10, 20);
  color: rgb(232, 232, 240);
  font-size: 16px;
  font-weight: 400;
  padding-top: 4px;
  padding-right: 4px;
  border-color: rgb(26, 26, 46);
  border-radius: 8px;
}
```

## Component Clusters

Reusable component instances grouped by DOM structure and style similarity:

### Button — 1 instance, 1 variant

**Variant 1** (1 instance)

```css
  background: oklab(0.999994 0.0000455678 0.0000200868 / 0.05);
  color: rgb(232, 232, 240);
  padding: 8px 12px 8px 12px;
  border-radius: 0px;
  border: 3px solid rgba(255, 184, 0, 0.7) rgba(218, 165, 32, 0.6) rgba(139, 92, 46, 0.6) rgba(255, 184, 0, 0.7);
  font-size: 14.4px;
  font-weight: 500;
```

### Button — 4 instances, 2 variants

**Variant 1** (3 instances)

```css
  background: rgba(0, 0, 0, 0);
  color: rgb(0, 217, 255);
  padding: 10px 0px 10px 0px;
  border-radius: 6px;
  border: 3px solid rgba(218, 165, 32, 0.4) rgba(139, 92, 46, 0.4) rgba(92, 64, 51, 0.4) rgba(218, 165, 32, 0.4);
  font-size: 12px;
  font-weight: 600;
```

**Variant 2** (1 instance)

```css
  background: rgba(0, 0, 0, 0);
  color: oklab(0.815954 -0.116777 -0.0864277 / 0.7);
  padding: 0px 0px 0px 0px;
  border-radius: 0px;
  border: 3px solid rgba(218, 165, 32, 0.4) rgba(139, 92, 46, 0.4) rgba(92, 64, 51, 0.4) rgba(218, 165, 32, 0.4);
  font-size: 12px;
  font-weight: 500;
```

### Input — 1 instance, 1 variant

**Variant 1** (1 instance)

```css
  background: oklab(0.16649 0.00612255 -0.0263443 / 0.8);
  color: rgb(232, 232, 240);
  padding: 12px 16px 12px 40px;
  border-radius: 8px;
  border: 1px solid oklab(0.815954 -0.116777 -0.0864277 / 0.15);
  font-size: 14px;
  font-weight: 400;
```

### Button — 1 instance, 1 variant

**Variant 1** (1 instance)

```css
  background: rgba(0, 0, 0, 0);
  color: rgb(156, 163, 175);
  padding: 0px 0px 0px 0px;
  border-radius: 0px;
  border: 3px solid rgba(218, 165, 32, 0.4) rgba(139, 92, 46, 0.4) rgba(92, 64, 51, 0.4) rgba(218, 165, 32, 0.4);
  font-size: 14.4px;
  font-weight: 500;
```

## Layout System

**0 grid containers** and **12 flex containers** detected.

### Container Widths

| Max Width | Padding |
|-----------|---------|
| 1440px | 32px |
| 100% | 0px |
| 440px | 0px |

### Flex Patterns

| Direction/Wrap | Count |
|----------------|-------|
| row/nowrap | 11x |
| column/nowrap | 1x |

**Gap values:** `12px`, `6px`, `8px`

## Responsive Design

### Viewport Snapshots

| Viewport | Body Font | Nav Visible | Max Columns | Hamburger | Page Height |
|----------|-----------|-------------|-------------|-----------|-------------|
| mobile (375px) | 16px | No | 2 | No | 17963px |
| tablet (768px) | 16px | No | 3 | No | 12397px |
| desktop (1280px) | 16px | No | 6 | No | 9659px |
| wide (1920px) | 16px | No | 6 | No | 9750px |

### Breakpoint Changes

**375px → 768px** (mobile → tablet):
- Max grid columns: `2` → `3`
- Page height: `17963px` → `12397px`

**768px → 1280px** (tablet → desktop):
- Max grid columns: `3` → `6`
- Page height: `12397px` → `9659px`

## Interaction States

### Button States

**"Accept All"**
```css
/* Hover */
background-color: rgba(0, 0, 0, 0) → oklab(0.815954 -0.116777 -0.0864277 / 0.0460276);
border-color: oklab(0.815954 -0.116777 -0.0864277 / 0.4) → oklab(0.815954 -0.116777 -0.0864277 / 0.676166);
box-shadow: rgba(139, 92, 46, 0.6) 0px 0px 0px 2px, rgba(0, 0, 0, 0.8) 0px 0px 0px 3px, rgba(255, 255, 255, 0.15) 0px 2px 4px 0px inset, rgba(0, 0, 0, 0.4) 0px -2px 4px 0px inset, rgba(0, 0, 0, 0.6) 0px 6px 12px 0px → rgba(248, 178, 3, 0.784) 0px 0px 0px 2px, rgba(0, 0, 0, 0.8) 0px 0px 0px 3px, rgba(255, 255, 255, 0.243) 0px 2px 4px 0px inset, rgba(0, 0, 0, 0.494) 0px -2px 4px 0px inset, rgba(0, 192, 226, 0.416) 0px 0.47669px 19.3644px 0px, rgba(0, 0, 0, 0.737) 0px 7.36441px 14.7288px 0px;
transform: none → matrix(1, 0, 0, 1, 0, -0.920552);
```
```css
/* Focus */
background-color: rgba(0, 0, 0, 0) → oklab(0.815954 -0.116777 -0.0864277 / 0.05);
border-color: oklab(0.815954 -0.116777 -0.0864277 / 0.4) → oklab(0.815954 -0.116777 -0.0864277 / 0.7);
box-shadow: rgba(139, 92, 46, 0.6) 0px 0px 0px 2px, rgba(0, 0, 0, 0.8) 0px 0px 0px 3px, rgba(255, 255, 255, 0.15) 0px 2px 4px 0px inset, rgba(0, 0, 0, 0.4) 0px -2px 4px 0px inset, rgba(0, 0, 0, 0.6) 0px 6px 12px 0px → rgba(255, 184, 0, 0.8) 0px 0px 0px 2px, rgba(0, 0, 0, 0.8) 0px 0px 0px 3px, rgba(255, 255, 255, 0.25) 0px 2px 4px 0px inset, rgba(0, 0, 0, 0.5) 0px -2px 4px 0px inset, rgba(0, 217, 255, 0.4) 0px 0px 20px 0px, rgba(0, 0, 0, 0.8) 0px 8px 16px 0px;
transform: none → matrix(1, 0, 0, 1, 0, -1);
outline: oklab(0.815954 -0.116777 -0.0864277 / 0.5) none 3px → oklab(0.815954 -0.116777 -0.0864277 / 0.5) auto 1px;
```

**"Reject Non-Essential"**
```css
/* Hover */
background-color: rgba(0, 0, 0, 0) → oklab(0.815954 -0.116777 -0.0864277 / 0.0418497);
border-color: oklab(0.815954 -0.116777 -0.0864277 / 0.4) → oklab(0.815954 -0.116777 -0.0864277 / 0.651098);
box-shadow: rgba(139, 92, 46, 0.6) 0px 0px 0px 2px, rgba(0, 0, 0, 0.8) 0px 0px 0px 3px, rgba(255, 255, 255, 0.15) 0px 2px 4px 0px inset, rgba(0, 0, 0, 0.4) 0px -2px 4px 0px inset, rgba(0, 0, 0, 0.6) 0px 6px 12px 0px → rgba(240, 172, 6, 0.77) 0px 0px 0px 2px, rgba(0, 0, 0, 0.8) 0px 0px 0px 3px, rgba(255, 255, 255, 0.235) 0px 2px 4px 0px inset, rgba(0, 0, 0, 0.486) 0px -2px 4px 0px inset, rgba(0, 168, 197, 0.43) 0px 0.978037px 18.696px 0px, rgba(0, 0, 0, 0.67) 0px 6.69595px 13.3919px 0px;
transform: none → matrix(1, 0, 0, 1, 0, -0.836994);
```
```css
/* Focus */
background-color: rgba(0, 0, 0, 0) → oklab(0.815954 -0.116777 -0.0864277 / 0.05);
border-color: oklab(0.815954 -0.116777 -0.0864277 / 0.4) → oklab(0.815954 -0.116777 -0.0864277 / 0.7);
box-shadow: rgba(139, 92, 46, 0.6) 0px 0px 0px 2px, rgba(0, 0, 0, 0.8) 0px 0px 0px 3px, rgba(255, 255, 255, 0.15) 0px 2px 4px 0px inset, rgba(0, 0, 0, 0.4) 0px -2px 4px 0px inset, rgba(0, 0, 0, 0.6) 0px 6px 12px 0px → rgba(255, 184, 0, 0.8) 0px 0px 0px 2px, rgba(0, 0, 0, 0.8) 0px 0px 0px 3px, rgba(255, 255, 255, 0.25) 0px 2px 4px 0px inset, rgba(0, 0, 0, 0.5) 0px -2px 4px 0px inset, rgba(0, 217, 255, 0.4) 0px 0px 20px 0px, rgba(0, 0, 0, 0.8) 0px 8px 16px 0px;
transform: none → matrix(1, 0, 0, 1, 0, -1);
outline: oklab(0.815954 -0.116777 -0.0864277 / 0.5) none 3px → oklab(0.815954 -0.116777 -0.0864277 / 0.5) auto 1px;
```

**"Manage Preferences"**
```css
/* Hover */
background-color: rgba(0, 0, 0, 0) → oklab(0.815954 -0.116777 -0.0864277 / 0.04185);
border-color: oklab(0.815954 -0.116777 -0.0864277 / 0.4) → oklab(0.815954 -0.116777 -0.0864277 / 0.6511);
box-shadow: rgba(139, 92, 46, 0.6) 0px 0px 0px 2px, rgba(0, 0, 0, 0.8) 0px 0px 0px 3px, rgba(255, 255, 255, 0.15) 0px 2px 4px 0px inset, rgba(0, 0, 0, 0.4) 0px -2px 4px 0px inset, rgba(0, 0, 0, 0.6) 0px 6px 12px 0px → rgba(240, 172, 6, 0.77) 0px 0px 0px 2px, rgba(0, 0, 0, 0.8) 0px 0px 0px 3px, rgba(255, 255, 255, 0.235) 0px 2px 4px 0px inset, rgba(0, 0, 0, 0.486) 0px -2px 4px 0px inset, rgba(0, 168, 197, 0.43) 0px 0.977998px 18.696px 0px, rgba(0, 0, 0, 0.67) 0px 6.696px 13.392px 0px;
transform: none → matrix(1, 0, 0, 1, 0, -0.837);
```
```css
/* Focus */
background-color: rgba(0, 0, 0, 0) → oklab(0.815954 -0.116777 -0.0864277 / 0.05);
border-color: oklab(0.815954 -0.116777 -0.0864277 / 0.4) → oklab(0.815954 -0.116777 -0.0864277 / 0.7);
box-shadow: rgba(139, 92, 46, 0.6) 0px 0px 0px 2px, rgba(0, 0, 0, 0.8) 0px 0px 0px 3px, rgba(255, 255, 255, 0.15) 0px 2px 4px 0px inset, rgba(0, 0, 0, 0.4) 0px -2px 4px 0px inset, rgba(0, 0, 0, 0.6) 0px 6px 12px 0px → rgba(255, 184, 0, 0.8) 0px 0px 0px 2px, rgba(0, 0, 0, 0.8) 0px 0px 0px 3px, rgba(255, 255, 255, 0.25) 0px 2px 4px 0px inset, rgba(0, 0, 0, 0.5) 0px -2px 4px 0px inset, rgba(0, 217, 255, 0.4) 0px 0px 20px 0px, rgba(0, 0, 0, 0.8) 0px 8px 16px 0px;
transform: none → matrix(1, 0, 0, 1, 0, -1);
outline: oklab(0.815954 -0.116777 -0.0864277 / 0.5) none 3px → oklab(0.815954 -0.116777 -0.0864277 / 0.5) auto 1px;
```

### Link Hover

```css
text-decoration: none → underline;
```

## Accessibility (WCAG 2.1)

**Overall Score: 17%** — 9 passing, 43 failing color pairs

### Failing Color Pairs

| Foreground | Background | Ratio | Level | Used On |
|------------|------------|-------|-------|---------|
| `#e8e8f0` | `#00d9ff` | 1.39:1 | FAIL | div (10x) |
| `#e8e8f0` | `#9333ea` | 4.42:1 | FAIL | div (10x) |
| `#e8e8f0` | `#4a90e2` | 2.7:1 | FAIL | div (10x) |
| `#e8e8f0` | `#00b4d8` | 2.02:1 | FAIL | div (10x) |
| `#e8e8f0` | `#ffffff` | 1.22:1 | FAIL | button, div (2x) |
| `#e8e8f0` | `#00b1ff` | 1.97:1 | FAIL | div (1x) |

### Passing Color Pairs

| Foreground | Background | Ratio | Level |
|------------|------------|-------|-------|
| `#e8e8f0` | `#0a0a0f` | 16.21:1 | AAA |
| `#e8e8f0` | `#010103` | 17.11:1 | AAA |
| `#e8e8f0` | `#0d0d18` | 15.84:1 | AAA |
| `#e8e8f0` | `#4a08d2` | 7.64:1 | AAA |
| `#e8e8f0` | `#0a0a14` | 16.16:1 | AAA |

## Design System Score

**Overall: 61/100 (Grade: D)**

| Category | Score |
|----------|-------|
| Color Discipline | 70/100 |
| Typography Consistency | 80/100 |
| Spacing System | 40/100 |
| Shadow Consistency | 50/100 |
| Border Radius Consistency | 100/100 |
| Accessibility | 17/100 |
| CSS Tokenization | 100/100 |

**Strengths:** Consistent border radii, Good CSS variable tokenization

**Issues:**
- No consistent spacing base unit detected — values appear arbitrary
- 42 unique shadows — consider a 3-level elevation scale (sm/md/lg)
- 43 WCAG contrast failures
- 1118 duplicate CSS declarations

## Gradients

**10 unique gradients** detected.

| Type | Direction | Stops | Classification |
|------|-----------|-------|----------------|
| linear | to right in oklab | 2 | brand |
| linear | — | 3 | bold |
| linear | to right bottom | 3 | bold |
| repeating-linear | 0deg | 3 | bold |
| repeating-linear | 90deg | 3 | bold |
| linear | to right bottom | 3 | bold |
| linear | to right | 3 | bold |
| linear | to right | 2 | brand |
| linear | to right | 3 | bold |
| linear | to right | 3 | bold |

```css
background: linear-gradient(to right in oklab, rgb(0, 217, 255) 0%, rgb(147, 51, 234) 100%);
background: linear-gradient(rgba(45, 27, 61, 0.9), rgba(29, 21, 45, 0.95) 45%, rgb(19, 13, 30));
background: linear-gradient(to right bottom, oklab(0.147333 0.00278564 -0.010363 / 0.95) 0%, oklab(0.16649 0.00612255 -0.0263443 / 0.85) 50%, oklab(0.192889 0.0350394 -0.0596025 / 0.9) 100%);
background: repeating-linear-gradient(0deg, rgb(0, 217, 255) 0px, rgba(0, 0, 0, 0) 1px, rgba(0, 0, 0, 0) 60px);
background: repeating-linear-gradient(90deg, rgb(0, 217, 255) 0px, rgba(0, 0, 0, 0) 1px, rgba(0, 0, 0, 0) 60px);
```

## Z-Index Map

**2 unique z-index values** across 1 layers.

| Layer | Range | Elements |
|-------|-------|----------|
| sticky | 10,50 | div.r.e.l.a.t.i.v.e. .z.-.1.0. .w.-.f.u.l.l. .m.a.x.-.w.-.[.4.4.0.p.x.]. .m.y.-.a.u.t.o, header.f.i.x.e.d. .t.o.p.-.0. .l.e.f.t.-.0. .r.i.g.h.t.-.0. .z.-.5.0. .b.g.-.[.#.0.d.0.d.1.8.]. .b.o.r.d.e.r.-.b. .b.o.r.d.e.r.-.[.v.a.r.(.-.-.a.r.c.a.n.e.-.c.y.a.n.).]./.1.5. .t.r.a.n.s.i.t.i.o.n.-.s.h.a.d.o.w. .d.u.r.a.t.i.o.n.-.3.0.0, div.r.e.l.a.t.i.v.e. .z.-.5.0 |

## SVG Icons

**5 unique SVG icons** detected. Dominant style: **outlined**.

| Size Class | Count |
|------------|-------|
| sm | 4 |
| md | 1 |

**Icon colors:** `currentColor`

## Image Style Patterns

| Pattern | Count | Key Styles |
|---------|-------|------------|
| thumbnail | 2 | objectFit: fill, borderRadius: 0px, shape: square |
| hero | 1 | objectFit: cover, borderRadius: 0px, shape: square |

**Aspect ratios:** 1:1 (2x), 3:2 (1x)

## Quick Start

To recreate this design in a new project:

1. **Install fonts:** Add `Inter` from Google Fonts or your font provider
2. **Import CSS variables:** Copy `variables.css` into your project
3. **Tailwind users:** Use the generated `tailwind.config.js` to extend your theme
4. **Design tokens:** Import `design-tokens.json` for tooling integration
