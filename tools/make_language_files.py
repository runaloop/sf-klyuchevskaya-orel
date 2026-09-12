#!/usr/bin/env python3
"""Build language_<xx>/aircraft_names.ini for every game language.

Two things are merged into each language's file:

1. The Soviet callsigns the original mod added to the English file.
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
LANGS = ["cn", "de", "es", "fr", "ja", "ko", "ru", "vn"]

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
}


class Text:
    def __init__(self, path):
        raw = path.read_bytes()
        self.bom = raw.startswith(b"\xef\xbb\xbf")
        text = raw[3:].decode("utf-8") if self.bom else raw.decode("utf-8")
        self.nl = "\r\n" if "\r\n" in text else "\n"
        self.lines = text.replace("\r\n", "\n").split("\n")

    def save(self, path):
        path.parent.mkdir(parents=True, exist_ok=True)
        data = self.nl.join(self.lines).encode("utf-8")
        path.write_bytes((b"\xef\xbb\xbf" if self.bom else b"") + data)


def parse_callsigns(line, duplicates=None):
    """'Callsigns=Squadron1,A,B|Squadron2,C' -> {'Squadron1': ['A','B'], ...}

    A squadron listed twice keeps its first entry. The game's own Russian file
    numbers the MiG-23A Tbilisi squadrons 3 and 4 a second time instead of 5
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


def sections(lines):
    heads = [i for i, l in enumerate(lines) if l.startswith("[")]
    for n, i in enumerate(heads):
        end = heads[n + 1] if n + 1 < len(heads) else len(lines)
        yield lines[i].strip(), i, end


def read_callsigns(path, report=False):
    out = {}
    t = Text(path)
    for name, start, end in sections(t.lines):
        for l in t.lines[start:end]:
            if l.startswith("Callsigns="):
                dups = set()
                out[name] = parse_callsigns(l, dups)
                if dups and report:
                    print(f"    {path.parent.name} {name}: duplicate squadron "
                          f"{sorted(dups)} in the game file, first entry kept")
                break
    return out


def main():
    original = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_ORIGINAL
    reference = read_callsigns(ROOT / "language_en" / "aircraft_names.ini")
    total_refs = sum(len(v) for v in reference.values())
    print(f"reference: {len(reference)} aircraft, {total_refs} squadron callsigns")

    for lang in LANGS:
        t = Text(original / f"language_{lang}" / "aircraft_names.ini")
        have = read_callsigns(original / f"language_{lang}" / "aircraft_names.ini", report=True)
        table = RU if lang == "ru" else {}
        added, unknown = 0, set()
        # walk backwards: inserting a line shifts every index after it
        for name, start, end in reversed(list(sections(t.lines))):
            if name not in reference:
                continue
            merged = dict(have.get(name, {}))
            for squadron, names in reference[name].items():
                if squadron in merged:
                    continue
                translated = []
                for n in names:
                    if table and n not in table:
                        unknown.add(n)
                    translated.append(table.get(n, n))
                merged[squadron] = translated
                added += 1
            if not merged:
                continue
            line = format_callsigns(merged)
            existing = [i for i in range(start, end) if t.lines[i].startswith("Callsigns=")]
            if existing:
                t.lines[existing[0]] = line
            else:
                last = end
                while last > start + 1 and not t.lines[last - 1].strip():
                    last -= 1
                t.lines.insert(last, line)
        t.save(ROOT / f"language_{lang}" / "aircraft_names.ini")
        note = f", {len(unknown)} not transliterated: {sorted(unknown)}" if unknown else ""
        print(f"  language_{lang}: {added} squadron callsigns filled in{note}")


if __name__ == "__main__":
    main()
