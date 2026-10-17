"""Third pass: Venti card inside the Tip, card-back panel for More about me, PNG Detailed Rules icon."""
import pathlib, re, sys

s = pathlib.Path(sys.argv[1])
t = (s / "readme_template.md").read_text(encoding="utf-8")


def swap(old, new):
    global t
    if old not in t:
        sys.exit(f"NOT FOUND: {old[:60]!r}")
    t = t.replace(old, new)


swap("> No formalities needed. Bugs, ideas, Genshin team comps, all welcome 🍃",
     "> No formalities needed. Bugs, ideas, Genshin team comps, all welcome 🍃\n>\n"
     '> <img alt="Venti\'s card: Anemo, Bow, Mondstadt" src="assets/cards/tip-card.png" width="100%">')
swap('srcset="assets/icons/more-dark.svg"', 'srcset="assets/icons/more-dark.png"')
swap('src="assets/icons/more-light.svg"', 'src="assets/icons/more-light.png"')
# Replace everything between the <br> after <summary> and </details> with the card + a links row.
t, n = re.subn(r"(</summary>\n<br>\n).*?(\n</details>)",
               lambda m: m.group(1) + "\n"
               '<img alt="XDA Developers, Senior Contributor (2019–2023): reported 400+ bugs in Android custom ROMs, '
               'helped 20+ developers run their communities, wrote a beginner\'s guide to custom ROMs for the Redmi K20 Pro. '
               'Research: A Comparative Study on Parsing in Natural Language Processing (IEEE Xplore, 2019). '
               'Older repos are from college (2018–2021)." src="assets/cards/about-card.png" width="100%">\n\n'
               "<p align=\"center\"><b>Links:</b> "
               "<a href=\"https://forum.xda-developers.com/t/simple-beginners-guide-to-raphael-in-custom-roms.4020543/\">XDA beginner's guide</a> · "
               "<a href=\"https://ieeexplore.ieee.org/document/8819687\">IEEE paper</a> · "
               "<a href=\"https://sandeeepkiran.github.io/\">Portfolio</a></p>\n" + m.group(2),
               t, flags=re.S)
if n != 1:
    sys.exit("details block not found")
(s / "readme_template.md").write_text(t, encoding="utf-8")
print("template OK")
