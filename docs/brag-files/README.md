# Brag files

Short launch-style video of Sandeep and his projects (made with /brag-slim, 2026-10-17).

| File | What it is |
|---|---|
| `brag-all.gif` | Everything: all my pages at a glance, me, then each project (25.6 s). Shown at the top of the profile. |
| `brag-me.gif` | Only the "me" part (name, skills, the AI-testing demo), plus the outro. |
| `brag-projects.gif` | The page grid and the projects, plus the outro. |
| `brag-all.mp4` | Full-quality video (no audio). Drag it into GitHub's web editor to embed it as a real video. |
| `brag.jpg` | Poster frame (also frame 0 of the MP4). |
| `share-copy.txt` | A caption ready to post. |
| `source/` | The video source: `brag.html` draws every frame from a time value; `capture.py` records it. |

## Re-render

1. Edit `source/brag.html` (scene times are in `SCENES` near the bottom).
2. Run `python source/capture.py frames frames30 30` (needs Python Playwright).
3. Encode with ffmpeg, for example
   `ffmpeg -framerate 30 -i frames30/f%05d.png -c:v libx264 -pix_fmt yuv420p brag-all.mp4`.
