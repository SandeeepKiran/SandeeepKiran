# Source media

The original files behind the profile's images, kept here so they never have to be found again.
The images the README actually shows are made from these (tinted, cut out or redrawn) and live in
`assets/icons/`, `assets/cards/` and the `output` branch.

Genshin Impact art and icons belong to HoYoverse and are used here as non-commercial fan content.

| File | Where it came from | Used for |
|---|---|---|
| `sakura-yae.png` | Cut out by Sandeep (free online background remover) from `sakura-palette-photo.jpg` | The blossom next to "Mousy" (`assets/icons/sakura.png`) |
| `sakura-palette-photo.jpg` | Pinterest: sakura photo with palette #DDBBC5 #D0A6B3 #DF7C8C #9D3C51 #161722 | Source of the sakura; palette for the drawn fallback blossom |
| `venti-blob-original.jpg` | Pinterest: Venti blob sticker | The waving blob after "Hi" (cut out → `assets/icons/venti-blob.png`) |
| `yae-hair-reference.jpg` | Pinterest: Yae Miko art | Colours of the "Mousy" gradient (#f2b6c0 → #df8894 → #c76774) |
| `hoyolab-entry-bg-tcg.png` | HoYoLAB wiki page background (`_nuxt/img/entry_bg_tcg.png`) | Background of the Venti tip card |
| `venti-card.png` | HoYoLAB wiki, Venti character card (entry 3838) | Tip card |
| `anemo-card-back.png` | HoYoLAB wiki, entry 3838 | "More about me" card background |
| `detailed-rules-icon.png` | HoYoLAB wiki, "Detailed Rules" skill icon | "More about me" heading icon |
| `anemo-icon.png` | HoYoLAB wiki, Anemo element icon | Tip card title |
| `albedo-splash.png` | HoYoLAB wiki, Albedo avatar art | Reference for Albedo's burst seal |
| `mondstadt-city.jpg` | military.com article image (Mondstadt city) | Brag video background |
| `genshin-icons/` | HoYoLAB wiki API, character talent icons (grey originals) | Section icons, tinted to their element colours by `make_icons` (see the CHANGELOG in Mousy-Portfolio) |
| `hoyowiki-talent-ring.svg` | HoYoWiki talent ring, as drawn on a character page (Electro colour) | Original of the contact-button hover seal (`assets/site/ring.svg`) |
| `hoyowiki-cursor.png` | HoYoWiki's cursor, `wiki.hoyolab.com/_nuxt/img/genshin.69b4156.png` | Original of `assets/site/cursor.png` |
| `../icons/logos/*.svg` | Simple Icons v11.0.0 (`cdn.jsdelivr.net/npm/simple-icons@11.0.0/icons/`): `openai`, `microsoftexcel` | Logos on the ChatGPT, Codex and Excel pills. shields.io no longer has them, so `tools/pills.py` embeds them |

## Icon picks

### Header icons

| Heading | Character | Skill icon | Element tint | Why it fits |
|---|---|---|---|---|
| What I do | Venti | Skyward Sonnet | Anemo | Venti is the bard, the voice that introduces the profile; Anemo is its theme |
| Skills | Jean | Dandelion Breeze | Anemo | Jean is the Acting Grand Master, the all-rounder who holds everything together |
| Projects | Albedo | Rite of Progeniture: Tectonic Tide | Geo | Albedo is the alchemist who creates things, like the projects |
| The Stats | Keqing | Stellar Restoration | Electro | Keqing is the hard worker who keeps count of results |
| Banner ring | Albedo | Abiogenesis: Solar Isotoma | Geo | Albedo's flower seal makes a ring around the banner |
| Portfolio button | — | Anemo element icon | Anemo | Matches the Anemo theme of the profile |
| Resume button | Keqing | Starward Sword (Elemental Burst), white | Electro badge | Keqing is the hard worker; her burst is the "show what I can do" move |

### Skills section icons

| Sub-heading | Character | Skill icon | Element tint | Why it fits |
|---|---|---|---|---|
| AI & LLMs | Ineffa | Cleaning Mode: Carrier Frequency | Electro | Ineffa is a robot housekeeper, Genshin's closest thing to an AI assistant |
| AI Evaluation | Nahida | All Schemes to Know | Dendro | Nahida is the God of Wisdom; her skill reads and marks every target, like scoring every AI answer (picked by Sandeep 2026-10-17; was Durin) |
| Testing | Chevreuse | Short-Range Rapid Interdiction Fire | Pyro | Chevreuse is a security officer who hunts down troublemakers, like finding bugs |
| Tech & Tools | Aino | Precision Hydronic Cooler | Hydro | Aino is an inventor who builds gadgets |
| Domains | Venti | Wind's Grand Ode | Anemo | Venti's Elemental Burst; matches the Anemo theme of the profile |

The "why it fits" reasons were written down after the picks were made (2026-10-17), so they are a
best reconstruction, not notes from the moment of picking.

## Getting more icons (HoYoLAB wiki API)

The grey skill icons in `genshin-icons/` come from the public JSON endpoint that the HoYoWiki
website itself uses. No login or key is needed:

```
https://sg-wiki-api-static.hoyolab.com/hoyowiki/genshin/wapi/entry_page?entry_page_id=<id>
```

- `<id>` is the number at the end of the character's HoYoWiki page address,
  e.g. `wiki.hoyolab.com/pc/genshin/entry/23` → Venti = `23`.
- Send the header `x-rpc-language: en-us` to get English names.
- In the response, find the `data.page.modules` entry named `Talents`. Its `components[0].data` is a
  JSON string; parse it, and `list[]` gives each talent's `title` and `icon_url` (list[0] is the
  Normal Attack, so the skill and burst follow it). Download the icon, then save it here as `<character>-<id>-Talents-<n>-<Skill_Name>.png`.
- Some `icon_url`s contain Chinese characters (e.g. Keqing's); percent-encode the URL before downloading.
- IDs used so far: Venti 23, Jean 27 (and 3192), Keqing 10, Albedo 47, Chevreuse 4577,
  Ineffa 7852, Aino 8397, Durin 9017 (no longer shown), Nahida 2850.
- Then add the pick to `PICKS` and `CHAR_ELEMENT` in `tools/make_icons.py` and run it to make the
  tinted light/dark versions in `assets/icons/`.

## Website-only files (`assets/site/`)

GitHub strips cursors, hover effects and video, so these only appear on the portfolio site that
`tools/build_preview_branch.py` builds (the `MousyGenshinPreview` branch of Mousy-Portfolio).

| File | Where it came from | Used for |
|---|---|---|
| `cursor.png` | HoYoWiki's own cursor, `wiki.hoyolab.com/_nuxt/img/genshin.69b4156.png` (set on `<body>` there) | The page cursor |
| `cursor-pointer.png` | Made from `cursor.png`: golden glow + a sparkle at the tip (hotspot 4,4) | Links and buttons. HoYoWiki has no clickable version, so its links show the plain system hand |
| `ring.svg` | HoYoWiki talent ring, the `svg.d-talent-keys-active` on a character page, recoloured white | Stencil for the contact-button hover seal; CSS paints it in each element's colour |
| `favicon.png`, `apple-touch-icon.png` | `assets/icons/venti-blob.png`, padded to a square | The browser tab icon |
| `bg/<element>.webm` | HoYoWiki character page background videos, `wiki.hoyolab.com/_nuxt/videos/bg_<element>.<hash>.webm`, unchanged | Firefly backgrounds for anemo, geo, electro, dendro, hydro, pyro, cryo |
| `bg/nodkrai.webm`, `bg/abyss.webm` | Made by us: the cryo video in grey and lightened (Nod-Krai, white), the electro video in grey and darkened (Abyss, black). No such videos exist on HoYoWiki | The two made-up regions |
| `bg/<element>.mp4` | The WebMs re-encoded at 1280×720 (H.264) | Backup for browsers that cannot play WebM |
| `bg/<element>.jpg` | First frame of each video | Shown while a video loads, and instead of video when the visitor asks for reduced motion |

Hover colours are HoYoWiki's exact values: ring = `.d-talent-keys-active.<element> path`, panel =
`.entry-common-module.<element>` background. Email = Pyro, Telegram = Cryo, LinkedIn = Hydro,
Portfolio = Geo, Resume = Electro.

Fireflies: the page is cut into nine equal scroll segments. The first is always Anemo; the other
eight get a new random order on every visit (`OTHERS` in `tools/build_preview_branch.py`). Changing
segment cross-fades over 1.6 s in time (not tied to scroll speed), so the change is smooth but each
element stays its own colour.

Two secret switches sit in the top-right corner, invisible until hovered: **Light / Dark** (also
rewrites the `<picture>` media rules so the README's images follow it) and **Fireflies** (off = the
card stays put and page + card share one solid colour). Both choices are remembered in that browser.
Light mode is a warm cream, `#f6f0e4`, not pure white.

Recolour recipes (ffmpeg, decode with `-c:v libvpx` and add `format=yuv420p` first, or the encoder
fails on the source's alpha channel):
- Nod-Krai: `hue=s=0,curves=all='0/0.50 0.15/0.66 0.35/0.80 1/1'` on `bg_cryo`
- Abyss: `hue=s=0,curves=all='0/0 0.12/0.05 0.35/0.2 0.6/0.6 1/1'` on `bg_electro`
