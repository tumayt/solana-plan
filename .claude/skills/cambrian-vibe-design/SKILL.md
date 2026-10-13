---
name: cambrian-vibe-design
description: Use when creating any Cambrian-branded visual asset - blog graphics, social cards, diagrams, deck art, video frames, or Figma imports - or when unsure which brand colors, fonts, or logo files are correct. Also use when a graphic "has two different greens" or looks off-brand.
---

# Cambrian Vibe Design

Produce on-brand Cambrian graphics from code, verify them pixel-exact, and land them in Figma as editable vectors.

**Source of truth for the brand is the Figma "Cambrian Redesign" file** (`figma.com/design/zTPHytioRvDLrrJ6aGPPj2/Cambrian-Redesign`, Redesign page; the desktop landing frame is node `2155:982`). That file defines no Figma variables, so the hexes live in the frames themselves: read fills with `get_design_context` or sample flat regions of a rendered frame. The deployed copy of the same system is the live cambrian.org CSS (`/_next/static/css/*.css`, or `firecrawl_scrape` with `formats: ["branding"]` for a quick pull). The hexes below were read from both in Aug 2026. If Figma and this table ever disagree, Figma won; update this table.

## Brand kit

**Two greens are deliberate. Do not unify them.**

| Token | Hex | Use for |
|-------|-----|---------|
| Primary green (primary-500) | `#4B9328` | CTAs, buttons, arrows, accents, focus. Matches logo green exactly |
| Highlight green (primary-600) | `#3B7120` | Background blocks behind serif headlines (the hero treatment) |
| Highlight text (primary-50) | `#ECEFD8` | Text ON highlight blocks. Pale green-cream, not white |
| Dark green (primary-800) | `#1D3212` | Hero/dark section backgrounds, ink on cream |
| Body sand (sand-300) | `#ECDFC3` | Main page body background. Use for light graphic canvases |
| HeroUI background | `#F8F0DE` | Alternate light surface |
| Card | `#F2EDE3` bg, `#D7D2C8` border | Site cards. Signature asymmetric radius: 24px top-left + bottom-right only |
| Secondary sand | `#DFCEA7` | Secondary buttons; text on them `#464032` |

**Type:** Crimson Text SemiBold (600) for all headings, letter-spacing -0.4px. Figtree Regular for body/UI (site body is 20px; graphic captions read well at 24px). Buttons: 12px radius. Hero headline is Crimson Text 600 in `#ECEFD8` on `#3B7120` blocks (padding 12px horizontal / 4px vertical, square corners) over `#1D3212`. Dark canvases pair `#1D3212` background with `#ECEFD8` headings and `#9FAF97` muted subtext.

**Logo:** official vector at `https://www.cambrian.org/redesign/cambrian-hexagon.svg` (green hexagon + cream leaf, aspect 31.123:35.961). Do NOT swap its fills to "invert" it. The mark is built as a green hexagon-minus-leaf compound over a cream base, so a fill swap breaks it. Raster fallback: `.claude/src/public/cambrian_logo.png`. Ammonite/Haeckel line-art texture: `.claude/src/launch-video/public/texture.png`. (Paths relative to the product-research repo root.)

**Backgrounds:** official background at `https://www.cambrian.org/redesign/background-pattern.svg` (seamless pattern for light and dark canvases)

**Writing on graphics:** no em dashes (hard fail), run /humanizer on copy, data examples use blue-chip protocols only.

## Producing a graphic

Reference implementation: `.claude/src/mockups/pipeline-graphic.html` (light + dark canvases, brand CSS vars, seeded-random art, Google Fonts link for Crimson Text + Figtree). The finished frames also live in the Figma "Cambrian-vibe-design" file (`figma.com/design/YA3lnEXqebnXOmCL51pDdI`, 3D assets page, the Pipeline Graphic Light and Dark frames) if you'd rather start from those.

1. Build as HTML with the brand tokens as CSS vars, one `<div>` canvas per variant sized in CSS pixels (e.g. 2400x840).
2. Serve with `python3 -m http.server` (Playwright blocks `file://`), navigate, screenshot the canvas element with `scale: "device"`. On a 2x display a 2400x840 div exports a 4800x1680 PNG, which is the retina deliverable.
3. Check colors numerically before delivering: a PIL most-common-color vote over flat regions must return the exact token hexes. Eyeballing misses stale renders.
4. Re-render after ANY source edit. A stale PNG next to a fixed HTML is the classic failure here.

## Vector / SVG deliverable

For scalable output, generate a standalone SVG with the same geometry (measure exact boxes from the rendered HTML via `getBoundingClientRect`). Keep text as `<text>` with `font-family` attributes so it stays editable downstream. Check it with blob-URL + canvas pixel probes in the browser. An `<img>`-embedded SVG cannot load webfonts, so text falls back in that context only; that is not a file defect.

## Getting it into Figma

Load the `figma:figma-use` skill first (mandatory before `use_figma`).

1. `upload_assets` with `Content-Type: image/svg+xml`, multipart `file` field (the filename becomes the layer name). SVGs import as fully editable vector trees with real text nodes.
2. Post-import fix, always: Figma maps `font-weight="600"` to Bold. Switch heading text nodes to Crimson Text SemiBold via `use_figma` (`loadFontAsync` first) and set letter-spacing -0.4px.
3. Compare `node.screenshot()` against the approved PNG.
4. Figma MCP on a View seat has a hard tool-call cap. If calls fail with a seat-limit error, hand the user the SVGs to drag in manually.

## Common mistakes

- Using `#4B9328` for headline highlight blocks (correct: `#3B7120` with `#ECEFD8` text)
- Treating the highlight-block green as an error and "unifying" the palette
- Sampling brand colors from resized screenshots (resampling shifts hexes; read Figma fills or vote over flat regions of native renders)
- Instrument Serif / Inter as stand-ins (the real faces are Crimson Text + Figtree, both on Google Fonts)
- Shipping a PNG rendered before the last source edit
