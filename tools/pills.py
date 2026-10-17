"""Builds the skill-pill markdown (shields.io for-the-badge) and checks each logo slug really renders."""
import base64, pathlib, sys, urllib.parse, urllib.request, concurrent.futures as cf

GROUPS = [
    ("ai|AI & LLMs", "134e4a", "99f6e4", [
        ("Claude Code", "claude"), ("Claude API", "anthropic"), ("ChatGPT", "file:openai"), ("Codex", "file:openai"),
        ("Gemini", "googlegemini"), ("Cursor", "cursor"), ("MCP", "modelcontextprotocol"),
        ("Prompt Engineering", None), ("LLM Evaluation", None), ("Agentic Workflows", None)]),
    ("ai-eval|AI Evaluation", "b8892b", "ffffff", [
        ("DeepEval", None), ("LLM-as-Judge", None), ("RAG", None), ("Hallucination & Groundedness", None),
        ("Synthetic Test Data", None), ("Agents & Chatbots", None), ("AI Safety", None), ("Prompt Injection", None)]),
    ("testing|Testing", "0f766e", "ffffff", [
        ("Test Strategy", None), ("Regression", None), ("Smoke", None), ("Functional", None), ("UAT", None),
        ("API", None), ("NLU & Intent", None), ("Voice AI (ASR, TTS)", None), ("pytest", "pytest"),
        ("Playwright", None), ("Postman", "postman")]),
    ("tech|Tech & Tools", "335c81", "ffffff", [
        ("Python", "python"), ("TypeScript", "typescript"), ("Kotlin", "kotlin"), ("VBA", None),
        ("Next.js", "nextdotjs"), ("REST", None), ("Git", "git"), ("GitLab", "gitlab"),
        ("CI/CD", "githubactions"), ("Jira", "jira"), ("Confluence", "confluence"), ("Excel", "file:microsoftexcel"),
        ("KPI & KRA Reporting", None)]),
    ("domains|Domains", "d9b25f", "134e4a", [
        ("Banking", None), ("Insurance", None), ("Healthcare", None), ("ITSD", None), ("E-commerce", None),
        ("Telecom", None), ("EdTech", None), ("Retail", None), ("Travel", None)]),
]


LOGOS = pathlib.Path(__file__).resolve().parent.parent / "assets" / "icons" / "logos"


def badge_url(text, color, logo_color, logo):
    label = text.replace("-", "--").replace("_", "__")
    url = f"https://img.shields.io/badge/{urllib.parse.quote(label, safe='')}-{color}?style=for-the-badge"
    if logo and logo.startswith("file:"):
        # shields.io dropped some brand logos (OpenAI, Microsoft) when Simple Icons removed them,
        # so those come from saved Simple Icons v11 SVGs, coloured here and embedded in the URL.
        svg = (LOGOS / f"{logo[5:]}.svg").read_text(encoding="utf-8").replace("<path ", f'<path fill="#{logo_color}" ', 1)
        data = "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()
        url += "&logo=" + urllib.parse.quote(data, safe="")
    elif logo:
        url += f"&logo={logo}&logoColor={logo_color}"
    return url


def check(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "x"}), timeout=20) as r:
        return "<image" in r.read().decode()


rows, checks = [], []
for title, color, logo_color, items in GROUPS:
    pills = []
    for text, logo in items:
        url = badge_url(text, color, logo_color, logo)
        pills.append(f'<img alt="{text}" src="{url}">')
        if logo:
            checks.append((text, logo, url))
    icon, name = title.split("|")
    pic = (f'<picture><source media="(prefers-color-scheme: dark)" srcset="assets/icons/{icon}-dark.png">'
           f'<img src="assets/icons/{icon}-light.png" height="22" align="absmiddle" alt=""></picture>')
    rows.append(f"### {pic} {name}\n\n" + " ".join(pills))

with cf.ThreadPoolExecutor(8) as pool:
    results = list(pool.map(lambda c: (c, check(c[2])), checks))
missing = [f"{c[0]} ({c[1]})" for c, ok in results if not ok]
print("MISSING LOGOS:", missing, file=sys.stderr)
open(sys.argv[1], "w", encoding="utf-8").write("\n\n".join(rows) + "\n")
