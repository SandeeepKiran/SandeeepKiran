# AGENTS.md — GitHub Profile README (`SandeeepKiran/SandeeepKiran`)

Read this first. Single source of truth for AI agents (Claude Code, Cursor, Codex) in this repo.

## What this is

Sandeep's **GitHub profile README**. GitHub shows `README.md` of the repo named after the user on
`https://github.com/SandeeepKiran`. The theme is Genshin Impact (Anemo/Venti, Albedo gold, teal).
The repo is **PUBLIC**. Remote: `git@github-personal:SandeeepKiran/SandeeepKiran.git`.

## Two places show this README

1. **github.com profile.** Plain Markdown + limited HTML. No CSS, no JS, no video, no cursors.
2. **The portfolio site.** `tools/build_preview_branch.py` turns `README.md` into a web page and adds
   site-only extras: HoYoWiki cursor, hover seals on contact buttons, firefly video backgrounds,
   and two secret switches (Light/Dark, Fireflies). The output goes to the `MousyGenshinPreview`
   branch of `Mousy-Portfolio`. The README itself has NO toggles or fireflies.
   Details: `assets/source/README.md`, section "Website-only files".

## Generated images (`output` branch)

- `.github/workflows/profile-cards.yml` runs `scripts/build_cards.py` and the Platane snake.
- It draws banner, typing line, dividers, stats, activity, streak and snake (light + dark SVGs).
- It force-pushes them to the `output` branch (one commit, no history). The README loads them from
  `raw.githubusercontent.com/SandeeepKiran/SandeeepKiran/output/...`.
- Triggers: daily 02:23 UTC, every push to `main`, and the "Run workflow" button.
- `effects.txt` picks the decoration style: `ai-drawn` (current), `fanart`, or `off`.
- Do not edit or commit to `output` by hand. Why: the next run replaces it.

## Folder map

```
README.md                 The profile (about 130 lines, mostly HTML <picture> blocks)
effects.txt               Decoration style for build_cards.py
.github/workflows/        profile-cards.yml (see above)
.github/build-site.sh     EMPTY file (0 bytes). Not used by the workflow
scripts/build_cards.py    Draws all output-branch images. Standard library only
tools/                    One-off helpers: make_icons.py (tint icons), make_panels.py (cards),
                          pills.py (skill badges), build_preview_branch.py (site), template passes
assets/icons/             Heading icons as <name>-light.png + <name>-dark.png pairs; logos/*.svg
assets/cards/             tip-card.png, about-card.png
assets/site/              Site-only files: cursors, ring.svg, favicon, bg/<element>.jpg/.mp4/.webm
assets/source/            Original media + README.md (where each file came from, icon picks)
assets/Sandeep-Kiran-Resume.pdf   Linked by the Resume button
docs/brag-files/          Brag GIF/MP4 (brag-all.gif shows at the top of the profile) + source
```

## How to edit safely

- Keep every themed image as a `<picture>`: dark file in `<source media="(prefers-color-scheme: dark)">`,
  light file in `<img>`. Why: GitHub picks the image from the viewer's theme.
- When you add a heading icon, make BOTH `assets/icons/<name>-light.png` and `<name>-dark.png`.
  Use `tools/make_icons.py` (add the pick to `PICKS`). Never add only one of the pair.
- Use relative paths (`assets/...`) for files in this repo. Use the `output` URL only for generated SVGs.
- Keep the contact button links unchanged unless Sandeep asks. Why: `build_preview_branch.py` finds them
  by their `href` and stops with an error if one is missing.
- When you add source media, add a row to `assets/source/README.md`.
- Keep `alt` text on every image. Why: screen readers and broken-image fallback.
- Do not add CSS, `<script>`, `<style>` or video to `README.md`. GitHub removes them.

## Preview and test

1. Push is the only true test of github.com rendering. Before a push, check the Markdown in a
   GitHub-flavoured preview (VS Code preview is close, not exact).
2. Draw the cards locally: `python scripts/build_cards.py dist`. Without `GITHUB_TOKEN`, stat cards show dashes.
3. Build the site locally: `python tools/build_preview_branch.py <repo> <cards-dir> <out-dir>`.
   It needs `gh` (it calls `gh api markdown`).
4. After a push, open `https://github.com/SandeeepKiran` in Firefox, in light and in dark theme.

## Rules

- ⚠️ The repo is PUBLIC. Never add private info: phone, home address, salary, or SoundHound-internal details.
- Only Claude Code pushes, with the personal account `SandeeepKiran`. Follow the `safe-push` skill.
  Every other agent: never `git push`.
- Never add AI co-author trailers (`Co-Authored-By: ...`, "Generated with ...") to commits.
- Keep the resume PDF the same as Sandeep's current default resume (QA Manager v2 on 2026-10-22).
  The source lives in his private notes, outside this repo. Ask him before you replace it.
- Genshin art belongs to HoYoverse. Keep the fan-content note in `assets/source/README.md`.

## The owner

Sandeep is a QA Manager and is newer to coding. Explain changes in plain words, with a short reason.

## Open questions

- `.github/build-site.sh` is empty but tracked. Keep or delete?
- `scripts/__pycache__/build_cards.cpython-311.pyc` is committed and there is no `.gitignore`. Add one?
- `effects.txt` supports `fanart`, but `assets/fanart/` does not exist.
- A newer resume, `Sandeep Kiran - Resume - QA v3.pdf` (2026-10-21), exists. Should it replace v2 here?
