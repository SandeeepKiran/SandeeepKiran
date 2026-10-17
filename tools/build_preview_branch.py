"""Builds the MousyGenshinPreview site: the profile README rendered like GitHub, following the
viewer's light/dark theme, with every image copied next to it (no outside dependencies)."""
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

shutil.copytree(cards, out / "cards")
shutil.copytree(profile / "assets", out / "assets")
(out / "docs" / "brag-files").mkdir(parents=True)
shutil.copy(profile / "docs" / "brag-files" / "brag-all.gif", out / "docs" / "brag-files" / "brag-all.gif")

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mousy Genshin Preview</title>
<meta name="description" content="Preview of Sandeep Kiran's GitHub profile README. It follows your light or dark theme.">
<style>
  :root {{ --bg:#ffffff; --text:#1f2328; --muted:#59636e; --line:#d1d9e0; --link:#0969da; --tip:#1a7f37; }}
  @media (prefers-color-scheme: dark) {{ :root {{ --bg:#0d1117; --text:#f0f6fc; --muted:#9198a1; --line:#3d444d; --link:#4493f8; --tip:#3fb950; }} }}
  body {{ margin:0; background:var(--bg); color:var(--text); font:15px/1.5 -apple-system,"Segoe UI",Helvetica,Arial,sans-serif; }}
  .bar {{ border-bottom:1px solid var(--line); padding:10px 16px; color:var(--muted); font-size:13px; text-align:center; }}
  main {{ max-width:880px; margin:0 auto; padding:24px 16px 64px; }}
  img {{ max-width:100%; }}
  a {{ color:var(--link); }}
  h2 {{ border-bottom:1px solid var(--line); padding-bottom:6px; }}
  table {{ border-collapse:collapse; display:block; overflow-x:auto; }}
  td, th {{ border:1px solid var(--line); padding:6px 12px; }}
  blockquote {{ margin:0 0 16px; padding:0 16px; border-left:4px solid var(--tip); }}
  .tip-title {{ color:var(--tip); font-weight:600; margin-bottom:0; }}
</style>
</head>
<body>
<div class="bar">Preview of <a href="https://github.com/SandeeepKiran">github.com/SandeeepKiran</a> · follows your light / dark theme · snapshot</div>
<main>
{html}
</main>
</body>
</html>
"""
(out / "index.html").write_text(page, encoding="utf-8")
print("preview built:", sum(1 for _ in out.rglob("*") if _.is_file()), "files")
