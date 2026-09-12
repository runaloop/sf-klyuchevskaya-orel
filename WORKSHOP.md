# Steam Workshop listing

Paste the body below into the "Mod Description" field of the game's Create Mod
window, or into the Workshop page editor. Steam accepts BBCode, which the game's
upload dialog passes through unchanged.

- **Title:** SF Klyuchevskaya '88: Orel Edition
- **Preview image:** `mod/workshop_preview.jpg` (800×800, 112 KB)
- **Visibility:** public
- **Required items:** none

---

## Description

[h1]SF Klyuchevskaya '88: Orel Edition[/h1]

A modified edition of [b]SF Klyuchevskaya '88[/b] by [b]StickHeroes[/b]. The
campaign is his; two things are different here.

[h2]The flagship is a real carrier[/h2]

You sail with [b]TAVKR Tbilisi[/b], a Project 1160 Orel-class fleet carrier,
instead of the Kiev-class Minsk. Catapults, arresting gear, and an air wing that
can actually contest the sky:

[list]
[*][b]8 MiG-23A[/b] for fleet air defence, with beyond-visual-range missiles
[*][b]6 Ko-45[/b] for stand-off anti-ship and land attack
[*][b]2 Ko-45E[/b] for jamming and SEAD
[*][b]1 P-42RLDN[/b] for the airborne radar picture. One. Lose it and you are blind.
[*][b]4 P-42[/b] for ASW beyond helicopter range
[*][b]1 Ka-25TS[/b] and [b]4 Ka-27[/b]
[/list]

The wing is not a gift. Its size is set by the game's own turnaround times: a
MiG-23A needs 75 minutes between sorties, a Ko-45 needs over two hours. Eight
fighters hold one pair on station and nothing more. Six attack aircraft mean one
strike package, not two.

[h2]The escort is thin[/h2]

You start with 635 points at moderate difficulty. That buys one Project 1164
Atlant and one Project 956 Sarych, and then you are done. The carrier is the most
valuable hull in the Pacific Fleet and she has almost nothing around her. Ten
main missions and four side missions later you will know whether that was enough.

[h2]Nine languages[/h2]

Chinese, English, French, German, Japanese, Korean, Russian, Spanish and
Vietnamese. Not just the menus: all 14 mission briefings, all 20 newspaper and
intelligence interludes, the unit descriptions in the task force builder, and all
13 award citations.

The Russian follows the developers' own Russian campaign. Every language was then
gone through line by line against the English and corrected — message headers,
unit names, ship classes, and a fair number of real errors, including one that
made the Korean version address every signal to the "enemy aircraft fleet". None
of it was proofread by a native speaker. If something reads badly in your
language, say so in the comments and it gets fixed.

[h2]Fixes carried over[/h2]

Several defects in the original campaign and in the base game's Russian files are
repaired here, including award images and a mission path referenced in the wrong
letter case, which is invisible on Windows and breaks silently on Linux, and a
Russian callsign list that numbered two squadrons twice and left the campaign's
own fighters showing as "DEFAULT".

[h2]Load order[/h2]

[b]This mod needs nothing else. Do not subscribe to anything for it.[/b]

Subscribe, enable it, play. If you are also subscribed to the original
SF Klyuchevskaya '88, both campaigns appear side by side and you can play either;
put [b]Orel Edition above the original[/b] in the Mod Manager, because this one
ships a more complete callsign file for every language.

[h2]Credits[/h2]

The campaign, its missions, briefings, interludes and artwork are the work of
[b]StickHeroes[/b]. This edition exists because that campaign was worth extending,
and it will be taken down at his request without argument.

The Project 1160 Orel and its aircraft are base-game content by Triassic Games
and MicroProse.

Source and a full list of every change:
[url=https://github.com/runaloop/sf-klyuchevskaya-orel]github.com/runaloop/sf-klyuchevskaya-orel[/url]

---

## Before publishing

In this order. Mission sheet 04 keeps the original Kiev-class screenshot on
purpose: the Kiev-class is still purchasable in this edition, and there is no
second Tbilisi shot that would not duplicate the cover.

1. [ ] Play a new campaign through the first few missions. The current balance
       has never been played: a save started before it cannot show the new
       starting budget or the trimmed air wing.
2. [x] `tools/rename_campaign.sh SF_Klyuchevskaya_88_Orel` — done, the campaign
       folder is `SF_Klyuchevskaya_88_Orel` and nothing references the old id.
3. [x] Pushed to github.com/runaloop/sf-klyuchevskaya-orel; the link is in the
       description above.
4. [ ] Upload: Mod Manager → Create Mod → pick the mod folder, title and
       description from this file, preview image `mod/workshop_preview.jpg`,
       visibility public, no required items.

Settled: the naval message headers are now translated in all nine languages.
Each language uses the vocabulary it already used elsewhere in the campaign, and
where the game itself defines the term, the game's own: SECRETO in Spanish, MẬT
in Vietnamese, 机密 in Chinese. French and Spanish keep FLASH, which both use as
the signal word; German has BLITZ and Russian МОЛНИЯ, following the developers'
own campaign.

---

## Change notes for the first upload

First release. Flagship swapped from the Kiev-class Minsk to the Project 1160
Orel-class Tbilisi, air wing and starting budget rebalanced around her,
localization into all nine game languages, several defects of the original
campaign and of the base game's Russian files repaired.
