"""
Draws every image on Sandeep's GitHub profile, in a light and a dark version.

    python scripts/build_cards.py <out-dir>

Needs a GitHub token in GITHUB_TOKEN (the Action passes its own). Without a token it
still draws the banner, typing line and divider, and fills the stat cards with dashes.

Reads effects.txt (repo root) to pick the decoration style:
    ai-drawn  original drawings: Venti-style dandelion seeds + Albedo-style gold bloom (default)
    fanart    uses images from assets/fanart/ (falls back to ai-drawn if that folder is empty)
    off       clean, still versions with no decoration

Only the Python standard library is used, so the Action needs no installs.
"""
import base64
import datetime as dt
import json
import math
import os
import pathlib
import random
import sys
import urllib.request

LOGIN = "SandeeepKiran"
REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
FONT = "'Segoe UI', 'Helvetica Neue', Arial, sans-serif"

# Light = warm ivory paper with teal and Albedo gold. Dark = deep teal-navy with the same accents.
PALETTES = {
    "light": dict(theme="light", title="#1d2b29", bg1="#fdfaf2", bg2="#f3ead6", card="#fbf6ea", edge="#e4d5b4", text="#1d2b29",
                  muted="#5d6f69", teal="#0f766e", deep="#134e4a", mint="#5cc3b0", gold="#b8892b",
                  gold2="#d9b25f", seed="#ffffff", seedline="#7a8f88", hill="#cfe9df", hill2="#a9d8c9"),
    "dark": dict(theme="dark", title="#e3c16f", bg1="#0c1626", bg2="#10302d", card="#0f1d2b", edge="#1e3b3a", text="#eaf4f1",
                 muted="#a7d3cc", teal="#2dd4bf", deep="#99f6e4", mint="#5eead4", gold="#e3c16f",
                 gold2="#f1d999", seed="#f4f1e6", seedline="#a7d3cc", hill="#123c38", hill2="#0f5148"),
}

TITLE_LINE = "QA Manager @ SoundHound AI"   # always visible, never typed
# (line, width in px at 24px Segoe UI Semibold). SVG cannot measure text, so the widths were measured
# once with the real font and are enforced with textLength: the line is then exactly this wide in any
# browser or fallback font, which keeps it centred and keeps the typing caret on the last letter.
# Changing a line? Re-measure: PIL ImageFont.truetype("seguisb.ttf", 24).getlength(text).
TYPING_LINES = [
    ("GenAI & Conversational Voice AI", 356),
    ("LLM Evaluation · AI Agents · RAG · Voice AI", 469),
    ("sandeeepkiran@gmail.com", 294),
]


def esc(text):
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------------------------------------------------------------------------- data

def fetch_stats():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("No GITHUB_TOKEN: stat cards get placeholders.")
        return None
    query = """
    query($login: String!) {
      user(login: $login) {
        createdAt
        repositories(ownerAffiliations: OWNER, privacy: PUBLIC, first: 100) {
          totalCount
          nodes { stargazerCount }
        }
        pullRequests { totalCount }
        issues { totalCount }
        repositoriesContributedTo(contributionTypes: [COMMIT, PULL_REQUEST, ISSUE, REPOSITORY], first: 1) { totalCount }
        contributionsCollection {
          totalCommitContributions
          contributionCalendar {
            totalContributions
            weeks { contributionDays { date contributionCount } }
          }
        }
      }
    }"""
    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": {"login": LOGIN}}).encode(),
        headers={"Authorization": f"bearer {token}", "User-Agent": "profile-cards"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
    if "errors" in payload:
        raise SystemExit(f"GitHub API error: {payload['errors']}")
    user = payload["data"]["user"]
    contributions = user["contributionsCollection"]
    days = [d for w in contributions["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    return {
        "stars": sum(r["stargazerCount"] for r in user["repositories"]["nodes"]),
        "repos": user["repositories"]["totalCount"],
        "commits": contributions["totalCommitContributions"],
        "prs": user["pullRequests"]["totalCount"],
        "issues": user["issues"]["totalCount"],
        "contributed": user["repositoriesContributedTo"]["totalCount"],
        "total": contributions["contributionCalendar"]["totalContributions"],
        "created": user["createdAt"][:10],
        "days": days,
    }


def streaks(days):
    """Current streak counts back from today (a quiet today does not break it yet)."""
    counts = [d["contributionCount"] for d in days]
    longest = run = 0
    for c in counts:
        run = run + 1 if c else 0
        longest = max(longest, run)
    current = 0
    tail = counts[:-1] if counts and counts[-1] == 0 else counts
    for c in reversed(tail):
        if not c:
            break
        current += 1
    return current, longest


def short(n):
    return f"{n / 1000:.1f}k" if n >= 1000 else str(n)


# ---------------------------------------------------------------------------- decorations

def dandelion(seed_id, p):
    """One real-looking dandelion seed: a slim brown achene, a long hair-thin beak, and a soft
    parachute (pappus) of many fine, slightly curved bristles that fan out like an umbrella."""
    rng = random.Random(11)
    top = -26
    bristles = []
    for i in range(30):
        a = math.radians(8 + 164 * i / 29 + rng.uniform(-3, 3))   # spread across the upper half-dome
        length = rng.uniform(12, 16) * (0.75 + 0.25 * math.sin(a))  # side bristles slightly shorter
        ex, ey = length * math.cos(a), top - length * math.sin(a) * 0.62
        cx, cy = ex * 0.55, top - length * math.sin(a) * 0.62 * 0.4 - 1.5  # gentle outward curve
        bristles.append(f'<path d="M0 {top} Q{cx:.1f} {cy:.1f} {ex:.1f} {ey:.1f}"/>')
    # A faint darker halo under the white bristles keeps them visible on the light banner too.
    return (f'<g id="{seed_id}">'
            f'<g fill="none" stroke="{p["seedline"]}" stroke-width="1" stroke-linecap="round" opacity="0.28">{"".join(bristles)}</g>'
            f'<g fill="none" stroke="{p["seed"]}" stroke-width="0.45" stroke-linecap="round" opacity="0.9">{"".join(bristles)}</g>'
            f'<line x1="0" y1="-5" x2="0" y2="{top}" stroke="{p["seedline"]}" stroke-width="0.5" opacity="0.8"/>'
            f'<path d="M0 -6 C1.4 -4 1.5 1 0 4 C-1.5 1 -1.4 -4 0 -6 Z" fill="#8b6a3e"/>'
            f'<circle cx="0" cy="{top}" r="0.9" fill="{p["seedline"]}"/></g>')


def seed_layer(p, width, height, count, rng):
    """Seeds drift left-to-right on a soft sine path, fading in and out, each at its own pace."""
    parts = [f"<defs>{dandelion('seed', p)}</defs>"]
    for i in range(count):
        y = rng.uniform(height * 0.15, height * 0.85)
        scale = rng.uniform(0.9, 1.6)
        duration = rng.uniform(14, 26)
        delay = -rng.uniform(0, duration)  # negative delay = already mid-flight on first paint
        rise = rng.uniform(-40, 25)
        spin = rng.uniform(-35, 35)
        path = f"M -40 {y:.0f} C {width * 0.3:.0f} {y - 50:.0f}, {width * 0.6:.0f} {y + 40 + rise:.0f}, {width + 40} {y + rise:.0f}"
        parts.append(
            f'<g opacity="0"><use href="#seed" transform="scale({scale:.2f})"/>'
            f'<animateMotion dur="{duration:.1f}s" begin="{delay:.1f}s" repeatCount="indefinite" path="{path}"/>'
            f'<animate attributeName="opacity" values="0;0.95;0.95;0" keyTimes="0;0.12;0.85;1" '
            f'dur="{duration:.1f}s" begin="{delay:.1f}s" repeatCount="indefinite"/>'
            f'<animateTransform attributeName="transform" type="rotate" additive="sum" values="{-spin:.0f};{spin:.0f};{-spin:.0f}" '
            f'dur="{duration / 3:.1f}s" begin="{delay:.1f}s" repeatCount="indefinite"/></g>')
    return "".join(parts)


def wind_streaks(p, width, height, animated):
    """Thin teal swirls, like Anemo wind currents, drawing themselves across the banner."""
    out = []
    # Kept below and right of the heading so the name always stays readable.
    for i, (x, y, length) in enumerate(((width * 0.05, height * 0.72, 300), (width * 0.42, height * 0.66, 340),
                                        (width * 0.55, height * 0.22, 200))):
        d = (f"M {x:.0f} {y:.0f} q {length * 0.35:.0f} -26 {length * 0.65:.0f} 0 "
             f"t {length * 0.35:.0f} -8 q 22 -14 6 -26 q -14 -8 -20 6")
        anim = (f'<animate attributeName="stroke-dashoffset" values="{length * 2};0;{-length * 2}" '
                f'dur="{7 + i * 2}s" begin="{-i * 2}s" repeatCount="indefinite"/>') if animated else ""
        dash = f'stroke-dasharray="{length} {length * 3}"' if animated else 'opacity="0.35"'
        out.append(f'<path d="{d}" fill="none" stroke="{p["mint"]}" stroke-width="2" stroke-linecap="round" '
                   f'{dash} opacity="0.55">{anim}</path>')
    return "".join(out)


def sakura(cx, cy, r):
    """A five-petal sakura blossom in the palette Sandeep picked (#DDBBC5 #D0A6B3 #DF7C8C #9D3C51 #161722):
    notched petals shading from deep pink at the heart to pale at the tips. It turns slowly."""
    petal = (f"M0 0 C{-r * .42:.1f} {-r * .25:.1f} {-r * .55:.1f} {-r * .8:.1f} {-r * .3:.1f} {-r:.1f} "
             f"L{-r * .08:.1f} {-r * .84:.1f} L0 {-r * .98:.1f} L{r * .08:.1f} {-r * .84:.1f} "
             f"L{r * .3:.1f} {-r:.1f} C{r * .55:.1f} {-r * .8:.1f} {r * .42:.1f} {-r * .25:.1f} 0 0 Z")
    petals = "".join(f'<path d="{petal}" transform="rotate({a})" fill="url(#sakura-fill)" stroke="#d0a6b3" stroke-width="0.6"/>'
                     for a in range(0, 360, 72))
    stamens = "".join(
        f'<line x1="0" y1="0" x2="{r * .34 * math.cos(math.radians(a)):.1f}" y2="{r * .34 * math.sin(math.radians(a)):.1f}" stroke="#9d3c51" stroke-width="0.7"/>'
        f'<circle cx="{r * .36 * math.cos(math.radians(a)):.1f}" cy="{r * .36 * math.sin(math.radians(a)):.1f}" r="0.9" fill="#161722"/>'
        for a in range(18, 360, 40))
    return (f'<defs><radialGradient id="sakura-fill" cx="0.5" cy="1" r="1.1">'
            f'<stop offset="0" stop-color="#9d3c51"/><stop offset="0.28" stop-color="#df7c8c"/>'
            f'<stop offset="0.7" stop-color="#d0a6b3"/><stop offset="1" stop-color="#ddbbc5"/></radialGradient></defs>'
            f'<g transform="translate({cx} {cy})"><g>{petals}{stamens}<circle r="{r * .12:.1f}" fill="#9d3c51"/>'
            f'<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="18s" repeatCount="indefinite"/></g></g>')


def blob_image(x, y, width):
    """The little Venti blob that waves "hi" in the banner (a sticker with its background cut out)."""
    f = REPO_ROOT / "assets" / "icons" / "venti-blob.png"
    if not f.exists():
        return ""
    uri = "data:image/png;base64," + base64.b64encode(f.read_bytes()).decode()
    height = width * 233 / 372   # the sticker's own proportions
    return (f'<image href="{uri}" x="{x}" y="{y}" width="{width}" height="{height:.0f}">'
            f'<animateTransform attributeName="transform" type="rotate" values="0 {x + width / 2} {y + height};-4 {x + width / 2} {y + height};0 {x + width / 2} {y + height};3 {x + width / 2} {y + height};0 {x + width / 2} {y + height}" '
            f'dur="3s" repeatCount="indefinite"/></image>')


def isotoma_uri(p):
    """Albedo's Solar Isotoma glyph (official skill icon, pre-tinted gold) as an embeddable data URI."""
    f = REPO_ROOT / "assets" / "icons" / f"isotoma-{p['theme']}.png"
    return "data:image/png;base64," + base64.b64encode(f.read_bytes()).decode() if f.exists() else None


def alchemy_circle(p, cx, cy, r, animated, opacity=0.5, centre=None):
    """Clock-like gold ring with Albedo's Solar Isotoma flower in the middle (slowly turning).
    Pass `centre` (SVG markup) to put something else inside the ring instead."""
    ticks = "".join(
        f'<line x1="{cx + r * 0.9 * math.cos(math.radians(a)):.1f}" y1="{cy + r * 0.9 * math.sin(math.radians(a)):.1f}" '
        f'x2="{cx + r * math.cos(math.radians(a)):.1f}" y2="{cy + r * math.sin(math.radians(a)):.1f}"/>'
        for a in range(0, 360, 15))
    spin = (f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" '
            f'dur="60s" repeatCount="indefinite"/>') if animated else ""
    counter = (f'<animateTransform attributeName="transform" type="rotate" from="360 {cx} {cy}" to="0 {cx} {cy}" '
               f'dur="40s" repeatCount="indefinite"/>') if animated else ""
    uri = isotoma_uri(p)
    size = r * 1.25
    if centre:
        pass
    elif uri:
        centre = (f'<g><image href="{uri}" x="{cx - size / 2:.1f}" y="{cy - size / 2:.1f}" width="{size:.1f}" height="{size:.1f}" '
                  f'opacity="{min(1, opacity + 0.35):.2f}"/>{counter}</g>')
    else:  # fallback if the icon file is missing: a plain gold diamond
        d = r * 0.18
        centre = f'<polygon points="{cx},{cy - d} {cx + d * 0.7},{cy} {cx},{cy + d} {cx - d * 0.7},{cy}" fill="{p["gold2"]}"/>'
    return (f'<g fill="none" stroke="{p["gold"]}" stroke-width="1.2" opacity="{opacity}">'
            f'<circle cx="{cx}" cy="{cy}" r="{r}"/><circle cx="{cx}" cy="{cy}" r="{r * 0.9:.1f}" stroke-dasharray="2 5"/>'
            f'<g>{ticks}{spin}</g></g>{centre}')


def cecilia(p, x, y, size, delay, animated):
    """A small five-petal Cecilia-style flower that blooms open, holds, then closes."""
    petals = "".join(
        f'<ellipse cx="0" cy="{-size * 0.55:.1f}" rx="{size * 0.32:.1f}" ry="{size * 0.55:.1f}" '
        f'transform="rotate({a})"/>' for a in range(0, 360, 72))
    bloom = (f'<animateTransform attributeName="transform" type="scale" additive="sum" values="0;1;1;0;0" '
             f'keyTimes="0;0.15;0.6;0.75;1" dur="8s" begin="{delay}s" repeatCount="indefinite"/>') if animated else ""
    return (f'<g transform="translate({x} {y})"><g fill="{p["seed"]}" stroke="{p["gold"]}" stroke-width="0.8">'
            f'{petals}<circle r="{size * 0.22:.1f}" fill="{p["gold2"]}"/>{bloom}</g></g>')


def fanart_image(name):
    folder = REPO_ROOT / "assets" / "fanart"
    for ext, mime in (("png", "image/png"), ("webp", "image/webp"), ("gif", "image/gif"), ("jpg", "image/jpeg")):
        f = folder / f"{name}.{ext}"
        if f.exists():
            return f"data:{mime};base64," + base64.b64encode(f.read_bytes()).decode()
    return None


# ---------------------------------------------------------------------------- images

def banner(p, mode):
    w, h = 1200, 300
    rng = random.Random(7)  # fixed seed: same layout every day, so the image only changes on purpose
    animated = mode != "off"
    art = fanart_image("banner") if mode == "fanart" else None
    deco = ""
    if art:
        deco = f'<image href="{art}" x="0" y="0" width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice" opacity="0.55"/>'
    elif animated:
        deco = wind_streaks(p, w, h, True) + seed_layer(p, w, h, 12, rng)
    else:
        deco = wind_streaks(p, w, h, False)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Hi, I'm Sandeep Kiran, aka Mousy.">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{p['bg1']}"/><stop offset="1" stop-color="{p['bg2']}"/></linearGradient>
  <linearGradient id="goldline" x1="0" x2="1"><stop offset="0" stop-color="{p['gold']}" stop-opacity="0"/><stop offset="0.5" stop-color="{p['gold2']}"/><stop offset="1" stop-color="{p['gold']}" stop-opacity="0"/></linearGradient>
  <clipPath id="round"><rect width="{w}" height="{h}" rx="22"/></clipPath>
</defs>
<g clip-path="url(#round)">
  <rect width="{w}" height="{h}" fill="url(#bg)"/>
  <path d="M0 {h - 60} C 220 {h - 110}, 420 {h - 30}, 640 {h - 70} S 1000 {h - 120}, {w} {h - 80} V {h} H 0 Z" fill="{p['hill']}"/>
  <path d="M0 {h - 30} C 260 {h - 70}, 520 {h - 10}, 780 {h - 40} S 1080 {h - 60}, {w} {h - 35} V {h} H 0 Z" fill="{p['hill2']}" opacity="0.8"/>
  {alchemy_circle(p, 1010, 130, 95, animated, 0.45)}
  {deco}
  <linearGradient id="yae" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f2b6c0"/><stop offset="0.45" stop-color="#df8894"/><stop offset="1" stop-color="#c76774"/></linearGradient>
  <text x="80" y="140" font-family="{FONT}" font-size="62" font-weight="800" fill="{p['text']}">Hi</text>
  {blob_image(172, 84, 104)}
  <text x="286" y="140" font-family="{FONT}" font-size="62" font-weight="800" fill="{p['text']}">, I'm <tspan fill="{p['teal']}">Sandeep Kiran</tspan></text>
  <rect x="82" y="164" width="560" height="2" fill="url(#goldline)"/>
  <text x="84" y="206" font-family="{FONT}" font-size="30" font-weight="600" fill="{p['muted']}">aka</text>
  <text x="140" y="206" textLength="94" lengthAdjust="spacingAndGlyphs" font-family="{FONT}" font-size="30" font-weight="700" fill="url(#yae)">Mousy</text>
  {sakura(260, 194, 16)}
  <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="22" fill="none" stroke="{p['gold']}" stroke-opacity="0.45"/>
</g>
</svg>"""


def typing(p, mode):
    """Types each line, holds it, erases it, then the next. Pure SMIL, so it plays inside an <img>."""
    w, h, size = 900, 96, 24
    slot, total = 4.0, 4.0 * len(TYPING_LINES)
    groups = []
    for i, (line, approx) in enumerate(TYPING_LINES):
        x0 = (w - approx) / 2
        t = lambda s: max(0.0, min(1.0, (i * slot + s) / total))  # noqa: E731
        # Keyframes: hidden, type in (1.4s), hold, erase (0.5s), hidden. The first line starts at
        # time 0, which collapses two keyframes into one, so duplicates are merged.
        frames = {}
        for k, v in ((0, 0), (t(0), 0), (t(1.4), approx + 8), (t(3.2), approx + 8), (t(3.7), 0), (1, 0)):
            frames[round(k, 4)] = v
        times = ";".join(f"{k:.4f}" for k in frames)
        widths = [f"{v:.0f}" for v in frames.values()]
        values = ";".join(widths)
        anim = f'<animate attributeName="width" values="{values}" keyTimes="{times}" dur="{total}s" repeatCount="indefinite" calcMode="linear"/>'
        caret_x = ";".join(f"{x0 + float(v):.0f}" for v in widths)
        groups.append(
            f'<clipPath id="c{i}"><rect x="{x0:.0f}" y="0" height="{h}" width="0">{anim}</rect></clipPath>'
            f'<text x="{x0:.0f}" y="78" clip-path="url(#c{i})" textLength="{approx}" lengthAdjust="spacingAndGlyphs" font-family="{FONT}" font-size="{size}" font-weight="600" fill="{p["teal"]}">{esc(line)}</text>'
            f'<rect y="57" width="2.5" height="27" fill="{p["gold"]}" opacity="0">'
            f'<animate attributeName="x" values="{caret_x}" keyTimes="{times}" dur="{total}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="{";".join("1" if v != "0" else "0" for v in widths)}" keyTimes="{times}" dur="{total}s" repeatCount="indefinite" calcMode="discrete"/></rect>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" '
            f'aria-label="{esc(" | ".join([TITLE_LINE] + [line for line, _ in TYPING_LINES]))}">'
            f'<text x="{w / 2}" y="32" text-anchor="middle" font-family="{FONT}" font-size="28" font-weight="700" fill="{p["title"]}">{esc(TITLE_LINE)}</text>'
            f'{"".join(groups)}</svg>')


def divider(p, mode):
    """Gold line with an Albedo glyph in the middle; Cecilia flowers bloom along it in turn."""
    w, h = 1200, 60
    animated = mode != "off"
    flowers = "".join(cecilia(p, x, 30, 9, d, animated)
                      for x, d in ((260, 0), (420, 1.2), (780, 2.4), (940, 3.6))) if animated else ""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" aria-hidden="true">
<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{p['gold']}" stop-opacity="0"/><stop offset="0.5" stop-color="{p['gold']}"/><stop offset="1" stop-color="{p['gold']}" stop-opacity="0"/></linearGradient></defs>
<rect x="60" y="29.5" width="{w - 120}" height="1.4" fill="url(#g)"/>
{flowers}
{alchemy_circle(p, w / 2, 30, 24, animated, 0.9)}
</svg>"""


def card_frame(p, w, h, body, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(label)}">'
            f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="16" fill="{p["card"]}" stroke="{p["edge"]}"/>'
            f'<rect x="24" y="1" width="{w - 48}" height="2" fill="{p["gold"]}" opacity="0.6"/>{body}</svg>')


ICONS = {  # tiny line icons, 16px grid
    "star": "M8 1.8l1.9 3.9 4.3.6-3.1 3 .7 4.3L8 11.6 4.2 13.6l.7-4.3-3.1-3 4.3-.6z",
    "commit": "M1 8h4M11 8h4M8 5.2a2.8 2.8 0 1 0 0 5.6 2.8 2.8 0 0 0 0-5.6z",
    "pr": "M4 2.5v11M4 2.5a1.6 1.6 0 1 0 0 .1M12 13.5V6c0-1.5-1-2.5-2.5-2.5H7M8.5 2l-1.5 1.5L8.5 5",
    "issue": "M8 1.5a6.5 6.5 0 1 0 0 13 6.5 6.5 0 0 0 0-13zM8 5v3.5M8 10.8v.2",
    "repo": "M3 2.5h8.5v11H4.5A1.5 1.5 0 0 1 3 12V2.5zM3 12a1.5 1.5 0 0 1 1.5-1.5h7",
}


def stats_card(p, s):
    rows = [("star", "Total stars", s and short(s["stars"])), ("commit", "Commits (past year)", s and short(s["commits"])),
            ("repo", "Public repos", s and s["repos"]), ("issue", "Issues", s and short(s["issues"])),
            ("pr", "Pull requests", s and short(s["prs"]))]
    body = [f'<text x="30" y="52" font-family="{FONT}" font-size="22" font-weight="700" fill="{p["teal"]}">Stats</text>']
    for i, (icon, label, value) in enumerate(rows):
        y = 92 + i * 34
        body.append(f'<g transform="translate(30 {y - 13})"><path d="{ICONS[icon]}" fill="none" stroke="{p["gold"]}" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></g>'
                    f'<text x="56" y="{y}" font-family="{FONT}" font-size="16" fill="{p["text"]}">{label}</text>'
                    f'<text x="250" y="{y}" font-family="{FONT}" font-size="16" font-weight="700" fill="{p["text"]}">{value if value is not None else "–"}</text>')
    body.append(alchemy_circle(p, 360, 150, 62, True, 0.8, centre=burst_seal(p, 360, 150, 52)))
    return card_frame(p, 460, 270, "".join(body), "GitHub stats")


def burst_seal(p, cx, cy, r):
    """The glowing seal from Albedo's burst (Rite of Progeniture: Tectonic Tide): a gold circle with
    four long diamonds (each holding a smaller diamond) on the main axes, and pointed petal-blades
    on the diagonals reaching in towards a bright centre. Turns slowly and pulses its glow."""
    gold, glow = "#f2b632", "#ffd97a"

    def diamond(angle, centre_r, half_len, half_w):
        a = math.radians(angle)
        ux, uy, vx, vy = math.cos(a), math.sin(a), -math.sin(a), math.cos(a)
        mx, my = cx + centre_r * ux, cy + centre_r * uy
        pts = [(mx + half_len * ux, my + half_len * uy), (mx + half_w * vx, my + half_w * vy),
               (mx - half_len * ux, my - half_len * uy), (mx - half_w * vx, my - half_w * vy)]
        return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)

    def blade(angle):
        a = math.radians(angle)
        ux, uy, vx, vy = math.cos(a), math.sin(a), -math.sin(a), math.cos(a)
        tip_out, tip_in, w = r * 0.62, r * 0.18, r * 0.11
        ox, oy, ix, iy = cx + tip_out * ux, cy + tip_out * uy, cx + tip_in * ux, cy + tip_in * uy
        mx, my = cx + r * 0.42 * ux, cy + r * 0.42 * uy
        return (f'M{ox:.1f} {oy:.1f} Q{mx + w * vx:.1f} {my + w * vy:.1f} {ix:.1f} {iy:.1f} '
                f'Q{mx - w * vx:.1f} {my - w * vy:.1f} {ox:.1f} {oy:.1f} Z')

    shapes = [f'<circle cx="{cx}" cy="{cy}" r="{r * 0.62:.1f}" fill="none" stroke-width="2.2"/>']
    for ang in (-90, 0, 90, 180):
        shapes.append(f'<polygon points="{diamond(ang, r * 0.62, r * 0.36, r * 0.13)}" fill="{p["card"]}" stroke-width="2"/>')
        shapes.append(f'<polygon points="{diamond(ang, r * 0.62, r * 0.17, r * 0.06)}" fill="none" stroke-width="1.4"/>')
    shapes += [f'<path d="{blade(ang)}" fill="none" stroke-width="1.6"/>' for ang in (-45, 45, 135, 225)]
    shapes.append(f'<circle cx="{cx}" cy="{cy}" r="{r * 0.09:.1f}" fill="{glow}" stroke="none"/>')
    turn = (f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="90 {cx} {cy}" '
            f'dur="24s" repeatCount="indefinite"/>')
    return (f'<defs><filter id="seal-glow" x="-50%" y="-50%" width="200%" height="200%">'
            f'<feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'
            f'<g stroke="{gold}" filter="url(#seal-glow)">{"".join(shapes)}{turn}'
            f'<animate attributeName="opacity" values="0.85;1;0.85" dur="4s" repeatCount="indefinite"/></g>')


def activity_card(p, s):
    w, h = 460, 270
    body = [f'<text x="30" y="52" font-family="{FONT}" font-size="22" font-weight="700" fill="{p["teal"]}">Activity</text>']
    if s:
        years = max(0, (dt.date.today() - dt.date.fromisoformat(s["created"])).days // 365)
        active = sum(1 for d in s["days"] if d["contributionCount"])
        facts = [f"{s['total']} contributions in the last year", f"{active} active days",
                 f"Joined GitHub {years} years ago"]
        weeks = [sum(d["contributionCount"] for d in s["days"][i:i + 7]) for i in range(0, len(s["days"]), 7)]
    else:
        facts, weeks = ["Stats appear after the first daily run", "", ""], [0] * 52
    for i, f in enumerate(facts):
        body.append(f'<text x="30" y="{84 + i * 22}" font-family="{FONT}" font-size="13" fill="{p["muted"]}">{esc(f)}</text>')
    # Smooth area chart of weekly contributions.
    x0, x1, y0, y1 = 30, w - 30, h - 34, 160
    peak = max(weeks) or 1
    pts = [(x0 + (x1 - x0) * i / max(1, len(weeks) - 1), y0 - (y0 - y1) * v / peak) for i, v in enumerate(weeks)]
    d = f"M {pts[0][0]:.1f} {pts[0][1]:.1f} " + " ".join(
        f"C {(a[0] + b[0]) / 2:.1f} {a[1]:.1f}, {(a[0] + b[0]) / 2:.1f} {b[1]:.1f}, {b[0]:.1f} {b[1]:.1f}" for a, b in zip(pts, pts[1:]))
    body.append(f'<defs><linearGradient id="area" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{p["teal"]}" stop-opacity="0.75"/>'
                f'<stop offset="1" stop-color="{p["teal"]}" stop-opacity="0.08"/></linearGradient></defs>'
                f'<path d="{d} L {x1} {y0} L {x0} {y0} Z" fill="url(#area)"/>'
                f'<path d="{d}" fill="none" stroke="{p["teal"]}" stroke-width="1.6"/>'
                f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" stroke="{p["gold"]}" stroke-opacity="0.5"/>'
                f'<text x="{x0}" y="{y0 + 18}" font-family="{FONT}" font-size="11" fill="{p["muted"]}">a year ago</text>'
                f'<text x="{x1}" y="{y0 + 18}" text-anchor="end" font-family="{FONT}" font-size="11" fill="{p["muted"]}">this week</text>')
    return card_frame(p, w, h, "".join(body), "Contributions in the last year")


def streak_card(p, s):
    w, h = 940, 130
    current, longest = streaks(s["days"]) if s else (None, None)
    cols = [("Total contributions", s and s["total"], "past year"), ("Current streak", current, "days in a row"),
            ("Longest streak", longest, "days, past year")]
    body = []
    for i, (label, value, sub) in enumerate(cols):
        cx = w * (i * 2 + 1) / 6
        colour = p["gold"] if i == 1 else p["teal"]
        body.append(f'<text x="{cx:.0f}" y="62" text-anchor="middle" font-family="{FONT}" font-size="34" font-weight="800" fill="{colour}">{value if value is not None else "–"}</text>'
                    f'<text x="{cx:.0f}" y="88" text-anchor="middle" font-family="{FONT}" font-size="15" font-weight="600" fill="{p["text"]}">{label}</text>'
                    f'<text x="{cx:.0f}" y="106" text-anchor="middle" font-family="{FONT}" font-size="12" fill="{p["muted"]}">{sub}</text>')
        if i:
            body.append(f'<line x1="{w * i / 3:.0f}" y1="30" x2="{w * i / 3:.0f}" y2="100" stroke="{p["gold"]}" stroke-opacity="0.4"/>')
    return card_frame(p, w, h, "".join(body), "Contribution streaks")


def main():
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "dist")
    out.mkdir(parents=True, exist_ok=True)
    effects_file = REPO_ROOT / "effects.txt"
    mode = effects_file.read_text(encoding="utf-8").strip().lower() if effects_file.exists() else "ai-drawn"
    if mode not in ("ai-drawn", "fanart", "off"):
        print(f"effects.txt says '{mode}'; using ai-drawn. Valid words: ai-drawn, fanart, off.")
        mode = "ai-drawn"
    if mode == "fanart" and not fanart_image("banner"):
        print("effects.txt says fanart, but assets/fanart/ has no banner image yet; using ai-drawn.")
        mode = "ai-drawn"
    stats = fetch_stats()
    for theme, p in PALETTES.items():
        files = {"banner": banner(p, mode), "typing": typing(p, mode), "divider": divider(p, mode),
                 "stats": stats_card(p, stats), "activity": activity_card(p, stats), "streak": streak_card(p, stats)}
        for name, svg in files.items():
            (out / f"{name}-{theme}.svg").write_text(svg, encoding="utf-8")
    print(f"Drew {len(PALETTES) * 6} images in {out} (effects: {mode}).")


if __name__ == "__main__":
    main()
