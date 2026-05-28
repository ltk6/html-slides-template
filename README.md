# HTML Slides Template

A **premium HTML presentation engine** — 1280×720 (16:9), built with vanilla HTML/CSS/JS, no dependencies. Features **10 dynamic color themes**, **22 reusable slide templates**, and a powerful Python exporter that generates high-resolution 2K PNGs and PDFs for every theme with one command.

---

## Repository Structure

```
html-slides-template/
│
├── README.md                        ← You are here
├── presentation/                    ← START HERE: Your active slide deck workspace
│   ├── README.md
│   ├── slides.html                  ← Presentation engine
│   └── slides/                      ← Your slide files go here
│
├── template/                        ← Reference gallery of 22+ premium slide layouts
│   ├── README.md
│   ├── slides.html                  ← Preview all templates
│   ├── SLIDE_GUIDE.md               ← Full component & design system reference
│   └── slides/                      ← The raw template files
│
├── scripts/                         ← Automation & export tools
│   ├── README.md
│   ├── export.py                    ← Multi-PDF/PNG export tool
│   ├── preview.py                   ← Headless script to quickly export previews
│   └── export_cover.py              ← Targeted single-slide export
│
└── examples/
    ├── README.md
    └── travel-exp-planner/          ← Full example deck
```

---

## Quick Start — New Deck

### 1. Open your workspace

```bash
cd presentation/
```

### 2. Run a local server

**Option A — VS Code**: Install the [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) extension, then click **Go Live** in the status bar.

**Option B — Python**:
```bash
python -m http.server 8080
# Then open http://localhost:8080/slides.html
```

> ⚠️ You **must** use a local server. Opening `slides.html` directly via `file://` causes a CORS error that blocks slide loading.

### 3. Create slides

1. Create slide files in `presentation/slides/` (use `02_blank.html` as a starting point)
2. Register them in `presentation/slides.html`'s `slideSources` array (in order)
3. See **`template/SLIDE_GUIDE.md`** or open `template/slides.html` for the full component reference

### 4. Navigate

| Key | Action |
|---|---|
| `→` / `Space` / `Enter` | Next slide |
| `←` / `PageUp` | Previous slide |
| `F` | Toggle fullscreen |
| Touch swipe | Navigate on mobile |

## 🎨 Global Theme Engine

The presentation engine includes a real-time, GPU-accelerated Theme Picker (floating in the bottom right corner). It supports **10 premium color schemes** (5 Dark Modes, 5 Light Modes). 

The engine uses CSS `hue-rotate` and `invert` matrix math to instantly swap palettes without modifying your code, and includes an intelligent *Anti-Filter* to protect your `<img>` and `<video>` tags from distortion in Light Mode. Your selected theme is saved to `localStorage`.

---

## Export to PDF & PNG

Exports every slide as a **2K (2560×1440) PNG** image, and automatically stitches them into **PDFs**. 

Because of the new Theme Engine, the script features a **Desktop GUI** that lets you choose exactly which color schemes you want to export.

```bash
# Install once
pip install playwright pillow
playwright install chromium

# 1. Full Export (GUI) - Select themes and generate full PDFs
python scripts/export.py

# 2. Quick Preview - Captures the 2nd slide across all 10 themes in the background
python scripts/preview.py
```

Full exports are saved to organized subfolders like `presentation/exported/slides/theme-emerald/Slide_01.png`, and PDFs are generated as `presentation_theme-emerald.pdf`. Quick previews are saved to `presentation/exported/previews/`.

---

## For AI Agents — Creating a New Deck

**Read `template/SLIDE_GUIDE.md` first.** It contains everything you need:

- All CSS design tokens (colors, fonts, spacing)
- Every reusable component with copy-paste HTML+CSS snippets
- Layout patterns (2-col, 3-col, tier rows, timelines, flow arrows)
- Slide file anatomy and naming rules
- Step-by-step creation checklist

### The short version

1. Each slide = one `.html` fragment file in `slides/`
2. Each slide has a scoped `<style>` block (prefix every rule with `.slide-[name]`)
3. Register files in `slides.html`'s `slideSources` array
4. Use CSS variables from the design system — never hard-code colors
5. The canvas is always **1280 × 720 px** — design for this exact size

See the `examples/travel-exp-planner/` deck for real-world usage of every pattern.

---

## Design System Overview

| Token | Value | Use |
|---|---|---|
| `--accent-orange` | `#FF6B35` | Primary accent — titles, icons, highlights |
| `--bg-dark-blue` | `#0A1128` | Slide background |
| `--card-blue` | `#14213D` | Card backgrounds |
| `--text-white` | `#FFFFFF` | Primary text |
| `--text-dim` | `#F1F5F9` | Secondary / dimmed text |
| `--badge-green` | `#10B981` | Success badges |
| Font | `Public Sans` | 400 / 500 / 600 / 700 / 800 |

---

## Tech Stack

- **HTML5** — semantic structure
- **Vanilla CSS** — scoped per-slide with CSS custom properties
- **Vanilla JS** — presentation engine (auto-scaler, keyboard nav, touch swipe, fullscreen)
- **FontAwesome 6** — icons via CDN
- **Playwright** — headless Chromium for PNG export
- No build step, no framework, no bundler