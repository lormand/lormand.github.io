#!/usr/bin/env python3
"""Fetch YouTube RSS for configured channels and write _data/videos.json.

No API key. RSS requires a channel ID (UC...), not a @handle.
IDs live in _data/channels.json. If an id is missing, this script
resolves it from the public channel page HTML.

Usage (from repo root):
  python3 scripts/fetch_youtube.py
"""

from __future__ import annotations

import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CHANNELS_PATH = ROOT / "_data" / "channels.json"
OUT_PATH = ROOT / "_data" / "videos.json"

ATOM = "{http://www.w3.org/2005/Atom}"
YT = "{http://www.youtube.com/xml/schemas/2015}"
MEDIA = "{http://search.yahoo.com/mrss/}"

UA = "lormand.com youtube-rss/1.0 (+https://lormand.com)"
HANDLE_ID_RE = re.compile(r"channel_id=(UC[A-Za-z0-9_-]{20,})")


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def resolve_channel_id(handle: str) -> str:
    html = fetch(f"https://www.youtube.com/@{handle}").decode("utf-8", "ignore")
    match = HANDLE_ID_RE.search(html)
    if not match:
        raise RuntimeError(f"Could not resolve channel ID for @{handle}")
    return match.group(1)


def is_livestream(title: str) -> bool:
    t = title.strip().lower()
    return t.endswith("live stream") or " live stream" in t


def parse_feed(xml_bytes: bytes, handle: str, channel_id: str) -> list[dict]:
    root = ET.fromstring(xml_bytes)
    videos = []
    for entry in root.findall(f"{ATOM}entry"):
        video_id = (entry.findtext(f"{YT}videoId") or "").strip()
        title = (entry.findtext(f"{ATOM}title") or "").strip()
        published = (entry.findtext(f"{ATOM}published") or "").strip()
        if not video_id:
            continue
        videos.append(
            {
                "id": video_id,
                "title": title,
                "published": published,
                "channel": handle,
                "channel_id": channel_id,
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "livestream": is_livestream(title),
            }
        )
    return videos


def load_channels() -> list[dict]:
    data = json.loads(CHANNELS_PATH.read_text(encoding="utf-8"))
    return data["channels"]


def main() -> int:
    channels = load_channels()
    all_videos: list[dict] = []
    resolved = []

    for ch in channels:
        handle = ch["handle"]
        channel_id = (ch.get("id") or "").strip()
        if not channel_id:
            channel_id = resolve_channel_id(handle)
            print(f"resolved @{handle} -> {channel_id}", file=sys.stderr)
        rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        xml_bytes = fetch(rss_url)
        all_videos.extend(parse_feed(xml_bytes, handle, channel_id))
        resolved.append(
            {
                "handle": handle,
                "id": channel_id,
                "url": ch.get("url") or f"https://www.youtube.com/@{handle}",
            }
        )

    all_videos.sort(key=lambda v: v["published"], reverse=True)
    published_only = [v for v in all_videos if not v["livestream"]]
    latest = published_only[:2] if published_only else all_videos[:1]

    payload = {
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "channels": resolved,
        "latest": latest,
        "videos": all_videos,
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    new_text = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"

    old = OUT_PATH.read_text(encoding="utf-8") if OUT_PATH.exists() else ""
    # Compare without updated_at so a no-op fetch does not dirty the file.
    def strip_updated(text: str) -> str:
        try:
            obj = json.loads(text)
        except json.JSONDecodeError:
            return text
        obj.pop("updated_at", None)
        return json.dumps(obj, indent=2, ensure_ascii=False)

    if strip_updated(old) == strip_updated(new_text):
        print("unchanged")
        return 0

    OUT_PATH.write_text(new_text, encoding="utf-8")
    print(f"wrote {OUT_PATH.relative_to(ROOT)} ({len(all_videos)} videos)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
