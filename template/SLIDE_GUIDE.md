# Slide Guide — AI Agent Reference Card
> **How to use this guide**: Read this document **before writing any slide HTML**. It contains every design token, component, and pattern used by this template. Copy-paste the snippets, fill in your content, and register the file in `slides.html`.
---
## Table of Contents
1. [Design Tokens (CSS Variables)](#1-design-tokens)
2. [Typography & Font Scale](#2-typography)
3. [Slide File Anatomy](#3-slide-file-anatomy)
4. [Registering Slides](#4-registering-slides)
5. [Layout Patterns](#5-layout-patterns)
6. [Component Library](#6-component-library)
7. [Color Accents & Variants](#7-color-accents--variants)
8. [Micro-Animation Patterns](#8-micro-animation-patterns)
9. [Naming Conventions](#9-naming-conventions)
10. [Export to PNG](#10-export-to-png)
---
## 1. Design Tokens
All CSS variables are defined on `:root` in `slides.html`. **Never hard-code colors — always use these variables.**
| Variable | Value | Usage |
|---|---|---|
| `--bg-dark-blue` | `#0A1128` | Default slide background |
| `--accent-orange` | `#FF6B35` | Primary accent — titles, icons, borders, highlights |
| `--text-white` | `#FFFFFF` | Primary text |
| `--card-blue` | `#14213D` | Card / panel backgrounds |
| `--border-blue` | `#3B5480` | Card borders, dividers |
| `--dim-blue` | `#3B5480` | Same as border-blue, alias for semantic clarity |
| `--text-dim` | `#F1F5F9` | Dimmed / secondary text |
| `--badge-green` | `#10B981` | Success badges, positive state indicators |
| `--glass-bg` | `rgba(10,17,40,0.7)` | Glassmorphism card backgrounds |
| `--glass-border` | `rgba(35,57,91,0.4)` | Glassmorphism card borders |
**Secondary accent colors** (use sparingly, for contrast/variety in the same slide):
| Color | Value | Semantic use |
|---|---|---|
| Cyan | `#00F0FF` | Alternative accent for "Tier 1 / UI layer" distinction |
| Green | `#10B981` | Success, positive outcome, confirmed state |
| Red | `#EF4444` | Error, bad state, "do not" examples |
| Slate | `#E2E8F0` | Body text on dark backgrounds |
---
## 2. Typography
**Font**: `Public Sans` (loaded from Google Fonts — do not change).
| Element | Font size | Weight | Notes |
|---|---|---|---|
| `h1.main-title` | 46px | 800 | Auto orange underbar, `margin-bottom: 40px` |
| Section headers | 26–30px | 800 | Usually colored with `var(--accent-orange)` |
| Card titles / col headers | 22–28px | 700–800 | |
| Body / description text | 18–23px | 400–600 | Line-height 1.45–1.55 |
| Bullet list items | 21px | 400 | `color: #E2E8F0` |
| Small labels / badges | 13–16px | 700–800 | Uppercase, letter-spacing 1–2px |
| `.tagline` | 14px | 700 | Orange, uppercase, `letter-spacing: 2px` |
---
## 3. Slide File Anatomy
Every slide is a **single HTML fragment** — no `<html>`, `<head>`, or `<body>` tags. The engine fetches and injects it.
```html
<!-- SPEAKER NOTES (not rendered):
     Write your spoken notes here. 45–90 seconds of material per slide.
-->
<!-- SLIDE N: SHORT DESCRIPTION -->
<div class="slide slide-[name]" id="slide-[0-based-index]" aria-label="Slide N: Topic">
    <style>
        /*
         * MANDATORY: scope ALL rules with .slide-[name]
         * This prevents styles from leaking to other slides.
         */
        .slide-[name] .my-component { ... }
    </style>
    <div class="content-wrapper">
        <!-- h1.main-title: slide heading with auto orange underbar -->
        <h1 class="main-title">Slide Title</h1>
        <!-- Your layout here -->
        <!-- Optional outcome box — always last child, uses margin-top: auto -->
        <div class="system-outcome-box">
            <div class="outcome-label">KEY TAKEAWAY</div>
            <div class="outcome-text">One-liner summary.</div>
        </div>
    </div>
</div>
```
**Rules:**
- Class `slide` is required (engine uses it to find all slides).
- Add `active` class to the first slide only (e.g., `class="slide slide-cover active"`).
- `id` must be `slide-[0-based-index]` matching its position in `slideSources`.
- Scope **every CSS rule** with `.slide-[name]` — no bare tag selectors.
- The slide canvas is always **1280 × 720 px** at 16:9. Design for this exact size.
---
## 4. Registering Slides
In `slides.html`, find the `slideSources` array and add your file paths **in order**:
```javascript
const slideSources = [
    'slides/999_cover.html',                     // index 0 → id="slide-0"
    'slides/1_blank.html',                       // index 1 → id="slide-1"
    'slides/2_text_and_image_split.html',        // index 2 → id="slide-2"
    'slides/3_problem_vs_solution_cards.html',   // index 3 → id="slide-3"
    // ... add more here
];
```
**Naming convention for files**: `[order]_[short-slug].html`  
Examples: `1_overview.html`, `4_three_tier_architecture.html`, `6_kpi_metrics_dashboard.html`
---
## 5. Layout Patterns
### 5a. Two-Column Split (most common)
```css
.slide-[name] .two-col {
    display: grid;
    grid-template-columns: 1fr 1fr;   /* equal */
    /* or: 1.1fr 0.9fr for slight left emphasis */
    gap: 40px;
    flex-grow: 1;
    align-items: center;
}
```
### 5b. Three-Column Cards
```css
.slide-[name] .grid-3 {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 25px;
    flex-grow: 1;
}
```
### 5c. Four-Column Cards
```css
.slide-[name] .grid-4 {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 15px;
    flex-grow: 1;
}
```
### 5d. Full-Width Horizontal Flow (arrow chains)
```html
<div style="display: flex; align-items: center; gap: 20px; flex-grow: 1;">
    <div class="col"> ... </div>
    <div class="flow-arrow"><i class="fa-solid fa-chevron-right"></i></div>
    <div class="col"> ... </div>
    <div class="flow-arrow"><i class="fa-solid fa-chevron-right"></i></div>
    <div class="col"> ... </div>
</div>
```
```css
.slide-[name] .flow-arrow {
    font-size: 34px;
    color: var(--accent-orange);
    opacity: 0.9;
    flex-shrink: 0;
    width: 30px;
}
```
### 5e. Vertical Timeline / Step List
```css
.slide-[name] .timeline { display: flex; flex-direction: column; gap: 14px; }
.slide-[name] .timeline-step {
    display: flex; gap: 18px; align-items: center;
    background: rgba(20,33,61,0.35);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 12px; padding: 14px 20px;
}
.slide-[name] .step-num {
    background: var(--accent-orange); color: #0c1830;
    font-weight: 800; width: 32px; height: 32px;
    border-radius: 50%; display: flex; align-items: center;
    justify-content: center; font-size: 16px; flex-shrink: 0;
}
```
---
## 6. Component Library
### 6a. `h1.main-title` — Slide Heading
Auto-generates an orange 360px underbar via `::after`.
```html
<h1 class="main-title">Your Slide Title</h1>
```
Reduce bottom margin if needed: `style="margin-bottom: 20px;"`
---
### 6b. `.tagline` — Orange Uppercase Label
Small label above a title or card heading.
```html
<span class="tagline">Section Label</span>
```
---
### 6c. `.bullet-list` — Arrow Bullet List
FontAwesome chevron bullets, 21px body text.
```html
<ul class="bullet-list">
    <li><strong>Bold key:</strong> Supporting explanation text.</li>
    <li>Another item without a bold prefix.</li>
</ul>
```
---
### 6d. Dark Card
Standard dark-background card with hover lift.
```html
<!-- CSS (scoped) -->
<style>
.slide-[name] .card {
    background-color: var(--card-blue);
    border: 1px solid var(--border-blue);
    border-radius: 20px; padding: 30px;
    display: flex; flex-direction: column;
    transition: transform 0.3s ease, border-color 0.3s ease;
}
.slide-[name] .card:hover { transform: translateY(-6px); border-color: var(--accent-orange); }
</style>
<!-- HTML -->
<div class="card">
    <div class="icon-circle"><i class="fa-solid fa-rocket"></i></div>
    <span class="tagline">Card Label</span>
    <h2 style="font-size:25px; font-weight:700; margin-bottom:12px;">Card Title</h2>
    <p style="font-size:19px; color:#E2E8F0; line-height:1.55;">Card body text here.</p>
    <div class="example-box" style="margin-top:auto;">
        <span class="example-label">Use when</span>
        <p class="example-text">Condition or context.</p>
    </div>
</div>
```
---
### 6e. `.icon-circle` — Icon Badge
Square-rounded orange icon badge (used at top of cards).
```html
<style>
.slide-[name] .icon-circle {
    width: 56px; height: 56px;
    background-color: var(--accent-orange);
    color: var(--bg-dark-blue);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 26px; margin-bottom: 22px;
}
</style>
<div class="icon-circle"><i class="fa-solid fa-brain"></i></div>
```
---
### 6f. Tier Container — Left-Bordered Row
Used for multi-tier architecture slides.
```html
<style>
.slide-[name] .tier-row {
    display: flex; align-items: center;
    background: rgba(20,33,61,0.4);
    border: 1.5px solid rgba(255,255,255,0.08);
    border-radius: 14px; padding: 16px 24px;
    position: relative; gap: 25px;
}
.slide-[name] .tier-row::before {
    content: ''; position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 4px;
    background: var(--accent-orange); /* or #00F0FF for cyan tiers */
    border-radius: 4px 0 0 4px;
}
.slide-[name] .tier-label { width: 200px; flex-shrink: 0; }
.slide-[name] .tier-num { font-size:17px; font-weight:800; color: var(--accent-orange); text-transform: uppercase; letter-spacing: 1.5px; }
.slide-[name] .tier-name { font-size:28px; font-weight:800; }
</style>
<div class="tier-row">
    <div class="tier-label">
        <div class="tier-num">Tier 1</div>
        <div class="tier-name">Layer Name</div>
    </div>
    <!-- content grid on the right -->
    <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:15px; flex-grow:1;">
        <!-- mini cards -->
    </div>
</div>
```
---
### 6g. `.example-box` — Callout Box (Orange Tint)
Use inside cards at the bottom, or as a standalone callout.
```html
<div class="example-box">
    <span class="example-label">Example / Context</span>
    <p class="example-text">The italic example sentence goes here.</p>
</div>
```
---
### 6h. `.system-outcome-box` — Bottom Summary Bar
Left-bordered orange bar. Always place as **last child** of `.content-wrapper` (it uses `margin-top: auto` to stick to the bottom).
```html
<div class="system-outcome-box">
    <div class="outcome-label">KEY TAKEAWAY</div>
    <div class="outcome-text">
        One memorable sentence summarizing this slide's core message.
    </div>
</div>
```
---
### 6i. Speech Bubble
Used for user-quote or dialogue examples.
```html
<style>
.slide-[name] .speech-bubble {
    position: relative;
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px; padding: 16px 20px;
    color: #E2E8F0;
    transition: all 0.25s ease;
}
.slide-[name] .speech-bubble:hover { background: rgba(255,255,255,0.05); border-color: var(--accent-orange); }
.slide-[name] .speech-bubble::after {
    content:''; position:absolute; bottom:-8px; left:24px;
    border-width:8px 8px 0; border-style:solid;
    border-color: rgba(255,255,255,0.035) transparent;
    display:block; width:0;
}
.slide-[name] .bubble-tag { font-size:15px; font-weight:800; color:var(--accent-orange); text-transform:uppercase; letter-spacing:1px; margin-bottom:8px; display:block; }
.slide-[name] .bubble-text { font-size:21px; font-style:italic; font-weight:600; line-height:1.45; }
</style>
<div class="speech-bubble">
    <span class="bubble-tag">User says</span>
    <div class="bubble-text">"The thing the user says goes here."</div>
</div>
```
---
### 6j. Status / Metric Badge
```html
<!-- Green success badge -->
<span style="background:rgba(16,185,129,0.15); border:1px solid #10B981; color:#10B981; padding:4px 10px; border-radius:6px; font-size:14px; font-weight:700; text-transform:uppercase;">
    Success
</span>
<!-- Orange accent badge -->
<span style="background:rgba(255,107,53,0.1); border:1px solid rgba(255,107,53,0.3); color:var(--accent-orange); padding:4px 10px; border-radius:6px; font-size:14px; font-weight:700;">
    Active
</span>
```
---
### 6k. Large Percentage / Stat Display
```html
<style>
.slide-[name] .stat-card {
    background: rgba(20,33,61,0.4);
    border: 1.5px solid rgba(255,107,53,0.25);
    border-radius: 16px; padding: 32px 24px;
    text-align: center; display: flex;
    flex-direction: column; gap: 14px;
}
.slide-[name] .stat-value { font-size: 48px; font-weight: 800; color: var(--accent-orange); line-height: 1; }
.slide-[name] .stat-label { font-size: 22px; font-weight: 800; color: var(--text-white); text-transform: uppercase; }
.slide-[name] .stat-desc { font-size: 18px; color: #F1F5F9; line-height: 1.45; }
</style>
<div class="stat-card">
    <span class="stat-value">50%</span>
    <span class="stat-label">Metric Name</span>
    <p class="stat-desc">Short explanation of what this metric means.</p>
</div>
```
---
### 6l. Animated Pulse Ring (for focal elements)
```css
.slide-[name] .pulse-element {
    animation: pulse-ring 2.5s infinite;
}
@keyframes pulse-ring {
    0%   { box-shadow: 0 0 0 0 rgba(255, 107, 53, 0.4); }
    70%  { box-shadow: 0 0 0 15px rgba(255, 107, 53, 0); }
    100% { box-shadow: 0 0 0 0 rgba(255, 107, 53, 0); }
}
```
---
### 6m. Formula / Code Display
```html
<div style="background:rgba(5,8,22,0.6); border:1px solid rgba(255,107,53,0.2); border-radius:12px; padding:14px; text-align:center;">
    <span style="font-size:14px; color:rgba(255,255,255,0.4); text-transform:uppercase; letter-spacing:1px; display:block; margin-bottom:10px;">Formula</span>
    <div style="display:flex; align-items:center; justify-content:center; gap:10px;">
        <span style="background:rgba(255,107,53,0.15); border:1px solid rgba(255,107,53,0.4); color:var(--accent-orange); padding:6px 16px; border-radius:8px; font-size:20px; font-weight:800; font-family:monospace;">var_a</span>
        <span style="font-size:20px; color:rgba(255,255,255,0.4); font-weight:700;">+</span>
        <span style="background:rgba(255,107,53,0.15); border:1px solid rgba(255,107,53,0.4); color:var(--accent-orange); padding:6px 16px; border-radius:8px; font-size:20px; font-weight:800; font-family:monospace;">var_b</span>
    </div>
</div>
```
---
## 7. Color Accents & Variants
When a slide needs **two competing accent colors** (e.g., to distinguish two systems or tiers), use:
- **Primary accent**: `var(--accent-orange)` — `#FF6B35`
- **Secondary accent**: Cyan `#00F0FF`
Pattern to apply a cyan tier (override orange defaults):
```css
.slide-[name] .tier-cyan::before { background: #00F0FF; }
.slide-[name] .tier-cyan .tier-num { color: #00F0FF; }
.slide-[name] .tier-cyan .tier-card-title i { color: #00F0FF !important; }
```
---
## 8. Micro-Animation Patterns
All hover effects use `transition: all 0.3s ease` unless specified.
| Pattern | CSS |
|---|---|
| Card lift on hover | `transform: translateY(-4px)` |
| Card border highlight | `border-color: var(--accent-orange)` |
| Row slide in | `transform: translateX(4px)` |
| Subtle scale | `transform: scale(1.02)` |
| Glow on hover | `box-shadow: 0 10px 30px rgba(255,107,53,0.12)` |
| Step pulse animation | `@keyframes pulse-ring` (see §6l) |
**Slide entrance** is handled by the engine — slides fade in with `translateY(20px) → translateY(0)`.
---
## 9. Naming Conventions
| Item | Convention | Example |
|---|---|---|
| Slide file | `[order]_[slug].html` | `3_architecture.html` |
| Slide class | `slide-[slug]` | `slide-architecture` |
| Slide id | `slide-[0-based-index]` | `id="slide-2"` |
| Scoped CSS | `.slide-[slug] .component` | `.slide-architecture .tier-row` |
| Layout wrappers | descriptive kebab-case | `.two-col`, `.flow-container`, `.feature-grid` |
**Important**: The engine finds slides by the `.slide` class. Never omit it.
---
## 10. Export to PNG & PDF (Multi-Theme)
Run the export scripts from the **deck's directory** (the folder containing `slides.html`):
```bash
# Install dependencies (once)
pip install playwright Pillow
playwright install chromium

# 1. Full Export (GUI) - Select themes and generate full PDFs
python export.py

# 2. Quick Preview - Automatically captures only Slide 1 across all 10 themes
python preview.py
```
**`export.py`**:
1. Starts a local HTTP server and opens a Desktop Tkinter GUI.
2. Lets you select exactly which themes you want to export.
3. Automatically bypasses CSS transitions for pixel-perfect instant PNG capture.
4. Saves to `exported_slides/[theme-name]/Slide_NN.png` and stitches `presentation_[theme].pdf`.

**`preview.py`**:
1. Runs entirely in the background (headless).
2. Instantly grabs Slide 01 for all 10 themes to generate 10 preview PNGs in `exported_previews/`.

**Output**: 10 `presentation_*.pdf` files and populated subfolders in `exported_slides/`.
---
## 11. Global Theme Engine
The engine includes an interactive GPU-accelerated Theme Picker that uses `hue-rotate` and `invert` matrix math.
**5 Dark Modes:**
- `theme-default` (Midnight Orange)
- `theme-emerald` (Teal & Green)
- `theme-cyberpunk` (Purple & Pink)
- `theme-monochrome` (Grayscale)
- `theme-ruby` (Plum & Red)

**5 Light Modes:**
- `theme-light-corporate` (Icy Blue)
- `theme-light-warm` (Cream & Sky Blue)
- `theme-light-mint` (Mint & Violet)
- `theme-light-lavender` (Lilac & Olive)
- `theme-light-monochrome` (White & Black)

> **Image Protection:** The CSS automatically applies inverse-filters (`hue-rotate(-180deg) invert(1)`) to `<img>` and `<video>` elements, so real-world photos never appear distorted or inverted when applying these global themes.

---
## Quick-Start Checklist for AI Agents
When creating a new slide deck:
- [ ] Copy `template/slides.html` to your new deck folder
- [ ] Utilize any of the **22 pre-built components** located in `template/slides/` (e.g., `01_cover.html`, `10_animated_tech_stack.html`)
- [ ] Update `<title>` in `slides.html`
- [ ] Build each slide as a separate HTML fragment file in `slides/`
- [ ] Add each file to `slideSources` array in `slides.html` in order
- [ ] Set `id="slide-0"` on slide 0, `id="slide-1"` on slide 1, etc.
- [ ] Add `active` class only to the first slide
- [ ] Scope all CSS with `.slide-[unique-name]`
- [ ] Use design tokens (`var(--accent-orange)`, etc.) — never hard-code colors
- [ ] Test by opening `slides.html` via a local server (`python -m http.server`)
- [ ] Export via `python export.py`
