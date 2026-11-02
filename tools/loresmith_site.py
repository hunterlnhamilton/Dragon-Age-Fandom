#!/usr/bin/env python3
"""
loresmith_site.py  VAULT_DIR  STAGING_DIR

Copies the vault to STAGING_DIR and adds read-only versions of Loresmith's
views, so Kiln can publish them. Your real vault is never changed.

  * Entry sheets   – an info box from each note's frontmatter, a
                     Connections list (what links here), empty sections hidden
  * Codex/         – a card page per category, Timeline, Calendars
  * Calendars      – month grids with holidays, weekdays, moons, eras
  * Maps           – the map image with clickable pins and areas
  * Home           – overview tiles with counts (Home.md becomes the site root)

Drafting tools (generators, writing log, goals, boards) stay in Obsidian.
"""
import html
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from urllib.parse import quote

try:
    import yaml
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "--user", "pyyaml"])
    import site
    sys.path.append(site.getusersitepackages())
    import yaml

VAULT, STAGE = sys.argv[1], sys.argv[2]
CODEX = "Codex"
# Facts Kiln can't work out from the staged pages, read by tools/postbuild.py
MANIFEST = STAGE.rstrip("/\\") + "-manifest.json"
SITE_TITLE = "Dragon Age: Fandom"
SITE_DESCRIPTION = ("A fan codex of Thedas, the world of Dragon Age: its people, "
                    "nations, history and calendars.")

# type -> (plural label, group). Order here is the order on the home page.
TYPES = {
    "character":    ("Characters", "People"),
    "organization": ("Organizations", "People"),
    "culture":      ("Cultures", "People"),
    "species":      ("Species", "People"),
    "creature":     ("Bestiary", "Nature"),
    "plant":        ("Flora", "Nature"),
    "nation":       ("Nations", "Places"),
    "region":       ("Regions", "Places"),
    "settlement":   ("Settlements", "Places"),
    "location":     ("Locations", "Places"),
    "map":          ("Maps", "Places"),
    "item":         ("Items", "Things"),
    "discovery":    ("Discoveries", "Things"),
    "event":        ("Events", "History"),
    "holiday":      ("Holidays", "History"),
    "calendar":     ("Calendars", "History"),
    "language":     ("Languages", "Language"),
    "word":         ("Dictionary", "Language"),
}
SINGULAR = {
    "character": "Character", "organization": "Organization", "culture": "Culture",
    "species": "Species", "creature": "Creature", "plant": "Plant", "nation": "Nation",
    "region": "Region", "settlement": "Settlement", "location": "Location", "map": "Map",
    "item": "Item", "discovery": "Discovery", "event": "Event", "holiday": "Holiday",
    "calendar": "Calendar", "language": "Language", "word": "Word",
}

# Frontmatter keys that are Loresmith's own bookkeeping, never shown
HIDDEN = {
    "type", "lore", "details", "attributes", "tags", "aliases", "cssclasses",
    "custom_calendar", "era_format", "era_repeat", "no_year_zero", "color", "short",
    "align", "new_year", "week_like", "in_use_from", "image", "aspect", "pins",
    "areas", "places", "changes", "ranks", "full_name",
}
# Preferred order and nicer labels
ORDER = [
    "birth_name", "titles", "kind", "category", "status", "pronouns", "species",
    "culture", "nationality", "occupation", "roles", "leaderOf", "born", "birthplace",
    "died", "death_place", "spouses", "partners", "children", "siblings", "parents",
    "government", "capital", "rulers", "nation", "partOf", "territory", "headquarters",
    "languages", "calendars", "founded", "dissolved", "ended_how", "date", "end",
    "era", "calendar", "participants", "days", "rarity", "classification",
]
LABELS = {
    "birth_name": "Birth name", "leaderOf": "Leader of", "partOf": "Part of",
    "death_place": "Place of death", "ended_how": "How it ended", "category": "Importance",
    "kind": "Kind", "date": "Date", "end": "Ended",
}

WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|([^\]]+))?\]\]")


# ---------------------------------------------------------------- git dates
def git_dates(vault):
    """{path relative to the vault: (first commit time, last commit time)}.
    A fresh clone gives every file the same timestamp, so history is the only
    honest source. Returns {} if there's no usable history."""
    try:
        out = subprocess.run(
            ["git", "-c", "core.quotepath=off", "log", "--format=%x00%aI", "--name-only",
             "--relative", "--", "."],
            cwd=vault, capture_output=True, text=True, encoding="utf-8", check=True).stdout
        shallow = subprocess.run(["git", "rev-parse", "--is-shallow-repository"], cwd=vault,
                                 capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return {}
    if shallow == "true":
        return {}
    dates = {}
    for chunk in out.split("\x00")[1:]:
        lines = [l for l in chunk.splitlines() if l.strip()]
        for path in lines[1:]:
            newest = dates.get(path, (None, lines[0]))[1]
            dates[path] = (lines[0], newest)   # log runs newest first
    return dates


# ---------------------------------------------------------------- helpers
def slug_url(rel_path):
    """Kiln's URL for a vault file: lowercase, spaces to dashes, no .md."""
    parts = rel_path.replace(os.sep, "/").split("/")
    parts = [p.lower().replace(" ", "-") for p in parts]
    if parts[-1].endswith(".md"):
        parts[-1] = parts[-1][:-3]
    return "/" + quote("/".join(parts), safe="/'")


def split_note(text):
    if text.startswith("---\n") or text.startswith("---\r\n"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            try:
                fm = yaml.safe_load(parts[1]) or {}
                if isinstance(fm, dict):
                    return fm, parts[2].lstrip("\r\n")
            except yaml.YAMLError:
                pass
    return {}, text


def strip_comments(body):
    return re.sub(r"%%.*?%%", "", body, flags=re.S)


def sections(body):
    """[(heading or None, text)] split on ## headings."""
    out, head, buf = [], None, []
    for line in body.splitlines():
        m = re.match(r"^##\s+(.*)$", line)
        if m:
            out.append((head, "\n".join(buf).strip()))
            head, buf = m.group(1).strip(), []
        else:
            buf.append(line)
    out.append((head, "\n".join(buf).strip()))
    return out


def drop_empty_sections(body):
    kept = []
    for head, text in sections(body):
        if head is None:
            if text:
                kept.append(text)
        elif text:
            kept.append(f"## {head}\n\n{text}")
    return "\n\n".join(kept)


def plain_excerpt(body, limit=150):
    for head, text in sections(strip_comments(body)):
        t = re.sub(r"!\[\[[^\]]*\]\]", "", text)
        t = WIKILINK.sub(lambda m: m.group(2) or m.group(1), t)
        t = re.sub(r"[#>*_`\-\[\]()]", "", t)
        t = " ".join(t.split())
        if t:
            return t[:limit].rstrip() + ("…" if len(t) > limit else "")
    return ""


def label(key):
    if key in LABELS:
        return LABELS[key]
    k = re.sub(r"(?<=[a-z])([A-Z])", r" \1", key).replace("_", " ")
    return k[:1].upper() + k[1:]


def sections_text(n):
    """The written part of a note. Calendars keep their data in lists, not prose."""
    body = strip_comments(n["body"])
    if n["type"] == "calendar":
        return "\n".join(t for h, t in sections(body)
                         if h and not re.match(r"^(Months|Weekdays|Moons|Eras)\b", h))
    return body


def count_words(markdown):
    """Words a reader would actually read: no markup, comments or link syntax."""
    t = re.sub(r"!\[\[[^\]]*\]\]", " ", strip_comments(markdown))
    t = WIKILINK.sub(lambda m: m.group(2) or m.group(1), t)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"^#+\s.*$", " ", t, flags=re.M)
    return len(re.findall(r"[^\W_][\w'’-]*", t))


def plain(value):
    """A frontmatter value as text, with wikilink brackets removed."""
    return WIKILINK.sub(lambda m: m.group(2) or m.group(1), str(value)).strip()


def describe(n):
    """One sentence for search results and link previews."""
    excerpt = plain_excerpt(sections_text(n), 155)
    if excerpt:
        return excerpt
    kind = SINGULAR.get(n["type"], "Entry").lower()
    title = (as_list(n["fm"].get("titles")) or [None])[0]
    who = f'{n["name"]}, {plain(title)}' if title else n["name"]
    return f"{who}: {kind} entry in a fan codex of Dragon Age's Thedas."


def esc(s):
    return html.escape(str(s), quote=True)


def as_list(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


# ---------------------------------------------------------------- load vault
if os.path.exists(STAGE):
    shutil.rmtree(STAGE)
shutil.copytree(VAULT, STAGE, ignore=shutil.ignore_patterns(".obsidian", ".trash", ".git"))

notes = {}      # name -> dict
for folder, dirs, files in os.walk(STAGE):
    dirs[:] = [d for d in dirs if not d.startswith(".")]
    for f in files:
        if not f.endswith(".md"):
            continue
        path = os.path.join(folder, f)
        rel = os.path.relpath(path, STAGE)
        with open(path, encoding="utf-8") as fh:
            fm, body = split_note(fh.read())
        name = f[:-3]
        ntype = str(fm.get("type") or fm.get("lore") or "").lower()
        notes[name] = {
            "name": name, "path": path, "rel": rel, "url": slug_url(rel),
            "fm": fm, "body": body, "type": ntype,
            "folder": os.path.basename(os.path.dirname(rel)),
        }

assets = {}     # file name -> url (for map images)
for folder, dirs, files in os.walk(STAGE):
    dirs[:] = [d for d in dirs if not d.startswith(".")]
    for f in files:
        if not f.endswith(".md"):
            assets[f] = slug_url(os.path.relpath(os.path.join(folder, f), STAGE))


def link(target_text):
    """Turn '[[Name]]' or 'Name' into an <a> (or plain text if unknown)."""
    s = str(target_text)
    m = WIKILINK.search(s)
    if m:
        name, alias = m.group(1).strip(), m.group(2)
        shown = alias or name
        n = notes.get(name)
        before, after = s[:m.start()], s[m.end():]
        inner = f'<a class="internal-link" href="{n["url"]}">{esc(shown)}</a>' if n \
            else f'<span class="ls-unresolved">{esc(shown)}</span>'
        return esc(before) + inner + link(after) if after else esc(before) + inner
    return esc(s)


def targets(value):
    out = []
    for v in as_list(value):
        for m in WIKILINK.finditer(str(v)):
            out.append(m.group(1).strip())
    return out


def lore_entries(ntype=None):
    items = [n for n in notes.values() if n["type"] in TYPES]
    if ntype:
        items = [n for n in items if n["type"] == ntype]
    return sorted(items, key=lambda n: n["name"].lower())


# ---------------------------------------------------------------- dates
def build_year_converter():
    ages = []  # (name, short) in order, from the calendar note that defines "Divine Age"
    offsets = {"ancient": 0}
    for n in notes.values():
        if n["type"] != "calendar":
            continue
        body = n["body"]
        eras = re.search(r"^## Eras\s*$(.*?)(?=^## |\Z)", body, flags=re.M | re.S)
        if eras and not ages and "Divine Age" in eras.group(1):
            for line in eras.group(1).splitlines():
                m = re.match(r"^-\s*([^(,]+?)\s*\(([^)]+)\)", line.strip())
                if m and m.group(1).strip().lower() != "ancient":
                    ages.append((m.group(1).strip(), m.group(2).strip()))
        align = str(n["fm"].get("align") or "")
        m = re.search(r"(-?\d+)\s+([A-Za-z']+)\s*=.*?(-?\d+)\s+Ancient", align)
        if m:
            offsets[m.group(2).lower()] = int(m.group(3)) - int(m.group(1))
    return ages, offsets


AGES, OFFSETS = build_year_converter()


def abs_year(date):
    """Best-effort absolute year for sorting. None if unparseable."""
    s = str(date or "").strip()
    m = re.match(r"^(\d+):(\d+)\s+(\w+)", s)            # 9:30 Dragon
    if m:
        age_no, yy, word = int(m.group(1)), int(m.group(2)), m.group(3).lower()
        for i, (name, short) in enumerate(AGES):
            if word in (short.lower(), name.split()[0].lower()):
                age_no = i + 1
        return (age_no - 1) * 100 + yy
    m = re.match(r"^(-?\d+)\s+([A-Za-z']+)", s)          # -981 Ancient, 992 TE
    if m:
        off = OFFSETS.get(m.group(2).lower())
        if off is not None:
            return int(m.group(1)) + off
    return None


def era_of(year):
    if year is None:
        return "Undated"
    if year < 1:
        return "Ancient"
    i = min(year // 100, len(AGES) - 1)  # Divine Age is 1-99, then 100 years each
    return AGES[i][0] if AGES else "Chantry era"


# ---------------------------------------------------------------- reverse links
backlinks = {}  # name -> [(source note, field)]
for n in notes.values():
    if n["type"] not in TYPES:
        continue
    for key, value in n["fm"].items():
        if key in ("pins", "areas"):
            continue
        for t in targets(value):
            if t in notes and t != n["name"]:
                backlinks.setdefault(t, []).append((n, key))


# ---------------------------------------------------------------- entry sheets
def connections(n):
    refs = backlinks.get(n["name"], [])
    if not refs:
        return ""
    groups = {}
    for src, key in refs:
        groups.setdefault((src["type"], key), []).append(src)
    parts = []
    for (stype, key), srcs in sorted(groups.items(), key=lambda kv: (list(TYPES).index(kv[0][0]), kv[0][1])):
        uniq = sorted({s["name"]: s for s in srcs}.values(), key=lambda s: s["name"].lower())
        links = ", ".join(f'<a class="internal-link" href="{s["url"]}">{esc(s["name"])}</a>' for s in uniq)
        parts.append(f'<div class="ls-row"><dt>{esc(TYPES[stype][0])} <span>({esc(label(key).lower())})</span></dt><dd>{links}</dd></div>')
    return f'<section class="ls-connections"><h2>Connections</h2><dl>{"".join(parts)}</dl></section>'


# ---------------------------------------------------------------- entry header + details
NAMED_COLORS = {
    "red": "var(--color-red)", "orange": "var(--color-orange)", "yellow": "var(--color-yellow)",
    "green": "var(--color-green)", "cyan": "var(--color-cyan)", "blue": "var(--color-blue)",
    "purple": "var(--color-purple)", "pink": "#f58cd2",
}
FALLBACK_COLORS = ["#c9a0ff", "#86d4ec", "#f0d282", "#78dcaa", "#ffa064", "#f58cd2", "#8caaff"]


def color_of(n, i=0):
    c = str((n or {}).get("fm", {}).get("color") or "").strip().lower()
    if c.startswith("#"):
        return c
    return NAMED_COLORS.get(c, FALLBACK_COLORS[i % len(FALLBACK_COLORS)])


def is_dead(n):
    fm = n["fm"]
    return bool(fm.get("died")) or str(fm.get("status") or "").lower() in ("dead", "deceased")


def entry_chips(n):
    fm, chips = n["fm"], []
    if n["type"] == "character":
        cat = str(fm.get("category") or "").strip()
        if cat:
            chips.append(("ls-chip", f"{cat.title()} character"))
        if is_dead(n):
            chips.append(("", "Deceased"))
            b, d = abs_year(fm.get("born")), abs_year(fm.get("died"))
            if b is not None and d is not None and d >= b:
                chips[-1] = ("", f"Died aged {d - b}")
        elif fm.get("status"):
            chips.append(("ls-chip", str(fm["status"])))
        if fm.get("pronouns"):
            chips.append(("ls-chip", str(fm["pronouns"])))
    else:
        for key in ("kind", "status", "government", "classification", "rarity"):
            if fm.get(key) and isinstance(fm[key], str):
                chips.append(("ls-chip", fm[key]))
        if fm.get("founded") or fm.get("dissolved"):
            span = f'{fm.get("founded") or "?"} – {fm.get("dissolved") or "now"}' if fm.get("dissolved") \
                else f'Founded {fm["founded"]}'
            chips.append(("ls-chip", span))
        if n["type"] == "event" and fm.get("date"):
            chips.append(("ls-chip", f'{fm["date"]}' + (f' – {fm["end"]}' if fm.get("end") else "")))
    return "".join(f'<span class="ls-chip">{esc(t)}</span>' for _, t in chips)


def portrait(n, big=False):
    img = targets(n["fm"].get("image")) if n["type"] != "map" else []
    url = assets.get(os.path.basename(img[0])) if img else None
    inner = f'<img src="{url}" alt="" loading="lazy">' if url else f'<span>{esc(n["name"][:1].upper())}</span>'
    return f'<div class="ls-portrait{" ls-portrait--big" if big else ""}">{inner}</div>'


def hero(n):
    fm = n["fm"]
    plural = TYPES[n["type"]][0]
    title = fm.get("full_name") or n["name"]
    sub = (as_list(fm.get("titles")) or [None])[0]
    return (f'<header class="ls-hero" data-type="{esc(n["type"])}">'
            f'{portrait(n, big=True) if n["type"] != "map" else ""}'
            f'<div class="ls-hero__text">'
            f'<a class="ls-badge" data-type="{esc(n["type"])}" href="{slug_url(CODEX + "/" + plural + ".md")}">{esc(SINGULAR.get(n["type"], plural))}</a>'
            f'<h1 class="ls-hero__name">{esc(title)}{"<span class=ls-dagger title=Deceased>†</span>" if n["type"] == "character" and is_dead(n) else ""}</h1>'
            f'{f"<p class=ls-hero__sub>{link(sub)}</p>" if sub else ""}'
            f'{f"<div class=ls-chips>{chips}</div>" if (chips := entry_chips(n)) else ""}</div></header>')


def details_panel(n):
    fm = n["fm"]
    shown_in_chips = {"category", "pronouns", "status", "kind", "government", "classification", "rarity"}
    rows = []
    keys = [k for k in ORDER if k in fm] + sorted(k for k in fm if k not in ORDER)
    for key in keys:
        if key in HIDDEN or key in shown_in_chips:
            continue
        if key == "titles" and len(as_list(fm[key])) < 2:
            continue
        vals = [v for v in as_list(fm[key]) if v not in (None, "", [])]
        if not vals or isinstance(fm[key], (dict, bool)):
            continue
        cell = link(vals[0]) if len(vals) == 1 else \
            "<ul>" + "".join(f"<li>{link(v)}</li>" for v in vals) + "</ul>"
        rows.append(f'<div class="ls-row"><dt>{esc(label(key))}</dt><dd>{cell}</dd></div>')
    if not rows:
        return ""
    return f'<aside class="ls-details"><p class="ls-details__title">At a glance</p><dl>{"".join(rows)}</dl></aside>'


def entry_page(n, body, extra=""):
    panel = details_panel(n)
    body = body or '<p class="ls-empty">Nothing written yet.</p>'
    parts = [hero(n)]
    if extra:
        parts.append(extra)
    parts.append(f'<div class="ls-entry{" ls-entry--full" if not panel else ""}">\n<div class="ls-entry__main">')
    parts.append(body)
    parts.append(f"</div>\n{panel}\n</div>")
    return "\n\n".join(parts)


# ---------------------------------------------------------------- calendars
def calendar_parts(n):
    body = strip_comments(n["body"])

    def section_list(name):
        m = re.search(rf"^## {name}\b[^\n]*$(.*?)(?=^## |\Z)", body, flags=re.M | re.S)
        if not m:
            return []
        return [l.strip()[1:].strip() for l in m.group(1).splitlines() if l.strip().startswith("-")]

    months = []
    for line in section_list("Months"):
        m = re.match(r"^(.+?),\s*(\d+)", line)
        if m:
            months.append((m.group(1).strip(), int(m.group(2))))
    return {
        "months": months,
        "weekdays": section_list("Weekdays"),
        "moons": section_list("Moons"),
        "eras": section_list("Eras"),
        "body": body,
    }


def calendar_short(n):
    return str(n["fm"].get("short") or n["name"].replace(" Calendar", "")).strip()


def holidays_for(n):
    """{month: {day: [holiday notes]}} for holidays dated in this calendar."""
    short = calendar_short(n).lower()
    out = {}
    for h in lore_entries("holiday"):
        for d in as_list(h["fm"].get("date")):
            m = re.match(r"^\s*([^:]+):\s*(\d+)\s+(.+?)\s*$", str(d))
            if m and m.group(1).strip().lower() == short:
                out.setdefault(m.group(3).strip(), {}).setdefault(int(m.group(2)), []).append(h)
    return out


def calendar_sheet(n):
    p = calendar_parts(n)
    fm = n["fm"]
    hol = holidays_for(n)
    facts = []
    for key, lab in (("short", "Short name"), ("new_year", "New year"), ("align", "Lines up with"),
                     ("in_use_from", "In use from"), ("week_like", "Weeks follow")):
        if fm.get(key) not in (None, ""):
            facts.append(f'<div class="ls-row"><dt>{lab}</dt><dd>{link(fm[key])}</dd></div>')
    if p["months"]:
        facts.append(f'<div class="ls-row"><dt>Year length</dt><dd>{sum(d for _, d in p["months"])} days, {len(p["months"])} months</dd></div>')
    out = [f'<h1 class="ls-sr">{esc(n["name"])}</h1><aside class="ls-sheet" data-type="calendar"><div class="ls-sheet__head"><a class="ls-badge" data-type="calendar" '
           f'href="{slug_url(CODEX + "/Calendars.md")}">Calendar</a><p class="ls-sheet__title">{esc(n["name"])}</p></div>'
           f'<dl>{"".join(facts)}</dl></aside>']

    if p["months"]:
        wk = p["weekdays"] or []
        grids = []
        for month, days in p["months"]:
            cells = []
            for d in range(1, days + 1):
                hs = hol.get(month, {}).get(d, [])
                if hs:
                    names = ", ".join(h["name"] for h in hs)
                    cells.append(f'<a class="ls-day is-holiday" href="{hs[0]["url"]}" title="{esc(names)}">{d}</a>')
                else:
                    cells.append(f'<span class="ls-day">{d}</span>')
            head = "".join(f"<span>{esc(w[:2])}</span>" for w in wk) if wk else ""
            cols = max(len(wk), 1) if wk else 7
            grids.append(f'<div class="ls-month"><h3>{esc(month)}</h3>'
                         f'<div class="ls-days" style="--cols:{cols}">{f"<div class=ls-wk>{head}</div>" if head else ""}{"".join(cells)}</div></div>')
        out.append(f'<h2>Year</h2><div class="ls-year">{"".join(grids)}</div>')
        out.append('<p class="ls-note">Week columns show each weekday’s first letters; days don’t shift with the year. '
                   'Highlighted days are holidays.</p>')

    hol_rows = []
    for month, _ in p["months"]:
        for d in sorted(hol.get(month, {})):
            for h in hol[month][d]:
                hol_rows.append(f'<tr><td>{d} {esc(month)}</td><td><a class="internal-link" href="{h["url"]}">{esc(h["name"])}</a></td></tr>')
    if hol_rows:
        out.append('<h2>Holidays</h2><table><thead><tr><th>Date</th><th>Holiday</th></tr></thead><tbody>'
                   + "".join(hol_rows) + "</tbody></table>")

    if p["weekdays"]:
        out.append("<h2>Weekdays</h2><p>" + " · ".join(esc(w) for w in p["weekdays"]) + "</p>")
    if p["moons"]:
        rows = []
        for line in p["moons"]:
            bits = [b.strip() for b in line.split(",")]
            rows.append(f"<tr><td>{esc(bits[0])}</td><td>{esc(bits[1]) + ' days' if len(bits) > 1 else ''}</td></tr>")
        out.append('<h2>Moons</h2><table><thead><tr><th>Moon</th><th>Cycle</th></tr></thead><tbody>' + "".join(rows) + "</tbody></table>")
    if p["eras"]:
        rows = []
        for line in p["eras"]:
            line = re.sub(r"\s{3,}.*$", "", line)  # drop trailing examples
            bits = [b.strip() for b in re.split(r",(?![^\"]*\"\s*$)", line)]
            m = re.match(r"^(.+?)\s*\(([^)]+)\)$", bits[0])
            name, short = (m.group(1), m.group(2)) if m else (bits[0], "")
            length = bits[1] + " years" if len(bits) > 1 and bits[1] else "—"
            rows.append(f"<tr><td>{esc(name)}</td><td>{esc(short)}</td><td>{esc(length)}</td></tr>")
        out.append('<h2>Eras</h2><table><thead><tr><th>Era</th><th>Short</th><th>Length</th></tr></thead><tbody>' + "".join(rows) + "</tbody></table>")

    # keep any other written sections (History notes etc.)
    rest = [f"## {h}\n\n{t}" for h, t in sections(p["body"])
            if h and not re.match(r"^(Months|Weekdays|Moons|Eras)\b", h) and t]
    return "\n\n".join(out) + ("\n\n" + "\n\n".join(rest) if rest else "")


# ---------------------------------------------------------------- maps
def map_view(n):
    fm = n["fm"]
    img = targets(fm.get("image"))
    img_name = img[0] if img else str(fm.get("image") or "").strip()
    url = assets.get(os.path.basename(img_name))
    if not url:
        return ""
    try:
        aspect = float(fm.get("aspect") or 1.3333)
    except (TypeError, ValueError):
        aspect = 1.3333

    capitals = {t: nat for nat in lore_entries("nation") for t in targets(nat["fm"].get("capital"))}
    counts, areas, labels, pins = {}, [], [], []

    for i, a in enumerate(as_list(fm.get("areas"))):
        name_part, _, pts = str(a).partition("|")
        t = targets(name_part)
        if not t or not pts.strip():
            continue
        xs, ys, coords = [], [], []
        for pair in pts.split():
            try:
                x, y = (float(v) for v in pair.split(","))
            except ValueError:
                continue
            xs.append(x); ys.append(y)
            coords.append(f"{x * 100:.2f},{y * 100:.2f}")
        if not coords:
            continue
        target = notes.get(t[0])
        ttype = target["type"] if target else "region"
        counts[ttype] = counts.get(ttype, 0) + 1
        col = color_of(target, i)
        poly = (f'<polygon data-type="{ttype}" style="--c:{col}" points="{" ".join(coords)}">'
                f'<title>{esc(t[0])}</title></polygon>')
        areas.append(f'<a href="{target["url"]}">{poly}</a>' if target else poly)
        cx, cy = sum(xs) / len(xs) * 100, sum(ys) / len(ys) * 100
        labels.append(f'<span class="ls-area-label" data-type="{ttype}" style="left:{cx:.2f}%;top:{cy:.2f}%">{esc(t[0])}</span>')

    for p in as_list(fm.get("pins")):
        name_part, _, xy = str(p).partition("|")
        t = targets(name_part)
        try:
            x, y = (float(v) for v in xy.split(","))
        except ValueError:
            continue
        if not t:
            continue
        target = notes.get(t[0])
        tfm = target["fm"] if target else {}
        ttype = target["type"] if target else "settlement"
        counts[ttype] = counts.get(ttype, 0) + 1
        kind = str(tfm.get("kind") or "").lower()
        owner = capitals.get(t[0]) or notes.get((targets(tfm.get("nation")) or [""])[0])
        shape = "anchor" if "port" in kind else ("star" if t[0] in capitals or "capital" in kind or "city-state" in kind else "dot")
        icon = {"anchor": "⚓", "star": "★", "dot": ""}[shape]
        col = color_of(owner) if owner else "var(--wh-accent-2)"
        tag, href = ("a", f' href="{target["url"]}"') if target else ("span", "")
        pins.append(f'<{tag} class="ls-pin ls-pin--{shape}" data-type="{ttype}"{href} '
                    f'style="left:{x * 100:.3f}%;top:{y * 100:.3f}%;--c:{col}">{icon}'
                    f'<span class="ls-pin__label">{esc(t[0])}</span></{tag}>')

    uid = re.sub(r"[^a-z0-9]+", "-", n["name"].lower())
    chips, rules = [], []
    for ttype in sorted(counts, key=lambda k: list(TYPES).index(k) if k in TYPES else 99):
        cid = f"ls-f-{uid}-{ttype}"
        chips.append(f'<input type="checkbox" class="ls-filter__input" id="{cid}" checked>'
                     f'<label for="{cid}" class="ls-filter" data-type="{ttype}">{esc(TYPES.get(ttype, (ttype.title(),))[0])} ({counts[ttype]})</label>')
        # [id=...], not #id: Kiln reads "#word" as a tag, even inside <style>,
        # and turning it into a link breaks the whole rule.
        rules.append(f'[id="{cid}"]:not(:checked) ~ .ls-map__scroll [data-type="{ttype}"]{{display:none}}')

    return (f'<div class="ls-mapwrap"><style>{"".join(rules)}</style>'
            f'<span class="ls-filters-label">Show</span>{"".join(chips)}'
            f'<p class="ls-map__hint">Swipe the map to see all of it.</p>'
            f'<div class="ls-map__scroll"><figure class="ls-map" style="aspect-ratio:{aspect}">'
            f'<img src="{url}" alt="Map of {esc(n["name"])}" loading="lazy">'
            f'<svg viewBox="0 0 100 100" preserveAspectRatio="none">{"".join(areas)}</svg>'
            f'{"".join(labels)}{"".join(pins)}</figure></div></div>')


# ---------------------------------------------------------------- write sheets
DATES = git_dates(VAULT)
manifest = {"pages": {}, "links": [], "home": {"title": SITE_TITLE, "description": SITE_DESCRIPTION}}


def graph_edges(n):
    """Note-to-note links. Sheets are written as HTML, so Kiln can't see these."""
    found = {t for value in n["fm"].values() for t in targets(value)}
    found |= {m.group(1).strip() for m in WIKILINK.finditer(strip_comments(n["body"]))}
    return [[n["url"], notes[t]["url"]] for t in sorted(found) if t in notes and t != n["name"]]


for n in notes.values():
    if n["type"] in TYPES:
        created, updated = DATES.get(n["rel"].replace(os.sep, "/"), (None, None))
        words = count_words(sections_text(n))
        manifest["pages"][n["url"]] = {
            "description": describe(n), "words": words, "created": created, "updated": updated,
        }
        manifest["links"] += graph_edges(n)

for n in notes.values():
    if n["type"] not in TYPES:
        if n["fm"] or "%%" in n["body"]:
            with open(n["path"], "w", encoding="utf-8") as fh:
                fh.write(strip_comments(n["body"]))
        continue

    if n["type"] == "calendar":
        main = calendar_sheet(n)
    else:
        body = drop_empty_sections(strip_comments(n["body"]))
        extra = map_view(n) if n["type"] == "map" else ""
        main = entry_page(n, body, extra)
    main += "\n\n" + connections(n)

    # keep tags so Kiln's tag pages still work
    tags = as_list(n["fm"].get("tags"))
    front = {"title": n["name"], "description": describe(n)}
    if tags:
        front["tags"] = tags
    head = "---\n" + yaml.safe_dump(front, allow_unicode=True) + "---\n\n"
    with open(n["path"], "w", encoding="utf-8") as fh:
        fh.write(head + main + "\n")
    # Kiln takes "Updated" and the sitemap date from the file's timestamp
    updated = manifest["pages"][n["url"]]["updated"]
    if updated:
        stamp = datetime.fromisoformat(updated).timestamp()
        os.utime(n["path"], (stamp, stamp))


# ---------------------------------------------------------------- codex pages
os.makedirs(os.path.join(STAGE, CODEX), exist_ok=True)


def write_page(rel, text, title, description):
    """A generated page. The h1 is for screen readers and search; the page's
    look starts at its first section."""
    path = os.path.join(STAGE, rel)
    os.makedirs(os.path.dirname(path) or STAGE, exist_ok=True)
    front = yaml.safe_dump({"title": title, "description": description}, allow_unicode=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(f'---\n{front}---\n\n<h1 class="ls-sr">{esc(title)}</h1>\n\n{text.strip()}\n')
    url = "/" if rel == "index.md" else slug_url(rel)
    manifest["pages"][url] = {"description": description, "words": None, "created": None, "updated": None}


def card(n):
    fm = n["fm"]
    sub = (as_list(fm.get("titles")) or [None])[0] or fm.get("kind") or fm.get("date") or ""
    dead = '<span class="ls-dagger" title="Deceased">†</span>' if n["type"] == "character" and is_dead(n) else ""
    return (f'<li class="ls-card ls-card--portrait" data-type="{esc(n["type"])}">'
            f'{portrait(n)}'
            f'<div class="ls-card__foot"><a class="ls-card__link" href="{n["url"]}">{esc(n["name"])}</a>{dead}'
            f'{f"<p class=ls-card__sub>{esc(sub)}</p>" if sub else ""}</div></li>')


category_counts = {}
for ntype, (plural, group) in TYPES.items():
    items = lore_entries(ntype)
    if not items or ntype == "calendar":
        category_counts[ntype] = len(items)
        continue
    category_counts[ntype] = len(items)
    folders = [n["folder"] for n in items]
    main_folder = max(set(folders), key=folders.count)
    groups = {}
    for n in items:
        if n["folder"] != main_folder:
            key = n["folder"]                                   # subfolder, e.g. Divines, Ancient
        else:
            key = str(n["fm"].get("kind") or n["fm"].get("category") or "").strip().title()
        groups.setdefault(key, []).append(n)
    parts = [f'<p class="ls-lede">{len(items)} {plural.lower()} · <a href="/">Codex home</a></p>']
    for key in sorted(groups, key=lambda k: (k == "", k)):
        title = key or ("Other" if len(groups) > 1 else "")
        if title:
            parts.append(f"<h2>{esc(title)} <small>{len(groups[key])}</small></h2>")
        parts.append('<ul class="ls-cards">' + "".join(card(n) for n in groups[key]) + "</ul>")
    write_page(f"{CODEX}/{plural}.md", "\n\n".join(parts), plural,
               f"All {len(items)} {plural.lower()} in a fan codex of Dragon Age's Thedas.")
    manifest["links"] += [[slug_url(f"{CODEX}/{plural}.md"), n["url"]] for n in items]

# Timeline
events = []
for n in lore_entries("event"):
    y = abs_year(n["fm"].get("date"))
    events.append((y, n))
events.sort(key=lambda e: (e[0] is None, e[0] if e[0] is not None else 0, e[1]["name"]))
tl, current = ['<p class="ls-lede">Every event, oldest first. Dates are shown as written; '
               'Tevinter and Elvhen years are lined up with the Chantry calendar for ordering.</p>'], None
for y, n in events:
    era = era_of(y)
    if era != current:
        if current is not None:
            tl.append("</ol>")
        tl.append(f'<h2>{esc(era)}</h2><ol class="ls-timeline">')
        current = era
    fm = n["fm"]
    when = esc(fm.get("date") or "Undated") + (f" – {esc(fm['end'])}" if fm.get("end") else "")
    kind = f'<span class="ls-tl__kind">{esc(fm["kind"])}</span>' if fm.get("kind") else ""
    who = targets(fm.get("participants"))
    who_html = (" · " + ", ".join(link(f"[[{w}]]") for w in who)) if who else ""
    ex = plain_excerpt(n["body"])
    tl.append(f'<li><time>{when}</time><div><a class="internal-link" href="{n["url"]}">{esc(n["name"])}</a>{kind}'
              f'{f"<p>{esc(ex)}</p>" if ex else ""}{f"<p class=ls-tl__who>{who_html[3:]}</p>" if who else ""}</div></li>')
if current is not None:
    tl.append("</ol>")
write_page(f"{CODEX}/Timeline.md", "\n".join(tl), "Timeline",
           f"{len(events)} events in the history of Thedas, oldest first, across every calendar.")
manifest["links"] += [[slug_url(f"{CODEX}/Timeline.md"), n["url"]] for _, n in events]

# Calendars overview
cals = lore_entries("calendar")
if cals:
    rows = []
    for c in cals:
        p = calendar_parts(c)
        days = sum(d for _, d in p["months"])
        align = f'<p class="ls-card__ex">{link(c["fm"]["align"])}</p>' if c["fm"].get("align") else ""
        rows.append(f'<li class="ls-card" data-type="calendar"><a class="ls-card__link" href="{c["url"]}">{esc(c["name"])}</a>'
                    f'<p class="ls-card__sub">{len(p["months"])} months · {days} days</p>{align}</li>')
    write_page(f"{CODEX}/Calendars.md", '<p class="ls-lede">The calendars of Thedas.</p>\n\n<ul class="ls-cards">' + "".join(rows) + "</ul>",
               "Calendars", f"The {len(cals)} calendars of Thedas, with months, weekdays, moons, eras and holidays.")
    manifest["links"] += [[slug_url(f"{CODEX}/Calendars.md"), c["url"]] for c in cals]

# ---------------------------------------------------------------- home
home_src = os.path.join(STAGE, "Home.md")
home_body = ""
if os.path.exists(home_src):
    with open(home_src, encoding="utf-8") as fh:
        _, home_body = split_note(fh.read())
    os.remove(home_src)
    if "Run `kiln generate`" in home_body:      # Kiln's starter text
        home_body = ""

tiles = {}
for ntype, (plural, group) in TYPES.items():
    count = category_counts.get(ntype, 0)
    if not count:
        continue
    tiles.setdefault(group, []).append(
        f'<li><a class="ls-tile" data-type="{ntype}" href="{slug_url(CODEX + "/" + plural + ".md")}">'
        f'<span>{esc(plural)}</span><b>{count}</b></a></li>')
home = ['<p class="ls-lede">A codex of Thedas: people, places and history, kept in Obsidian with Loresmith.</p>',
        f'<ul class="ls-tiles ls-tiles--feature"><li><a class="ls-tile" data-type="event" href="{slug_url(CODEX + "/Timeline.md")}">'
        f'<span>Timeline</span><b>{len(events)}</b></a></li>'
        + (f'<li><a class="ls-tile" data-type="calendar" href="{slug_url(CODEX + "/Calendars.md")}"><span>Calendars</span><b>{len(cals)}</b></a></li>' if cals else "")
        + "".join(f'<li><a class="ls-tile" data-type="map" href="{m["url"]}"><span>Map of {esc(m["name"])}</span><b></b></a></li>' for m in lore_entries("map"))
        + "</ul>"]
for group in ["People", "Nature", "Places", "Things", "History", "Language"]:
    if group in tiles:
        home.append(f"<h2>{group}</h2>")
        home.append('<ul class="ls-tiles">' + "".join(tiles[group]) + "</ul>")
if home_body.strip():
    home.append(home_body)
write_page("index.md", "\n\n".join(home), SITE_TITLE, SITE_DESCRIPTION)
codex_pages = [plural for ntype, (plural, _) in TYPES.items() if category_counts.get(ntype)]
manifest["links"] += [["/", slug_url(f"{CODEX}/{p}.md")] for p in codex_pages + ["Timeline"]]
manifest["links"] += [["/", m["url"]] for m in lore_entries("map")]

with open(MANIFEST, "w", encoding="utf-8") as fh:
    json.dump(manifest, fh, ensure_ascii=False)

print(f"loresmith_site: {len(lore_entries())} entries, {len(events)} events, {len(cals)} calendars")
