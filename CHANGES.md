# Changes relative to the original mod

Every entry names the file and what was replaced. The unchanged import of the
original mod is the root commit of this repository.

## Names

- `mod/_info.ini`, `campaign.ini`: display names changed to
  "SF Klyuchevskaya '88: Orel Edition", mod description rewritten. The campaign
  folder is `campaigns/SF_Klyuchevskaya_88_Orel`, renamed from the original id by
  `tools/rename_campaign.sh` so this edition can sit next to the original mod
  without either one shadowing the other.

## Flagship: TAVKR Minsk replaced by TAVKR Tbilisi (Project 1160 Orel)

Applied by `tools/apply_orel.py`; the air wing is configured at the top of that
script.

- `missions/01 FAR EAST DEPARTURE.ini`: the carrier that joins the task force
  is now `wp_cv_orel` Variant3 (Tbilisi, in service 1988) instead of
  `wp_takr_kiev` Variant2 (Minsk). The 18 airborne Yak-38 were replaced by a
  32-aircraft fly-in: 16 MiG-23A (two squadrons of the 311th OKIAP), 8 Ko-45,
  2 Ko-45E EW, 2 P-42RLDN AEW, 4 P-42 ASW. Helicopters reduced from 15 to 10
  (2 Ka-25TS AEW, 8 Ka-27PL). Formations, unit counts and campaign tags
  regenerated accordingly. Map labels and the start message now name TBILISI.
  Every fly-in aircraft and helicopter now carries `HomeBase=Taskforce2Vessel2`,
  binding it to the carrier. The original mission left them unattached, so
  nothing in the file said where they belonged.
- `missions/02 ... 10 (all main missions and 09A)`: the Task Force Mode anchor
  vessel is `wp_cv_orel` Variant3 with the same air group as above instead of
  the Kiev-class with 15-19 Yak-38.
- `missions/05 SUDDEN STRIKE.ini`: trigger "MINSK detected" renamed.
- `missions/06 SHOCK AND AWE.ini`, `07 APEX PREDATORS.ini`: formation
  "TAVKR Minsk" renamed "TAVKR Tbilisi".
- `campaign.ini`: `TaskForceNameOptions` "MINSK SAG" -> "TBILISI SAG";
  campaign description names the new flagship; every
  `TaskForceModeAllowedRosterUnits` list additionally allows MiG-23A
  squadrons 5 and 6, Ko-45, Ko-45E, P-42, P-42RLDN squadron 3, and, where the
  Kiev-class was purchasable, `wp_cv_orel` Variant2 (Riga).
- `player_task_force_roster.ini`: added `wp_cv_orel=Variant2|600`,
  `wp_taifun=Squadron3|65`, `wp_taifun_ew=Squadron3|120`, `wp_p-42=Squadron3|65`;
  MiG-23A now also squadrons 5 and 6, P-42RLDN also squadron 3.
  The Kiev-class (Novorossiysk) stays purchasable as in the original.
- `unit_roster_descriptions_en.ini`: new entries for the Orel-class, Ko-45,
  Ko-45E and P-42; the Slava entry now refers to TBILISI's 16 SS-N-19.
- `missions/Briefings/01/BriefingText_en.xml`, `art/update1.xml`: MINSK
  references replaced by TBILISI; the prelude names the ship as the newest
  Project 1160 carrier of the Pacific Fleet.
- Not changed on purpose: `art/update9.xml` (the Yak-38 there belong to
  SF Narod, a different task force) and `missions/06A THE GREY GHOST.ini`
  (Yak-38 on a RoRo ship of that side mission).

## Bugs fixed in the original campaign

Found while localizing; all of them are in the original mod.

- `commander_settings.ini`: all 13 award images were referenced as
  `art/medals/m1.png` while the files are named `M1.png`. Case matters on
  Linux, so every medal image failed to load there. References corrected.
- `language_ru/aircraft_names.ini` (a base-game file, fixed in our copy): the
  MiG-23A callsign list numbered the Tbilisi squadrons 3 and 4 a second time
  instead of 5 and 6. The duplicates overwrote the Riga callsigns and left the
  Tbilisi ones undefined, so the campaign's own fighters showed up as
  "DEFAULT" in Russian. `tools/make_language_files.py` now keeps the first
  entry of a duplicated squadron and fills every callsign a language is
  missing from the English list, which also fixes Ka-27, Ka-25TS and Ko-45E.
- `campaign.ini`: the mission file of "04A SUBS AND TARGETS" was referenced as
  `04a SUBS AND TARGETS.ini`, again wrong case for Linux.
- `campaign.ini [Mission9]`: the campaign timeline showed mission 04 under the
  title of mission 03 ("INTO THE NORTH PACIFIC"); now "NORTH PACIFIC HAPPY
  TIMES".
- `missions/08A THE SILENT SERVICE.ini`: `Name` read "08A SUBS AND TARGETS".
- `missions/06 SHOCK AND AWE.ini`: the start message was titled "SUDDEN
  STRIKE", the title of mission 05, and contained a doubled "Note: Note:".
- `art/update12.xml`: the final letter of the distribution line sat outside the
  underlined run, so it rendered unmarked and confused every translator.

`tools/loc_tools.py paths` now verifies that every referenced file exists with
exactly the right case, against both the mod and the base game.

## Balance and artwork

- Starting air wing trimmed to 26 aircraft of the carrier's 60 slots:
  8 MiG-23A, 6 Ko-45, 2 Ko-45E EW, 1 P-42RLDN AEW, 4 P-42 ASW, 1 Ka-25TS,
  4 Ka-27. Sized against the game's own turnaround times rather than by
  eye: the MiG-23A needs 75 minutes between sorties, so 8 is the floor for a
  continuous pair on station; the Ko-45 needs 120, so the pool size caps how
  many strikes a mission can mount; the Ka-27 needs 45, so 4 sustains one or
  two airborne. The single AEW aircraft means losing it costs the task force
  its radar picture, and the escorts bring one Ka-25TS and one Ka-27 of their
  own on top of this.
- Starting points cut so the screen is thin: 850 easy, 635 moderate, 500
  difficult. At moderate that buys exactly one Project 1164 Atlant and one
  Project 956 Sarych and nothing else.
- `ShipIncludesAirwing` forced to True on every preset. The difficult preset
  used to make the player buy the air wing, which is impossible here: bought
  separately this wing costs about 2000 points.
- Cover art, mission sheet 01 and mission sheet 03 replaced with screenshots of
  TAVKR Tbilisi; the old ones showed the Minsk. The cover tagline no longer
  refers to the Yak-38. `mod/workshop_preview.jpg` added for the Workshop tile.

## Localization

- `language_<xx>/aircraft_names.ini` for cn, de, es, fr, ja, ko, ru, vn:
  generated by `tools/make_language_files.py` from the game's own files with
  the original mod's Soviet callsign additions applied (Cyrillic for Russian).
- Campaign, missions, briefings, slideshows, unit roster descriptions and
  award citations translated into the eight other game languages: Chinese,
  French, German, Japanese, Korean, Russian, Spanish, Vietnamese. Each language
  has all 14 briefings, all 20 slideshows, its roster file and its own callsign
  file, and all 198 localized campaign keys.
- Russian additionally reviewed against the developers' own Russian campaign:
  dates spelled out rather than abbreviated, classification markers in Cyrillic,
  US and Japanese ship names as the game itself renders them, and the formation
  called КУГ, the established Soviet term the game uses for a surface action
  group. Because the game does not localize the task force name the player picks
  in the builder, Russian names the formation directly instead of using the
  `{TaskForceName}` placeholder.
- Merged with `tools/loc_tools.py`; `tools/loc_tools.py check` verifies that
  every English key and file has a counterpart in every language, that briefings
  and slideshows are not untranslated copies, that placeholders survive, and
  that every referenced path resolves with the right case.

## Localization review pass

Every language was reviewed against the English original, file by file, after the
chrome pass above. What the review changed:

- **Naval-message chrome completed.** The briefings carried their message form in
  English in French, Spanish, Chinese, Korean and Vietnamese: the FM / TO / INFO /
  SUBJ field labels, the classification and precedence markers, the addressee line
  and the unit designations. 808 strings. Each language now uses the vocabulary it
  already used in its own slideshows, and, where the game defines one, the game's
  own: `ClassificationSecret` is SECRETO in Spanish, MẬT in Vietnamese, 机密 in
  Chinese. French and Spanish keep FLASH, which both languages use as the signal
  word; German and Russian follow the developers' own campaign with BLITZ and
  МОЛНИЯ.
- **Korean**: "Red Banner" was 적기, which reads as 敵機, "enemy aircraft" — in the
  sender line of every message, in all 13 award citations and in the flagship's own
  description. Now 붉은기. The spaced-out classification banners lost their inserted
  full-width space, which in Korean reads as two disconnected syllables rather than
  emphasis.
- **Spanish**: "KTOF sends" had become "KTOF saluda", KTOF sends greetings, in ten
  situation reports; the mission files already had the correct "KTOF envía". One
  intelligence assessment said our own aviation had taken the damage it had in fact
  inflicted, and a division was "rebasada", overrun, where the English had it
  rebased.
- **French**: SSGN was rendered SNLE, a ballistic-missile submarine — a different
  class of boat and of order. Distances read "nq" in thirteen places, which is not
  a French abbreviation and invites reading knots for miles.
- **Russian**: КУГ is feminine and was conjugated as neuter in six places; one
  order stood in the dative; the FLASH precedence of briefing 10 had been flattened
  into the same words as IMMEDIATE while the body of the same message read МОЛНИЯ
  МОЛНИЯ МОЛНИЯ; the recurring SITREP headings had drifted into three wordings for
  the same English one.
- **Chinese**: one sentence about the enemy's compensating measures was garbled
  into nonsense; the Kara and Udaloy carried SILEX-A where the English says
  SILEX-B; the Kh-59 had been tagged with Gadfly, which belongs to the SA-N-7; the
  addressee line put 指挥官 before the task force name in ten files; OPBOX had
  become 战区, a theatre of war.
- **Vietnamese**: the largest drift — the commander field alternated between TƯ
  LỆNH and CHỈ HUY halfway through the campaign, the 55th Naval Infantry Division
  and the 14th Landing Ship Brigade each had three different names, and three
  briefings turned hedged intelligence ("not expected in area") into flat
  assertions, one of them recasting a screening order as reconnaissance.
- **Mission 04's title** was a copy of mission 03's in German and in Vietnamese,
  both in `campaign.ini` and in the mission file, so two missions shared a name and
  "happy times" was lost. An audit of all nine languages found no other duplicate.
- **Typos in the original English**: `Febuary` (12 times, including the award
  citations), `posiion`, `seperate`, `recieve`.

`tools/loc_tools.py check` now compares every string of every localized XML,
attribute values included, against its English counterpart and reports anything
left identical that is not on an explicit list of things that stay (BT, DECL OADR,
the routing line, document control numbers, the EO 13526 authorities, date-time
groups, place names Latin-script languages spell the same way, and the words
French and Spanish share with English). Before this it only compared passages
longer than 25 characters and never looked at `Text="..."` attributes, which is
how the entire message chrome stayed English without the check noticing.
