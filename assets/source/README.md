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

### Skills section icons

| Sub-heading | Character | Skill icon | Element tint | Why it fits |
|---|---|---|---|---|
| AI & LLMs | Ineffa | Cleaning Mode: Carrier Frequency | Electro | Ineffa is a robot housekeeper, Genshin's closest thing to an AI assistant |
| AI Evaluation | Durin | Binary Form: Convergence and Division | Pyro | The skill switches between two forms, like comparing two answers when judging an AI |
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
- IDs used so far: Venti 23, Jean 27 (and 3192), Keqing 10, Albedo 47, Chevreuse 4577,
  Ineffa 7852, Aino 8397, Durin 9017.
- Then add the pick to `PICKS` and `CHAR_ELEMENT` in `tools/make_icons.py` and run it to make the
  tinted light/dark versions in `assets/icons/`.
