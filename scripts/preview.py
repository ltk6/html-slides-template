import os
import time
import socket
import threading
import sys
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

def export_previews(deck_dir=None, scale_factor=2):
    """
    Export only the FIRST slide of all 10 themes for quick previewing.
    """
    if deck_dir:
        cwd = deck_dir
        os.chdir(cwd)
    else:
        cwd = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "presentation"))
        os.chdir(cwd)
    out_w, out_h = 1280 * scale_factor, 720 * scale_factor
    print(f"📁 Deck directory: {cwd}")
    print(f"🖼️  Preview resolution: {out_w}×{out_h}px (scale factor {scale_factor}x)")

    port = find_free_port()
    print(f"📡 Starting local HTTP server at http://127.0.0.1:{port}...")
    server = HTTPServer(('127.0.0.1', port), SimpleHTTPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    time.sleep(0.5)

    output_dir = os.path.abspath(os.path.join("exported", "previews"))
    os.makedirs(output_dir, exist_ok=True)
    
    url = f"http://127.0.0.1:{port}/slides.html?export"

    try:
        print("🚀 Launching Playwright browser for quick previews...")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={"width": 1280, "height": 720},
                device_scale_factor=scale_factor
            )
            page = context.new_page()

            page.goto(url)
            page.wait_for_selector(".slide", timeout=15000)

            # Disable CSS animations & transitions globally
            page.evaluate('''() => {
                const style = document.createElement('style');
                style.innerHTML = "body.export-mode .slide { transition: none !important; animation: none !important; }";
                document.head.appendChild(style);
            }''')

            for theme in ALL_THEMES:
                print(f"  📸 Capturing preview for: {theme}...")
                page.evaluate(f"applyTheme('{theme}')")
                
                # Allow DOM to apply theme colors
                time.sleep(0.5)

                # Capture the 2nd slide (index 1)
                slide_idx = 1
                page.evaluate(f"if(typeof goToSlide !== 'undefined') goToSlide({slide_idx});")
                time.sleep(0.3)
                
                output_file = os.path.join(output_dir, f"preview_{theme}.png")
                page.screenshot(path=output_file, type="png")

            browser.close()
            print(f"\n🎉 Done! Generated 10 preview images in: {output_dir}")

    finally:
        server.shutdown()
        server.server_close()

if __name__ == "__main__":
    deck_dir_arg = sys.argv[1] if len(sys.argv) > 1 else None
    scale_arg = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    
    export_previews(deck_dir_arg, scale_arg)
