# lormand.com

Public stills-and-motion showcase. GitHub Pages, custom domain `lormand.com`.

A second unrelated site may branch later. No code for it here.

## Local

Jekyll, same family GitHub Pages uses:

```bash
bundle install
bundle exec jekyll serve
```

Open http://127.0.0.1:4000/

Refresh the YouTube cache without an API key:

```bash
python3 scripts/fetch_youtube.py
```

Stills in `assets/images/` are compressed web JPEGs. Do not commit 4K or HEVC masters. Pages has a 100MB per-file cap.

## How Pages deploys

This is a user site (`lormand.github.io`). GitHub Pages builds Jekyll from the root of `main`. Keep the `CNAME` file claiming `lormand.com` — do not edit DNS, MX, or the Pages custom-domain setting unless you mean to.

`README.md` and `REQUIREMENTS.md` are excluded from the built site.

## How to add a series / Lime Creek week N

1. Drop a new markdown file in `_series/`, e.g. `_series/lime-creek-road-w02.md`.
2. Front matter (copy week 1 and edit):

   ```yaml
   title: Lime Creek Road — Week 02
   series: Lime Creek Road
   series_slug: lime-creek-road
   week: 2
   date: 2026-09-07
   location: Lime Creek Road, Lake Travis, Austin
   featured: false
   hero: /assets/images/series/lime-creek-road/your-cover.jpg
   stills:
     - src: /assets/images/series/lime-creek-road/your-cover.jpg
       alt: Describe the frame.
       placeholder: false
   youtube:
     - id: REAL_YOUTUBE_ID
       title: Video title
       channel: route66roadkill
   ```

3. Put compressed stills under `assets/images/series/<slug>/`.
4. Set `featured: true` only on the shoot that should own the home hero.
5. Do not edit `_layouts/series.html` or `work.html` to add a week — the collection picks it up.

The file becomes `/work/<filename>/`. Work (`/work/`) lists every shoot.

## YouTube action (no API key)

`.github/workflows/youtube.yml` runs weekdays at 10:00 UTC and on **Run workflow**.

It reads `_data/channels.json`, fetches each channel’s public RSS, and writes `_data/videos.json`. The site reads `site.data.videos.latest` for the home embeds. Livestream RSS leftovers (`… Live Stream`) are kept in `videos` but skipped for `latest` when a finished upload exists.

The job commits to the branch only if the video list changed (not merely `updated_at`).

### Channel IDs

YouTube RSS is `https://www.youtube.com/feeds/videos.xml?channel_id=UC…`. Handles are not valid RSS ids.

IDs already stored:

| Handle | Channel ID |
| --- | --- |
| `@atxdroneguild` | `UCm4VScfiwLjD_wDR5ldnK3w` |
| `@route66roadkill` | `UCudnPVIrU8JFnVmjc4g2plw` |

To resolve a new handle:

```bash
curl -sL -A "Mozilla/5.0" "https://www.youtube.com/@HANDLE" | grep -oE 'channel_id=UC[A-Za-z0-9_-]+' | head -1
```

Put `handle` + `id` in `_data/channels.json`. If `id` is omitted, `scripts/fetch_youtube.py` will try to resolve it from the public channel page.

Do not invent video ids. v1 cache was fetched from live RSS. `@route66roadkill` had one upload: [Sunday on Lime Creek Road](https://www.youtube.com/watch?v=jt4Bmo0GLXM) (`jt4Bmo0GLXM`).

## Formspree

1. Create a form at [formspree.io](https://formspree.io) for `randy@lormand.com`.
2. Replace `YOUR_FORM_ID` in `_includes/contact-form.html` (the `action` URL and `data-formspree-id`).
3. Until that placeholder is replaced, the contact form intercepts submit and opens a mailto to `randy@lormand.com`.

No accounts, comments, or mailing list in v1. Feature flags live in `_config.yml` (`features.comments`, `features.mailing_list`, `features.accounts`). The default layout already includes `_includes/site-extensions.html` so those can land later without rewriting chrome.

## Watermarks

YouTube embeds cannot be watermarked. Gallery stills get a CSS corner mark (`lormand`). Real file watermarks can come later from NAS masters — do not add a second host for that in this repo.

Placeholder stills are generated stand-ins and labeled **Placeholder still** on the image.
