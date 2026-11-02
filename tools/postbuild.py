#!/usr/bin/env python3
"""
postbuild.py  PUBLIC_DIR  MANIFEST

Runs after Kiln and fills in what it can't work out from the staged pages:

  * graph.json  - note-to-note links (sheets are HTML, so Kiln doesn't see them)
  * <head>      - page titles and descriptions
  * Meta bar    - real word counts and git dates, or nothing where there are none
  * feed.xml    - real publication dates
"""
import html
import json
import os
import re
import sys
from datetime import datetime
from email.utils import format_datetime
from urllib.parse import unquote

PUBLIC, MANIFEST = sys.argv[1], sys.argv[2]
with open(MANIFEST, encoding="utf-8") as fh:
    data = json.load(fh)
PAGES, HOME = data["pages"], data["home"]


def page_file(url):
    rel = unquote(url).strip("/")
    for candidate in (os.path.join(rel, "index.html"), rel + ".html"):
        path = os.path.join(PUBLIC, candidate)
        if os.path.exists(path):
            return path
    return None


# ---------------------------------------------------------------- graph
graph_path = os.path.join(PUBLIC, "graph.json")
with open(graph_path, encoding="utf-8") as fh:
    graph = json.load(fh)
ids = {n["id"] for n in graph["nodes"]}
seen = {(l["source"], l["target"]) for l in graph["links"]}
added, missing = 0, set()
for src, dst in data["links"]:
    src, dst = unquote(src), unquote(dst)
    if src not in ids or dst not in ids:
        missing |= {src, dst} - ids
    elif (src, dst) not in seen and (dst, src) not in seen:
        seen.add((src, dst))
        graph["links"].append({"source": src, "target": dst})
        added += 1
for node in graph["nodes"]:
    if node["id"] == "/":
        node["label"] = "Home"
with open(graph_path, "w", encoding="utf-8") as fh:
    json.dump(graph, fh, ensure_ascii=False)
if missing:
    print("postbuild: graph has no node for:", ", ".join(sorted(missing)))


# ---------------------------------------------------------------- pages
ITEM = r'<span class="note-meta-item">(?:(?!</span>).)*?'


def short(stamp):
    return datetime.fromisoformat(stamp).strftime("%b %d, %Y")


def set_description(page, text):
    value = html.escape(text, quote=True)
    return re.sub(r'(<meta (?:name="description"|property="og:description"|name="twitter:description") content=")[^"]*"',
                  lambda m: f'{m.group(1)}{value}"', page)


def set_stats(page, info):
    words = info["words"]
    if words:
        minutes = max(1, words // 200)
        page = re.sub(ITEM + r'\d+ min read</span>', lambda m: re.sub(r"\d+ min read", f"{minutes} min read", m.group(0)), page, count=1)
        page = re.sub(r'(<span class="note-meta-item">)\d+ words', rf"\g<1>{words} words", page, count=1)
    else:   # nothing written: no reading time, no word count
        page = re.sub(ITEM + r'\d+ min read</span>\s*', "", page, count=1)
        page = re.sub(r'<span class="note-meta-item">\d+ words</span>\s*', "", page, count=1)
    if info["created"]:
        page = re.sub(r"Created [A-Z][a-z]{2} \d{2}, \d{4}", f'Created {short(info["created"])}', page, count=1)
        page = re.sub(r'("datePublished":")[^"]*"', rf'\g<1>{info["created"]}"', page, count=1)
        page = re.sub(r'("dateModified":")[^"]*"', rf'\g<1>{info["updated"]}"', page, count=1)
        page = re.sub(r"Updated [A-Z][a-z]{2} \d{2}, \d{4}", f'Updated {short(info["updated"])}', page, count=1)
    else:   # no history for this page: say nothing rather than show the build date
        page = re.sub(ITEM + r"(?:Updated|Created) [A-Z][a-z]{2} \d{2}, \d{4}</span>\s*", "", page)
    return page


for url, info in PAGES.items():
    path = page_file(url)
    if not path:
        print("postbuild: no page for", url)
        continue
    with open(path, encoding="utf-8") as fh:
        page = fh.read()
    page = set_description(page, info["description"])
    if url != "/":
        page = set_stats(page, info)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(page)

# Home: the site's name alone, not "Name • Name"
home_path = page_file("/")
with open(home_path, encoding="utf-8") as fh:
    home = fh.read()
home = re.sub(r"<title>[^<]*</title>", f'<title>{html.escape(HOME["title"])}</title>', home, count=1)
with open(home_path, "w", encoding="utf-8") as fh:
    fh.write(home)

# Folder pages: "Calendars", not "Lore/Canon/Calendars"
for folder, _, files in os.walk(PUBLIC):
    if "index.html" not in files:
        continue
    path = os.path.join(folder, "index.html")
    with open(path, encoding="utf-8") as fh:
        page = fh.read()
    fixed = re.sub(r"<title>[^<]*/([^</]*)</title>", r"<title>\1</title>", page, count=1)
    if fixed != page:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(fixed)


# ---------------------------------------------------------------- feed
feed_path = os.path.join(PUBLIC, "feed.xml")
if os.path.exists(feed_path):
    with open(feed_path, encoding="utf-8") as fh:
        feed = fh.read()

    def fix_item(m):
        url = re.sub(r"^https?://[^/]+", "", m.group(2)) or "/"
        info = PAGES.get(url) or {}
        if not info.get("created"):
            return m.group(0)
        stamp = format_datetime(datetime.fromisoformat(info["created"]))
        return f"{m.group(1)}{m.group(2)}{m.group(3)}{stamp}{m.group(4)}"

    feed = re.sub(r"(<link>)([^<]+)(</link>\s*<pubDate>)[^<]*(</pubDate>)", fix_item, feed)
    with open(feed_path, "w", encoding="utf-8") as fh:
        fh.write(feed)

print(f"postbuild: {added} note links added to the graph, {len(PAGES)} pages finished")
