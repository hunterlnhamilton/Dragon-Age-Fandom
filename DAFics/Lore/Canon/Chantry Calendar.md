---
type: calendar
custom_calendar: true
short: Chantry
color: red
era_format: "{n}:{y} {short}"
no_year_zero: true
new_year: 1 Wintermarch
era_repeat: 100
---

%% Loresmith reads this note. With custom_calendar and custom_eras off, the world uses the modern calendar,
and an empty "present" means today. Anything between double percent signs is ignored. %%

## Months

%% Used when custom_calendar is on. One per line, in order: name, number of days.
If the calendar changes partway through history, add another section such as "## Months (from 1100)".
Write "Modern" in a dated section to switch back to January to December. %%
- Wintermarch, 30
- Guardian, 30
- Drakonis, 30
- Cloudreach, 30
- Bloomingtide, 30
- Justinian, 30
- Solace, 30
- August, 30
- Kingsway, 30
- Harvestmere, 30
- Firstfall, 30
- Haring, 30

## Weekdays

%% Used when custom_calendar is on. One per line, starting with the weekday of the first day of year 1.
A dated section such as "## Weekdays (from 1100)" starts its week on the first day of that year. %%
- Monday
- Tuesday
- Wednesday
- Thursday
- Friday
- Saturday
- Sunday

## Moons

%% One per line: name, days per cycle, days after the first day of year 1 that it was new.
Leave empty for Earth's moon on the modern calendar. %%
- The Moon, 30, 0
- Satina, 360, 0

## Eras

- Ancient (Ancient), , up to -1, "{y} {name}"
- Divine Age (Divine), 99, up from 1, "{n}:{y} {short}"
- Glory Age (Glory), 100, up from 0, "{n}:{y} {short}"
- Towers Age (Towers), 100, up from 0
- Black Age (Black), 100, up from 0
- Exalted Age (Exalted), 100, up from 0
- Steel Age (Steel), 100, up from 0
- Storm Age (Storm), 100, up from 0
- Blessed Age (Blessed), 100, up from 0
- Dragon Age (Dragon), 100, up from 0

## History

%% The easy way to add holidays is the Holidays tab, under History. You can also write them here,
one per line: "Name: day Month". Add years in brackets for when it was kept, and a note after a comma:
- Midwinter Feast: 1 Frostmoon
- Founders' Day: 3 Frostmoon (from 1012)
- Feast of Lanterns: 14 Seedtime (until 1050), forgotten after the Grey Plague
- Harvest Night: last Moonday of Seedtime
Lines that start with a date are history notes, shown on the timeline and calendar:
- 1050: The Grey Plague. Nobody lights the lanterns that autumn. %%
