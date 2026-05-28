# Scripts

This folder contains Python tools used to automate tasks in the presentation repository.

- **`export.py`**: A GUI-based exporter that launches a headless Chromium browser using Playwright to capture every slide as a 2K PNG across any selected themes, stitching them into full PDF documents.
- **`preview.py`**: A fast, background script that captures a specific slide (e.g., the title card) across all 10 themes and saves them to the `exported/previews/` folder.
- **`export_cover.py`**: A targeted script for exporting just the 00_title.html slide.
- **`upgrade_engine.py`**: Sync utility to automatically update HTML manifests.

**Usage:**

Run these scripts from the repository root:

```bash
python scripts/export.py
```
