# Loresmith

Loresmith is a worldbuilding and story manager for [Obsidian](https://obsidian.md). It keeps characters, nations,
settlements, cultures, species, creatures, items, events, calendars, languages and stories together in one project,
works out how everything is connected, and helps you plan, write and track a book, all stored as ordinary markdown
notes.

- **Plain markdown, no database.** Every entry is a note with frontmatter, so your work stays readable without the
  plugin and works with the graph, backlinks, search, Dataview and Bases.
- **Desktop and mobile.** No Node APIs, so it runs on desktop, iPad and phones.
- **Theme-friendly.** Colors and fonts come only from Obsidian's theme variables (interface and text fonts, UI sizes,
  heading styles), so your theme, its Style Settings and Obsidian's font size restyle it.

## Contents

- [Installation](#installation)
- [Getting started](#getting-started)
- [How your data is stored](#how-your-data-is-stored)
- [Views](#views)
- [Entries](#entries)
- [Characters](#characters)
- [Relationships](#relationships)
- [Organizations, groups and roles](#organizations-groups-and-roles)
- [Places](#places)
- [Maps](#maps)
- [Species, creatures and plants](#species-creatures-and-plants)
- [Stories, chapters and scenes](#stories-chapters-and-scenes)
- [Outlines and plot arcs](#outlines-and-plot-arcs)
- [Time: events, timeline and dates](#time-events-timeline-and-dates)
- [Calendars](#calendars)
- [Holidays](#holidays)
- [The Calendar page](#the-calendar-page)
- [Languages and the dictionary](#languages-and-the-dictionary)
- [Relations web](#relations-web)
- [Who has met whom](#who-has-met-whom)
- [Writing log](#writing-log)
- [Generators](#generators)
- [Name builder](#name-builder)
- [Moodboards and tension](#moodboards-and-tension)
- [Export](#export)
- [Commands](#commands)
- [Settings](#settings)

## Installation

### Manual

1. Download `main.js`, `manifest.json` and `styles.css` from the latest release.
2. Create a folder called `loresmith` in `<your vault>/.obsidian/plugins/` and put the three files in it.
3. In Obsidian, open **Settings → Community plugins**, refresh the list and enable **Loresmith**.

### Optional companion plugins

- **[Randomness](https://github.com/Obsidian-TTRPG-Community/Randomness)** is required for the
  [Generators](#generators). Everything else works without it.

## Getting started

1. Click the **library** icon in the ribbon, or run **Loresmith: Open overview**.
2. Create a project. A project is a folder inside your lore folder (`Lore` by default).
3. Use the **+** buttons, the **Create entry** command or the category pages to add characters, places, stories and
   anything else.
4. Click the **bookmark** icon in the ribbon to open the sidebar panel, and keep it open while you write.

A project starts on the modern calendar with today's date as the present, so a contemporary story needs no setup. See
[Calendars](#calendars) to give your world its own.

## How your data is stored

Everything is a normal markdown note.

```
Lore/
  Example Project/              ← a project
    Calendar.md                 ← the primary calendar
    Calendars/Coastal Calendar.md
    Characters/Elena Hart.md
    Nations/Kingdom of Westmarch.md
    Regions/Grey Mountains.md
    Settlements/Kingsport.md
    Locations/The Crooked Lantern.md
    Organizations/Lantern Guild.md
    Events/Siege of Kingsport.md
    Holidays/Midwinter Feast.md
    Stories/
      First Draft/
        First Draft.md          ← story note: synopsis, main characters, chapter order
        First Draft outline.md  ← the story's outline
        Chapter 1/
          Scene 1.md            ← write here
```

- Each entry has `type: <type>` in its frontmatter (`lore:` is also read).
- Links between entries (species, residence, member of, nationality and so on) are frontmatter wikilinks, so they
  appear in the graph, backlinks, Dataview and Bases.
- The large text boxes in the editor are the note's `## Heading` sections. Edit them in Loresmith or in the note.
- Custom attributes are top-level properties, listed in `attributes` to keep their order.
- Scene folders follow a chapter/scene layout that works alongside other writing plugins such as Longform and Novelr.

## Views

### Overview

The main view, opened from the ribbon or **Open overview**. A navigation column on the left reaches every part of
the project: stories, notes, the writing log, plotting tools, generators and every category, grouped into People,
Nature, Places, Things, History and Language. The home page shows writing goals, stories with chapter and word counts,
character portraits, a tile for every category and a tag cloud.

### Sidebar panel

A compact Loresmith for the right sidebar, opened with the bookmark icon or **Open sidebar panel**. It moves between
its own pages with back and home buttons instead of opening tabs.

- **Home**: what you are writing right now (status, story and chapter, who is in the scene), today's words, stories,
  plotting tools, generators and every category with counts.
- **Writing log**: the Today, Trend, Goals and Authorship tabs, sized for the sidebar. The Today tab and a running
  pomodoro update while you type.
- **Story**: synopsis, main characters and word goal, then collapsible chapters with scenes. Change status, cast,
  order and names, and add chapters and scenes. Tapping a scene opens it in the editor you were last writing in.
- **Category and entry**: search a category, then read an entry's details, sections and appearances as a quick
  reference. Links between entries open inside the panel.

**Edit**, **Board**, **Outline** and anything marked with an arrow open the full view in the main area.

### Category pages

Grid or list layout, search, and a right-click menu to open, open as a note, move to a folder or delete.

- **Grouping**: group any list by **folders** (subfolders inside the type's folder, nested as deep as you like), **by
  type** (the Type or Kind field; species by classification, characters by importance) or not at all. Pick it on the
  overview or with the folder button in the sidebar; it is remembered per type. Click a heading to fold it, and use
  the **+** on a heading to create an entry in that folder or with that type.
- **Nesting**: subspecies sit under their species, branches under the organization they are part of, and places
  under the place they are part of (a province under its kingdom, a district under its city).
- **Move to folder…** in an entry's right-click menu files it into a subfolder with its links intact.

### Entry editor

Section editors with preview, reorderable Details sections, linked fields, custom attributes, tags and a
**Linked from** list. Fields such as Classification, Type, Era, Status, Role, Heritage, Government and Part of speech
suggest values you have already used, so "Noble" and "noble" don't become two groups.

## Entries

| Group | Entry types |
| --- | --- |
| People | Characters, Organizations, Cultures, Species |
| Nature | Creatures (Bestiary), Plants (Flora) |
| Places | Nations, Regions, Settlements, Locations, Maps |
| Things | Items, Discoveries, Relations |
| History | Events, Holidays, Calendars, plus the Timeline and the Calendar page |
| Language | Languages, Dictionary words |
| Plotting | Stories, Plot arcs, Notes |

Every entry lists **Connections**: what it links to and what links to it. A nation shows its people, settlements and
the regions it holds; a settlement shows its residents, who was born there and its events; an organization shows its
members; a species shows its characters.

## Characters

Character sheets have a portrait header with age, status, species, role, home, traits and flaws, then:

- **At a glance**: scenes, chapters, first and last appearance, and who they appear with most. A strip of every scene
  in the book with theirs filled in (click one to open it), a warning when they vanish for three or more chapters,
  and a profile checklist of what is still blank. Click a checklist item to jump to it.
- **A one-line look** under the header: apparent age, height, build, hair, eyes and skin.
- **Relationship cards**, a **family tree** across five generations, and **Connections**.
- **Sidebar fields** in groups you can fold away: Identity, Appearance, Personality, Abilities, Life, Family, Ties and
  Holdings.
- **Author's notes**: Want, Need, Wound, Lie, Arc, Voice and Secrets.

Other details:

- **Birth names**: the Birth name field holds a maiden or former name, shown as "née …" (or "né", or "born" when
  gender isn't set) under their name, on relationship cards and in the family tree. Searching for it finds them.
- **Heritage**: a free label for what people call someone, separate from biology ("noble-born", "clanless").
- **Nationality** (Identity group): the nations they belong to. The nation's page lists them, and if the nation keeps
  a calendar, their dates are read in it.
- **Initials** on cards and avatars use the first and last name ("Elena Mae Hart" is EH).
- **Ages** are worked out from their birth date and the story's in-world date (see
  [Time](#time-events-timeline-and-dates)). Ages count in the calendar the birth date is written in.
- The **Species** check on the profile only appears once the project has a species, so the plugin suits any genre.

### Scene cast

Each scene has a `characters` list in its frontmatter. Fill it from the people icon on the chapters board or in the
sidebar, with the **Characters in this scene** command, or by hand. Characters listed there appear in the scene;
characters only linked in the text count as mentioned. **Add an empty characters property to scenes that lack one**
updates older scenes.

## Relationships

One engine reads links from both notes, so if Jonah lists Elena as an ally, Elena's page shows Jonah too.

- **Worked out for you**: full, half and step siblings, grandparents, aunts and uncles, nieces and nephews, cousins,
  in-laws and step-family. Siblings listed by name share parents, and named siblings of siblings are siblings too.
- **Labels follow pronouns or gender**: "Sister", "Half-brother", "Mother-in-law".
- Anything found from another note is marked with a sparkle and says where it came from.
- Add relationships with **Add relationship** on a character, or in the sidebar fields.

### Ties that change over time

The clock icon on a relationship card (or **A tie that changed over time…** under Add relationship) opens a history
for that pair, one line per stage, with optional years:

```yaml
ties:
  - "[[Jonah]]: Enemy (1000–1015)"
  - "[[Jonah]]: Friend (1015–)"
  - "[[Rafe]]: Lover (until 1010)"
  - "[[Rafe]]: Nemesis (1010–)"
  - "[[Claire]]: Ex-wife"
  - "[[Paul]]: Brother, estranged"
```

- The current stage becomes the relationship card, with "Before: Former enemy (1000–1015)" underneath.
- Someone with only past ties moves to a **Past ties** group ("Ex-wife", "Former rival").
- A past stage retires the same kind of link written in the plain fields, so you don't have to delete it.
- Everyday words are understood (nemesis, lover, fiancée, apprentice, best friend); anything else shows as typed, and
  a note after a comma ("estranged") is kept.
- Lines are read from both characters' notes, so you only write them once.

### Two-way links

With **Keep links two-way** on (the default), adding or removing a link also updates the other note: spouses,
partners, siblings, friends, allies, rivals, enemies, mentors and students, parents and children, members, leaders,
owners, pioneers, cultures and the places they live, languages and where they are spoken, calendars and who keeps
them, and between nations: allies, rivals, wars, and what came before and after. **Make relationship links two-way**
fills in every missing side in the project at once; nothing is removed.

## Organizations, groups and roles

Schools, companies, teams, bands, crews, guilds and noble houses are all Organizations. A character joins one through
**Affiliation**, **Leader of**, **Education** or **Workplace** (**House**, under Family, is for a noble house or
dynasty).

Use the pencil on a group chip to give someone roles there, one line per position, each with optional years and a
**No longer active** switch:

```yaml
roles:
  - "[[Northgate Academy]]: Student (1971–1978)"
  - "[[Northgate Academy]]: Professor, Chemistry (1981–)"
  - "[[Ember House]]: Head of House (1985–)"
  - "[[Lantern Guild]]: (former)"
```

- A role is **former** when its end year is before the story's present date, when it is marked former, or when the
  character has died. Former members stay linked and keep their titles ("Former Student").
- **Subdivisions**: an organization that is **Part of** another (houses of a school, departments of a government,
  squads of an army) is a subdivision, at any depth. Its people also appear on the parent's page, labeled with their
  subdivision. Adding someone to the parent asks which subdivision they belong to.
- **Ranks**: an organization with a hierarchy (an army, a knightly order, a church, a guild) can list its ranks,
  highest first, in the **Ranks** section of its page. Reorder them with the arrows, rename them in place, or add the
  titles people already hold with one tap. A person's rank is the first part of their title ("Knight, Order of the
  Rose" is a Knight), and a rank can list other spellings ("Captain/Capt."). The People section is then listed in rank
  order, the role editor suggests the ranks, **Groups and positions** says "rank 3 of 7", and subdivisions use their
  parent's ranks until given their own. In the note they are a plain list:

  ```yaml
  ranks:
    - Grand Master
    - Knight-Commander
    - Knight
    - Squire
  ```

- **People section** on organization pages: everyone current, grouped by role or by subdivision, with earlier titles
  on each card. Former members follow in their own section, which you can hide.
- **Groups and positions** on character sheets: every group they are or were in, with each title and its years,
  active ones first. The header shows their current titles.

### Rulers of places

**Leader of** also takes nations, settlements and locations, so a character can lead a noble house (an organization),
rule a kingdom, be mayor of a town or command a keep. Their titles work the same way as roles in a group:

```yaml
leaderOf:
  - "[[Ferelden]]"
  - "[[Highever]]"
roles:
  - "[[Ferelden]]: King (9:10–9:25)"
  - "[[Highever]]: Teyrn"
  - "[[Fort Drakon]]: Commander (until 9:30)"
```

- Leader of is kept two-way with the place's **Ruled by** (and with a group's **Leaders**).
- Nations, settlements and locations get a **Rulers** section: current rulers grouped by title, then **Former
  rulers**. A ruler is former when their reign ended before the present date, when they're marked as no longer
  active, or when they have died.
- The pencil on a ruler's chip, on either page, sets their title and years. The character's **Groups and positions**
  and header list the places they rule alongside their groups.

## Places

There are four kinds of place, because a kingdom isn't a culture, an organization or a building.

| Kind | For | Folder |
| --- | --- | --- |
| **Nations** | Kingdoms, empires, republics, city-states, clan lands | `Nations/` |
| **Regions** | Continents, provinces, forests, mountain ranges, seas, islands | `Regions/` |
| **Settlements** | Cities, towns, villages, forts, ports | `Settlements/` |
| **Locations** | Everything else: taverns, temples, ruins, schools, battlefields | `Locations/` |

### Nations

- **Type** and **Status** ("Thriving", "In decline", "Fallen").
- **Rule**: Government, Ruled by (characters or organizations), Ruling house, Capital, and **Part of** for a vassal,
  province or member of a federation. Rulers are listed, current and former, in the page's **Rulers** section (see
  [Rulers of places](#rulers-of-places)).
- **Land**: Territory (the regions it holds) and Population.
- **Map color**: the color the nation, its areas and its settlements are drawn in on maps.
- **People**: Cultures, Species, Languages, Faiths and Calendars, as many of each as you need, since a kingdom usually
  holds more than one people.
- **Ties**: Allies, Rivals, At war with, and Currency.
- **History**: Founded, Fell, Came after and Followed by.
- Sections: About, Government, Society, Economy, Military, History, plus Laws and Foreign Relations.

The page shows how long it stood and how long ago it fell. Its founding and fall go on the timeline and the calendar.

### Regions

Type, Part of (a larger region), Map color, Formed, Ended, Terrain, Climate, Population, Cultures and Languages. Sections: About,
Geography, Climate, Ecology, History.

### Settlements

Type, **Nation** (the nation it belongs to), **In** (the region it's in, or the city it's a district of), Ruled by,
Population, Cultures, Languages, Founded, Ended, How it ended and Status. Sections: About, Districts, People, Economy, History.

### Locations

Type, Part of, **Built**, **Ended**, **How it ended**, Ruled by, Population, Cultures and Languages.

### When places began and ended

Every kind of place, and every organization, has a start and an end date: a nation is **Founded** and **Fell**, a
region is **Formed** and **Ended**, a settlement is **Founded**, a location is **Built**, an organization is
**Founded** and **Dissolved**. **How it ended** says what happened ("Razed", "Conquered by Tevinter", "Sank"), and the
timeline and calendar word it that way ("Kingsport is razed"). Both dates take any calendar. The page shows how long it
stood and how long ago it began or ended, both dates go on the timeline and the Calendar page (with yearly
anniversaries until it ends), and anything that has ended says so in its list.

### Through history: names, owners, destruction

A place or group that lives for centuries changes. **Through history** on its page (**Add a change**) records each
change with its date:

```yaml
changes:
  - "Renamed from Port Aldis to Kingsport (1050 AD)"
  - "Conquered from [[Westmarch]] by [[Tevinter Imperium]] (12 Haring, 1102 AD), after a six-month siege"
  - "Destroyed by [[The Blight]] (1130 AD)"
  - "Rebuilt (1150 AD)"
  - "Became independent (1200 AD)"
  - "The great fire (1066 AD)"
```

- **What happened**: renamed; conquered, annexed, ceded, granted, inherited, sold, merged or changed hands; became
  independent; besieged, sacked or occupied; destroyed, razed, abandoned, fell into ruin, sank or disbanded; rebuilt,
  resettled, restored or refounded; or anything else as a dated note.
- **Names**: the page says what it is called in the present day, the timeline uses the name it had at the time
  ("Port Aldis is founded", "Kingsport is conquered by…"), and searching for an old name finds it.
- **Owners**: the page lists everyone who held it, with years. On a settlement, nation or organization, whoever holds
  it as of the present date is written into its **Nation** or **Part of** field, so the new owner's page lists it.
  Nations and organizations get a **Held over time** section: what they hold now and what they held once.
- **Standing**: a destruction that hasn't been rebuilt counts as its end, without needing the Ended field.
- Every dated change goes on the timeline (filter by the nation to see what it won and lost) and on the Calendar
  page.

### Linking places

Anywhere a place is asked for (a birthplace, a residence, where an event happened, a culture's lands, a creature's
habitat, where a language is spoken, an item's origin), any of the four kinds will do.

### Sorting older locations

Projects from before places were split up have everything under Locations. **Sort into nations, regions…** on the
Locations page (or the **Sort locations into nations, regions and settlements** command) lists every location with a
guess from its Type and name: "Kingdom" becomes a Nation, "Continent" a Region, "City" a Settlement. Change any guess
before moving. To change a single place, use the swap icon on its page or **Change kind of place…** in its right-click
menu.

- Links keep working, and subfolders carry over (`Locations/North/Kingsport.md` becomes
  `Settlements/North/Kingsport.md`).
- A city that was **Part of** a kingdom becomes a settlement of that nation.

## Maps

A map is an image with your world drawn onto it: pins for cities and buildings, outlined areas for nations and
regions, and free text labels for seas and mountain ranges. Everything on it links to an entry.

### Making a map

**Maps** is under Places (or **Create map**). Name it, then **Upload an image** from your computer or tablet (it is saved
in `Maps/Images/`) or **Choose from vault**. A map can be of anything: the world, a region, a city, a castle's floor
plan, a battlefield. **Map of** (in the map's options) ties it to the place it shows.

### Drawing on it

| Tool | What it does |
| --- | --- |
| **Move and select** | Drag to pan, scroll or pinch to zoom. Tap a pin, area or label to see it; double-tap to open its entry. Drag pins and labels to move them. |
| **Drop a pin** | Tap the map, then choose the entry it is (or create one). |
| **Draw an area** | Tap each corner in turn. Tap the first corner, double-tap, or press Enter to finish, then choose the entry. Undo point and Cancel are in the toolbar. |
| **Add a label** | Tap and type: "The Narrow Sea". |

- **Reshaping an area**: select it, then drag its corners. The small dots between corners add a new corner where you
  drag them. Right-click a corner, or tap it and press **Remove corner**, to take one away.
- **Nation colors**: a nation has a **Map color** (on its page, or from its area's **…** menu). Its areas, and the
  pins of every settlement and location inside it (through **Nation** or **Part of**), are drawn in that color on
  every map. Without one, it gets a color from its name. Regions can have a Map color too; other areas get a color
  from their name, or one you pick in the area's **…** menu, including any custom color.
- **Pins by type**: each pin is drawn by its entry's **Type**. A "Capital City" (or any settlement a nation names as
  its **Capital**) is a star; ports get an anchor, forts a castle, cities a large dot, villages a small one, and so
  on. Nation areas are solid and region areas dashed.
- **Map key**: the list button shows a key of what's on the map and the nations in it. Click a line (or **Pin
  styles for each type of place…** in the map's options, or **Drawn as …** on a selected pin) to choose, for each
  Type, the marker (dot, ring, square, diamond, triangle, star, or an icon such as an anchor, castle, temple or
  tavern), its size, how its name is written (plain, bold, capitals, italics, with its type, or only on hover) and
  whether the name shows when zoomed out. The choices apply to every map.
- **Anything can be pinned**: places, characters, organizations, events, creatures, items, even another map. A pin
  to a city's own map opens that map, so you can drill down from the world to a city to a building.
- A pin or area can also just have a name, without linking to an entry ("Old watchtower").
- **Show** chips filter what is on the map by kind; **Find on map** jumps to anything by name.
- The card for a selected place shows who holds it now and whether it has fallen, from its
  [history](#through-history-names-owners-destruction), and which other maps it is on.
- Keys: Esc cancels or deselects, Delete removes the selection, + and − zoom.

### Through time

The clock button opens the **year slider**. Drag it, press play to run through the years, or type any date in any
calendar. **Years in** works like the timeline's: count in any of your calendars, or **In use at the time**, which shows
each year in the calendar people used then. It starts on the timeline's choice and remembers its own after that. The
slider spans everything dated on the map, or your whole timeline while the map has nothing dated yet. At each year:

- Places appear from the year they were founded, built or formed. A destroyed or abandoned settlement or building
  shows as ruins (a hollow pin) until it is rebuilt; a nation or region that fell disappears.
- Names are the ones used at the time: "Port Aldis" before 1050, "Kingsport" after.
- **Color by holder** colors every place by whoever held it that year, from its
  [history](#through-history-names-owners-destruction). Draw each province or territory as its own area, and as they
  are conquered, ceded or inherited they turn the conqueror's color, so you watch empires grow and shrink.
- The selected place's card says what it was called, who held it and whether it still stood that year.

**Borders that move.** Any pin, area or label can be shown for only some years ("900 – 1102", "from 1102",
"until 1200"; **Show only for some years…** in its menu). To change a border, move the slider to the year it changes,
select the area and press **Redraw from** *that year*: the old shape now ends the year before and a copy starts that
year, ready to reshape. Without the slider open, the map shows each shape as it stands at the present day.

### On entry pages

Every entry on a map gets an **On the map** section: a cropped preview of each map it is on, which opens the map
centred on it. **Place a pin on a map** and **Draw it on a map** there (or the **Place the current entry on a map**
command) open a map ready to place that entry.

### How maps are stored

The map note keeps everything as positions on the image (0 to 1 across and down), so a redrawn or higher-resolution
image of the same map keeps every pin in place:

```yaml
type: map
image: "[[world.png]]"
of: "[[The Known World]]"
pins:
  - "[[Kingsport]] | 0.51234, 0.33410"
  - "Old watchtower | 0.20000, 0.30000"
areas:
  - "[[Westmarch]] | 0.1200,0.3000 0.1800,0.3300 0.2000,0.4100 | red | 900 – 1101"
  - "[[Westmarch]] | 0.1200,0.3000 0.1600,0.3100 0.1700,0.3800 | red | from 1102"
labels:
  - "The Narrow Sea | 0.40000, 0.61000"
places:
  - "[[Kingsport]]"
  - "[[Westmarch]]"
```

An area's color can be a theme color name or a hex color ("#3a7bd5"). The years a shape is shown are optional, last on its line. `places` lists every linked entry so backlinks and the graph see them. Renaming an entry updates its pins and areas.

## Species, creatures and plants

### Species

Three layers. A species' **Classification** sits above it ("Person", "Animal", or a path like "Animal › Bird").
**Subspecies of** sits below, as many levels deep as you like, and a subspecies without its own classification
inherits its parent's.

```
Person   › Human › Highlander, Lowlander
Animal   › Dog   › Sheepdog, Hound
Animal   › Bird  › Raven
```

- The Species page groups everything under its classification, with subspecies indented under their parents.
- Each species page lists its characters, including those of every subspecies.
- A character's header shows the whole line ("Highlander · Human · Person").
- Note names are unique, so name subspecies in full ("Highland Pony", not "Highland").

### Hybrids and ancestry

- For a one-off mix, give a character more than one Species ("Wolf, Dog").
- For a mix with a name of its own, make it a species and set **Hybrid of** ("Wolfdog" → Wolf, Dog).
- **Ancestry** is worked out from the family tree: each parent gives half, all the way up. A character with parents of
  different species gets a line like "Ancestry: ½ Wolf, ½ Dog", "¾ Dog, ¼ Wolf" a generation later, or
  "Human (½ Highlander, ½ Lowlander)" within one species. Named hybrids count as their parts.
- If the parents can't have produced the species you set, the line becomes a dashed "Parents: …" warning, which is
  fine for someone who was changed by magic or science and a continuity check otherwise.

### Bestiary and Flora

Creatures and plants are their own kinds of entry, kept apart from Species (which is for peoples your characters
belong to). Each has its own folder (`Bestiary/`, `Flora/`).

- **Creatures**: Classification, Variant of, Threat, Mind (animal, cunning, sapient), Temperament, Size, Diet,
  Lifespan, Rarity, Active (nocturnal, winter only) and Habitat; Abilities, Weaknesses and Yields; Companions
  (characters) and Kept by (cultures, organizations). Sections: About, Appearance, Behavior, Lore, plus Ecology.
- **Plants**: Classification, Variant of, Toxicity, Rarity, Season, Climate, Habitat, Useful parts, Uses and Grown by.
  Sections: About, Appearance, Uses, Lore, plus Cultivation.

Both work like species: Classification groups the list, variants nest under their parent, and the page shows key facts
at the top (deadly threats and toxins in red). Characters have a **Creatures** field for pets, mounts and companions,
kept two-way with the creature's Companions. Items have **Made from**, events can involve creatures, and places list
the creatures and plants that live there.

**Moving existing species**: **Move to Species, Bestiary or Flora** (on a species page and in its right-click menu)
moves the entry and everything filed under it, renaming Subspecies of to Variant of and Homeland to Habitat, with every
link kept. **Move a whole classification of species to the Bestiary or Flora** moves a whole group at once.

## Stories, chapters and scenes

- **Story notes** hold the synopsis, themes, main characters, locations, status, word goal, deadline, present date and
  the calendar the story's dates are read in.
- **Chapters board**: chapters and scenes with word counts, clickable status dots (draft / revised / done), reordering
  through menus, moving scenes between chapters, and compiling a story into one note. Scenes and chapters attached to
  an outline card show that beat's name.

## Outlines and plot arcs

### Outline

One per story, opened from the story card, the chapters board or **Open story outline**. Start from a structure
(three-act, Save the Cat, hero's journey, seven-point, kishōtenketsu, Freytag, blank, or one you saved yourself), then
rename, add and reorder beats. Each plot line is a column: write cards under each beat, attach scenes or chapters to
them, or turn a card into a new scene. Saved as `<Story> outline.md` in the story folder:

```markdown
## Act 1: Inciting incident
> The event that upends normal life.

### Main
- Elena finds the letter.
  → [[Chapter 2/Scene 1|Scene 1]]
```

### Plot arcs

An optional `type: arc` entry for a thread you want to develop in depth, with Premise, Stakes and Resolution. Link a
plot line to it from the outline's column menu, and the arc's page lists every card on that line and its events.

## Time: events, timeline and dates

### In-world dates

Set when a story, chapter or scene takes place (the story's **Present date**, or **Set chapter date** /
**Set scene date** on the chapters board). Character pages show their age, appearances show their age in each scene
(red if the scene falls before birth or after death), and organizations, nations, events and the timeline show
"N years ago". Ages count from the latest date in the project.

Write dates however your world writes them:

- "6 October 2026", "October 6, 2026", "6 Oct 2026", or a date property ("2026-10-06").
- Your own calendar's months and years: "14 Thaw, 1041 AF", "8 Harvest, 9:41 Ninth".
- A year on its own: "1041 AF", "9:41 Ninth", "-395 Old".
- Dates in a calendar other than the usual one can name it: "Coastal: 3 Early Spring, 400" or
  "3 Early Spring, 400 (Coastal)". See [Which calendar a date is in](#which-calendar-a-date-is-in).

### Events

An event has a **Starts** and an **Ends** date, and both take a full date in any calendar and any way of writing
years.

- Leave **Ends** empty for something that happened on one day.
- **Ends** can leave out the year ("10 Harvest"). It's then the next such day after the start, so a siege from
  "20 Long Night, 1041 AF" to "5 Thaw" ends in 1042 AF.
- The event's page says how long it lasted ("1 year, 165 days", "3 days") and what both days are in your other
  calendars, or why a date can't be read.
- Other fields: Calendar, Era, Type, Involved (characters, organizations, cultures, species, creatures), Where and
  Plot arcs. Sections: About, Causes, Consequences.

Older notes that used **Sort year** and an **Ends** year still read the same.

### Timeline

Events in historical order, grouped by era, with characters' births and deaths and when organizations and places
were founded, formed or built and when they ended. Filter to one character, organization, culture or plot arc. Characters get a
Timeline section, arcs an Events section.

- Every date is sorted by the day it falls on, whatever calendar it's written in. An event sorts by the day it starts.
- Events that last show their span ("1040 AF–1042 AF") and how long they lasted.
- **Years in** (when the project has more than one calendar) shows every year in the calendar you pick, or in
  **In use at the time**: each date in the calendar people used then, with a heading wherever the reckoning changes.
  Entries written in another calendar carry its name and the converted day.
- Calendars with eras get a heading at the start of each era ("Third Age, 100 years").
- **Calendar history** (dashed entries, hidden with the **Calendar history** button): eras beginning, calendars coming
  into and falling out of use, calendar changes, holidays first and last held, and history notes.

## Calendars

A project can keep as many calendars as its cultures use, and they all count the same days: a date written in one lands
on the right day of every other.

- The first calendar is the **primary** calendar, at `Lore/<Project>/Calendar.md`. It reads dates that give no other
  clue, and its years are the ones shown on ages, roles and "years ago". Others go in `Lore/<Project>/Calendars/`.
- Each calendar is a note with `type: calendar`. The calendar editor writes it for you; you can also edit it by hand.

### Making a calendar

The calendar-plus button on the Calendar page, the **Create calendar** command, or **Settings → Loresmith →
Calendars → New calendar**. Start from:

- **Blank**: your own months, week and moons.
- **Modern (Gregorian)**: January to December with leap years, the real week and Earth's moon.
- **Thirteen months of 28 days**: every month starts on the same weekday, plus a year day and a leap day.
- **Twelve months of 30 days + 5**: twelve even months and five festival days, with a leap day every fourth year.
- **Lunar**: months of 30 and 29 days with a leap month in some years.
- **A copy** of one of your calendars, to change from there.

### The calendar editor

The pencil on the Calendar page, or **Edit a calendar**, opens one page with everything about a calendar. It shows the
length of the year, how years will be written and how the calendar lines up as you type.

- **Name**: name, short name and color. The short name marks dates written in it ("Coastal: 3 Early Spring, 400").
- **Kind of calendar**: modern or custom.
- **Months**: a table of names, days and leap rules (see below). Write "Frost/Fr" to accept a short form too.
- **Week**: one weekday per line, starting with the weekday of the first day of year 1. Leave it empty for no week.
  **Keep step with** another calendar pairs its weekdays with that calendar's (see
  [Weeks in step](#weeks-in-step)).
- **New Year**: the day the year number changes, if not the first day of the first month (see
  [New Year](#new-year-partway-through-the-months)).
- **Moons**: name, days per cycle, and the day after year 1 began on which it was new.
- **Years and eras**: how years are numbered (see [Eras](#eras)).
- **In use**: when people used the calendar (see [Calendars that come and go](#calendars-that-come-and-go)).
- **How it lines up**: one day you know in both calendars (see [Lining calendars up](#lining-calendars-up)).
- **Kept by**: the cultures, organizations, peoples, nations or places that use it.
- **Present day** (primary calendar): the world's "now", written in any calendar. Leave it empty for today on a modern
  calendar.

### Months and leap years

Each month has a name and a number of days. A leap rule adds days in some years:

| Leap rule | Means |
| --- | --- |
| `+1 every 4` | One extra day every fourth year |
| `+1 every 4, except every 100, but every 400` | The Gregorian rule |
| `0, +30 every 3` (as the month's days and rule) | A whole leap month that only exists every third year |

Leap days are counted exactly, so conversions between calendars never drift.

### Eras

Every calendar numbers its years with its own list of **eras**, oldest first. Each era has:

- a **name** and a **short form** (several spellings allowed: "BC/BCE"),
- how many **years** it lasts (blank for an open-ended era at either end),
- how its years **count**: *up from* a number (1, 2, 3 …), *up to* a number (… -2, -1), or *down to* a number
  (… 3, 2, 1),
- optionally, how its years are **written** (see the patterns below).

The first era that counts up is where the count starts; the others follow on before and after it. **Start from** in
the editor fills in each of these:

| Shape | Eras | Years read |
| --- | --- | --- |
| Plain years (the default) | BC/BCE, down to 1 · plain numbers, up from 1 | 395 BC, 2026 |
| BC and AD | Before Christ (BC/BCE), down to 1 · Anno Domini (AD), up from 1 | 395 BC … 1 BC, 1 AD … 2026 AD |
| Before and after a founding | Before the Founding (BF), down to 1 · After the Founding (AF), up from 1 | 120 BF, 1041 AF |
| One count through zero | (YC), up from 1 | -395 YC, 0 YC, 1 YC |
| Negative years, then ages | Old Era (Old), up to -1 · First Age (First), 100 years · Second Age (Second), 100 years … | -1195 Old, 1:1 First, 9:41 Ninth |
| Eras of different lengths | Before the Eras (BE), down to 1 · First Era (1E), 2920 years · Second Era (2E), 896 years · Third Era (3E), 433 years · Fourth Era (4E), open | 500 BE, 1E 2920, 4E 201 |

- **After the last era**: if the last era listed has a length, another era of the same length follows when it ends,
  and another after that, numbered until you name them. They count their years the way your last era does, so ages
  of 9:00–9:99 go on to 10:00, and ages of 1:1–1:100 go on to 2:1. **Then keep adding eras of N years** sets a
  different length. Leave the last era's length blank for an era that runs on (AD, 4E). Write "?" as the name of an
  era that isn't named yet.
- **Skip year 0** for a count that goes … -1, 1 … instead of … -1, 0, 1 ….
- **Years are written** sets the default pattern, and each era can have its own:

| Pattern | Example |
| --- | --- |
| `{y} {short}` | 1041 AF |
| `{short} {y}` | AD 1041, 4E 201 |
| `{n}:{y} {short}` | 9:41 Ninth |
| `{n}:{yy} {short}` | 9:05 Ninth (years always two digits) |
| `{y} {name}` | 41 Ninth Age |
| `Year {y} of the {name}` | Year 41 of the Ninth Age |
| `{y} {ord} {word}` | 41 9th Age |
| `{roman}.{y}` | IX.41 |

`{y}` is the year within the era (`{yy}` with at least two digits), `{n}` the era's number (the first era that counts up is 1), `{ord}` "9th",
`{roman}` "IX", `{word}` what eras are called (Age, Era). Any of these spellings is understood when you type a date,
so "Ninth 41", "9:41" and "9:41 Ninth" are the same year. Under every era the editor shows the years it covers as
they'll be written, and warns if two years would read the same.

Underneath, years count straight through, so ages, "years ago", sorting and converting between calendars all work
across era boundaries.

### New Year partway through the months

A calendar can keep its months in their usual order but change the year number on another day: a year running from
1 June to 31 May, a fiscal year from 1 October, or the old English year that began on 25 March.

- Set **The year begins on** ("1 June") and whether a year is numbered by the year it **begins** in or **ends** in.
- Leap days, weekdays and holidays stay where they are; only the year number moves. On a June-start calendar,
  "3 March 2026" is the March after June 2026 (plain 3 March 2027).
- The year view runs from the New Year's month to the month before it, dimming the days of a split month that belong
  to the year before or after.
- Write dates, including the line-up, the way this calendar numbers them. Lining up on a day just after the New Year
  ("1 June 2000 = 1 June 2000") is the easiest.

Two calendars with different months already start their years on different days: line them up and every date
converts.

### Lining calendars up

On any calendar but the primary, under **How it lines up**, write one day you know in both, with "=" between:

```
1 Early Spring, 1 = 14 Thaw, 900 AF
```

From that one day, every date converts exactly in both directions, and a calendar can line up against any other, not
only the primary. As you type, the editor:

- shows where the present day falls in this calendar,
- says whether the two years are the same length. If they aren't, it warns how far they drift apart each year: a
  330-day year next to a 360-day one moves a month a year, which is right for calendars that really differ, and a
  sign of a missing month when they shouldn't,
- lists this calendar's months next to the other's, starting from the line-up day, so you can check they match.

Until a calendar is lined up, its year 1 is taken to begin on the same day as the primary's, and the Calendar page
reminds you.

### Weeks in step

Each calendar's week counts from its own year 1 unless you say otherwise. Under **Week**, choose **Keep step with**
another calendar whose week has the same number of days, and the weekdays pair up in order on every day
(Restday = Sunday, Workday = Monday, …).

### Calendars that come and go

A calendar's **In use** dates ("from 1:1 First", "until 1:20 First", written in any calendar) say when people actually
used it. A world can keep one count for twelve centuries, switch to a new calendar, and have another people's calendar
alongside, each in its own period.

- Outside its years, a calendar's holidays aren't kept.
- Its adoption and end go on the timeline with the calendar history.
- **In use at the time**, under **Show** on the Calendar page and **Years in** on the Timeline, shows each day in the
  calendar people used then. Where two calendars were in use at once, the primary is used.

### Which calendar a date is in

When a date doesn't name its calendar, Loresmith checks, in order:

1. a calendar named on the date ("Coastal: 3 Early Spring, 400" or "3 Early Spring, 400 (Coastal)"),
2. an era or short form only one calendar uses ("400 AF"),
3. month names only one calendar uses ("Frost"),
4. the entry's own calendar: its **Calendar** field, its story's, or a calendar kept by its culture, nation, house or
   group,
5. the primary calendar.

Moons belong to the world, so every calendar shows the same moons in the same phase. List each moon in one calendar
only.

### Converting dates

**Convert a date between calendars** (command, or **Settings → Loresmith → Calendars → Convert a date**): type a date
in any calendar and see it in all of them, with weekdays, ready to copy. Characters, events, organizations and nations
also show their dates in your other calendars under the date fields.

### The calendar note

For anyone who prefers typing, this is what the editor writes:

```markdown
---
type: calendar
short: Northern
custom_calendar: true
align: "1 Frost, 1 AF = 1 January, 900"
kept_by:
  - "[[Northern Culture]]"
week_like: "Calendar"
in_use_from: "1 Frost, 1 AF"
---
## Months
- Frost, 30
- Thaw, 30
- Sowing, 30
- Blossom, 30
- High Sun, 30
- Harvest, 30
- Falling Leaf, 30
- Long Night, 35, +1 every 4

## Weekdays
- Restday
- Workday
- Marketday

## Moons
- Moon, 29.5, 0

## Eras
- Before the Founding (BF), , down to 1
- After the Founding (AF), , up from 1

## History
- Midwinter Feast: 1 Frost
- Founders' Day: 3 Thaw (from 1012)
- Feast of Lanterns: 14 Sowing (until 1050), forgotten after the plague
- Harvest Night: last Marketday of Harvest
- 1050: The Great Plague.

## Months (from 1100)
- Summer, 180
- Winter, 185
```

| Property | Meaning |
| --- | --- |
| `primary` | `true` on the primary calendar |
| `present` | The world's present date (primary calendar); empty for today |
| `short`, `aliases`, `color` | Names a date can be marked with, and the calendar's color in the views |
| `custom_calendar` | `false` for the modern calendar |
| `align` | The line-up: a day here, "=", the same day on another calendar |
| `kept_by` | Who uses it |
| `week_like` | Another calendar whose weekdays this one keeps step with |
| `new_year`, `new_year_numbering` | The day the year number changes, and `start` or `end` |
| `in_use_from`, `in_use_until` | When it was used |
| `era_repeat`, `era_format`, `era_word`, `no_year_zero` | Eras that keep coming, the default pattern, what eras are called, and skipping year 0 |

- **History** holds holidays as plain lines ("Name: day Month", or a weekday rule such as "fourth Thursday of
  November"), with years in brackets for when they were kept ("(from 1012)", "(until 1050)", "(1000–1020)"; here the
  end year is the first year it isn't held). Lines that start with a year are history notes.
- **Calendar changes**: a section with a year in its heading, like `## Months (from 1100)` or
  `## Weekdays (from 1100)`, takes over from that year. Day counts, weekdays and moons run on unbroken. Write "Modern"
  in a dated Months section to switch to January to December.
- Notes from earlier versions of Loresmith (the BC/era switches, the old `## Ages` section, and calendar settings from
  the settings page) keep reading the same, and the editor brings them up to date the next time you save.

## Holidays

A holiday is its own kind of entry: an event happened once, a holiday comes back every year, on the calendar of the
people who keep it.

- **When**: one row per calendar it's kept on. Pick the calendar (or let Loresmith work it out from the month names),
  write the day with no year ("1 Frost", "July 4", "last Marketday of Harvest", "fourth Thursday of November"), and, if
  that date was only kept for part of history, its years ("from 1012", "1012–1050", "from 100 until 199"; the last year
  given is the last year it was kept). **Add a date on another calendar** adds a row. A note after a comma
  ("20 Long Night, the longest night") shows in the day's details.
- **Lasts (days)**: for festivals longer than a day.
- **First held** and **Last held**: the years the holiday itself was kept, on every calendar, written in any calendar.
- **Type**, **Kept by** (cultures, organizations, species, nations, places) and **Commemorates** (an event).
- About, Traditions and History sections.

A holiday the northerners keep on 1 Frost and the coastal people on 20 Early Winter is one entry with two rows; when two
rows land on the same day, it shows once. In the note, **When** is `date`, one line or a list:

```yaml
date:
  - "Northern: 1 Frost"
  - "Coastal: 20 Early Winter (from 100 until 199), the longest night"
```

The page lists each date with when it next falls, then the soonest of them in every calendar, how long the holiday has
been kept, or what's wrong with a date ("Frosts" isn't a month on the Northern calendar). Holidays from older versions
(one date plus a Calendar link) keep working.

## The Calendar page

Places every dated event, birth, founding and scene on its day, with weekdays, moon phases and holidays, whichever
calendar each date was written in.

- **Show** picks the calendar to look at, or **In use at the time**. **Alongside** adds a second calendar: every day in
  the month view carries its date in the other calendar too, and each month in the year view says which months of the
  other calendar it spans. Switching calendars keeps you on the same days.
- **Year** and **Month** views. Tap a day or a month name in the year view to open that month. **Go to a date** takes
  a date in any calendar, and **Present** jumps back to the present day.
- A line under the toolbar shows the era you're in and how far through it ("Ninth Age, year 41 of 100").
- In the month view, tap a day for its weekday, the same day on every other calendar (tap one to switch to it),
  holidays, moon phases, everything on that day, **New event on this day**, **New holiday on this day** and a
  copy-date button. With no day picked, the side panel lists the month as an agenda.
- Events that last several days show on every day they run ("Day 2 of 3"), or on their first and last days if they
  went on for more than a year and a half.
- Birthdays and anniversaries repeat every year of the calendar they were written in ("Elena turns 25", "Siege of
  Kingsport · 20 yrs"); round anniversaries are bold, and birthdays stop after a character dies.
- Holidays of other calendars show in that calendar's color with a ◆.
- Scenes without their own date use their chapter's or story's date.
- The legend is also the filter: tap a kind to hide or show it.
- Moons are drawn at their real phase; the exact new, quarter and full moon days are outlined.
- Warnings appear when a calendar isn't lined up yet, or wasn't in use in the year you're looking at.

## Languages and the dictionary

### Languages

A language is its own kind of entry, so a world can have as many as it needs: invented, dead, ritual or trade
languages, and real ones your characters borrow from (set **Basis** to Real-world).

- **Type**, **Status** (living, dying, dead), **Language family**, **Descended from** and **Also called**.
- **Spoken by** (cultures), **Species**, **Spoken in** (nations, regions, settlements or locations) and **Speakers**.
- **Word order** and **Script**.
- About, Sounds, Grammar, Writing and History sections.

Cultures and places have a **Languages** field kept in step with the language's Spoken by and Spoken in. A language's
page shows its own dictionary, the words it lent to other languages, and its daughter languages.

### Dictionary

`type: word` entries with meaning, part of speech, pronunciation and other forms, plus **Language**, **Used by**
(cultures), **Borrowed from** and **Original word** for loanwords, and **Register** (formal, slang, archaic, ritual).

- Group the Dictionary **by language**; the **+** on a language heading starts a new word in it.
- **Hover a word in a scene** to see its definition. When the same spelling exists in two languages, the tip shows
  both.
- The sidebar lists the invented words in the scene you are writing.

## Relations web

A graph of your entries built from the relationship engine, so ties written on either note and family it works out
all appear. Parents and children, siblings, extended family, marriage, partners, friends and allies, mentors, rivals
and enemies, membership, Relation entries, past ties, shared scenes and other links each have their own line style
and can be switched off. Each end of a line keeps its own label.

Drag a dot to pin it (pins are saved per project), tap to see its ties, double-tap to open it, and pinch or scroll to
zoom. **Show in relations web** on any entry jumps there.

## Who has met whom

Pick a character from the portrait strip to see everyone they have shared a scene with, closest first, with their
relationship and first scene together, plus who they have never met. Or switch to the grid of everyone. **Tied but
never together** lists close family, friends and rivals who never share a scene. The sidebar shows how the people in
your current scene are related and flags first meetings.

## Writing log

Opened from the top of the navigation, the sidebar's home page, or **Open writing log**. Four tabs:

- **Today**: active typing time, characters typed, pasted and deleted, net words, peak and current speed, with chips
  to count scenes, lore and other notes together or apart. Rings for the daily word goal and a daily typing-time goal.
  A pomodoro that counts typing time only, so it waits while you think (also in the status bar, and **Start pomodoro**
  in the command palette). The note you last typed in, with this session's numbers and a words-over-time chart.
- **Trend**: 7, 30 or 90 days of typed, active time, net words, pasted or peak speed, stacked by kind, and an 18-week
  heatmap.
- **Goals**: the daily word goal, streak, history, and per-story word goals with deadlines.
- **Authorship**: for a story, how long each scene took to type, how much was typed versus pasted, and whether each
  scene still matches what was there when you last finished typing it. **Export report** writes
  `<Story> authorship report.md` next to the story.

### How tracking works

- Every change in the editor is sorted by how it arrived: typed (including autocorrect and autocomplete), pasted or
  dropped, deleted, undone or redone, or inserted by a command or another plugin. Typing in Loresmith's own text
  boxes counts too.
- Scenes, lore (other notes in the lore folder) and other notes (the rest of the vault, which you can switch off) are
  kept apart.
- Typing time adds up the gaps between keystrokes shorter than the idle limit (30 seconds by default).

### Sessions and seals

A session is a stretch of typing in one note with no break over 20 minutes. When it ends, the note's text (without its
properties) is fingerprinted with SHA-256 and the session is sealed by hashing it with the seal before it. If a note's
text changes between sessions without being typed in a tracked editor, the next session is flagged, and altering an
old session breaks the chain, which the Authorship tab and report check.

The log is stored as `typing/<device>.json` in the plugin folder, one file per device, so devices syncing the same
vault never overwrite each other. The log is evidence rather than proof; keeping a dated copy of the latest seal (an
email to yourself, for example) whenever you finish a draft pins the record in time.

## Generators

Roll a **Story prompt**, **Plot**, **Character** or **Place**, look it over, then save it as a real entry. Open them
from the **Generators** group in the navigation or the sidebar, or with the **Generate: …** commands.

1. Pick an audience (Middle Grade, Young Adult, New Adult, Adult, Adult with mature themes, or Random) and a genre
   family (Fantasy, Science Fiction, Horror, Mystery, Thriller, Romance, Historical, or Random). Characters and places
   can also have no genre.
2. Press **Roll**. Every field has its own dice to reroll it and a lock; locked fields stay put when you roll again.
   Every box can be edited by hand.
3. Name it and **Save**.

| Generator | Saved as | What gets filled in |
| --- | --- | --- |
| Story prompt | A note in `Notes/Prompts` | Genre, setting, theme, tone, central conflict, plot tropes, two characters and their dynamic |
| Plot | A plot arc | Premise (genre, theme, tone, inciting incident, conflict, tropes), Stakes, Resolution (twist, ending) |
| Character | A character | Occupation, build, features, traits, flaws, skills and fears; archetype and genre tropes as attributes; wound and motivation in Author's notes; the inner conflict in Psychology |
| Place | A location | Type, About, Points of Interest, History (secret and trouble brewing) |

A story prompt's two characters can be saved as characters too, linked to each other by the rolled relationship
(siblings, rivals, mentor and student, and so on). Everything saved is tagged `generated`. A generated place can be
turned into a nation, region or settlement afterwards with **Change kind of place…**.

### Generator tables

The lists the generators roll are [Randomness](https://github.com/Obsidian-TTRPG-Community/Randomness) generator files
(`.rdm`), published in this repository's [`generators/`](generators) folder, so the Randomness plugin must be enabled.

- **Install them** with **Settings → Loresmith → Generator tables → Install or update**, the **Install or update
  generator tables** command, or the button the Generators page shows when tables are missing.
- They are downloaded into `<Randomness Generator root>/Loresmith/`, or `Lore/Generators/` when Randomness has no
  Generator root, from the release tag matching your version of Loresmith (falling back to `main`).
- **Your edits are safe**: a file you have edited is never overwritten; the new version is saved beside it as a `.txt`
  to copy from. A file whose tables you already have elsewhere in the vault is skipped, so nothing is defined twice.

### Audience-appropriate lists

Every table is tried in the audience's own version first. For Middle Grade that is `<Table> MG`, then `<Table> YA`,
then `<Table>`; for Young Adult `<Table> YA`, then `<Table>`. To keep a list age-appropriate, add an `MG` or `YA` copy
with the unsuitable lines removed. Middle Grade never rolls Romance.

### Adding your own

The generators are the `GENERATORS` list near the top of `main.js`. Each field names the Randomness table it rolls,
with `{family}` standing for the chosen genre ("{family} Plot Tropes" becomes "Horror Plot Tropes"), and `count`
rolling several different results. See [`generators/README.md`](generators/README.md) for adding tables.

## Name builder

Run **Name builder**, use the dice on a culture page, or **Roll a name** when creating a character. Fill in a
culture's Naming lists (starts, middles, ends), or let it learn from the names already used in that culture.

## Moodboards and tension

- **Moodboards**: images on any entry, chapter or scene (`moodboard:`). The sidebar shows the moodboard for the scene
  you are writing, gathered from the scene, its chapter, its cast and the story.
- **Tension graph**: rate scenes 1 to 5 with the number button on the chapters board (`tension:` in the scene) and
  toggle **Tension** for a graph of the whole book.

## Export

**Export** on the chapters board, or the export commands, produce:

- **Manuscript (.docx)**: a standard manuscript with a title page and word count, 12 pt double spacing, a
  "Surname / TITLE / page" header, chapters on new pages and `#` scene breaks.
- **Ebook (.epub)**, with the story's image as the cover.

Files are saved next to the story note. Headings and `%%comments%%` in scenes are left out. Your name and contact
details go under **Settings → Loresmith → Manuscript and ebook**.

## Commands

| Command | What it does |
| --- | --- |
| Open overview | Opens the main view |
| Open sidebar panel | Opens the compact panel in the right sidebar |
| Switch project | Picks the active project |
| Create entry / character / story / event / holiday / plot arc / creature / plant / language / dictionary word | Creates an entry of that type |
| Open current note in lore editor | Opens the active note in Loresmith's entry editor |
| Open chapters for current story | Opens the chapters board |
| Open story outline | Opens a story's outline |
| Characters in this scene | Edits the active scene's cast |
| Add an empty characters property to scenes that lack one | Prepares older scenes for scene casts |
| Open relations web | Opens the relations web |
| Open timeline / Open calendar | Opens the timeline or the Calendar page |
| Open a map / Create map | Opens or makes a map |
| Place the current entry on a map | Opens a map ready to pin or draw the entry you are in |
| Open calendar note | Opens a calendar's note, asking which one |
| Edit a calendar | Opens the calendar editor |
| Create calendar | Makes a new calendar from a template or a copy |
| Convert a date between calendars | Shows a date in every calendar |
| Sort locations into nations, regions and settlements | Sorts older locations into the new place categories |
| Open who has met whom | Opens the meetings view |
| Open writing log | Opens goals, typing time and authorship |
| Start pomodoro | Starts a pomodoro that counts typing time |
| Export authorship report for a story | Writes the authorship report |
| Export manuscript (.docx) / Export ebook (.epub) | Exports the current or a chosen story |
| Make relationship links two-way | Fills in missing sides of links across the project |
| Move a whole classification of species to the Bestiary or Flora | Moves a group of species |
| Name builder | Opens the name builder |
| Generate: story prompt / plot / character / place | Opens a generator |
| Install or update generator tables | Downloads the generator tables into the vault |

## Settings

- **Lore folder**: the folder whose subfolders are projects (`Lore` by default).
- **Open entries in a new tab**.
- **Relationships**: **Keep links two-way**, and **Fill in missing sides now**.
- **Writing goals**: the daily word goal and whether the status bar shows today's words.
- **Typing log**: whether notes outside the lore folder are tracked, the idle limit (seconds), a daily typing-time
  goal and the pomodoro length.
- **Calendars**: every calendar in the project with its months, week, period of use and who keeps it, and buttons to
  edit it, open its note or make it the primary; **New calendar**; the **Present date**; and **Convert a date**.
- **Generators**: install or update the generator tables, with a status line showing whether they are all found.
- **Manuscript and ebook**: your name, byline, contact details, manuscript font and ebook language.
