"""Record brag.html frame by frame.

Usage:
  python capture.py stills <out-dir> t1 t2 ...   # single frames at the given seconds
  python capture.py frames <out-dir> [fps]        # every frame of the video (default 30 fps)

The page is served over a local HTTP server, so the SVG iframes can be controlled from the page.
"""
import functools
import http.server
import pathlib
import sys
import threading

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
END = 23.4


def serve():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass  # Keep the console clean during capture.

    handler = functools.partial(Quiet, directory=str(HERE))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def main():
    mode, out = sys.argv[1], pathlib.Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    server = serve()
    url = f"http://127.0.0.1:{server.server_address[1]}/brag.html"
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page(viewport={"width": 1920, "height": 1080})
            page.goto(url)
            page.evaluate("window.ready")
            if mode == "stills":
                for s in sys.argv[3:]:
                    page.evaluate(f"window.renderAt({float(s)})")
                    page.screenshot(path=str(out / f"still_{float(s):05.2f}.png"))
            else:
                fps = int(sys.argv[3]) if len(sys.argv) > 3 else 30
                n = round(END * fps)
                for i in range(n):
                    page.evaluate(f"window.renderAt({i / fps})")
                    page.screenshot(path=str(out / f"f{i:05d}.png"))
                    if i % 60 == 0:
                        print(f"frame {i}/{n}", flush=True)
        finally:
            browser.close()
            server.shutdown()


if __name__ == "__main__":
    main()
