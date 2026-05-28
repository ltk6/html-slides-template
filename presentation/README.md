# Presentation Workspace

This folder is your active sandbox for creating slide decks!

1. Edit **`slides.html`** to manage the order of your slides in the `slideSources` array.
2. Add your individual slide templates to the **`slides/`** folder.
3. Start a local server (e.g. `python -m http.server 8080`) to view them, or use VS Code Live Server.

## Exporting

When you're ready to export, run the export script from the root repository:

```bash
cd ..
python scripts/export.py
```

Outputs will be saved in `presentation/exported/`.
