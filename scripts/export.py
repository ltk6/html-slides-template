import os
import time
import socket
import threading
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from http.server import SimpleHTTPRequestHandler, HTTPServer
from playwright.sync_api import sync_playwright

ALL_THEMES = [
    "theme-default", "theme-emerald", "theme-cyberpunk", "theme-monochrome", "theme-ruby",
    "theme-light-corporate", "theme-light-warm", "theme-light-mint", "theme-light-lavender", "theme-light-monochrome"
]

def find_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 0))
    port = s.getsockname()[1]
    s.close()
    return port

def export_presentation(selected_themes, deck_dir=None, scale_factor=2):
    """
    Export all slides in a deck to high-resolution PNG images and combine into PDFs.
    """
    if deck_dir:
        cwd = deck_dir
        os.chdir(cwd)
    else:
        cwd = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "presentation"))
        os.chdir(cwd)
        
    out_w, out_h = 1280 * scale_factor, 720 * scale_factor
    print(f"📁 Deck directory: {cwd}")
    print(f"🖼️  Output resolution: {out_w}×{out_h}px (scale factor {scale_factor}x)")

    port = find_free_port()
    print(f"📡 Starting local HTTP server at http://127.0.0.1:{port}...")
    server = HTTPServer(('127.0.0.1', port), SimpleHTTPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    time.sleep(0.5)

    output_dir = os.path.abspath(os.path.join("exported", "slides"))
    os.makedirs(output_dir, exist_ok=True)

    slide_names = _parse_slide_names(os.path.join(cwd, "slides.html"))
    if slide_names:
        print(f"🗂️  Found {len(slide_names)} slide name(s) in slideSources")
    
    url = f"http://127.0.0.1:{port}/slides.html?export"

    try:
        print("🚀 Launching Playwright browser...")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={"width": 1280, "height": 720},
                device_scale_factor=scale_factor
            )
            page = context.new_page()

            print(f"🔗 Loading slides via local server: {url}")
            page.goto(url)
            page.wait_for_selector(".slide", timeout=15000)

            total_slides = page.locator(".slide").count()
            print(f"📊 Detected {total_slides} slides.")

            # FIX: Disable CSS animations & transitions globally so screenshots are never taken mid-frame
            page.evaluate('''() => {
                const style = document.createElement('style');
                style.innerHTML = "body.export-mode .slide { transition: none !important; animation: none !important; }";
                document.head.appendChild(style);
            }''')

            all_exported_pdfs = []

            for theme in selected_themes:
                print(f"\n🎨 Starting export for theme: {theme}")
                page.evaluate(f"applyTheme('{theme}')")
                
                # Allow DOM to apply theme colors
                time.sleep(0.5)

                theme_output_dir = os.path.join(output_dir, theme)
                os.makedirs(theme_output_dir, exist_ok=True)

                exported_files = []
                for i in range(total_slides):
                    # FIX: Jump exactly to the slide index instead of sending 'ArrowRight'
                    page.evaluate(f"if(typeof goToSlide !== 'undefined') goToSlide({i});")
                    
                    slide_num = i + 1
                    if slide_names and i < len(slide_names):
                        filename = f"{slide_names[i]}.png"
                    else:
                        filename = f"Slide_{slide_num:02d}.png"

                    print(f"  📸 Capturing {filename}...")

                    # Wait slightly for DOM paint (much faster now since transitions are disabled)
                    time.sleep(0.3)

                    output_file = os.path.join(theme_output_dir, filename)
                    page.screenshot(path=output_file, type="png")
                    exported_files.append(output_file)

                # Combine PNGs to PDF
                try:
                    from PIL import Image
                    print(f"  📄 Generating presentation_{theme}.pdf...")
                    images = [Image.open(f).convert('RGB') for f in exported_files]
                    if images:
                        pdf_dir = os.path.abspath(os.path.join("exported", "pdfs"))
                        os.makedirs(pdf_dir, exist_ok=True)
                        pdf_path = os.path.join(pdf_dir, f"presentation_{theme}.pdf")
                        images[0].save(pdf_path, save_all=True, append_images=images[1:], resolution=100.0)
                        all_exported_pdfs.append(pdf_path)
                        print(f"  ✅ Saved: {pdf_path}")
                except ImportError:
                    print("⚠️  Pillow library not found. Skipping PDF generation.")
            
            browser.close()
            print(f"\n🎉 Done! Generated {len(all_exported_pdfs)} PDFs successfully.")

    finally:
        print("🔌 Shutting down local HTTP server...")
        server.shutdown()
        server.server_close()
        print("✅ Server stopped.")

def _parse_slide_names(slides_html_path: str) -> list[str]:
    import re
    try:
        with open(slides_html_path, encoding="utf-8") as f:
            source = f.read()
    except FileNotFoundError:
        return []
    match = re.search(r'const\s+slideSources\s*=\s*\[(.+?)\]', source, re.DOTALL)
    if not match: return []
    array_body = re.sub(r'//[^\n]*', '', match.group(1))
    entries = re.findall(r'[\'"]([^\'"]+)[\'"]', array_body)
    return [os.path.splitext(os.path.basename(e))[0] for e in entries]

def run_gui(deck_dir, scale):
    root = tk.Tk()
    root.title("Presentation Exporter")
    root.geometry("450x500")
    root.configure(bg="#0A1128")

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TCheckbutton", background="#0A1128", foreground="#FFFFFF", font=("Arial", 11))

    title = tk.Label(root, text="Select Themes to Export", font=("Arial", 16, "bold"), bg="#0A1128", fg="#FFFFFF")
    title.pack(pady=20)

    vars_dict = {}
    frame = tk.Frame(root, bg="#0A1128")
    frame.pack(fill="both", expand=True, padx=40)

    for theme in ALL_THEMES:
        var = tk.BooleanVar(value=False)
        # Default to checking just the first theme
        if theme == "theme-default":
            var.set(True)
        
        display_name = theme.replace("theme-", "").replace("-", " ").title()
        chk = ttk.Checkbutton(frame, text=display_name, variable=var, style="TCheckbutton")
        chk.pack(anchor="w", pady=4)
        vars_dict[theme] = var

    def start_export():
        selected = [t for t, v in vars_dict.items() if v.get()]
        if not selected:
            messagebox.showwarning("No Selection", "Please select at least one theme.")
            return
        root.destroy()
        export_presentation(selected, deck_dir, scale)

    btn = tk.Button(root, text="🚀 Export Selected Themes", command=start_export, 
                    bg="#FF6B35", fg="#FFFFFF", font=("Arial", 12, "bold"), 
                    activebackground="#CA3600", activeforeground="#FFFFFF", 
                    borderwidth=0, padx=20, pady=10, cursor="hand2")
    btn.pack(pady=30)

    root.mainloop()

if __name__ == "__main__":
    deck_dir_arg = sys.argv[1] if len(sys.argv) > 1 else None
    scale_arg = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    
    # Launch GUI
    run_gui(deck_dir_arg, scale_arg)
