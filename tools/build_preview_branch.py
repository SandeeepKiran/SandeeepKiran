"""Builds the MousyGenshinPreview site: the profile README rendered like GitHub, following the
viewer's light/dark theme, with every image copied next to it (no outside dependencies).

Since 2026-10-17 this is the live portfolio, so on top of the README it adds the site-only extras
GitHub cannot show: the HoYoWiki cursor (plus a matching "clickable" one), element-coloured hover
seals on the contact buttons, and the HoYoWiki firefly backgrounds that change element as you scroll.
Their files live in assets/site/ (see assets/source/README.md for where each came from)."""
import json, pathlib, re, shutil, subprocess, sys

profile, cards, out = (pathlib.Path(a) for a in sys.argv[1:4])
if out.exists():
    shutil.rmtree(out)
out.mkdir(parents=True)

md = (profile / "README.md").read_text(encoding="utf-8")
html = subprocess.run(["gh", "api", "markdown", "--input", "-"], input=json.dumps({"text": md, "mode": "markdown"}),
                      capture_output=True, text=True, encoding="utf-8", check=True).stdout
html = html.replace("https://raw.githubusercontent.com/SandeeepKiran/SandeeepKiran/output/", "cards/")
html = re.sub(r'<a target="_blank"[^>]*>(<img[^>]*>)</a>', r"\1", html)   # GitHub's site does not wrap these
html = html.replace("<p>[!TIP]", '<p class="tip-title">💡 Tip</p><p>')

# Contact buttons -> element, the way HoYoWiki colours a talent by its element.
CONTACT_ELEMENT = {"mailto:": "pyro", "https://t.me/": "cryo", "https://www.linkedin.com/": "hydro",
                   "https://sandeeepkiran.github.io/": "geo", "assets/Sandeep-Kiran-Resume.pdf": "electro"}
for href, element in CONTACT_ELEMENT.items():
    html, n = re.subn(rf'<a href="({re.escape(href)}[^"]*)"', rf'<a class="seal {element}" href="\1"', html, count=1)
    if n != 1:
        sys.exit(f"contact button not found: {href}")

shutil.copytree(cards, out / "cards")
shutil.copytree(profile / "assets", out / "assets")
shutil.rmtree(out / "assets" / "source")   # originals for the repo, not needed by the page
(out / "docs" / "brag-files").mkdir(parents=True)
shutil.copy(profile / "docs" / "brag-files" / "brag-all.gif", out / "docs" / "brag-files" / "brag-all.gif")

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sandeeep's Portfolio</title>
<meta name="description" content="Sandeep Kiran: QA Manager at SoundHound AI. GenAI and conversational voice AI, LLM evaluation, AI agents.">
<link rel="icon" type="image/png" href="assets/site/favicon.png">
<link rel="apple-touch-icon" href="assets/site/apple-touch-icon.png">
<style>
  :root {{ --bg:#ffffff; --text:#1f2328; --muted:#59636e; --line:#d1d9e0; --link:#0969da; --tip:#1a7f37;
           --panel:rgba(255,255,255,.93); }}
  @media (prefers-color-scheme: dark) {{ :root {{ --bg:#0d1117; --text:#f0f6fc; --muted:#9198a1; --line:#3d444d; --link:#4493f8; --tip:#3fb950;
           --panel:rgba(13,17,23,.74); }} }}

  /* HoYoWiki's cursor; it only sets it on <body>, so links fall back to the system hand.
     Here clickable things get a matching lit-up version instead. */
  html {{ cursor:url("assets/site/cursor.png") 0 0, auto; }}
  a, button, summary, label, [role="button"] {{ cursor:url("assets/site/cursor-pointer.png") 4 4, pointer; }}

  body {{ margin:0; background:var(--bg); color:var(--text); font:15px/1.5 -apple-system,"Segoe UI",Helvetica,Arial,sans-serif; }}
  main {{ max-width:880px; margin:32px auto; padding:24px 32px 64px; background:var(--panel); border-radius:16px;
          box-shadow:0 10px 40px rgba(0,0,0,.35); backdrop-filter:blur(3px); }}
  @media (max-width:920px) {{ main {{ margin:0; border-radius:0; padding:24px 16px 64px; }} }}
  img {{ max-width:100%; }}
  a {{ color:var(--link); }}
  h2 {{ border-bottom:1px solid var(--line); padding-bottom:6px; }}
  table {{ border-collapse:collapse; display:block; overflow-x:auto; }}
  td, th {{ border:1px solid var(--line); padding:6px 12px; }}
  blockquote {{ margin:0 0 16px; padding:0 16px; border-left:4px solid var(--tip); }}
  .tip-title {{ color:var(--tip); font-weight:600; margin-bottom:0; }}

  /* Firefly backgrounds: HoYoWiki's own element videos, cross-faded as you scroll. */
  #fireflies {{ position:fixed; inset:0; z-index:-1; background:#0c1626; overflow:hidden; }}
  #fireflies video {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; opacity:0; }}
  #fireflies::after {{ content:""; position:absolute; inset:0; background:radial-gradient(50% 50%, transparent 27%, rgba(0,0,0,.125) 100%); }}

  /* Contact buttons: an element seal pops up behind the button on hover, like a HoYoWiki talent. */
  a.seal {{ position:relative; display:inline-block; margin:6px 5px; isolation:isolate; transition:transform .2s; }}
  a.seal img {{ display:block; }}
  a.seal::before, a.seal::after {{ content:""; position:absolute; z-index:-1; opacity:0; pointer-events:none;
          transition:opacity .25s, transform .35s cubic-bezier(.34,1.56,.64,1); }}
  a.seal::before {{ inset:-6px; border-radius:10px; background:var(--seal-bg); border:2px solid var(--seal); transform:scale(.8); }}
  a.seal::after {{ width:64px; height:64px; left:16px; top:50%; background:var(--seal);
          -webkit-mask:url("assets/site/ring.svg") center/contain no-repeat; mask:url("assets/site/ring.svg") center/contain no-repeat;
          transform:translate(-50%,-50%) scale(.5) rotate(-45deg); }}
  a.seal:hover, a.seal:focus-visible {{ z-index:2; transform:translateY(-2px); }}
  a.seal:hover::before, a.seal:focus-visible::before {{ opacity:1; transform:scale(1); box-shadow:0 0 14px var(--seal); }}
  a.seal:hover::after, a.seal:focus-visible::after {{ opacity:1; transform:translate(-50%,-50%) scale(1) rotate(0); }}
  /* HoYoWiki's own colours: ring = .d-talent-keys-active <element>, panel = .entry-common-module.<element> */
  a.seal.pyro    {{ --seal:rgba(255,102,64,.85);  --seal-bg:rgb(61,24,24); }}
  a.seal.cryo    {{ --seal:rgba(122,242,242,.85); --seal-bg:rgb(9,55,92); }}
  a.seal.hydro   {{ --seal:rgba(0,192,255,.85);   --seal-bg:rgb(21,49,92); }}
  a.seal.geo     {{ --seal:rgba(255,176,13,.85);  --seal-bg:rgb(61,48,21); }}
  a.seal.electro {{ --seal:rgba(204,128,255,.85); --seal-bg:rgb(42,26,103); }}

  @media (prefers-reduced-motion: reduce) {{ a.seal, a.seal::before, a.seal::after {{ transition:none; }} }}
</style>
</head>
<body>
<div id="fireflies" aria-hidden="true"></div>
<main>
{html}
</main>
<script>
// Element order top to bottom follows the Traveler's journey: Mondstadt, Liyue, Inazuma, Sumeru,
// Fontaine, Natlan, Nod-Krai, Snezhnaya, then the Abyss at the very end. Edit this list to reorder.
const ELEMENTS = ["anemo", "geo", "electro", "dendro", "hydro", "pyro", "nodkrai", "cryo", "abyss"];
const still = matchMedia("(prefers-reduced-motion: reduce)").matches;
const box = document.getElementById("fireflies");
const layers = ELEMENTS.map((name, i) => {{
  const v = document.createElement("video");
  Object.assign(v, {{ muted: true, loop: true, playsInline: true, preload: "none", poster: `assets/site/bg/${{name}}.jpg` }});
  v.style.zIndex = i;   // the next element fades in on top of the current one
  v.innerHTML = `<source src="assets/site/bg/${{name}}.webm" type="video/webm"><source src="assets/site/bg/${{name}}.mp4" type="video/mp4">`;
  box.appendChild(v);
  return v;
}});

function update() {{
  const room = document.documentElement.scrollHeight - innerHeight;
  const t = room > 0 ? Math.min(Math.max(scrollY / room, 0), 1) * (ELEMENTS.length - 1) : 0;
  const i = Math.min(Math.floor(t), ELEMENTS.length - 2);
  const f = t - i;
  const blend = Math.min(Math.max((f - 0.35) / 0.3, 0), 1);   // hold each colour, then fade over the middle 30%
  layers.forEach((v, k) => {{
    const o = k === i ? (blend < 1 ? 1 : 0) : k === i + 1 ? blend * blend * (3 - 2 * blend) : 0;   // fully covered = paused
    v.style.opacity = o;
    if (o > 0 && !still) {{ if (v.paused) v.play().catch(() => {{}}); }}
    else if (!v.paused) v.pause();
  }});
}}
addEventListener("scroll", () => requestAnimationFrame(update), {{ passive: true }});
addEventListener("resize", update);
addEventListener("load", update);
update();
</script>
</body>
</html>
"""
(out / "index.html").write_text(page, encoding="utf-8")
print("site built:", sum(1 for _ in out.rglob("*") if _.is_file()), "files")
