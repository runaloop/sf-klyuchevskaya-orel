#!/usr/bin/env python3
"""Build language_<xx>/aircraft_names/sf_klyuchevskaya_orel.ini for every game language.

The game merges every file in language_<xx>/aircraft_names/ into its own
aircraft_names.ini key by key, so each file here carries only the Callsigns=
lines that differ from the game's. The `#!extend` header makes the one reader
that opens aircraft_names.ini directly (mission aircraft with CallsignIndex) see
them too. Everything else, including names the game adds later, comes from the
game's own file.

Two things are merged into each language's Callsigns lines:

1. The Soviet callsigns the original mod added (SOVIET below).
2. Every callsign English has that the language is missing. The game's own
   translations are incomplete: Russian, for instance, defines callsigns for
   MiG-23A squadrons 1-4 only, so squadrons 5 and 6 (the Tbilisi air wing) show
   up in game as "DEFAULT". Existing translations are never overwritten.

  make_language_files.py [<StreamingAssets/original dir>]
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1] / "mod"
DEFAULT_ORIGINAL = (pathlib.Path.home() / ".steam/debian-installation/steamapps/common/Sea Power"
                    / "Sea Power_Data/StreamingAssets/original")
LANGS = ["en", "cn", "de", "es", "fr", "ja", "ko", "ru", "vn"]
OUT_NAME = "sf_klyuchevskaya_orel.ini"

# The original mod's additions to the English callsign lists.
SOVIET = {
    "[wp_il-38]": {"Squadron3": ["Cikada"]},
    "[wp_mig-23mld]": {"Squadron2": ["Narzan"]},
    "[wp_mig-25pd]": {"Squadron1": ["Kuznechik"]},
    "[wp_su-24m]": {"Squadron2": ["Argon"]},
    "[wp_tu-142m]": {"Squadron3": ["Atlet"]},
    "[wp_tu-16k]": {"Squadron11": ["Kinzhal"], "Squadron12": ["Lavina"]},
    "[wp_tu-16p]": {"Squadron6": ["Topaz"]},
    "[wp_tu-22m2]": {"Squadron8": ["Molot"]},
    "[wp_tu-95rt]": {"Squadron2": ["Berkut"], "Squadron3": ["Buran"]},
}

# Callsigns are romanized Russian words; Russian needs them back in Cyrillic.
RU = {
    "Aist": "Аист", "Albatros": "Альбатрос", "Argon": "Аргон", "Atlet": "Атлет",
    "Baykal": "Байкал", "Berkut": "Беркут", "Bizon": "Бизон", "Bor": "Бор",
    "Buran": "Буран", "Cikada": "Цикада", "Cricket": "Сверчок", "Dizel": "Дизель",
    "Drakon": "Дракон", "Goretz": "Горец", "Kaskad": "Каскад", "Kalibr": "Калибр",
    "Karniz": "Карниз", "Kinzhal": "Кинжал", "Klinok": "Клинок", "Kometa": "Комета",
    "Kompas": "Компас", "Kondor": "Кондор", "Korshun": "Коршун", "Krechet": "Кречет",
    "Kurgan": "Курган", "Kurok": "Курок", "Kuznechik": "Кузнечик", "Lava": "Лава",
    "Lavina": "Лавина", "Lednik": "Ледник", "Metel": "Метель", "Molot": "Молот",
    "Nalim": "Налим", "Narzan": "Нарзан", "Okun": "Окунь", "Orlan": "Орлан",
    "Prolog": "Пролог", "Raduga": "Радуга", "Redut": "Редут", "Regal": "Регал",
    "Sapsan": "Сапсан", "Shchuka": "Щука", "Skopa": "Скопа", "Slepen": "Слепень",
    "Sokol": "Сокол", "Strela": "Стрела", "Svoboda": "Свобода", "Tigr": "Тигр",
    "Topaz": "Топаз", "Uragan": "Ураган", "Vikhr": "Вихрь", "Vityaz": "Витязь",
    "Volna": "Волна", "Vulkan": "Вулкан", "Vympel": "Вымпел", "Vyuga": "Вьюга",
    "Yastreb": "Ястреб", "Zakat": "Закат", "Zenit": "Зенит", "Zhuravl": "Журавль",
    "Zima": "Зима", "Zoloto": "Золото", "Zubr": "Зубр", "Groza": "Гроза",
    "Burya": "Буря", "Almaz": "Алмаз", "Sverchok": "Сверчок",
    "Rozhok": "Рожок", "Putnik": "Путник", "Sapfir": "Сапфир", "Elita": "Элита", "Ovod": "Овод",
}


def read_lines(path):
    raw = path.read_bytes()
    text = raw[3:].decode("utf-8") if raw.startswith(b"\xef\xbb\xbf") else raw.decode("utf-8")
    return text.replace("\r\n", "\n").split("\n")


def parse_callsigns(line, duplicates=None):
    """'Callsigns=Squadron1,A,B|Squadron2,C' -> {'Squadron1': ['A','B'], ...}

    A squadron listed twice keeps its first entry. The game's own Russian file
    numbered the MiG-23A Tbilisi squadrons 3 and 4 a second time instead of 5
    and 6, which silently overwrote the Riga callsigns and left the Tbilisi
    ones undefined.
    """
    out = {}
    for group in line.partition("=")[2].split("|"):
        parts = group.split(",")
        if not parts or not parts[0]:
            continue
        if parts[0] in out:
            if duplicates is not None:
                duplicates.add(parts[0])
            continue
        out[parts[0]] = parts[1:]
    return out


def format_callsigns(mapping):
    def key(name):
        m = re.search(r"\d+", name)
        return (0, int(m.group())) if m else (1, 0)
    groups = [",".join([s] + mapping[s]) for s in sorted(mapping, key=key)]
    return "Callsigns=" + "|".join(groups)


def read_callsigns(path):
    """{'[section]': (callsigns, has_duplicates)} for every section of the file."""
    out, section = {}, None
    for l in read_lines(path):
        if l.startswith("["):
            section = l.strip()
            out.setdefault(section, ({}, False))
        elif section and l.startswith("Callsigns=") and not out[section][0]:
            dups = set()
            out[section] = (parse_callsigns(l, dups), bool(dups))
    return out


def main():
    original = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_ORIGINAL
    reference = {s: dict(c) for s, (c, _) in read_callsigns(original / "language_en" / "aircraft_names.ini").items()}
    for section, extra in SOVIET.items():
        if section not in reference:
            sys.exit(f"{section} is gone from the game's English aircraft_names.ini")
        for squadron, names in extra.items():
            reference[section].setdefault(squadron, names)

    for lang in LANGS:
        have = read_callsigns(original / f"language_{lang}" / "aircraft_names.ini")
        table = RU if lang == "ru" else {}
        out = [f"#!extend language_{lang}/aircraft_names.ini",
               "# SF Klyuchevskaya '88: Orel Edition. Generated by tools/make_language_files.py;",
               "# only the Callsigns lines that differ from the game's own file.", ""]
        filled, fixed, unknown = 0, [], set()
        for section, (current, dups) in have.items():
            if section not in reference:
                continue
            merged = dict(current)
            for squadron, names in reference[section].items():
                if squadron in merged:
                    continue
                translated = []
                for n in names:
                    if table and n not in table:
                        unknown.add(n)
                    translated.append(table.get(n, n))
                merged[squadron] = translated
                filled += 1
            if merged == current and not dups:
                continue
            if dups:
                fixed.append(section)
            out += [section, format_callsigns(merged), ""]
        path = ROOT / f"language_{lang}" / "aircraft_names" / OUT_NAME
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes("\r\n".join(out).encode("utf-8"))
        notes = []
        if fixed:
            notes.append(f"duplicate squadrons resolved in {fixed}")
        if unknown:
            notes.append(f"{len(unknown)} not transliterated: {sorted(unknown)}")
        print(f"  language_{lang}: {filled} squadron callsigns filled in, "
              f"{(len(out) - 4) // 3} sections" + "".join(f"; {n}" for n in notes))


if __name__ == "__main__":
    main()
