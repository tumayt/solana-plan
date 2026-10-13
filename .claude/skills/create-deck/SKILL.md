---
name: create-deck
description: Generate an HTML slide deck with Cambrian design system
argument-hint: "[topic or title]"
---

# Create Slide Deck: $ARGUMENTS

Generate a self-contained HTML slide deck for the given topic using the Cambrian presentation design system.

## Steps

1. **Gather content** — Research the topic using repo files, and Cambrian API docs as needed.

2. **Plan the deck** — Outline 8-15 slides. Every deck should have:
   - Title slide (slide 0)
   - Problem / context slide
   - Core content slides (data, comparisons, proposals)
   - Discussion / open questions slide (if applicable)
   - Next steps / action items slide (final)

3. **Generate the HTML file** — Write a single self-contained HTML file to the target path.

4. **Verify** — Open the file path and confirm the slide count, navigation, and theme toggle work.

## Design System Reference

Use this exact design system. Do NOT deviate from these styles, fonts, or colors.

### HTML Shell

```html
<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Cambrian API: DECK_TITLE</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
```

### Theme Variables

```css
[data-theme="dark"] {
  --bg: #0a0a0a;
  --text: #e5e5e5;
  --text-dim: #999;
  --text-muted: #666;
  --accent: #4b9328;
  --accent-light: #78AD59;
  --border: #1a1a1a;
  --border-light: #252525;
  --surface: #111;
  --toggle-bg: #1a1a1a;
  --dot-inactive: #252525;
  --code-bg: #111;
  --code-text: #78AD59;
  --table-stripe: rgba(255,255,255,0.02);
  --risk-bg: transparent;
  --blue: #2a5a8a;
  --blue-light: #3a7ab8;
}

[data-theme="light"] {
  --bg: #fafaf8;
  --text: #11181c;
  --text-dim: #57606a;
  --text-muted: #8b949e;
  --accent: #4b9328;
  --accent-light: #3b7120;
  --border: #e8e8e4;
  --border-light: #d8d8d4;
  --surface: #f0efe8;
  --toggle-bg: #e8e8e4;
  --dot-inactive: #d0d0c8;
  --code-bg: #f0efe8;
  --code-text: #3b7120;
  --table-stripe: rgba(0,0,0,0.02);
  --risk-bg: #f5f5f0;
  --blue: #2a5a8a;
  --blue-light: #1e4a72;
}
```

### Toolbar & Controls

All controls live in a fixed `.toolbar` flex container (top-right). Use `.toolbar-btn` for consistent styling.

```html
<div class="toolbar" id="toolbar">
  <div class="toolbar-btn" id="modeToggle" onclick="toggleMode()">
    <span class="mode-icon" id="modeIcon">&#9654;</span>
    <span class="label-text" id="modeLabel">present</span>
  </div>
  <div class="export-wrapper">
    <div class="toolbar-btn" id="exportBtn" onclick="toggleExport(event)">
      <span class="export-icon">&darr;</span>
      <span class="label-text" id="exportLabel">export</span>
    </div>
    <div class="export-dropdown" id="exportDropdown">
      <div class="export-dropdown-item" onclick="exportMarkdown('current')">Copy this slide as Markdown <span class="item-hint">clipboard</span></div>
      <div class="export-dropdown-item" onclick="exportMarkdown('all')">Copy all slides as Markdown <span class="item-hint">clipboard</span></div>
      <div class="export-divider"></div>
      <div class="export-dropdown-item" onclick="exportPDF('current')">Print this slide as PDF <span class="item-hint">&#8984;P</span></div>
      <div class="export-dropdown-item" onclick="exportPDF('all')">Print all slides as PDF <span class="item-hint">&#8984;P</span></div>
    </div>
  </div>
  <div class="toolbar-btn" id="themeToggle" onclick="toggleTheme()">
    <span class="icon icon-moon">&#9790;</span>
    <span class="icon icon-sun">&#9788;</span>
    <span class="label-text" id="themeLabel">dark</span>
  </div>
</div>
```

```css
.toolbar { position: fixed; top: 20px; right: 24px; z-index: 200; display: flex; align-items: center; gap: 10px; }
.toolbar-btn {
  display: flex; align-items: center; gap: 8px;
  background: var(--toggle-bg); border: 1px solid var(--border-light);
  border-radius: 24px; padding: 6px 14px; cursor: pointer;
  transition: all 0.3s ease; user-select: none;
}
.toolbar-btn:hover { border-color: var(--accent); }
.toolbar-btn .label-text { font-size: 11px; font-weight: 500; text-transform: uppercase; letter-spacing: 1.5px; color: var(--text-muted); font-family: 'IBM Plex Mono', monospace; }
.export-wrapper { position: relative; }
.export-dropdown { position: absolute; top: calc(100% + 6px); right: 0; z-index: 201; background: var(--bg); border: 1px solid var(--border-light); border-radius: 10px; padding: 6px 0; min-width: 240px; box-shadow: 0 8px 32px rgba(0,0,0,0.3); opacity: 0; pointer-events: none; transform: translateY(-8px); transition: all 0.2s ease; }
.export-dropdown.open { opacity: 1; pointer-events: auto; transform: translateY(0); }
.export-dropdown-item { padding: 10px 18px; font-size: 13px; color: var(--text-dim); cursor: pointer; transition: all 0.15s ease; }
.export-dropdown-item:hover { background: rgba(75,147,40,0.08); color: var(--text); }
.export-dropdown-item .item-hint { font-size: 10px; color: var(--text-muted); margin-left: 4px; font-family: 'IBM Plex Mono', monospace; }
.export-divider { height: 1px; background: var(--border); margin: 6px 18px; }
```

### Slide Controls (Edit Mode — Top Center)

Show hide/delete controls in edit mode.

```html
<div class="slide-controls" id="slideControls">
  <span class="slide-info" id="slideInfo">Slide 1</span>
  <div class="ctrl-btn" onclick="toggleHideSlide()">
    <span class="ctrl-icon" id="hideIcon">&#9678;</span>
    <span class="ctrl-label" id="hideLabel">hide</span>
  </div>
  <div class="ctrl-btn delete-btn" id="deleteSlideBtn" onclick="deleteCurrentSlide()">
    <span class="ctrl-icon" style="color:#c9873a;">&#10005;</span>
    <span class="ctrl-label" style="color:#c9873a;">delete</span>
  </div>
</div>
```

### Edit / Present Mode CSS

```css
body.edit-mode .click-zone { pointer-events: none; }
body.edit-mode [contenteditable]:hover { outline: 1px dashed var(--accent); outline-offset: 2px; }
body.edit-mode [contenteditable]:focus { outline: 2px solid var(--accent); outline-offset: 2px; background: rgba(75,147,40,0.04); border-radius: 4px; }
body.present-mode #modeToggle, body.present-mode .export-wrapper, body.present-mode .progress,
body.present-mode .slide-counter, body.present-mode .slide-controls { display: none !important; }
body.present-mode .slide-frame { max-width: 100vw; max-height: 100vh; width: 100vw; height: 100vh; border-radius: 0; }
.slide.slide-hidden { outline: 2px dashed #c9873a; outline-offset: -4px; }
body:not(.edit-mode) .slide.slide-hidden { display: none; }
.slide-controls { position: fixed; top: 20px; left: 50%; transform: translateX(-50%); z-index: 200; display: none; align-items: center; gap: 12px; background: var(--toggle-bg); border: 1px solid var(--border-light); border-radius: 24px; padding: 4px 16px; }
body.edit-mode .slide-controls { display: flex; }
```

### Print CSS Requirements

Always include these print overrides:
```css
@media print {
  .toolbar, .export-dropdown, .progress, .slide-counter, .click-zone, .slide-controls { display: none !important; }
  body { overflow: visible !important; height: auto !important; display: block !important; }
  .slide-frame { width: 100% !important; height: auto !important; max-width: none !important; position: static !important; background-image: none !important; }
  .slide-frame::before { display: none !important; }
  .slide .fragment { opacity: 1 !important; transform: none !important; }
  .slide > div { zoom: 1 !important; }
  body.print-all .slide { position: static !important; opacity: 1 !important; display: flex !important; page-break-after: always; page-break-inside: avoid; min-height: 90vh; }
  body.print-current .slide { display: none !important; }
  body.print-current .slide.active { display: flex !important; position: static !important; opacity: 1 !important; }
}
```

### JavaScript Engine

The JS engine includes:
- **Navigation**: `next()`, `prev()`, `goToSlide()`, touch + keyboard. Every navigation action advances directly to the requested slide with all its content visible, including clicks, keyboard, touch and progress dots.
- **Edit/Present mode**: `enterEditMode()`, `enterPresentMode()`, `toggleMode()`, fullscreen API
- **Hide/Delete slides**: `toggleHideSlide()`, `deleteCurrentSlide()`, `findVisibleSlide()`, progress dot sync
- **Persistence (localStorage)**: Hidden slide state (`saveHidden()`/`loadHidden()`) and text edits (`saveEdits()`/`loadEdits()`) both persist across reloads
- **Auto-scale**: `autoScaleSlide()` — dynamic text sizing per slide using CSS `zoom`
- **Export**: Markdown clipboard + PDF print, both skip hidden slides

Key patterns:
- `let slides = Array.from(...)` — mutable for delete support
- `data-edit-id` attributes on all editable elements for stable text persistence
- `blur` event listener (capture phase) auto-saves edited text
- Present mode auto-jumps to nearest visible slide if current is hidden
- Keyboard handler respects `contenteditable` focus (returns early if editing text)
- Press `e` to toggle edit/present mode
- `next()` advances immediately; `goToSlide()` calls `showAllFragments()` on the destination. Never consume a navigation action just to reveal content.
- `prev()` goes directly to the previous slide (no fragment-by-fragment reversal)

### Slide Anchors (Required)

Every generated deck must support direct slide links, such as `deck.html#common`, using the anchor implementation in [the canonical template](../../src/deck/decks/agentic-consumption.html).

1. Give every slide a unique, stable `data-anchor` slug. Use lowercase words separated by hyphens, such as `decision`, `common`, `path-2`, and `next-steps`. Preserve existing slugs when editing headings or reordering slides; resolve duplicate slugs explicitly.
   ```html
   <div class="slide" data-slide="9" data-anchor="common" data-title="Common work">
     <div><!-- All slide content --></div>
   </div>
   ```
2. Use `slideAnchor()`, `syncSlideAnchor()`, and `followSlideAnchor()` from the template. Resolve anchors against the current slide array, not a fixed numeric index. Do not assign matching DOM IDs: native anchor scrolling can displace the fixed presentation layout.
3. After initialization, decode the URL hash safely and open the matching visible slide with all fragments revealed. Run this after navigation state and controls are initialized. Empty, unknown, malformed, hidden, or deleted targets must not crash the deck or reveal a hidden slide; keep a valid visible slide selected.
4. Call `syncSlideAnchor()` after changing slides. Route previous/next buttons, keyboard, touch and progress dots through the same navigation path. Use `history.pushState()` for a new slide and `replaceState()` for initial URL normalization. Only write history when the target hash differs from the current hash.
5. Handle both `hashchange` and `popstate` so pasted hashes and browser Back/Forward restore the correct slide. Following an existing history entry must not create another entry.
6. Verify a direct `#common`-style link, refresh on that slide, one-click next/previous, a progress-dot jump, a manually changed hash, and browser Back/Forward. Check that the URL and active slide agree and all destination content is visible. Also check unknown and malformed hashes and hidden/deleted slide targets.

### Auto-Scale (Dynamic Text Sizing)

Every slide's content auto-scales so dense slides shrink to fit and sparse slides grow for readability.

**How it works:** Uses CSS `zoom` (not `transform: scale`) on each slide's inner `<div>` wrapper. `zoom` changes layout — text reflows at the new size, unlike transform which only changes visual appearance.

```javascript
function autoScaleSlide(slideEl) {
  const inner = slideEl.children[0];
  if (!inner) return;
  inner.style.zoom = '1'; // reset to measure natural height
  const style = getComputedStyle(slideEl);
  const availH = slideEl.clientHeight - parseFloat(style.paddingTop) - parseFloat(style.paddingBottom);
  const naturalH = inner.scrollHeight;
  if (naturalH <= 0 || availH <= 0) return;
  let scale = availH / naturalH;
  if (scale > 1) scale = 1 + (scale - 1) * 0.5; // dampen upscale (text reflow makes content taller)
  scale = Math.min(1.25, Math.max(0.55, scale)); // clamp range
  if (scale > 0.97 && scale < 1.03) { inner.style.zoom = ''; return; } // dead zone
  inner.style.zoom = scale;
}
```

**When to call it:**
- `goToSlide()` and `prev()` — after setting active slide
- Init — after `showAllFragments(slides[0])`
- `enterPresentMode()` — `setTimeout(() => autoScaleSlide(...), 100)` (after fullscreen activates)
- `fullscreenchange` event — `setTimeout(() => autoScaleSlide(...), 100)`
- `window resize` event

**Slide structure requirement:** Every slide MUST have a single `<div>` wrapper as its only direct child. All content goes inside this wrapper. This is required for auto-scale measurement.

```html
<div class="slide" data-slide="0">
  <div>  <!-- wrapper — required for auto-scale -->
    <h2 class="fragment">Title</h2>
    <ul>...</ul>
  </div>
</div>
```

### Core CSS, Body Structure, and Component Catalog

For the complete reference implementation of all features, see existing production decks:
- `.claude/src/deck/decks/agentic-consumption.html` (canonical reference — v2 typography, all features)

Component catalog: KPI stats, tables, cards, timelines, status cards, action cards, diff cards, etc.

### Component Variants

| Component | Variants | Usage |
|-----------|----------|-------|
| `.status-card` | `.blocker` (orange border), `.positive` (green border) | Highlight risks or wins |
| `.action-card` | `.action` (green left border), `.question` (orange left border) | Next steps vs open questions |
| `.phase-tag` | `.green`, `.orange`, `.blue` | Timeline phase indicators |
| `.vtimeline-step` | `.done` (green dot), `.wip` (orange dot), `.pending` (empty dot) | Timeline progress |
| `.diff-card` | (no variants) | Side-by-side comparison items |
| `.seq-badge` | `.ok` (green), `.warn` (orange) | Status codes in sequence diagrams |

## Diagram Components (Reusable)

All diagrams are pure CSS — no SVG, no external libraries. They support both dark and light themes via CSS variables. Use two-column layouts (`.columns.two`) with text on the left and diagram on the right.

### Sequence Diagram (Primary)

Use for request/response flows, API interactions, protocol handshakes. Shows two entities with lifelines, directional arrows, status badges, and action boxes.

**CSS:**
```css
.seq-diagram {
  position: relative; background: var(--surface);
  border: 1px solid var(--border-light); border-radius: 12px;
  padding: 20px 0 12px; overflow: hidden;
  transition: background 0.4s ease, border-color 0.4s ease;
}
.seq-header {
  display: flex; justify-content: space-between;
  padding: 0 24px; margin-bottom: 4px; position: relative; z-index: 2;
}
.seq-entity { display: flex; flex-direction: column; align-items: center; gap: 6px; }
.seq-icon {
  width: 48px; height: 48px; border: 2px solid var(--border-light); border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-family: 'IBM Plex Mono', monospace; font-size: 15px; font-weight: 700;
  color: var(--text-dim); background: var(--bg); transition: all 0.4s ease;
}
.seq-icon.accent { border-color: var(--accent); color: var(--accent); }
.seq-name {
  font-family: 'IBM Plex Mono', monospace; font-size: 11px; font-weight: 700;
  text-transform: uppercase; letter-spacing: 1px; color: var(--text-dim);
}
.seq-body { position: relative; padding: 4px 0; }
.seq-body::before, .seq-body::after {
  content: ''; position: absolute; top: 0; bottom: 0; width: 0;
  border-left: 2px dashed var(--border-light); z-index: 0;
  transition: border-color 0.4s ease;
}
.seq-body::before { left: 48px; }
.seq-body::after { right: 48px; }
.seq-row { position: relative; z-index: 1; padding: 10px 0; }
.seq-msg {
  position: relative; margin: 0 50px;
  display: flex; flex-direction: column; align-items: center; gap: 6px;
}
.seq-msg-label {
  font-family: 'IBM Plex Mono', monospace; font-size: 13px; font-weight: 500;
  color: var(--text-dim); display: flex; align-items: center; gap: 6px;
  background: var(--surface); padding: 2px 8px; border-radius: 4px;
  white-space: nowrap; position: relative; z-index: 2;
  transition: background 0.4s ease, color 0.4s ease;
}
.seq-line { width: 100%; position: relative; height: 0; }
.seq-line.solid { border-top: 2px solid var(--text-muted); }
.seq-line.dashed { border-top: 2px dashed var(--text-muted); }
.seq-line.arrow-r::after {
  content: ''; position: absolute; right: -1px; top: -6px;
  border-left: 8px solid var(--text-muted);
  border-top: 5px solid transparent; border-bottom: 5px solid transparent;
}
.seq-line.arrow-l::after {
  content: ''; position: absolute; left: -1px; top: -6px;
  border-right: 8px solid var(--text-muted);
  border-top: 5px solid transparent; border-bottom: 5px solid transparent;
}
.seq-action {
  margin: 0 auto; padding: 6px 14px;
  border: 1px solid #c9873a; border-radius: 8px; background: rgba(201,135,58,0.06);
  font-family: 'IBM Plex Mono', monospace; font-size: 13px; font-weight: 600;
  color: var(--text); text-align: center; width: fit-content;
  position: relative; z-index: 2; transition: background 0.4s ease, color 0.4s ease;
}
.seq-badge {
  font-family: 'IBM Plex Mono', monospace; font-size: 12px; font-weight: 700;
  padding: 1px 7px; border-radius: 4px;
}
.seq-badge.warn { background: rgba(201,135,58,0.15); color: #c9873a; border: 1px solid rgba(201,135,58,0.3); }
.seq-badge.ok { background: rgba(75,147,40,0.15); color: var(--accent); border: 1px solid rgba(75,147,40,0.3); }
```

**HTML (x402 example):**
```html
<div class="seq-diagram">
  <div class="seq-header">
    <div class="seq-entity">
      <div class="seq-icon">&gt;_</div>
      <div class="seq-name">Agent</div>
    </div>
    <div class="seq-entity">
      <div class="seq-icon accent">API</div>
      <div class="seq-name">Server</div>
    </div>
  </div>
  <div class="seq-body">
    <div class="seq-row">
      <div class="seq-msg">
        <div class="seq-msg-label">GET /api/resource</div>
        <div class="seq-line solid arrow-r"></div>
      </div>
    </div>
    <div class="seq-row">
      <div class="seq-msg">
        <div class="seq-msg-label"><span class="seq-badge warn">402</span> PAYMENT REQUIRED</div>
        <div class="seq-line dashed arrow-l"></div>
      </div>
    </div>
    <div class="seq-row" style="padding: 6px 0;">
      <div class="seq-action">Sign EIP-712 (Wallet)</div>
    </div>
    <div class="seq-row">
      <div class="seq-msg">
        <div class="seq-msg-label">GET + Payment-Sig</div>
        <div class="seq-line solid arrow-r"></div>
      </div>
    </div>
    <div class="seq-row">
      <div class="seq-msg">
        <div class="seq-msg-label"><span class="seq-badge ok">200</span> OK + DATA</div>
        <div class="seq-line dashed arrow-l"></div>
      </div>
    </div>
  </div>
</div>
```

**Key elements:**
- `.seq-line.solid.arrow-r` = request (solid line, arrowhead right)
- `.seq-line.dashed.arrow-l` = response (dashed line, arrowhead left)
- `.seq-badge.warn` = error/warning status (orange, e.g. 402)
- `.seq-badge.ok` = success status (green, e.g. 200)
- `.seq-action` = local action box (orange border, e.g. "Sign Payment")

### Routing / Architecture Diagram

Use for showing data flow through processing layers: source → hub → output. Best for architecture overviews where entities aren't doing a time-based back-and-forth.

**CSS:**
```css
.routing-diagram { display: flex; align-items: center; gap: 14px; margin: 16px 0; }
.routing-box {
  padding: 18px 16px; border: 1px solid var(--border-light); border-radius: 10px;
  text-align: center; transition: border-color 0.4s ease;
}
.routing-box.source { min-width: 120px; }
.routing-box.hub { flex: 1; }
.routing-box.target { min-width: 140px; }
.routing-box .box-label {
  font-size: 14px; font-weight: 600; text-transform: uppercase;
  letter-spacing: 1.2px; color: var(--accent); margin-bottom: 8px;
}
.routing-box .box-title { font-size: 22px; font-weight: 600; }
.routing-box .box-items { display: flex; flex-direction: column; gap: 6px; margin-top: 8px; }
.routing-box .box-item {
  font-family: 'IBM Plex Mono', monospace; font-size: 16px; color: var(--code-text);
  background: var(--code-bg); padding: 8px 14px; border-radius: 6px; text-align: left;
  transition: background 0.4s ease, color 0.4s ease;
}
.routing-arrow {
  font-size: 32px; color: var(--accent); flex-shrink: 0;
  font-family: 'IBM Plex Mono', monospace; font-weight: 300;
}
```

**HTML:**
```html
<div class="routing-diagram fragment">
  <div class="routing-box source">
    <div class="box-label">Input</div>
    <div class="box-title">Source</div>
  </div>
  <div class="routing-arrow">&rarr;</div>
  <div class="routing-box hub">
    <div class="box-label">Processing Layer</div>
    <div class="box-items">
      <div class="box-item">Component A</div>
      <div class="box-item">Component B</div>
    </div>
  </div>
  <div class="routing-arrow">&rarr;</div>
  <div class="routing-box target">
    <div class="box-label">Output</div>
    <div class="box-title" style="font-size: 42px; color: var(--accent);">N+</div>
    <div style="font-size: 18px; color: var(--text-dim);">items</div>
  </div>
</div>
```

### When to Use Diagrams

| Content Type | Diagram | Example |
|-------------|---------|---------|
| Request/response protocols | `.seq-diagram` | x402 flow, MCP handshake, API auth |
| Architecture / data routing | `.routing-diagram` | MCP tool routing, pipeline layers |
| Comparisons | `.columns.two` + `.diff-card` | Two approaches side-by-side |
| Metrics | `.stat-grid` + `.big-number` | KPIs, market stats |

**Layout pattern:** Use `.columns.two` with text/bullets on the left and the diagram on the right. Heading spans full width above.

## Content Guidelines

- **Cambrian green** (`#4b9328`) is the accent. Use `.green` class or `var(--accent)`.
- If using `class="fragment"` for entry transitions, reveal every fragment together on slide entry and on initial load. Content must never require an extra click to become visible.
- Keep text concise. Slides are for presenting, not reading.
- Brand voice: confident, precise, minimal. No marketing fluff.
- Aim for 8-15 slides. Fewer is better.
- Every slide should make exactly one point.
- End with actionable next steps, not a "thank you" slide.
- **Prefer diagrams over text** for protocol flows and architecture. One diagram replaces paragraphs of explanation.
- All diagram CSS uses `var()` theme variables and `transition` for seamless dark/light switching.
- **Always include** the toolbar (mode toggle + export + theme), slide controls (hide/delete), and persistence JS engine. These are standard features in every deck.

## Learnings

One click or arrow-key press must advance one slide with its full content visible. Reveal fragments on initial load and in `goToSlide()`, and remove fragment-reveal early returns from `next()`. Verify forward/back navigation and direct progress-dot jumps on a generated deck; updating CSS visibility alone leaves the extra navigation step in place.

Slide deep links are standard deck behavior; follow the required Slide Anchors implementation and verification steps above.
