---
type: calendar
custom_calendar: true
short: Elvhen
color: green
in_use_from: "1"
align: 1 Soun'vun'ise'man 1 FA = 1 Solace -7600 Ancient
no_year_zero: true
new_year: 1 Soun'vun'ise'man
week_like: Chantry Calendar
---

%% Loresmith reads this note. The easiest way to change it is Edit calendar, on the Calendar page.
Anything between double percent signs is ignored. %%

## Months

%% Used when custom_calendar is on. One per line, in order: name, number of days, and a leap rule if it has one:
"Poa, 27, +1 every 4" or "+1 every 4, except every 100, but every 400". A 0-day month with a rule is a leap month.
If the calendar changes partway through history, add another section such as "## Months (from 1100)".
Write "Modern" in a dated section to switch back to January to December. %%
- Vare'eir'man, 30
- En'tara'syl'nu'man, 30
- Em'syla'man, 30
- Soun'tara'syl'nu'man, 30
- Adahl'shena'man, 30
- Ena'vun'ise'man, 30
- Soun'vun'ise'man, 30
- Alas'mamae'man, 30
- Alas'davhen'man, 30
- Tua'sal'adahl'man, 30
- Ena'eir'man, 30
- Bre'eir'man, 30

## Weekdays

%% Used when custom_calendar is on. One per line, starting with the weekday of the first day of year 1.
A dated section such as "## Weekdays (from 1100)" starts its week on the first day of that year. %%
- Fel'vun'in
- Syl'vun'in
- Shi'vun'in
- U'lea'vun'in
- Ghi'lan'vun'in
- Hamiin'vun'in
- Lean'vun'in

## Moons

%% One per line: name, days per cycle, days after the first day of year 1 that it was new.
Moons belong to the world, so every calendar shows them. Leave empty for Earth's moon on the modern calendar. %%

## Eras

%% How years are numbered. Easiest to change with Edit calendar. One era per line, oldest first:
name (short form), length in years (blank: open-ended), how its years count, and optionally how they're written.
- Before Christ (BC/BCE), , down to 1          395 BC … 1 BC
- Anno Domini (AD), , up from 1                1 AD, 2 AD …
- Ancient, , up to -1, "{y} {short}"           -1195 Ancient … -1 Ancient
- Divine Age (Divine), 100, up from 1           1 Divine … 100 Divine
era_repeat: 100 in the properties keeps adding eras of that length after the last one. Empty: BC and plain years. %%
- Founding of Arlathan (FA), , up from 1

## History

%% The easy way to add holidays is the Holidays tab, under History. You can also write them here,
one per line: "Name: day Month". Add years in brackets for when it was kept, and a note after a comma:
- Midwinter Feast: 1 Frostmoon
- Founders' Day: 3 Frostmoon (from 1012)
- Feast of Lanterns: 14 Seedtime (until 1050), forgotten after the Grey Plague
- Harvest Night: last Moonday of Seedtime
Lines that start with a date are history notes, shown on the timeline and calendar:
- 1050: The Grey Plague. Nobody lights the lanterns that autumn. %%
