"""Tints the official Genshin skill glyphs into light/dark heading icons for the profile README.
Keeps the glyph's own shading (luminance) and alpha, and only swaps the colour."""
import pathlib, sys
from PIL import Image

raw = pathlib.Path(sys.argv[1])
out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)

PICKS = {  # README name -> source glyph
    "what-i-do": "venti-23-Talents-1-Skyward_Sonnet.png",
    "skills": "jean-27-Talents-2-Dandelion_Breeze.png",
    "ai": "ineffa-7852-Talents-1-Cleaning_Mode_Carrier_Frequency.png",
    "ai-eval": "nahida-2850-Talents-1-All_Schemes_to_Know.png",
    "testing": "chevreuse-4577-Talents-1-*.png",
    "tech": "aino-8397-Talents-2-*.png",
    "domains": "venti-23-Talents-2-Wind_s_Grand_Ode.png",
    "projects": "albedo-47-Talents-2-Rite_of_Progeniture_Tectonic_Tide.png",
    "stats": "keqing-10-Talents-1-Stellar_Restoration.png",
    "isotoma": "albedo-47-Talents-1-Abiogenesis_Solar_Isotoma.png",
    "albedo-burst": "albedo-47-Talents-2-Rite_of_Progeniture_Tectonic_Tide.png",
}
# Official element colours (dark pages) and a deeper shade of the same hue (light pages).
ELEMENT = {
    "anemo": {"dark": (116, 194, 168), "light": (46, 140, 112)},
    "electro": {"dark": (179, 142, 243), "light": (124, 79, 201)},
    "pyro": {"dark": (239, 121, 56), "light": (206, 88, 24)},
    "hydro": {"dark": (76, 194, 241), "light": (22, 128, 186)},
    "geo": {"dark": (250, 182, 50), "light": (190, 132, 10)},
    "dendro": {"dark": (165, 200, 59), "light": (98, 138, 18)},
}
CHAR_ELEMENT = {"what-i-do": "anemo", "skills": "anemo", "domains": "anemo", "ai": "electro", "stats": "electro",
                "ai-eval": "dendro", "testing": "pyro", "tech": "hydro", "projects": "geo", "isotoma": "geo", "albedo-burst": "geo"}


def find(pattern):
    for folder in (raw, raw.parent / "raw2"):
        hits = sorted(folder.glob(pattern))
        if hits:
            return hits[0]
    raise SystemExit(f"missing {pattern}")


def tint(img, rgb):
    img = img.convert("RGBA")
    px = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = px[x, y]
            lum = (0.3 * r + 0.59 * g + 0.11 * b) / 255
            k = 0.6 + 0.4 * lum          # darker grey parts stay a softer shade of the tint
            px[x, y] = (int(rgb[0] * k), int(rgb[1] * k), int(rgb[2] * k), a)
    return img.crop(img.getbbox() or (0, 0, img.width, img.height))


for name, pattern in PICKS.items():
    src = Image.open(find(pattern))
    for theme in ("light", "dark"):
        colour = ELEMENT[CHAR_ELEMENT[name]][theme]
        tint(src, colour).save(out / f"{name}-{theme}.png")
print("ok", len(list(out.glob("*.png"))))
