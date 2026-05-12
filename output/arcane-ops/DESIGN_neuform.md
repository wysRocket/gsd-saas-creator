---
version: "alpha"
name: "Curated Creator Marketplace"
description: "Curated Creator Background Effect is designed for delivering a visual treatment or immersive background effect. Key features include atmospheric visuals, motion depth, and flexible presentation layering. It is suitable for visual-first pages, motion studies, and atmospheric hero treatments."
colors:
  primary: "#FF6A3D"
  secondary: "#0D0F10"
  tertiary: "#FFF247"
  neutral: "#0D0F10"
  background: "#151819"
  surface: "#0D0F10"
  text-primary: "#0D0F10"
  text-secondary: "#A8B0B3"
  border: "#202426"
  accent: "#FF6A3D"
typography:
  display-lg:
    fontFamily: "Bebas Neue"
    fontSize: "48px"
    fontWeight: 400
    lineHeight: "44.16px"
    letterSpacing: "-0.025em"
    textTransform: "uppercase"
  body-md:
    fontFamily: "Inter"
    fontSize: "12px"
    fontWeight: 500
    lineHeight: "16px"
    letterSpacing: "0.05em"
    textTransform: "uppercase"
spacing:
  base: "4px"
  sm: "4px"
  md: "8px"
  lg: "24px"
  xl: "32px"
  gap: "4px"
  card-padding: "32px"
  section-padding: "32px"
---

## Overview

- **Composition cues:**
  - Layout: Grid
  - Content Width: Full Bleed
  - Framing: Open
  - Grid: Strong

## Colors

The color system uses light mode with #FF6A3D as the main accent and #0D0F10 as the neutral foundation.

- **Primary (#FF6A3D):** Main accent and emphasis color.
- **Secondary (#0D0F10):** Supporting accent for secondary emphasis.
- **Tertiary (#FFF247):** Reserved accent for supporting contrast moments.
- **Neutral (#0D0F10):** Neutral foundation for backgrounds, surfaces, and supporting chrome.

- **Usage:** Background: #151819; Surface: #0D0F10; Text Primary: #0D0F10; Text Secondary: #A8B0B3; Border: #202426; Accent: #FF6A3D

## Typography

Typography pairs Bebas Neue for display hierarchy with Inter for supporting content and interface copy.

- **Display (`display-lg`):** Bebas Neue, 48px, weight 400, line-height 44.16px, letter-spacing -0.025em, uppercase.
- **Body (`body-md`):** Inter, 12px, weight 500, line-height 16px, letter-spacing 0.05em, uppercase.

## Layout

Layout follows a grid composition with reusable spacing tokens. Preserve the grid, full bleed structural frame before changing ornament or component styling. Use 4px as the base rhythm and let larger gaps step up from that cadence instead of introducing unrelated spacing values.

Treat the page as a grid / full bleed composition, and keep that framing stable when adding or remixing sections.

- **Layout type:** Grid
- **Content width:** Full Bleed
- **Base unit:** 4px
- **Scale:** 4px, 8px, 24px, 32px, 64px, 96px, 160px
- **Section padding:** 32px
- **Card padding:** 32px
- **Gaps:** 4px, 8px, 32px, 40px

## Elevation & Depth

Depth is communicated through elevated, border contrast, and reusable shadow or blur treatments. Keep those recipes consistent across hero panels, cards, and controls so the page reads as one material system.

Surfaces should read as elevated first, with borders, shadows, and blur only reinforcing that material choice.

- **Surface style:** Elevated
- **Borders:** 1px #202426; 1px #FFFFFF; 1px #000000; 1px #151819
- **Shadows:** rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0.25) 0px 25px 50px -12px; rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0.1) 0px 20px 25px -5px, rgba(0, 0, 0, 0.1) 0px 8px 10px -6px; rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0.5) 0px 20px 50px 0px

### Techniques
- **Gradient border shell:** Use a thin gradient border shell around the main card. Wrap the surface in an outer shell with 0px padding and a 0px radius. Drive the shell with radial-gradient(circle, rgb(243, 239, 232) 1px, rgba(0, 0, 0, 0) 1px) so the edge reads like premium depth instead of a flat stroke. Keep the actual stroke understated so the gradient shell remains the hero edge treatment. Inset the real content surface inside the wrapper with a slightly smaller radius so the gradient only appears as a hairline frame.

## Shapes

Shapes stay consistent across cards, controls, and icon treatments.

- **Icon treatment:** Linear
- **Icon sets:** Solar

## Components

Component styling should inherit the shared button, icon, spacing, and surface rules instead of inventing one-off treatments. Favor a small family of repeatable patterns for actions, content containers, and fields.

### Iconography
- **Treatment:** Linear.
- **Sets:** Solar.

## Do's and Don'ts

Use these constraints to keep future generations aligned with the current system instead of drifting into adjacent styles.

### Do
- Do use the primary palette as the main accent for emphasis and action states.
- Do keep spacing aligned to the detected 4px rhythm.
- Do reuse the Elevated surface treatment consistently across cards and controls.

### Don't
- Don't introduce extra accent colors outside the core palette roles unless the page needs a new semantic state.
- Don't mix unrelated shadow or blur recipes that break the current depth system.
- Don't exceed the detected minimal motion intensity without a deliberate reason.

## Motion

Motion stays restrained and interface-led across text, layout, and scroll transitions. Easing favors ease. Scroll choreography uses GSAP ScrollTrigger and Parallax for section reveals and pacing.

**Motion Level:** minimal

**Easings:** ease

**Scroll Patterns:** gsap-scrolltrigger, parallax

## WebGL

Reconstruct the graphics as a full-bleed background field using webgl, custom shaders. The effect should read as technical, meditative, and atmospheric: dot-matrix particle field with black and sparse spacing. Build it from dot particles + soft depth fade so the effect reads clearly. Animate it as slow breathing pulse. Interaction can react to the pointer, but only as a subtle drift. Preserve dom fallback.

**Id:** webgl

**Label:** WebGL

**Stack:** WebGL

**Insights:**
  - **Scene:**
    - **Value:** Full-bleed background field
  - **Effect:**
    - **Value:** Dot-matrix particle field
  - **Primitives:**
    - **Value:** Dot particles + soft depth fade
  - **Motion:**
    - **Value:** Slow breathing pulse
  - **Interaction:**
    - **Value:** Pointer-reactive drift
  - **Render:**
    - **Value:** WebGL, custom shaders

**Techniques:** Dot matrix, Breathing pulse, Pointer parallax, Shader gradients, Noise fields

**Code Evidence:**
  - **HTML reference:**
    - **Language:** html
    - **Snippet:**
      ```html
      <!-- Dither Background Skill: WebGL Canvas -->
      <canvas id="dither-bg" class="fixed inset-0 z-0 pointer-events-none w-full h-full opacity-60"></canvas>

      <!-- Subtle Dot Grid Background -->
      ```
  - **JS reference:**
    - **Language:** js
    - **Snippet:**
      ```
      // 1. WEBGL DITHER BACKGROUND
      // ----------------------------------------------------
      function initWebGL() {
        const canvas = document.getElementById('dither-bg');
        if (!canvas) return;
        const gl = canvas.getContext('webgl');
        if (!gl) return;
      …
      ```
  - **Renderer setup:**
    - **Language:** js
    - **Snippet:**
      ```
      // ----------------------------------------------------
      function initWebGL() {
        const canvas = document.getElementById('dither-bg');
        if (!canvas) return;
        const gl = canvas.getContext('webgl');
        if (!gl) return;

        const vsSource = `
      …
      ```
  - **Draw call:**
    - **Language:** js
    - **Snippet:**
      ```
      `;

          const fsSource = `
            precision highp float;
            uniform float uTime;
            uniform vec2 uResolution;

            float hash(vec2 p) {
      …
      ```
