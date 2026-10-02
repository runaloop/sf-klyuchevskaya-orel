#!/usr/bin/env python3
"""Build language_<xx>/ammunition_names/sf_klyuchevskaya_orel.ini for every game language.

When the selected language has no [AmmunitionNames] entry for a weapon, the game
shows its internal id (wp_sa-n-10) instead of falling back to English; NATO names
do fall back. Sea Power 0.8.3 added weapons faster than its translations, so each
file here carries the entries the game's own file lacks, taken from
tools/translations/ammunition_names/<xx>.ini. The game merges every file in
language_<xx>/ammunition_names/ into its own list key by key.

Only keys missing from the game's file are written, so once the developers
translate an entry, re-running this drops ours. A missing key without a
translation is copied from English, which still beats the internal id.

  make_ammunition_names.py [<StreamingAssets/original dir>]
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
MOD = ROOT / "mod"
TRANSLATIONS = ROOT / "tools" / "translations" / "ammunition_names"
DEFAULT_ORIGINAL = (pathlib.Path.home() / ".steam/debian-installation/steamapps/common/Sea Power"
                    / "Sea Power_Data/StreamingAssets/original")
LANGS = ["cn", "de", "es", "fr", "ja", "ko", "ru", "vn"]
OUT_NAME = "sf_klyuchevskaya_orel.ini"
SECTION = "[AmmunitionNames]"
ENTRY = re.compile(r"^([A-Za-z0-9_\-\.]+)=(.*)$")


def read_section(path, section=SECTION):
    """{key: value} of one section; the first occurrence of a key wins, as in the game."""
    out, current = {}, None
    raw = path.read_bytes()
    text = raw[3:].decode("utf-8") if raw.startswith(b"\xef\xbb\xbf") else raw.decode("utf-8")
    for line in text.replace("\r\n", "\n").split("\n"):
        if line.startswith("["):
            current = line.strip()
            continue
        m = ENTRY.match(line)
        if m and current == section:
            out.setdefault(m.group(1), m.group(2))
    return out


def main():
    original = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_ORIGINAL
    english = read_section(original / "language_en" / "ammunition_names.ini")
    for lang in LANGS:
        have = read_section(original / f"language_{lang}" / "ammunition_names.ini")
        source = TRANSLATIONS / f"{lang}.ini"
        translated = read_section(source) if source.exists() else {}
        missing = [k for k in english if k not in have]
        untranslated = [k for k in missing if k not in translated]
        obsolete = sorted(k for k in translated if k in have or k not in english)
        out = MOD / f"language_{lang}" / "ammunition_names" / OUT_NAME
        if not missing:
            if out.exists():
                out.unlink()
        else:
            lines = [SECTION] + [f"{k}={translated.get(k, english[k])}" for k in missing]
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(("\r\n".join(lines) + "\r\n").encode("utf-8"))
        notes = []
        if untranslated:
            notes.append(f"copied from English: {untranslated}")
        if obsolete:
            notes.append(f"no longer needed: {obsolete}")
        print(f"  language_{lang}: {len(missing)} entries" + "".join(f"; {n}" for n in notes))


if __name__ == "__main__":
    main()
