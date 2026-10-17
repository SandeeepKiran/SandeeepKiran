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

# Toggle artwork pieces (left, top, size in px inside the 52x24 track).
STAR = ('<svg class="star" style="left:{0}px;top:{1}px;width:{2}px;height:{2}px" viewBox="0 0 24 24">'
        '<path fill="{3}" d="M12 1.8l2.9 6.4 7 .7-5.3 4.7 1.5 6.9L12 16.9l-6.1 3.6 1.5-6.9L2.1 8.9l7-.7z"/></svg>')
STAR_SPOTS = [(5, 4, 4), (11, 12, 8), (20, 4, 5), (27, 14, 4), (25, 2, 3), (3, 15, 3)]
def stars(colour):
    return '<span class="stars">' + "".join(STAR.format(x, y, s, colour) for x, y, s in STAR_SPOTS) + "</span>"
CLOUD = ('<svg class="cloud" style="left:{0}px;top:{1}px;width:{2}px" viewBox="0 0 20 12">'
         '<path fill="url(#cloudfill)" d="M5 12h11a4 4 0 0 0 .6-7.95A5 5 0 0 0 7.2 3.2 3.8 3.8 0 0 0 5 12z"/></svg>')
CLOUDS = "".join(CLOUD.format(x, y, w) for x, y, w in [(25, 4, 12), (37, 2, 9), (32, 11, 14)])
SUN = ('<svg class="sun" viewBox="0 0 18 18"><defs>'
       '<linearGradient id="sunfill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f8be3d"/><stop offset="1" stop-color="#f3a35a"/></linearGradient>'
       '<linearGradient id="sunrim" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f2654a"/><stop offset="1" stop-color="#f6b366"/></linearGradient>'
       '<linearGradient id="cloudfill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#d4e6fb"/></linearGradient>'
       '<clipPath id="suninner"><circle cx="9" cy="9" r="7.4"/></clipPath></defs>'
       '<circle cx="9" cy="9" r="8.2" fill="url(#sunfill)" stroke="url(#sunrim)" stroke-width="1.6"/>'
       '<path clip-path="url(#suninner)" fill="#fff" opacity=".18" d="M0 8.6c2.6-1.9 5.2-1.1 7.3.2s4.7 2.1 10.7-.4V18H0z"/></svg>')
MOON = '<span class="moon"><i style="left:12px;top:4px;width:3px;height:3px"></i><i style="left:13.5px;top:10px;width:2.4px;height:2.4px"></i><i style="left:10px;top:13px;width:2px;height:2px"></i></span>'
THEME_TRACK = f'<span class="track sky" aria-hidden="true"><span class="dusk"></span>{CLOUDS}{stars("#cfc8ff")}<span class="knob">{SUN}{MOON}</span></span>'
MAPLE_PATH = ("M12 1.5L13.6 5.1 15.8 4 15.2 8.4 18.5 5.8 19.4 8 22 7.5 20.6 11.5 22.3 12.5 16.8 16.7 17.4 18.9 12.6 18 "
              "12.6 22.5 11.4 22.5 11.4 18 6.6 18.9 7.2 16.7 1.7 12.5 3.4 11.5 2 7.5 4.6 8 5.5 5.8 8.8 8.4 8.2 4 10.4 5.1Z")
MAPLE_KNOB = ('<svg class="maple" viewBox="0 0 24 24"><defs><linearGradient id="maplefill" x1="0" y1="0" x2="0" y2="1">'
              '<stop offset="0" stop-color="#ec5a2e"/><stop offset="1" stop-color="#a9261b"/></linearGradient></defs>'
              f'<path fill="url(#maplefill)" d="{MAPLE_PATH}"/>'
              '<path d="M12 18V7M12 13l4-3.5M12 13L8 9.5" stroke="#8f2a17" stroke-width=".7" stroke-linecap="round" fill="none" opacity=".5"/></svg>')
FALLING = ('<svg class="fall" style="left:{0}px;top:{1}px;width:{2}px;height:{2}px" viewBox="0 0 24 24">'
           f'<path fill="{{3}}" d="{MAPLE_PATH}"/></svg>')
LEAVES = '<span class="leaves">' + "".join(FALLING.format(x, y, s, c) for x, y, s, c in
                                           [(27, 4, 7, "#ffd27a"), (37, 12, 8, "#fbe3b0"), (44, 3, 6, "#ffc15c")]) + "</span>"
FX_TRACK = f'<span class="track glow" aria-hidden="true">{LEAVES}{stars("#effffa")}<span class="knob">{MAPLE_KNOB}</span></span>'

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sandeeep's Portfolio</title>
<meta name="description" content="Sandeep Kiran: QA Manager at SoundHound AI. GenAI and conversational voice AI, LLM evaluation, AI agents.">
<link rel="icon" type="image/png" href="assets/site/favicon.png">
<link rel="apple-touch-icon" href="assets/site/apple-touch-icon.png">
<script>  // apply a saved Light/Dark choice before the page paints, so a refresh never flashes the other theme
  try {{ const t = localStorage.getItem("theme"); if (t === "light" || t === "dark") document.documentElement.dataset.theme = t; }} catch (e) {{}}
</script>
<style>
  /* Light = a soft warm cream (pure white was too harsh); dark = GitHub's near-black.
     The theme follows the system unless the Light/Dark switch picked one (html[data-theme]). */
  :root {{ --bg:#f6f0e4; --text:#2b2722; --muted:#6b6255; --line:#e2d8c5; --link:#0b63c7; --tip:#1a7f37;
           --panel:rgba(246,240,228,.93); color-scheme:light; }}
  @media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg:#0d1117; --text:#f0f6fc; --muted:#9198a1; --line:#3d444d;
           --link:#4493f8; --tip:#3fb950; --panel:rgba(13,17,23,.74); color-scheme:dark; }} }}
  :root[data-theme="dark"] {{ --bg:#0d1117; --text:#f0f6fc; --muted:#9198a1; --line:#3d444d;
           --link:#4493f8; --tip:#3fb950; --panel:rgba(13,17,23,.74); color-scheme:dark; }}

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

  /* Fireflies switched off: the card stays exactly where it is (no layout jump); only the colours
     change, so the page and the card share one solid background. The shadow stays. */
  html.no-fireflies #fireflies {{ display:none; }}
  html.no-fireflies main {{ background:var(--bg); backdrop-filter:none; }}

  /* The secret switches, top right: invisible until the corner is hovered (or focused by keyboard). */
  #switches {{ position:fixed; top:0; right:0; z-index:10; display:flex; gap:8px; padding:12px;
          opacity:0; transition:opacity .45s ease; }}
  #switches:hover, #switches:focus-within, #switches.intro {{ opacity:1; }}   /* .intro: shown for a few seconds on load */
  .pill {{ display:flex; align-items:center; gap:8px; padding:6px 12px 6px 8px; border-radius:999px;
          border:1px solid rgba(153,246,228,.45); background:rgba(13,17,23,.72); color:#d5ece8;
          font:600 12px/1 "Segoe UI",system-ui,sans-serif; letter-spacing:.04em;
          backdrop-filter:blur(6px); box-shadow:0 4px 14px rgba(0,0,0,.35); }}
  .pill:hover {{ border-color:#99f6e4; }}

  /* Toggle artwork, drawn in CSS/SVG: a little sky in a track. */
  .track {{ position:relative; flex:none; width:52px; height:24px; border-radius:999px; overflow:hidden;
          box-shadow:inset 0 1px 3px rgba(0,0,0,.35); transition:background .45s, box-shadow .45s; }}
  .track > * {{ position:absolute; }}
  .knob {{ top:3px; left:3px; width:18px; height:18px; border-radius:50%;
          transition:transform .55s cubic-bezier(.65,-.25,.35,1.25), box-shadow .45s, background .45s; }}
  .pill[aria-pressed="true"] .knob {{ transform:translateX(28px); }}
  .stars {{ inset:0; }}
  .star {{ position:absolute; opacity:0; transform:scale(.2); transition:opacity .3s, transform .45s cubic-bezier(.34,1.56,.64,1); }}
  .pill[aria-pressed="true"] .star {{ opacity:1; transform:scale(1); animation:twinkle 2.6s ease-in-out infinite; }}
  .pill[aria-pressed="true"] .star:nth-child(1) {{ transition-delay:.25s; animation-delay:.9s; }}
  .pill[aria-pressed="true"] .star:nth-child(2) {{ transition-delay:.31s; animation-delay:1.7s; }}
  .pill[aria-pressed="true"] .star:nth-child(3) {{ transition-delay:.37s; animation-delay:1.2s; }}
  .pill[aria-pressed="true"] .star:nth-child(4) {{ transition-delay:.43s; animation-delay:2.1s; }}
  .pill[aria-pressed="true"] .star:nth-child(5) {{ transition-delay:.49s; animation-delay:1.4s; }}
  .pill[aria-pressed="true"] .star:nth-child(6) {{ transition-delay:.55s; animation-delay:.6s; }}
  @keyframes twinkle {{ 50% {{ opacity:.45; transform:scale(.75); }} }}

  /* Light/Dark: day sky + sun on the left, night sky + half moon on the right. */
  .sky {{ background:linear-gradient(180deg,#3b82f6,#93d5ef); }}
  .sky::before {{ content:""; position:absolute; inset:0; background:linear-gradient(180deg,#4c12f2,#5d60f3); opacity:0; transition:opacity .6s; }}
  #theme-toggle[aria-pressed="true"] .sky::before {{ opacity:1; }}
  #theme-toggle[aria-pressed="true"] .sky {{ box-shadow:inset 0 1px 3px rgba(0,0,0,.35), 0 0 10px rgba(93,96,243,.55); }}
  .dusk {{ inset:0; background:linear-gradient(180deg,#9c6fc0,#d89ca8); opacity:0; }}
  .switching .dusk {{ animation:dusk .7s ease; }}
  @keyframes dusk {{ 45% {{ opacity:.85; }} }}
  .cloud {{ transition:transform .5s cubic-bezier(.5,0,.3,1), opacity .4s; }}
  .cloud:nth-child(2) {{ transition-delay:.05s; }} .cloud:nth-child(3) {{ transition-delay:.1s; }}
  #theme-toggle[aria-pressed="true"] .cloud {{ transform:translateY(16px); opacity:0; }}
  .sky .knob {{ box-shadow:0 0 8px rgba(255,170,60,.75); }}
  #theme-toggle[aria-pressed="true"] .sky .knob {{ box-shadow:0 0 9px rgba(205,220,255,.8); }}
  .sun {{ position:absolute; inset:0; width:100%; height:100%; transition:opacity .35s, transform .55s; }}
  #theme-toggle[aria-pressed="true"] .sun {{ opacity:0; transform:rotate(90deg) scale(.6); }}
  /* The ")" half moon: a pale disc with a hidden shadow circle that slides in from the left. */
  .moon {{ position:absolute; inset:0; border-radius:50%; opacity:0;
          background:radial-gradient(circle at 70% 35%, #f6f9ff, #cbdaf4 75%);
          -webkit-mask:radial-gradient(circle at center, transparent 8px, #000 8.5px) -54px -32.5px / 80px 80px no-repeat;
          mask:radial-gradient(circle at center, transparent 8px, #000 8.5px) -54px -32.5px / 80px 80px no-repeat;
          transition:opacity .3s .1s, -webkit-mask-position .6s .15s, mask-position .6s .15s; }}
  #theme-toggle[aria-pressed="true"] .moon {{ opacity:1; -webkit-mask-position:-36.5px -32.5px; mask-position:-36.5px -32.5px; }}
  .moon i {{ position:absolute; border-radius:50%; background:rgba(150,170,215,.45); }}

  /* Fireflies on: green fill, mini stars and a glowing white orb.
     Fireflies off: autumn — an amber-to-rust sky, swaying maple leaves and a maple-leaf knob. */
  .glow {{ background:rgba(51,215,160,.55); }}
  .glow::before {{ content:""; position:absolute; inset:0; background:linear-gradient(180deg,#f4bd5c,#d0773a); transition:opacity .5s; }}
  #fx-toggle[aria-pressed="true"] .glow::before {{ opacity:0; }}
  .glow {{ box-shadow:inset 0 1px 3px rgba(0,0,0,.35), 0 0 10px rgba(226,110,50,.4); }}
  #fx-toggle[aria-pressed="true"] .glow {{ box-shadow:inset 0 1px 3px rgba(0,0,0,.35), 0 0 10px rgba(51,215,160,.45); }}
  .glow .knob::before {{ content:""; position:absolute; inset:0; border-radius:50%; background:#fff; opacity:0; transform:scale(.4);
          transition:opacity .35s .15s, transform .45s .15s cubic-bezier(.34,1.56,.64,1); }}
  #fx-toggle[aria-pressed="true"] .glow .knob {{ box-shadow:0 0 8px #99f6e4; }}
  #fx-toggle[aria-pressed="true"] .glow .knob::before {{ opacity:1; transform:scale(1); }}
  .maple {{ position:absolute; inset:-1px; width:20px; height:20px; filter:drop-shadow(0 1px 1.5px rgba(90,25,10,.5));
          transition:opacity .35s, transform .55s; }}
  #fx-toggle[aria-pressed="true"] .maple {{ opacity:0; transform:rotate(-140deg) scale(.4); }}
  .leaves {{ inset:0; transition:opacity .4s; }}
  .fall {{ position:absolute; animation:sway 3.2s ease-in-out infinite; transition:transform .6s ease-in; }}
  .fall:nth-child(2) {{ animation-delay:-1.1s; animation-duration:3.8s; }}
  .fall:nth-child(3) {{ animation-delay:-2.2s; animation-duration:2.9s; }}
  @keyframes sway {{ 0%, 100% {{ transform:translate(0,0) rotate(-14deg); }} 50% {{ transform:translate(-2px,2px) rotate(16deg); }} }}
  #fx-toggle[aria-pressed="true"] .leaves {{ opacity:0; }}
  #fx-toggle[aria-pressed="true"] .fall {{ animation:none; transform:translateY(18px) rotate(60deg); }}

  @media (prefers-reduced-motion: reduce) {{ .track, .track * {{ transition:none !important; animation:none !important; }} }}

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
<div id="switches">
  <button id="theme-toggle" class="pill" type="button" aria-pressed="false" title="Switch between light and dark">{THEME_TRACK}<span class="label">Light</span></button>
  <button id="fx-toggle" class="pill" type="button" aria-pressed="true" title="Turn the firefly background on or off">{FX_TRACK}<span class="label">Fireflies</span></button>
</div>
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

// Light/Dark switch. The README's images choose light or dark with <picture><source media="(prefers-color-scheme: dark)">,
// which CSS cannot override, so a forced theme rewrites those media rules ("all" = always dark, "not all" = never).
const themeToggle = document.getElementById("theme-toggle");
const systemDark = matchMedia("(prefers-color-scheme: dark)");
const darkSources = [...document.querySelectorAll('picture source[media*="prefers-color-scheme: dark"]')];
function applyTheme() {{
  const forced = root.dataset.theme;
  const dark = forced ? forced === "dark" : systemDark.matches;
  darkSources.forEach(s => s.media = forced ? (dark ? "all" : "not all") : "(prefers-color-scheme: dark)");
  themeToggle.setAttribute("aria-pressed", dark);
  themeToggle.querySelector(".label").textContent = dark ? "Dark" : "Light";
}}
themeToggle.addEventListener("click", () => {{
  themeToggle.classList.remove("switching"); themeToggle.offsetWidth; themeToggle.classList.add("switching");   // replay the dusk flash
  root.dataset.theme = themeToggle.getAttribute("aria-pressed") === "true" ? "light" : "dark";
  try {{ localStorage.setItem("theme", root.dataset.theme); }} catch (e) {{}}
  applyTheme();
}});
systemDark.addEventListener("change", applyTheme);
applyTheme();

// The switches are a secret: show them for a few seconds on load, then fade out (hover the corner to bring them back).
const switches = document.getElementById("switches");
switches.classList.add("intro");
setTimeout(() => switches.classList.remove("intro"), 3500);
addEventListener("scroll", () => requestAnimationFrame(update), {{ passive: true }});
addEventListener("resize", update);
setOn(on);
</script>
</body>
</html>
"""
(out / "index.html").write_text(page, encoding="utf-8")
print("site built:", sum(1 for _ in out.rglob("*") if _.is_file()), "files")
