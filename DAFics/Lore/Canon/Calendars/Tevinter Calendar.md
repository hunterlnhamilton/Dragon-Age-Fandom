---
type: calendar
custom_calendar: true
short: Tevinter
align: 0 TE = -1195 Ancient
new_year: 1 Verimensis
week_like: Chantry Calendar
---

%% Loresmith reads this note. With custom_calendar and custom_eras off, the world uses the modern calendar,
and an empty "present" means today. Anything between double percent signs is ignored. %%

## Months

%% Used when custom_calendar is on. One per line, in order: name, number of days.
If the calendar changes partway through history, add another section such as "## Months (from 1100)".
Write "Modern" in a dated section to switch back to January to December. %%
- Verimensis, 30
- Pluitanis, 30
- Nubulis, 30
- Eluviesta, 30
- Molioris, 30
- Ferventis, 30
- Solis, 30
- Matrinalis, 30
- Parvulis, 30
- Frumentum, 30
- Umbralis, 30
- Cassus, 30

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

- TE (TE), , up from 0, "{y} {short}"

## History

%% The easy way to add holidays is the Holidays tab, under History. You can also write them here,
one per line: "Name: day Month". Add years in brackets for when it was kept, and a note after a comma:
- Midwinter Feast: 1 Frostmoon
- Founders' Day: 3 Frostmoon (from 1012)
- Feast of Lanterns: 14 Seedtime (until 1050), forgotten after the Grey Plague
- Harvest Night: last Moonday of Seedtime
Lines that start with a date are history notes, shown on the timeline and calendar:
- 1050: The Grey Plague. Nobody lights the lanterns that autumn. %%
