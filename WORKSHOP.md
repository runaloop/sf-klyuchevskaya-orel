# Steam Workshop listing

Paste the body below into the "Mod Description" field of the game's Create Mod
window, or into the Workshop page editor. Steam accepts BBCode, which the game's
upload dialog passes through unchanged.

- **Title:** SF Klyuchevskaya '88: Orel Edition
- **Workshop item:** 3800243486 —
  https://steamcommunity.com/sharedfiles/filedetails/?id=3800243486
- **Preview image:** `mod/workshop_preview.jpg` (800×800, 112 KB)
- **Visibility:** public
- **Required items:** none

---

## Description

[h1]SF Klyuchevskaya '88: Orel Edition[/h1]

A modified edition of [b]SF Klyuchevskaya '88[/b] by [b]StickHeroes[/b]. The
campaign is his; three things are different here.

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
Atlant, one Project 956 Sarych and one or two small escorts, and then you are
done. The carrier is the most valuable hull in the Pacific Fleet and she has
almost nothing around her. Ten main missions and four side missions later you
will know whether that was enough.

[h2]Experimental R-27 loadouts[/h2]

In the 1988 campaign the first two MiG-23A flight deck options are
[list]
[*][b]two R-27ER and two R-73[/b] (default)
[*][b]two R-27ET and two R-73[/b]
[/list]
A separate experimental option carries two R-27ER and four R-73 from 1987.
All three R-27 options are available on the flight deck and in campaign CAP slots.
The R-24 options are at the end of the combat loadout list. The Yak-38 now
defaults to four R-73 and retains its R-60, mixed strike and gun options. CAP zones drawn during a mission accept only the standard loadouts; that
is the game's rule, so send R-27 flights out by hand.

[h2]Aircraft behaviour observed in Sea Power 0.9.3[/h2]

[list]
[*]Il-38s and P-42s may circle a submarine for a long time before releasing a torpedo. In one playthrough a pair of P-42s dropped just one torpedo in about half an hour.
[*]With advanced missile evasion enabled, a MiG-23A may climb despite a manual order to descend.
[*]If a Yak-38 stops beside a deck elevator on Tbilisi, return it to the hangar and launch it again. This freed both aircraft in our test.
[*]The P-42RLDN radar aircraft may appear to fly with its wings still folded after takeoff.
[/list]

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

[b]Requires Sea Power 0.9.3 or later in the 0.9 series.[/b] The files were
regenerated from public release 0.9.3 Build 261116 (Steam build 26712472) and
passed static checks. In-game verification is in progress.

[b]This mod needs nothing else. Do not subscribe to anything for it.[/b]

Subscribe, enable it, play. If you are also subscribed to the original
SF Klyuchevskaya '88, both campaigns appear side by side and you can play either;
put [b]Orel Edition above the original[/b] in the Mod Manager, because this one
carries more complete callsigns for every language. The same goes for
SF Klyuchevskaya 88' Advanced Edition.

[h2]Credits[/h2]

The campaign, its missions, briefings, interludes and artwork are the work of
[b]StickHeroes[/b]. This edition exists because that campaign was worth extending,
and it will be taken down at his request without argument.

The Project 1160 Orel and its aircraft are base-game content by Triassic Games
and MicroProse.

Source and a full list of every change:
[url=https://github.com/runaloop/sf-klyuchevskaya-orel]github.com/runaloop/sf-klyuchevskaya-orel[/url]

---

## Publishing checklist

In this order. Mission sheet 04 keeps the original Kiev-class screenshot on
purpose: the Kiev-class is still purchasable in this edition, and there is no
second Tbilisi shot that would not duplicate the cover.

1. [x] Play a new campaign through the first few missions — played, the
       campaign holds together with the new starting budget and the trimmed
       air wing.
2. [x] `tools/rename_campaign.sh SF_Klyuchevskaya_88_Orel` — done, the campaign
       folder is `SF_Klyuchevskaya_88_Orel` and nothing references the old id.
3. [x] Pushed to github.com/runaloop/sf-klyuchevskaya-orel; the link is in the
       description above.
4. [x] Upload: Mod Manager → Create Mod → pick the mod folder, title and
       description from this file, preview image `mod/workshop_preview.jpg`,
       visibility public, no required items. Uploaded 2026-09-12 as item
       3800243486 and set to public; `GetPublishedFileDetails` reports
       `visibility: 0`, and the page opens for a signed-out visitor.

Settled: the naval message headers are now translated in all nine languages.
Each language uses the vocabulary it already used elsewhere in the campaign, and
where the game itself defines the term, the game's own: SECRETO in Spanish, MẬT
in Vietnamese, 机密 in Chinese. French and Spanish keep FLASH, which both use as
the signal word; German has BLITZ and Russian МОЛНИЯ, following the developers'
own campaign.

---

## Change notes for the next update

Sea Power 0.9.3 compatibility

Mission 01 was completed on this build. Carrier launches were checked in mission 02, and a mission 03 campaign save confirmed the revised 10 NM search-area diameter.
- Aircraft definitions regenerated from 0.9.3 Build 261116, retaining the mod's
  loadouts and picking up the updated stock Tu-95RT gun system definitions.
- Callsigns and missing weapon names refreshed. Official translations take
  over where available. The two new Iowa-class rounds use English names in
  languages that lack their own entries. Russian still uses English for 18
  callsigns without a Cyrillic mapping.
- Compatibility metadata now requires Sea Power 0.9.3 or later in the 0.9
  series. Static checks passed.

Mission 07 "Apex Predators":
- The mission now ends when a replenishment ship reaches the Tsugaru Strait, as
  the briefing says. Before, it ended only when both American SSNs were sunk,
  and reaching the strait did nothing. Sinking both SSNs still ends it early,
  and it is still the only way to win if both replenishment ships are lost.
- The SSNs now wait inside their DATUM circles until your force comes within
  about 70 nm. Then they leave to intercept you, and the circle disappears with
  a message. Before, they started outside the circles and ran through them, so
  a circle was usually out of date within an hour or two.
- The second DATUM message no longer says "Location 1".
- A save made inside mission 07 keeps the old version. Exit to the campaign map
  and start the mission again from there.

## Change notes for the 2026-10-05 update

Mission 05 "Sudden Strike":
- Fog removed. The game keeps fog on for the whole mission and treats it like
  night for TV-guided weapons. The Ko-45's Kh-59 (AntiShip Precision) and
  Kh-29T (Strike Precision) therefore reported "Can't See Target" all mission
  long, even after the daylight warning cleared at dawn. Weather records for
  21–22 February 1988 show no fog off Misawa either. TV-guided weapons now work
  once the game's night ends, at about 05:50 on the game clock.
- Sea state raised from 2 to 4, to match the recorded northwesterly wind and
  swell off the Tohoku coast. Sonar and radar conditions get a little worse for
  both sides.
- Weather sources (NOAA NCEI):
  - hourly shore reports from Misawa and Hachinohe in the
    [url=https://www.ncei.noaa.gov/products/land-based-station/integrated-surface-database]Integrated Surface Database[/url];
  - ship reports off the Tohoku coast in
    [url=https://www.ncei.noaa.gov/products/international-comprehensive-ocean-atmosphere-data-set]ICOADS Release 3.1[/url].
- A save made inside mission 05 keeps the old weather; restart the mission to
  get the change.

Checked against Sea Power 0.8.4; nothing else needed changing.

Thanks to marseu for the report.

## Change notes for the first upload

First release. Flagship swapped from the Kiev-class Minsk to the Project 1160
Orel-class Tbilisi, air wing and starting budget rebalanced around her,
localization into all nine game languages, several defects of the original
campaign and of the base game's Russian files repaired.
