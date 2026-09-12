# SF Klyuchevskaya '88: Orel Edition

A modified edition of the Sea Power campaign **SF Klyuchevskaya '88** by
**StickHeroes** ([Steam Workshop item 3781504583][original]). Two things change:

- The flagship is **TAVKR Tbilisi**, a Project 1160 Orel-class fleet carrier
  with a MiG-23A, Ko-45 and P-42 air wing, instead of the Kiev-class Minsk and
  her Yak-38s. Missions, roster, prices and texts follow.
- The campaign is localized into **all nine game languages**: Chinese, English,
  French, German, Japanese, Korean, Russian, Spanish, Vietnamese.

Everything else is the original campaign: 10 main missions, 4 side missions,
its artwork, briefings, slideshows and awards.

`CREDITS.md` names the original author; `CHANGES.md` lists every change file by
file. The unchanged import of the original mod is the first commit of this
repository, so `git diff` against it shows exactly what this edition does.

[original]: https://steamcommunity.com/sharedfiles/filedetails/?id=3781504583

## Requirements

Sea Power 0.8.2 or newer. No other mods needed.

## Install

Subscribe on the Steam Workshop, or copy `mod/` into

    <Sea Power>/Sea Power_Data/StreamingAssets/<any folder name>

and enable it in the game's Mod Manager. Place it above the original
SF Klyuchevskaya '88 if you have that one subscribed too.

## Repository layout

    mod/                 the mod itself, exactly as it is published
    tools/               scripts that produce the edition
    CHANGES.md           every change against the original mod
    CREDITS.md           attribution

## Tools

    tools/apply_orel.py            swap the flagship and regenerate the air wing
    tools/make_language_files.py   build language_<xx>/aircraft_names.ini
    tools/loc_tools.py             extract / merge / check translations
    tools/rename_campaign.sh       rename the campaign folder id

`apply_orel.py` is the interesting one: the air wing, the prices and the roster
entries are declared at the top of the file, so changing the composition is a
matter of editing those tables and re-running it. It is idempotent.

`loc_tools.py check` verifies that every English key and every referenced file
has a counterpart in each language, that placeholders such as
`{TaskForceName}` survive translation, and that the briefing and slideshow XML
is well formed.

## Translations

Russian, German, Spanish, French, Japanese, Korean, Chinese and Vietnamese were
machine-translated, checked for structural correctness, then reviewed line by
line against the English original and corrected. None of them were proofread by a
native speaker. `tools/loc_tools.py check` holds the line from here: it compares
every string, attribute values included, and reports anything left identical to
the English that is not on an explicit list of things that stay that way.
Corrections are welcome: open an issue or a pull request against the matching
`language` file, or say so in the Workshop comments.

## License and reuse

The original campaign is the work of StickHeroes and is not covered by any
license the author published. This edition is distributed with attribution and
will be taken down on the original author's request. The Project 1160 Orel and
its aircraft are base-game content by Triassic Games / MicroProse.
