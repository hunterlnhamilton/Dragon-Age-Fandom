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
import os
import re
import shutil
import sys
from urllib.parse import quote

try:
    import yaml
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "--user", "pyyaml"])
    import site
    sys.path.append(site.getusersitepackages())
    import yaml

VAULT, STAGE = sys.argv[1], sys.argv[2]
CODEX = "Codex"

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
def infobox(n):
    fm = n["fm"]
    rows = []
    keys = [k for k in ORDER if k in fm] + sorted(k for k in fm if k not in ORDER)
    for key in keys:
        if key in HIDDEN or (n["type"] == "calendar"):
            continue
        vals = [v for v in as_list(fm[key]) if v not in (None, "", [])]
        if not vals or isinstance(fm[key], (dict, bool)):
            continue
        if len(vals) == 1:
            cell = link(vals[0])
        else:
            cell = "<ul>" + "".join(f"<li>{link(v)}</li>" for v in vals) + "</ul>"
        rows.append(f'<div class="ls-row"><dt>{esc(label(key))}</dt><dd>{cell}</dd></div>')

    plural, group = TYPES[n["type"]]
    title = fm.get("full_name") or n["name"]
    codex = slug_url(f"{CODEX}/{plural}.md")
    head = (f'<div class="ls-sheet__head">'
            f'<a class="ls-badge" data-type="{esc(n["type"])}" href="{codex}">{esc(SINGULAR.get(n["type"], plural))}</a>'
            f'<p class="ls-sheet__title">{esc(title)}</p></div>')
    if not rows:
        return f'<div class="ls-sheet ls-sheet--bare" data-type="{esc(n["type"])}">{head}</div>'
    return f'<aside class="ls-sheet" data-type="{esc(n["type"])}">{head}<dl>{"".join(rows)}</dl></aside>'


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
    out = [f'<aside class="ls-sheet" data-type="calendar"><div class="ls-sheet__head"><a class="ls-badge" data-type="calendar" '
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

    areas = []
    for a in as_list(fm.get("areas")):
        name_part, _, pts = str(a).partition("|")
        t = targets(name_part)
        if not t or not pts.strip():
            continue
        coords = []
        for pair in pts.split():
            try:
                x, y = (float(v) for v in pair.split(","))
                coords.append(f"{x * 100:.2f},{y * 100:.2f}")
            except ValueError:
                pass
        target = notes.get(t[0])
        poly = f'<polygon points="{" ".join(coords)}"><title>{esc(t[0])}</title></polygon>'
        areas.append(f'<a href="{target["url"]}">{poly}</a>' if target else poly)

    pins = []
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
        tag = "a" if target else "span"
        href = f' href="{target["url"]}"' if target else ""
        pins.append(f'<{tag} class="ls-pin"{href} style="left:{x * 100:.3f}%;top:{y * 100:.3f}%">'
                    f'<span class="ls-pin__label">{esc(t[0])}</span></{tag}>')

    return (f'<figure class="ls-map" style="aspect-ratio:{aspect}">'
            f'<img src="{url}" alt="Map of {esc(n["name"])}" loading="lazy">'
            f'<svg viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="false">{"".join(areas)}</svg>'
            f'{"".join(pins)}</figure>'
            f'<p class="ls-note">{len(pins)} places, {len(areas)} areas. Hover or tap to see names.</p>')


# ---------------------------------------------------------------- write sheets
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
        main = infobox(n) + "\n\n" + (extra + "\n\n" if extra else "") + \
            (body if body else '<p class="ls-empty">Nothing written yet.</p>')
    main += "\n\n" + connections(n)

    # keep tags so Kiln's tag pages still work
    tags = as_list(n["fm"].get("tags"))
    head = "---\n" + yaml.safe_dump({"tags": tags}, allow_unicode=True) + "---\n\n" if tags else ""
    with open(n["path"], "w", encoding="utf-8") as fh:
        fh.write(head + main + "\n")


# ---------------------------------------------------------------- codex pages
os.makedirs(os.path.join(STAGE, CODEX), exist_ok=True)


def write_page(rel, text):
    path = os.path.join(STAGE, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text.strip() + "\n")


def card(n):
    fm = n["fm"]
    sub = fm.get("full_name") if fm.get("full_name") not in (None, n["name"]) else None
    sub = sub or (as_list(fm.get("titles")) or [None])[0] or fm.get("kind") or fm.get("date") or ""
    ex = plain_excerpt(n["body"])
    return (f'<li class="ls-card" data-type="{esc(n["type"])}">'
            f'<a class="ls-card__link" href="{n["url"]}">{esc(n["name"])}</a>'
            f'{f"<p class=ls-card__sub>{link(sub)}</p>" if sub else ""}'
            f'{f"<p class=ls-card__ex>{esc(ex)}</p>" if ex else ""}</li>')


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
    write_page(f"{CODEX}/{plural}.md", "\n\n".join(parts))

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
write_page(f"{CODEX}/Timeline.md", "\n".join(tl))

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
    write_page(f"{CODEX}/Calendars.md", '<p class="ls-lede">The calendars of Thedas.</p>\n\n<ul class="ls-cards">' + "".join(rows) + "</ul>")

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
        + "".join(f'<li><a class="ls-tile" data-type="map" href="{m["url"]}"><span>Map of {esc(m["name"])}</span><b>✦</b></a></li>' for m in lore_entries("map"))
        + "</ul>"]
for group in ["People", "Nature", "Places", "Things", "History", "Language"]:
    if group in tiles:
        home.append(f"<h2>{group}</h2>")
        home.append('<ul class="ls-tiles">' + "".join(tiles[group]) + "</ul>")
if home_body.strip():
    home.append(home_body)
write_page("index.md", "\n\n".join(home))

print(f"loresmith_site: {len(lore_entries())} entries, {len(events)} events, {len(cals)} calendars")
