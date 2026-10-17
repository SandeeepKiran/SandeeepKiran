"""Renders the Tip card and the More-about-me card as crisp 2x PNGs for the profile README."""
import base64, pathlib, sys
from PIL import Image
from playwright.sync_api import sync_playwright

s = pathlib.Path(sys.argv[1])
out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
v = s / "venti"


def uri(path):
    return "data:image/png;base64," + base64.b64encode(pathlib.Path(path).read_bytes()).decode()


# Anemo element icon in its own teal, as the wiki shows it next to the name.
anemo = Image.open(v / "v13.png").convert("RGBA")
px = anemo.load()
for y in range(anemo.height):
    for x in range(anemo.width):
        r, g, b, a = px[x, y]
        lum = (0.3 * r + 0.59 * g + 0.11 * b) / 255
        px[x, y] = (int(116 * (0.6 + 0.4 * lum)), int(194 * (0.6 + 0.4 * lum)), int(168 * (0.6 + 0.4 * lum)), a)
anemo.save(s / "anemo-teal.png")

tip = f"""<!doctype html><html><head><meta charset="utf-8"><style>
body {{ margin:0; width:1000px; height:310px; font-family:'Segoe UI',sans-serif; }}
.wrap {{ position:relative; width:100%; height:100%; box-sizing:border-box; padding:22px 30px; display:flex; gap:30px;
  background: url('{uri(s / "round4" / "entry_bg.png")}') center top / cover no-repeat, #3a4256; border-radius:18px; overflow:hidden; }}
.card {{ height:262px; border-radius:12px; border:3px solid #e6d8b8; box-shadow:0 8px 24px rgba(0,0,0,.35); }}
h1 {{ margin:6px 0 10px; font-family:Georgia,'Times New Roman',serif; font-size:46px; color:#f2ede4; display:flex; align-items:center; gap:12px; }}
h1 img {{ width:38px; }}
.tags {{ display:flex; flex-wrap:wrap; gap:8px; margin-bottom:14px; }}
.tags span {{ background:#232733; color:#ecdcb8; padding:5px 12px; border-radius:7px; font-size:16px; }}
.who {{ color:#fff; font-size:17px; margin-bottom:4px; }}
p {{ margin:0; color:#cfd3db; font-size:16px; line-height:1.5; }}
</style></head><body><div class="wrap">
<img class="card" src="{uri(v / 'v10.png')}">
<div><h1>Venti <img src="{uri(s / 'anemo-teal.png')}"></h1>
<div class="tags"><span>Anemo</span><span>Character Invitations</span><span>Bow</span><span>Summon</span><span>Mondstadt</span></div>
<div class="who">"Windborne Bard" Venti</div>
<p>As the four seasons in turn shall say their piece, so the four winds too shall never cease.<br>
Of course, to look at it differently, I am the one who should be credited here, and not they.<br>
Credits should be given where credits belong — if not for the bard who pens the song, then who shall ensure that these tales are passed on!?</p>
</div></div></body></html>"""

about = f"""<!doctype html><html><head><meta charset="utf-8"><style>
body {{ margin:0; width:1000px; height:380px; font-family:'Segoe UI',sans-serif; }}
.wrap {{ position:relative; width:100%; height:100%; border-radius:18px; overflow:hidden; }}
.bg {{ position:absolute; inset:-40px; background:url('{uri(v / 'v21.png')}') center/cover; filter:blur(10px) saturate(1.1); }}
.shade {{ position:absolute; inset:0; background:linear-gradient(90deg, rgba(8,40,48,.86) 0%, rgba(8,40,48,.72) 62%, rgba(8,40,48,.25) 100%); }}
.card {{ position:absolute; right:34px; top:22px; height:336px; border-radius:12px; box-shadow:0 10px 30px rgba(0,0,0,.45); }}
.text {{ position:absolute; left:40px; top:30px; width:690px; color:#e6f4f0; }}
h2 {{ margin:0 0 6px; font-size:24px; color:#fff; }}
.gold {{ color:#f1d58c; }}
ul {{ margin:6px 0 18px; padding-left:22px; font-size:18px; line-height:1.55; }}
.row {{ font-size:18px; margin:4px 0; }}
.note {{ position:absolute; left:40px; bottom:22px; font-size:14px; color:#a9cfc8; }}
</style></head><body><div class="wrap"><div class="bg"></div><div class="shade"></div>
<img class="card" src="{uri(v / 'v21.png')}">
<div class="text">
<h2>XDA Developers <span class="gold">· Senior Contributor (2019–2023)</span></h2>
<ul><li>Reported 400+ bugs in Android custom ROMs.</li><li>Helped 20+ developers run their communities.</li>
<li>Wrote a beginner's guide to custom ROMs for the Redmi K20 Pro.</li></ul>
<div class="row"><b class="gold">Research</b> · A Comparative Study on Parsing in Natural Language Processing (IEEE Xplore, 2019)</div>
<div class="row"><b class="gold">Portfolio</b> · sandeeepkiran.github.io</div>
</div>
<div class="note">Older repos below are from college (2018–2021). I've kept them as a record of where I started.</div>
</div></body></html>"""

with sync_playwright() as p:
    b = p.chromium.launch()
    for name, html, h in (("tip-card", tip, 310), ("about-card", about, 380)):
        f = s / f"{name}.html"
        f.write_text(html, encoding="utf-8")
        pg = b.new_page(viewport={"width": 1000, "height": h}, device_scale_factor=2)
        pg.goto(f.as_uri())
        pg.wait_for_timeout(800)
        pg.screenshot(path=str(out / f"{name}.png"), omit_background=True)
        pg.close()
    b.close()
print("panels ok")
