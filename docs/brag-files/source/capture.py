"""Captures brag.html frame by frame.

    python capture.py stills <out-dir> t1 t2 ...      -> PNG stills at chosen times
    python capture.py frames <out-dir> <fps>          -> every frame of the full timeline
"""
import pathlib, sys
from playwright.sync_api import sync_playwright

here = pathlib.Path(__file__).resolve().parent
mode, out = sys.argv[1], pathlib.Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 720})
    page.goto((here / "brag.html").as_uri())
    page.evaluate("document.fonts.ready")
    page.wait_for_function("Array.from(document.images).every(i => i.complete && i.naturalWidth > 0)")
    if mode == "stills":
        for t in sys.argv[3:]:
            page.evaluate(f"render({t})")
            page.screenshot(path=str(out / f"still_{float(t):05.2f}.png"))
    else:
        fps = int(sys.argv[3])
        total = page.evaluate("TOTAL")
        for n in range(int(total * fps)):
            page.evaluate(f"render({n / fps})")
            page.screenshot(path=str(out / f"f{n:05d}.png"))
    browser.close()
print("done")
