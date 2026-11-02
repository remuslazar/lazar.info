#!/usr/bin/env python3
"""Write the latest Medium posts to a JSON file for the homepage.

Usage: fetch_posts.py OUT.json

If Medium cannot be reached, the posts.json currently live on lazar.info is
kept, so a failed fetch never empties the list. If neither is available the
script writes nothing and the page falls back to the list baked into
index.html.
"""
import html
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

FEED = "https://medium.com/feed/@remuslazar"
LIVE = "https://lazar.info/posts.json"
CONTENT = "{http://purl.org/rss/1.0/modules/content/}encoded"
MAX_POSTS = 10


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "lazar.info-build (+https://lazar.info)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def text(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()


def parse(feed):
    posts = []
    for item in ET.fromstring(feed).iter("item"):
        url = (item.findtext("link") or "").split("?")[0]
        if not url.startswith("https://"):
            continue
        # Medium puts the subtitle first as <h4>; a later <h4> is a section heading.
        sub = re.match(r"\s*<h4>(.*?)</h4>", item.findtext(CONTENT) or "", re.S)
        posts.append({
            "title": text(item.findtext("title")),
            "subtitle": text(sub.group(1)) if sub else "",
            "date": parsedate_to_datetime(item.findtext("pubDate")).date().isoformat(),
            "url": url,
        })
    return posts[:MAX_POSTS]


def main(out):
    try:
        posts = parse(get(FEED))
        if not posts:
            raise ValueError("feed has no posts")
        data = json.dumps({"source": FEED, "posts": posts}, indent=2, ensure_ascii=False)
        print(f"medium: {len(posts)} posts, latest {posts[0]['date']} {posts[0]['title']}")
    except Exception as e:
        print(f"medium fetch failed ({e}), keeping the live posts.json", file=sys.stderr)
        try:
            data = get(LIVE).decode()
            json.loads(data)
        except Exception as e2:
            print(f"no live posts.json either ({e2}), the static list stays", file=sys.stderr)
            return
    with open(out, "w") as f:
        f.write(data + "\n")


if __name__ == "__main__":
    main(sys.argv[1])
