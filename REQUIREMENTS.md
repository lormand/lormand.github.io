# Product spec — lormand.com v1

Snapshot of the v1 constraints so git tracks them. Public photo/video showcase on GitHub Pages. Custom domain `lormand.com` is already live. Audience: the public. Nothing personal.

## Host and what this repo is not

- Host is GitHub Pages. Do **not** add NAS hosting, a second git remote, a CDN, or a database.
- Do **not** self-host video files in the repo. Embed YouTube. Link Instagram.
- Do **not** build the English-tutoring site here. A second unrelated site may branch later — no code for it in this repo.
- Keep `CNAME` exactly as-is (`lormand.com`). Do not change DNS, MX, or Pages custom-domain settings from this work if it can be avoided.
- GitHub Pages has a 100MB file cap. Web stills only, compressed. No original 4K/HEVC.

## Look

Dark, editorial, cinematic. Closer to a rally-film title sequence than Squarespace. Large type, lots of black, one hero still, sparse chrome. System fonts or one distinctive display face plus a clean body. Motion is YouTube embeds, not autoplay backgrounds. Accessible contrast. Mobile-first.

## Pages

- **Home:** hero + short positioning + featured Lime Creek Road series + latest YouTube embed(s).
- **About:** short, public, not a bio dump.
- **Work / Lime Creek Road:** first gallery series. Weekly canyon sports-car shoots. Grid of stills (placeholders marked as such) + YouTube embeds.
- **Contact:** working-shaped form. Formspree with a clearly marked `YOUR_FORM_ID` placeholder, plus a mailto fallback to `randy@lormand.com`. No accounts, comments, or mailing list. Structure the code so those can be added later without a rewrite.

## Social

- YouTube: https://www.youtube.com/@atxdroneguild and https://www.youtube.com/@route66roadkill
- Instagram: https://www.instagram.com/atxdroneguild/ — header/footer link only. Do not scrape Instagram.
- Do not invent X or Facebook handles.

## Auto-include new YouTube

Weekday cron (10:00 UTC) plus `workflow_dispatch`. Fetch YouTube RSS for both channels, write `_data/videos.json` (`id` / `title` / `published` / `channel`), commit only if the list changed. No YouTube API key. Channel IDs are required for RSS; resolve from handles if needed (documented in README).

## Watermarks

Do not try to watermark YouTube embeds. For stills: a small corner mark via CSS overlay (`lormand`) for v1. Real file watermarks can come later from NAS masters.

## Content model

Each shoot is a file in `_series/` with title, date, location, stills, YouTube ids. Adding Lime Creek week N is dropping a file, not editing a layout.

## Stack

Pages-native Jekyll from `main` (user site). No heavy framework. No `/docs` or `gh-pages` branch required.
