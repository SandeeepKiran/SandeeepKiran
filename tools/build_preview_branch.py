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
shutil.copytree(profile / "assets", out / "assets")   # includes assets/source: Sandeep keeps every original image here too
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
  #fireflies video {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; opacity:0; transition:opacity 1.6s ease-in-out; }}
  #fireflies::after {{ content:""; position:absolute; inset:0; background:radial-gradient(50% 50%, transparent 27%, rgba(0,0,0,.125) 100%); z-index:100000; }}

  /* Fireflies switched off: the plain page from before (GitHub's own background, no panel). */
  html.no-fireflies #fireflies {{ display:none; }}
  html.no-fireflies main {{ margin:0 auto; background:none; box-shadow:none; backdrop-filter:none; border-radius:0; }}

  /* The on/off switch, top right. */
  #fx-toggle {{ position:fixed; top:12px; right:12px; z-index:10; display:flex; align-items:center; gap:8px;
          padding:6px 12px 6px 8px; border-radius:999px; border:1px solid rgba(153,246,228,.45);
          background:rgba(13,17,23,.72); color:#d5ece8; font:600 12px/1 "Segoe UI",system-ui,sans-serif; letter-spacing:.04em;
          backdrop-filter:blur(6px); box-shadow:0 4px 14px rgba(0,0,0,.35); }}
  #fx-toggle .knob {{ width:26px; height:14px; border-radius:999px; background:rgba(255,255,255,.18); position:relative; transition:background .25s; }}
  #fx-toggle .knob::after {{ content:""; position:absolute; top:2px; left:2px; width:10px; height:10px; border-radius:50%;
          background:#a7d3cc; transition:transform .25s, background .25s; }}
  #fx-toggle[aria-pressed="true"] .knob {{ background:rgba(51,215,160,.55); }}
  #fx-toggle[aria-pressed="true"] .knob::after {{ transform:translateX(12px); background:#fff; box-shadow:0 0 8px #99f6e4; }}
  #fx-toggle:hover {{ border-color:#99f6e4; }}

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

  @media (prefers-reduced-motion: reduce) {{ a.seal, a.seal::before, a.seal::after, #fireflies video {{ transition:none; }} }}
</style>
</head>
<body>
<div id="fireflies" aria-hidden="true"></div>
<button id="fx-toggle" type="button" aria-pressed="true" title="Turn the firefly background on or off"><span class="knob"></span><span class="label">Fireflies</span></button>
<main>
{html}
</main>
<script>
// The page is cut into equal scroll segments, one element each. Anemo (Mondstadt, the profile's
// theme) is always first; the other eight come in a new random order on every visit.
const OTHERS = ["geo", "electro", "dendro", "hydro", "pyro", "nodkrai", "cryo", "abyss"];
for (let i = OTHERS.length - 1; i > 0; i--) {{ const j = Math.floor(Math.random() * (i + 1)); [OTHERS[i], OTHERS[j]] = [OTHERS[j], OTHERS[i]]; }}
const ELEMENTS = ["anemo", ...OTHERS];
const FADE_MS = 1600;   // matches the CSS opacity transition on #fireflies video

const still = matchMedia("(prefers-reduced-motion: reduce)").matches;
const root = document.documentElement;
const box = document.getElementById("fireflies");
const toggle = document.getElementById("fx-toggle");
const layers = ELEMENTS.map(name => {{
  const v = document.createElement("video");
  Object.assign(v, {{ muted: true, loop: true, playsInline: true, preload: "none", poster: `assets/site/bg/${{name}}.jpg` }});
  v.innerHTML = `<source src="assets/site/bg/${{name}}.webm" type="video/webm"><source src="assets/site/bg/${{name}}.mp4" type="video/mp4">`;
  box.appendChild(v);
  return v;
}});

let on = true, current = -1, topZ = 0, tidy;
try {{ on = localStorage.getItem("fireflies") !== "off"; }} catch (e) {{}}

function segment() {{
  const room = root.scrollHeight - innerHeight;
  const p = room > 0 ? Math.min(Math.max(scrollY / room, 0), 1) : 0;
  return Math.min(Math.floor(p * ELEMENTS.length), ELEMENTS.length - 1);
}}

// Cross-fade in time, not with the scroll position: the new element fades in over the old one,
// so a fast scroll still gets the full smooth fade and each element stays its own distinct colour.
function show(i, instant) {{
  if (i === current) return;
  const v = layers[i];
  if (instant) v.style.transition = "none";
  v.style.zIndex = ++topZ;
  v.style.opacity = 1;
  if (instant) {{ v.offsetHeight; v.style.transition = ""; }}
  if (!still) v.play().catch(() => {{}});
  for (const k of [i - 1, i + 1]) if (layers[k]) layers[k].preload = "auto";   // neighbours ready before they are needed
  current = i;
  clearTimeout(tidy);
  tidy = setTimeout(() => layers.forEach((l, k) => {{
    if (k === current) return;
    l.style.transition = "none"; l.style.opacity = 0; l.offsetHeight; l.style.transition = "";
    l.pause();
  }}), instant ? 0 : FADE_MS + 100);
}}

function update() {{ if (on) show(segment(), current === -1); }}

function setOn(value) {{
  on = value;
  root.classList.toggle("no-fireflies", !on);
  toggle.setAttribute("aria-pressed", on);
  try {{ localStorage.setItem("fireflies", on ? "on" : "off"); }} catch (e) {{}}
  if (on) {{ current = -1; update(); }}
  else layers.forEach(l => l.pause());
}}

toggle.addEventListener("click", () => setOn(!on));
addEventListener("scroll", () => requestAnimationFrame(update), {{ passive: true }});
addEventListener("resize", update);
setOn(on);
</script>
</body>
</html>
"""
(out / "index.html").write_text(page, encoding="utf-8")
print("site built:", sum(1 for _ in out.rglob("*") if _.is_file()), "files")
