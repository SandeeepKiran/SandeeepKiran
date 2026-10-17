"""Second pass on the README template: brand-coloured contact buttons, Genshin icon headings, nested XDA bullets."""
import pathlib, sys

s = pathlib.Path(sys.argv[1])
t = (s / "readme_template.md").read_text(encoding="utf-8")


def pic(icon, height=28, ext="png"):
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="assets/icons/{icon}-dark.{ext}">'
            f'<img src="assets/icons/{icon}-light.{ext}" height="{height}" align="absmiddle" alt=""></picture>')


def swap(old, new):
    global t
    if old not in t:
        sys.exit(f"NOT FOUND: {old[:60]!r}")
    t = t.replace(old, new)


swap('src="https://img.shields.io/badge/Email-0f766e?style=for-the-badge&logo=gmail&logoColor=99f6e4"',
     'src="https://img.shields.io/badge/Email-EA4335?style=for-the-badge&logo=gmail&logoColor=white"')
swap('src="https://img.shields.io/badge/Telegram-0f766e?style=for-the-badge&logo=telegram&logoColor=99f6e4"',
     'src="https://img.shields.io/badge/Telegram-26A5E4?style=for-the-badge&logo=telegram&logoColor=white"')
swap('src="https://img.shields.io/badge/Portfolio-b8892b?style=for-the-badge&logo=githubpages&logoColor=ffffff"',
     'src="{{PORTFOLIO}}"')
swap("## 🍃 What I do", f"## {pic('what-i-do')} What I do")
swap("## 🧰 Skills", f"## {pic('skills')} Skills")
swap("## 🚀 Projects", f"## {pic('projects')} Projects")
swap("## 📊 The Stats", f"## {pic('stats')} The Stats")
swap("<summary><b>🌱 More about me</b></summary>", f"<summary>{pic('more', 24, 'svg')} <b>More about me</b></summary>")
swap("""- **XDA Developers, Senior Contributor (2019–2023):** reported 400+ bugs in Android custom ROMs, helped 20+ developers
  run their communities, and wrote a [beginner's guide to custom ROMs](https://forum.xda-developers.com/t/simple-beginners-guide-to-raphael-in-custom-roms.4020543/)
  for the Redmi K20 Pro.""",
     """- **XDA Developers, Senior Contributor (2019–2023)**
  - Reported 400+ bugs in Android custom ROMs.
  - Helped 20+ developers run their communities.
  - Wrote a [beginner's guide to custom ROMs](https://forum.xda-developers.com/t/simple-beginners-guide-to-raphael-in-custom-roms.4020543/) for the Redmi K20 Pro.""")
swap('alt="QA Manager @ SoundHound AI | GenAI', 'alt="QA Manager @ SoundHound AI. GenAI')
(s / "readme_template.md").write_text(t, encoding="utf-8")
print("template OK")
