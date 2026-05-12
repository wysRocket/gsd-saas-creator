# Design Language: AI HTML Landing Page Builder and Remix Templates | Neuform

> Extracted from `https://neuform.ai/?detail=%2Fcommunity%2Fa6e6b2ee-cadb-4dbd-bcd6-d03c781fd650%2Findex.html&pageId=a6e6b2ee-cadb-4dbd-bcd6-d03c781fd650` on May 3, 2026
> 326 elements analyzed

This document describes the complete design language of the website. It is structured for AI/LLM consumption — use it to faithfully recreate the visual design in any framework.

## Color Palette

### Primary Colors

| Role | Hex | RGB | HSL | Usage Count |
|------|-----|-----|-----|-------------|
| Primary | `#fff0c5` | rgb(255, 240, 197) | hsl(44, 100%, 89%) | 18 |
| Secondary | `#7684ff` | rgb(118, 132, 255) | hsl(234, 100%, 73%) | 8 |
| Accent | `#9db1ff` | rgb(157, 177, 255) | hsl(228, 100%, 81%) | 2 |

### Neutral Colors

| Hex | HSL | Usage Count |
|-----|-----|-------------|
| `#ffffff` | hsl(0, 0%, 100%) | 215 |
| `#e7e7e7` | hsl(0, 0%, 91%) | 146 |
| `#c8ccd4` | hsl(220, 12%, 81%) | 122 |
| `#050505` | hsl(0, 0%, 2%) | 21 |
| `#141414` | hsl(0, 0%, 8%) | 16 |
| `#66625b` | hsl(38, 6%, 38%) | 10 |
| `#1c1c22` | hsl(240, 10%, 12%) | 9 |
| `#737f97` | hsl(220, 15%, 52%) | 8 |
| `#7d786f` | hsl(39, 6%, 46%) | 4 |
| `#c8c2b8` | hsl(37, 13%, 75%) | 2 |
| `#b5afa4` | hsl(39, 10%, 68%) | 2 |
| `#252b39` | hsl(222, 21%, 18%) | 2 |

### Background Colors

Used on large-area elements: `#050505`, `#05070b`

### Text Colors

Text color palette: `#ffffff`, `#e7e7e7`, `#c8c2b8`, `#9db1ff`, `#b5afa4`, `#c8ccd4`, `#252b39`, `#141414`, `#171717`, `#948f87`

### Gradients

```css
background-image: radial-gradient(circle, rgba(255, 255, 255, 0.02), rgba(0, 0, 0, 0) 58%), repeating-linear-gradient(45deg, rgba(255, 255, 255, 0.01) 0px, rgba(255, 255, 255, 0.01) 1px, rgba(0, 0, 0, 0) 1px, rgba(0, 0, 0, 0) 18px), none;
```

```css
background-image: linear-gradient(rgb(29, 29, 32), rgb(23, 23, 25));
```

```css
background-image: linear-gradient(90deg, rgba(255, 255, 255, 0), rgba(255, 255, 255, 0.14), rgba(255, 255, 255, 0));
```

```css
background-image: linear-gradient(rgba(11, 14, 20, 0.7), rgba(11, 14, 20, 0.7)), linear-gradient(225deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0) 50%, rgba(255, 255, 255, 0.1) 100%);
```

```css
background-image: linear-gradient(rgba(88, 101, 242, 0.98), rgba(77, 90, 226, 0.98)), linear-gradient(rgba(145, 156, 255, 0.5), rgba(88, 101, 242, 0.28));
```

```css
background-image: linear-gradient(145deg, rgba(16, 20, 28, 0.64), rgba(8, 11, 17, 0.72)), linear-gradient(225deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0) 50%, rgba(255, 255, 255, 0.1) 100%);
```

```css
background-image: linear-gradient(145deg, rgba(158, 112, 19, 0.82), rgba(104, 65, 10, 0.9)), linear-gradient(225deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0) 50%, rgba(255, 255, 255, 0.1) 100%);
```

```css
background-image: linear-gradient(145deg, rgba(15, 19, 28, 0.72), rgba(9, 12, 18, 0.78)), linear-gradient(225deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0) 50%, rgba(255, 255, 255, 0.1) 100%);
```

### Full Color Inventory

| Hex | Contexts | Count |
|-----|----------|-------|
| `#ffffff` | text, border, background | 215 |
| `#e7e7e7` | text, border | 146 |
| `#c8ccd4` | text, border | 122 |
| `#f4f1ea` | background, text, border | 49 |
| `#050505` | background, border | 21 |
| `#fff0c5` | text, border | 18 |
| `#141414` | text, border, background | 16 |
| `#66625b` | text, border | 10 |
| `#1c1c22` | background, text, border | 9 |
| `#d8e6f9` | text | 9 |
| `#7684ff` | border | 8 |
| `#737f97` | border | 8 |
| `#7d786f` | text, border | 4 |
| `#c8c2b8` | text, border | 2 |
| `#9db1ff` | text, border | 2 |
| `#b5afa4` | text, border | 2 |
| `#252b39` | text, border | 2 |
| `#948f87` | text, border | 2 |
| `#51588a` | border | 1 |

## Typography

### Font Families

- **Segoe UI** — used for body (159 elements)
- **Arial** — used for body (83 elements)
- **Times** — used for body (45 elements)
- **Inter** — used for all (20 elements)
- **JetBrains Mono** — used for body (11 elements)
- **IBM Plex Mono** — used for body (6 elements)
- **DM Sans** — used for all (2 elements)

### Type Scale

| Size (px) | Size (rem) | Weight | Line Height | Letter Spacing | Used On |
|-----------|------------|--------|-------------|----------------|---------|
| 32.64px | 2.04rem | 300 | 31.9872px | -1.3056px | h1 |
| 16px | 1rem | 400 | normal | normal | html, head, meta, script |
| 15.36px | 0.96rem | 500 | 21.12px | -0.4608px | span |
| 15.04px | 0.94rem | 400 | 24.816px | normal | p |
| 13.3333px | 0.8333rem | 400 | normal | normal | button, img, span, svg |
| 12.8px | 0.8rem | 500 | 15.36px | normal | span, svg, path, input |
| 12.48px | 0.78rem | 300 | 17.16px | normal | span, button, svg, g |
| 11px | 0.6875rem | 400 | 14.3px | normal | div, span, svg, g |
| 10.88px | 0.68rem | 400 | 10.88px | 0.1088px | span |
| 10.24px | 0.64rem | 400 | normal | 0.3072px | div |
| 9.92px | 0.62rem | 400 | 9.92px | 2.1824px | span |
| 9.6px | 0.6rem | 500 | normal | normal | span, img |
| 9.28px | 0.58rem | 400 | 11.136px | 2.0416px | p, span, label, button |
| 8.96px | 0.56rem | 400 | 10.752px | 1.6128px | a, p |
| 8.64px | 0.54rem | 400 | 8.64px | 2.4192px | span |

### Heading Scale

```css
h1 { font-size: 32.64px; font-weight: 300; line-height: 31.9872px; }
```

### Body Text

```css
body { font-size: 11px; font-weight: 400; line-height: 14.3px; }
```

### Font Weights in Use

`400` (295x), `500` (23x), `700` (6x), `300` (2x)

## Spacing

**Base unit:** 2px

| Token | Value | Rem |
|-------|-------|-----|
| spacing-1 | 1px | 0.0625rem |
| spacing-4 | 4px | 0.25rem |
| spacing-16 | 16px | 1rem |
| spacing-18 | 18px | 1.125rem |
| spacing-20 | 20px | 1.25rem |
| spacing-208 | 208px | 13rem |

## Border Radii

| Label | Value | Count |
|-------|-------|-------|
| md | 6px | 17 |
| full | 999px | 51 |

## Box Shadows

**sm** — blur: 0px
```css
box-shadow: rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(255, 255, 255, 0.16) 0px 0px 0px 1px, rgba(0, 0, 0, 0.32) 0px 10px 24px 0px;
```

**xs (inset)** — blur: 0px
```css
box-shadow: rgba(255, 255, 255, 0.04) 0px 1px 0px 0px inset;
```

**md** — blur: 16px
```css
box-shadow: rgba(255, 255, 255, 0.08) 0px 0px 16px 0px;
```

**lg (inset)** — blur: 13px
```css
box-shadow: rgba(0, 0, 0, 0.28) 0px 6px 13px 0px, rgba(255, 255, 255, 0.08) 0px 1px 0px 0px inset;
```

**lg (inset)** — blur: 14px
```css
box-shadow: rgba(0, 0, 0, 0.22) 0px 6px 14px 0px, rgba(255, 255, 255, 0.06) 0px 1px 0px 0px inset;
```

**lg (inset)** — blur: 18px
```css
box-shadow: rgba(88, 101, 242, 0.34) 0px 8px 18px 0px, rgba(255, 255, 255, 0.24) 0px 1px 0px 0px inset;
```

**lg (inset)** — blur: 22px
```css
box-shadow: rgba(60, 35, 4, 0.3) 0px 10px 22px 0px, rgba(255, 247, 221, 0.22) 0px 1px 0px 0px inset;
```

**xl** — blur: 72px
```css
box-shadow: rgba(0, 0, 0, 0.36) 0px 26px 72px 0px;
```

## CSS Custom Properties

### Colors

```css
--popover-width: 320px;
--prompt-surface-border-width: .5px;
--glass-border-gradient: linear-gradient( 225deg, rgba(255, 255, 255, .1) 0%, rgba(255, 255, 255, 0) 50%, rgba(255, 255, 255, .1) 100% );
--color-cyan-400: oklch(78.9% .154 211.53);
--color-amber-400: oklch(82.8% .189 84.429);
--tw-ring-shadow: 0 0 #0000;
--color-zinc-200: oklch(92% .004 286.32);
--color-zinc-100: oklch(96.7% .001 286.375);
--color-slate-200: oklch(92.9% .013 255.508);
--color-sky-500: oklch(68.5% .169 237.323);
--color-pink-500: oklch(65.6% .241 354.308);
--color-slate-700: oklch(37.2% .044 257.287);
--color-neutral-600: oklch(43.9% 0 0);
--color-neutral-500: oklch(55.6% 0 0);
--color-neutral-300: oklch(87% 0 0);
--color-slate-500: oklch(55.4% .046 257.417);
--color-slate-900: oklch(20.8% .042 265.755);
--color-stone-400: oklch(70.9% .01 56.259);
--tw-inset-ring-shadow: 0 0 #0000;
--color-red-200: oklch(88.5% .062 18.334);
--color-neutral-200: oklch(92.2% 0 0);
--color-gray-300: oklch(87.2% .01 258.338);
--color-slate-300: oklch(86.9% .022 252.894);
--color-amber-300: oklch(87.9% .169 91.605);
--color-gray-500: oklch(55.1% .027 264.364);
--color-zinc-50: oklch(98.5% 0 0);
--color-stone-950: oklch(14.7% .004 49.25);
--color-gray-50: oklch(98.5% .002 247.839);
--tw-ring-offset-color: #fff;
--color-red-400: oklch(70.4% .191 22.216);
--color-white: #fff;
--color-gray-400: oklch(70.7% .022 261.325);
--color-slate-400: oklch(70.4% .04 256.788);
--color-stone-900: oklch(21.6% .006 56.043);
--color-rose-100: oklch(94.1% .03 12.58);
--color-zinc-950: oklch(14.1% .005 285.823);
--color-gray-100: oklch(96.7% .003 264.542);
--color-emerald-100: oklch(95% .052 163.051);
--color-red-500: oklch(63.7% .237 25.331);
--color-rose-400: oklch(71.2% .194 13.428);
--tw-ring-offset-width: 0px;
--color-zinc-300: oklch(87.1% .006 286.286);
--color-zinc-700: oklch(37% .013 285.805);
--color-neutral-700: oklch(37.1% 0 0);
--color-violet-500: oklch(60.6% .25 292.717);
--color-neutral-50: oklch(98.5% 0 0);
--color-neutral-900: oklch(20.5% 0 0);
--color-slate-50: oklch(98.4% .003 247.858);
--tw-ring-offset-shadow: 0 0 #0000;
--color-neutral-100: oklch(97% 0 0);
--color-gray-800: oklch(27.8% .033 256.848);
--color-stone-100: oklch(97% .001 106.424);
--color-zinc-500: oklch(55.2% .016 285.938);
--color-zinc-900: oklch(21% .006 285.885);
--color-sky-300: oklch(82.8% .111 230.318);
--color-cyan-500: oklch(71.5% .143 215.221);
--color-zinc-800: oklch(27.4% .006 286.033);
--color-slate-800: oklch(27.9% .041 260.031);
--color-orange-500: oklch(70.5% .213 47.604);
--color-sky-100: oklch(95.1% .026 236.824);
--color-stone-500: oklch(55.3% .013 58.071);
--color-rose-50: oklch(96.9% .015 12.422);
--color-slate-600: oklch(44.6% .043 257.281);
--color-stone-600: oklch(44.4% .011 73.639);
--color-slate-950: oklch(12.9% .042 264.695);
--color-rose-500: oklch(64.5% .246 16.439);
--color-slate-100: oklch(96.8% .007 247.896);
--color-emerald-500: oklch(69.6% .17 162.48);
--color-blue-500: oklch(62.3% .214 259.815);
--color-gray-900: oklch(21% .034 264.665);
--color-gray-950: oklch(13% .028 261.692);
--color-zinc-400: oklch(70.5% .015 286.067);
--color-gray-700: oklch(37.3% .034 259.733);
--color-zinc-600: oklch(44.2% .017 285.786);
--color-indigo-500: oklch(58.5% .233 277.117);
--color-gray-600: oklch(44.6% .03 256.802);
--color-red-100: oklch(93.6% .032 17.717);
--tw-border-style: solid;
--color-stone-200: oklch(92.3% .003 48.717);
--color-red-50: oklch(97.1% .013 17.38);
--color-stone-700: oklch(37.4% .01 67.558);
--color-gray-200: oklch(92.8% .006 264.531);
--color-black: #000;
--color-neutral-950: oklch(14.5% 0 0);
--color-neutral-400: oklch(70.8% 0 0);
--color-emerald-400: oklch(76.5% .177 163.223);
--color-amber-100: oklch(96.2% .059 95.617);
--color-neutral-800: oklch(26.9% 0 0);
--color-teal-500: oklch(70.4% .14 182.503);
--color-stone-800: oklch(26.8% .007 34.298);
--color-amber-50: oklch(98.7% .022 95.277);
--color-stone-300: oklch(86.9% .005 56.366);
--color-stone-50: oklch(98.5% .001 106.423);
--color-amber-200: oklch(92.4% .12 95.746);
```

### Spacing

```css
--grid-gap: 8px;
--spacing: .25rem;
--tw-space-y-reverse: 0;
```

### Typography

```css
--text-2xl: 1.5rem;
--text-7xl: 4.5rem;
--text-lg: 1.125rem;
--text-5xl--line-height: 1;
--text-base--line-height: 1.5;
--font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
--tracking-wider: .05em;
--text-lg--line-height: calc(1.75 / 1.125);
--font-sans: ui-sans-serif, system-ui, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
--font-weight-bold: 700;
--text-6xl: 3.75rem;
--text-xs--line-height: calc(1 / .75);
--font-weight-light: 300;
--font-inter: "Inter", system-ui, sans-serif;
--text-7xl--line-height: 1;
--leading-relaxed: 1.625;
--leading-snug: 1.375;
--tracking-tighter: -.05em;
--text-2xl--line-height: calc(2 / 1.5);
--tracking-wide: .025em;
--font-weight-semibold: 600;
--text-sm: .875rem;
--leading-tight: 1.25;
--text-4xl: 2.25rem;
--tracking-normal: 0em;
--text-sm--line-height: calc(1.25 / .875);
--text-3xl--line-height: 1.2;
--text-5xl: 3rem;
--text-3xl: 1.875rem;
--text-xs: .75rem;
--tracking-widest: .1em;
--font-weight-medium: 500;
--font-weight-normal: 400;
--font-serif: ui-serif, Georgia, Cambria, "Times New Roman", Times, serif;
--font-weight-thin: 100;
--text-6xl--line-height: 1;
--text-4xl--line-height: calc(2.5 / 2.25);
--font-dm-sans: "DM Sans", sans-serif;
--text-base: 1rem;
--tracking-tight: -.025em;
```

### Shadows

```css
--tw-inset-shadow-alpha: 100%;
--tw-drop-shadow-alpha: 100%;
--tw-inset-shadow: 0 0 #0000;
--tw-shadow-alpha: 100%;
--tw-shadow: 0 0 #0000;
```

### Radii

```css
--radius-md: 6px;
--radius-sm: .25rem;
--radius-lg: .5rem;
```

### Other

```css
--tile-stroke: #1d1d1d;
--prompt-divider-gradient: linear-gradient( 90deg, rgba(194, 216, 244, .03) 0%, rgba(194, 216, 244, .12) 52%, rgba(194, 216, 244, .03) 100% );
--container-md: 28rem;
--aspect-video: 16 / 9;
--tw-outline-style: solid;
--blur-xl: 24px;
--tw-gradient-from: rgba(0, 0, 0, 0);
--tw-gradient-to: rgba(0, 0, 0, 0);
--tw-scale-z: 1;
--tw-gradient-via-position: 50%;
--tw-scroll-snap-strictness: proximity;
--container-lg: 32rem;
--tw-gradient-to-position: 100%;
--default-transition-duration: .15s;
--animate-pulse: pulse 2s cubic-bezier(.4, 0, .6, 1) infinite;
--tw-gradient-from-position: 0%;
--ease-in-out: cubic-bezier(.4, 0, .2, 1);
--default-transition-timing-function: cubic-bezier(.4, 0, .2, 1);
--container-5xl: 64rem;
--tw-translate-z: 0;
--tw-gradient-via: rgba(0, 0, 0, 0);
--tw-scale-y: 1;
--container-3xl: 48rem;
--tw-translate-y: 0;
--blur-md: 12px;
--ease-out: cubic-bezier(0, 0, .2, 1);
--animate-spin: spin 1s linear infinite;
--container-4xl: 56rem;
--tw-divide-y-reverse: 0;
--container-2xl: 42rem;
--tw-translate-x: 0;
--tw-scale-x: 1;
--container-xl: 36rem;
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
| sm | 520px | max-width |
| sm | 540px | max-width |
| sm | 620px | max-width |
| sm | 640px | max-width |
| sm | 680px | max-width |
| sm | 700px | max-width |
| md | 720px | max-width |
| md | 760px | max-width |
| md | 761px | min-width |
| md | 767px | max-width |
| md | 768px | max-width |
| 860px | 860px | max-width |
| 900px | 900px | max-width |
| lg | 960px | max-width |
| lg | 980px | max-width |
| lg | 1023px | max-width |
| 1100px | 1100px | max-width |
| 1179px | 1179px | max-width |
| 1180px | 1180px | max-width |
| xl | 1279px | max-width |
| xl | 1280px | max-width |
| 1366px | 1366px | max-width |

## Transitions & Animations

**Easing functions:** `[object Object]`, `[object Object]`

**Durations:** `0.18s`, `0.24s`, `0.22s`, `0.32s`, `0.42s`, `0.15s`, `0.52s`

### Common Transitions

```css
transition: all;
transition: transform 0.18s, background 0.18s, box-shadow 0.18s, border-color 0.18s, color 0.18s, opacity 0.18s, filter 0.24s;
transition: transform 0.22s cubic-bezier(0.16, 1, 0.3, 1), background 0.22s;
transition: transform 0.22s cubic-bezier(0.16, 1, 0.3, 1);
transition: color 0.18s, opacity 0.18s;
transition: border-color 0.18s, box-shadow 0.18s, background 0.18s;
transition: height 0.32s cubic-bezier(0.16, 1, 0.3, 1), margin-top 0.32s cubic-bezier(0.16, 1, 0.3, 1);
transition: transform 0.22s cubic-bezier(0.16, 1, 0.3, 1), color 0.22s;
transition: box-shadow 0.42s;
transition: opacity 0.15s, transform 0.15s;
```

### Keyframe Animations

**app-session-loading-pulse**
```css
@keyframes app-session-loading-pulse {
  0%, 100% { opacity: 0.35; }
  50% { opacity: 1; }
}
```

**auth-shell-fade-in**
```css
@keyframes auth-shell-fade-in {
  100% { opacity: 1; }
}
```

**auth-shell-fade-up**
```css
@keyframes auth-shell-fade-up {
  0% { opacity: 0; transform: translateY(12px); }
  100% { opacity: 1; transform: translateY(0px); }
}
```

**auth-shell-square-in**
```css
@keyframes auth-shell-square-in {
  0% { opacity: 0; transform: scale(0.6); }
  100% { opacity: 1; transform: scale(1); }
}
```

**auth-shell-stripe-in**
```css
@keyframes auth-shell-stripe-in {
  100% { transform: scaleX(1); }
}
```

**viewer-landing-sidebar-reveal**
```css
@keyframes viewer-landing-sidebar-reveal {
  0% { opacity: 0; filter: blur(18px); transform: translate3d(0px, 18px, 0px); }
  100% { opacity: 1; filter: blur(0px); transform: translateZ(0px); }
}
```

**public-page-shell-reveal**
```css
@keyframes public-page-shell-reveal {
  0% { opacity: 0; filter: blur(18px); transform: translate3d(0px, -18px, 0px); }
  100% { opacity: 1; filter: blur(0px); transform: translateZ(0px); }
}
```

**public-top-nav-mobile-item-reveal**
```css
@keyframes public-top-nav-mobile-item-reveal {
  0% { opacity: 0; filter: blur(12px); transform: translate3d(0px, -12px, 0px); }
  100% { opacity: 1; filter: blur(0px); transform: translateZ(0px); }
}
```

**public-content-fade-in**
```css
@keyframes public-content-fade-in {
  0% { opacity: 0; }
  100% { opacity: 1; }
}
```

**public-project-loader-border-glimmer**
```css
@keyframes public-project-loader-border-glimmer {
  0% { background-position: 170% 50%; }
  100% { background-position: -70% 50%; }
}
```

## Component Patterns

Detected UI component patterns and their most common styles:

### Buttons (36 instances)

```css
.button {
  background-color: rgb(244, 241, 234);
  color: rgb(208, 208, 208);
  font-size: 13.3333px;
  font-weight: 400;
  padding-top: 1px;
  padding-right: 6px;
  border-radius: 999px;
}
```

### Inputs (1 instances)

```css
.input {
  background-color: rgba(255, 255, 255, 0.02);
  color: rgb(239, 235, 227);
  border-color: rgba(255, 255, 255, 0.06);
  border-radius: 999px;
  font-size: 12.8px;
  padding-top: 0px;
  padding-right: 16px;
}
```

### Links (5 instances)

```css
.link {
  color: rgb(102, 98, 91);
  font-size: 8.96px;
  font-weight: 400;
}
```

### Navigation (1 instances)

```css
.navigatio {
  color: rgb(231, 231, 231);
  padding-top: 0px;
  padding-bottom: 0px;
  padding-left: 0px;
  padding-right: 0px;
  position: static;
}
```

### Footer (8 instances)

```css
.foote {
  color: rgb(102, 98, 91);
  padding-top: 0px;
  padding-bottom: 0px;
  font-size: 8.96px;
}
```

### Badges (35 instances)

```css
.badge {
  color: rgb(243, 243, 243);
  font-size: 11px;
  font-weight: 400;
  padding-top: 0px;
  padding-right: 0px;
  border-radius: 0px;
}
```

### Switches (22 instances)

```css
.switche {
  border-radius: 999px;
}
```

## Component Clusters

Reusable component instances grouped by DOM structure and style similarity:

### Button — 1 instance, 1 variant

**Variant 1** (1 instance)

```css
  background: rgba(0, 0, 0, 0);
  color: rgb(255, 255, 255);
  padding: 0px 0px 0px 0px;
  border-radius: 0px;
  border: 0px none rgb(255, 255, 255);
  font-size: 13.3333px;
  font-weight: 400;
```

### Button — 1 instance, 1 variant

**Variant 1** (1 instance)

```css
  background: rgb(244, 241, 234);
  color: rgb(20, 20, 20);
  padding: 5.44px 6.4px 5.44px 12.8px;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  font-size: 13.3333px;
  font-weight: 400;
```

### Button — 9 instances, 2 variants

**Variant 1** (1 instance)

```css
  background: rgba(0, 0, 0, 0);
  color: rgb(125, 120, 111);
  padding: 0px 0px 0px 0px;
  border-radius: 0px;
  border: 0px none rgb(125, 120, 111);
  font-size: 9.28px;
  font-weight: 400;
```

**Variant 2** (8 instances)

```css
  background: rgba(0, 0, 0, 0);
  color: rgb(255, 255, 255);
  padding: 0px 0px 0px 0px;
  border-radius: 0px;
  border: 0px none rgb(255, 255, 255);
  font-size: 13.3333px;
  font-weight: 400;
```

### Input — 1 instance, 1 variant

**Variant 1** (1 instance)

```css
  background: rgba(255, 255, 255, 0.02);
  color: rgb(239, 235, 227);
  padding: 0px 16px 0px 16px;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.06);
  font-size: 12.8px;
  font-weight: 400;
```

### Button — 1 instance, 1 variant

**Variant 1** (1 instance)

```css
  background: rgba(255, 255, 255, 0.14);
  color: rgb(239, 235, 227);
  padding: 1px 6px 1px 6px;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.04);
  font-size: 12.48px;
  font-weight: 500;
```

### Button — 24 instances, 1 variant

**Variant 1** (24 instances)

```css
  background: rgba(0, 0, 0, 0);
  color: rgb(208, 208, 208);
  padding: 1px 6px 1px 6px;
  border-radius: 999px;
  border: 1px solid rgba(0, 0, 0, 0);
  font-size: 13.3333px;
  font-weight: 400;
```

## Layout System

**5 grid containers** and **97 flex containers** detected.

### Grid Column Patterns

| Columns | Usage Count |
|---------|-------------|
| 1-column | 4x |
| 3-column | 1x |

### Grid Templates

```css
grid-template-columns: 322.812px;
gap: 12px;
grid-template-columns: 322.812px;
gap: 11.52px;
grid-template-columns: 322.812px;
gap: 8.96px;
grid-template-columns: 141.344px 17.75px 141.344px;
gap: 11.2px;
grid-template-columns: 60.7969px;
gap: 6px;
```

### Flex Patterns

| Direction/Wrap | Count |
|----------------|-------|
| column/nowrap | 3x |
| row/nowrap | 93x |
| row/wrap | 1x |

**Gap values:** `10.4px`, `11.2px`, `11.52px`, `12.8px`, `12px`, `16px`, `4.48px`, `4.8px`, `6px`, `8.8px`, `8.96px`, `9.28px`, `9.6px`

## Responsive Design

### Viewport Snapshots

| Viewport | Body Font | Nav Visible | Max Columns | Hamburger | Page Height |
|----------|-----------|-------------|-------------|-----------|-------------|
| mobile (375px) | 16px | No | 3 | No | 812px |
| tablet (768px) | 16px | No | 3 | No | 1024px |
| desktop (1280px) | 16px | No | 3 | No | 800px |
| wide (1920px) | 16px | No | 3 | No | 1080px |

### Breakpoint Changes

**375px → 768px** (mobile → tablet):
- H1 size: `37.5px` → `28.48px`
- Page height: `812px` → `1024px`

**768px → 1280px** (tablet → desktop):
- H1 size: `28.48px` → `32.64px`
- Page height: `1024px` → `800px`

**1280px → 1920px** (desktop → wide):
- H1 size: `32.64px` → `38.72px`
- Page height: `800px` → `1080px`

## Interaction States

### Button States

**"Neuform"**
```css
/* Focus */
outline: rgb(255, 255, 255) none 3px → rgb(153, 200, 255) auto 1px;
```

**"Continue with Google"**
```css
/* Focus */
outline: rgb(20, 20, 20) none 3px → rgb(153, 200, 255) auto 1px;
```

**"Forgot"**
```css
/* Hover */
color: rgb(125, 120, 111) → rgb(244, 243, 243);
border-color: rgb(125, 120, 111) → rgb(244, 243, 243);
outline: rgb(125, 120, 111) none 3px → rgb(244, 243, 243) none 3px;
```
```css
/* Focus */
color: rgb(125, 120, 111) → rgb(255, 255, 255);
border-color: rgb(125, 120, 111) → rgb(255, 255, 255);
outline: rgb(125, 120, 111) none 3px → rgb(255, 255, 255) none 3px;
```

### Link Hover

```css
color: rgb(102, 98, 91) → rgb(255, 255, 255);
border-color: rgb(102, 98, 91) → rgb(255, 255, 255);
outline: rgb(102, 98, 91) none 3px → rgb(255, 255, 255) none 3px;
```

### Input Focus

```css
background-color: rgba(255, 255, 255, 0.02) → rgba(255, 255, 255, 0.03);
border-color: rgba(255, 255, 255, 0.06) → rgba(152, 176, 255, 0.153);
box-shadow: none → rgba(123, 149, 255, 0.07) 0px 0px 0px 2.28945px;
```

## Accessibility (WCAG 2.1)

**Overall Score: 100%** — 0 passing, 0 failing color pairs

## Design System Score

**Overall: 83/100 (Grade: B)**

| Category | Score |
|----------|-------|
| Color Discipline | 92/100 |
| Typography Consistency | 50/100 |
| Spacing System | 100/100 |
| Shadow Consistency | 90/100 |
| Border Radius Consistency | 100/100 |
| Accessibility | 100/100 |
| CSS Tokenization | 100/100 |

**Strengths:** Tight, disciplined color palette, Well-defined spacing scale, Clean elevation system, Consistent border radii, Strong accessibility compliance, Good CSS variable tokenization

**Issues:**
- 7 font families — consider limiting to 2 (heading + body)
- 125 !important rules — prefer specificity over overrides
- 83% of CSS is unused — consider purging
- 15285 duplicate CSS declarations

## Gradients

**11 unique gradients** detected.

| Type | Direction | Stops | Classification |
|------|-----------|-------|----------------|
| radial | circle | 2 | brand |
| repeating-linear | 45deg | 4 | bold |
| linear | — | 2 | brand |
| linear | 90deg | 3 | bold |
| linear | — | 2 | brand |
| linear | 225deg | 3 | bold |
| linear | — | 2 | brand |
| linear | — | 2 | brand |
| linear | 145deg | 2 | brand |
| linear | 145deg | 2 | brand |
| linear | 145deg | 2 | brand |

```css
background: radial-gradient(circle, rgba(255, 255, 255, 0.02), rgba(0, 0, 0, 0) 58%);
background: repeating-linear-gradient(45deg, rgba(255, 255, 255, 0.01) 0px, rgba(255, 255, 255, 0.01) 1px, rgba(0, 0, 0, 0) 1px, rgba(0, 0, 0, 0) 18px);
background: linear-gradient(rgb(29, 29, 32), rgb(23, 23, 25));
background: linear-gradient(90deg, rgba(255, 255, 255, 0), rgba(255, 255, 255, 0.14), rgba(255, 255, 255, 0));
background: linear-gradient(rgba(11, 14, 20, 0.7), rgba(11, 14, 20, 0.7));
```

## Z-Index Map

**7 unique z-index values** across 2 layers.

| Layer | Range | Elements |
|-------|-------|----------|
| sticky | 24,31 | aside.v.i.e.w.e.r._._.l.a.n.d.i.n.g.-.s.i.d.e.b.a.r, div.v.i.e.w.e.r._._.s.t.a.t.u.s.-.h.u.d |
| base | 1,8 | div.v.i.e.w.e.r._._.l.a.n.d.i.n.g.-.s.i.d.e.b.a.r.-.s.h.e.l.l. .v.i.e.w.e.r._._.l.a.n.d.i.n.g.-.s.i.d.e.b.a.r.-.s.h.e.l.l.-.-.a.n.i.m.a.t.e.d, span.a.b.s.o.l.u.t.e. .l.e.f.t.-.0. .t.o.p.-.0. .i.n.l.i.n.e.-.f.l.e.x. .s.h.r.i.n.k.-.0. .i.t.e.m.s.-.c.e.n.t.e.r. .j.u.s.t.i.f.y.-.c.e.n.t.e.r. .o.v.e.r.f.l.o.w.-.h.i.d.d.e.n. .r.o.u.n.d.e.d.-.f.u.l.l. .b.o.r.d.e.r. .b.o.r.d.e.r.-.[.#.0.8.0.8.0.a.]. .b.g.-.[.#.1.c.1.c.2.2.]. .f.o.n.t.-.m.e.d.i.u.m. .t.e.x.t.-.w.h.i.t.e. .s.h.a.d.o.w.-.[.0._.0._.0._.1.p.x._.r.g.b.a.(.2.5.5.,.2.5.5.,.2.5.5.,.0...1.6.).,.0._.1.0.p.x._.2.4.p.x._.r.g.b.a.(.0.,.0.,.0.,.0...3.2.).]. .h.-.7. .w.-.7. .t.e.x.t.-.[.0...6.r.e.m.], span.a.b.s.o.l.u.t.e. .l.e.f.t.-.0. .t.o.p.-.0. .i.n.l.i.n.e.-.f.l.e.x. .s.h.r.i.n.k.-.0. .i.t.e.m.s.-.c.e.n.t.e.r. .j.u.s.t.i.f.y.-.c.e.n.t.e.r. .o.v.e.r.f.l.o.w.-.h.i.d.d.e.n. .r.o.u.n.d.e.d.-.f.u.l.l. .b.o.r.d.e.r. .b.o.r.d.e.r.-.[.#.0.8.0.8.0.a.]. .b.g.-.[.#.1.c.1.c.2.2.]. .f.o.n.t.-.m.e.d.i.u.m. .t.e.x.t.-.w.h.i.t.e. .s.h.a.d.o.w.-.[.0._.0._.0._.1.p.x._.r.g.b.a.(.2.5.5.,.2.5.5.,.2.5.5.,.0...1.6.).,.0._.1.0.p.x._.2.4.p.x._.r.g.b.a.(.0.,.0.,.0.,.0...3.2.).]. .h.-.7. .w.-.7. .t.e.x.t.-.[.0...6.r.e.m.] |

## SVG Icons

**7 unique SVG icons** detected. Dominant style: **outlined**.

| Size Class | Count |
|------------|-------|
| xs | 4 |
| sm | 1 |
| md | 2 |

**Icon colors:** `#FFC107`, `#FF3D00`, `#4CAF50`, `#1976D2`, `rgb(0, 0, 0)`, `currentColor`

## Image Style Patterns

| Pattern | Count | Key Styles |
|---------|-------|------------|
| thumbnail | 39 | objectFit: fill, borderRadius: 0px, shape: square |
| avatar | 6 | objectFit: fill, borderRadius: 999px, shape: circular |

**Aspect ratios:** 3:4 (24x), 1:1 (21x)

## Motion Language

**Feel:** responsive · **Scroll-linked:** yes

### Duration Tokens

| name | value | ms |
|---|---|---|
| `xs` | `150ms` | 150 |
| `sm` | `180ms` | 180 |
| `md` | `320ms` | 320 |
| `lg` | `420ms` | 420 |

### Easing Families

- **ease-out** (12 uses) — `cubic-bezier(0.16, 1, 0.3, 1)`, `cubic-bezier(0.22, 1, 0.36, 1)`

### Keyframes In Use

| name | kind | properties | uses |
|---|---|---|---|
| `viewer-landing-sidebar-reveal` | slide | opacity, filter, transform | 9 |

## Component Anatomy

### button — 36 instances

**Slots:** label, icon
**Variants:** link

| variant | count | sample label |
|---|---|---|
| default | 35 | NEUFORM |
| link | 1 | Send magic link |

## Brand Voice

**Tone:** formal · **Pronoun:** third-person · **Headings:** Sentence case (balanced)

### Top CTA Verbs

- **neuform** (1)
- **continue** (1)
- **forgot** (1)
- **send** (1)

### Button Copy Patterns

- "neuform" (1×)
- "continue with google" (1×)
- "forgot" (1×)
- "send magic link" (1×)

### Sample Headings

> Turn one prompt into web, mobile & design systems
> Turn one prompt into web, mobile & design systems

## Page Intent

**Type:** `landing` (confidence 0.45)
**Description:** Neuform turns prompts into AI HTML landing pages, remix templates, and reusable DESIGN.md files for agent-ready design systems.

## Section Roles

Reading order (top→bottom): faq → faq → content → content → content → content → footer → content → content → content → content

| # | Role | Heading | Confidence |
|---|------|---------|------------|
| 0 | faq | Turn one prompt into web, mobile & design systems | 0.85 |
| 1 | faq | Turn one prompt into web, mobile & design systems | 0.85 |
| 2 | footer | — | 0.95 |
| 3 | content | — | 0.3 |
| 4 | content | — | 0.3 |
| 5 | content | — | 0.3 |
| 6 | content | — | 0.3 |
| 7 | content | — | 0.3 |
| 8 | content | — | 0.3 |
| 9 | content | — | 0.3 |
| 10 | content | — | 0.3 |

## Material Language

**Label:** `flat` (confidence 0)

| Metric | Value |
|--------|-------|
| Avg saturation | 0.16 |
| Shadow profile | soft |
| Avg shadow blur | 0px |
| Max radius | 999px |
| backdrop-filter in use | no |
| Gradients | 11 |

## Imagery Style

**Label:** `mixed` (confidence 0.044)
**Counts:** total 45, svg 36, icon 46, screenshot-like 0, photo-like 0
**Dominant aspect:** portrait
**Radius profile on images:** rounded

## Component Screenshots

4 retina crops written to `screenshots/`. Index: `*-screenshots.json`.

| Cluster | Variant | Size (px) | File |
|---------|---------|-----------|------|
| button--default | 0 | 82 × 16 | `screenshots/button-default-0.png` |
| button--default | 1 | 323 × 46 | `screenshots/button-default-1.png` |
| button--default | 2 | 43 × 11 | `screenshots/button-default-2.png` |
| input--default | 0 | 323 × 44 | `screenshots/input-default-0.png` |

Full-page: `screenshots/full-page.png`

## Quick Start

To recreate this design in a new project:

1. **Install fonts:** Add `Segoe UI` from Google Fonts or your font provider
2. **Import CSS variables:** Copy `variables.css` into your project
3. **Tailwind users:** Use the generated `tailwind.config.js` to extend your theme
4. **Design tokens:** Import `design-tokens.json` for tooling integration
