#!/usr/bin/env python3
"""Localization helpers for the campaign.

  loc_tools.py extract <dir>            write the English sources to <dir>/en
  loc_tools.py merge <dir> <lang>       merge <dir>/<lang> into the mod files
  loc_tools.py check [--loc <dir>] <lang>...
                                        verify completeness (merged files, or the
                                        unmerged <dir>/<lang> when --loc is given)

Layout of a language folder <dir>/<lang>:
  campaign_keys.ini    [Language_xx] section + [MissionN] sections with *_xx keys
  commander_keys.ini   [Ribbon_mN] sections with *_xx keys
  info.ini             [Language_xx] section for _info.ini
  missions/<name>.ini  [Language_xx] section of that mission
Briefings, slideshows and unit_roster_descriptions_xx.ini are written straight
into the mod folder.
"""
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1] / "mod"
CAMP = next(d for d in sorted((ROOT / "campaigns").iterdir()) if d.is_dir())
MISSIONS = CAMP / "missions"
LANGS = ["cn", "de", "es", "fr", "ja", "ko", "ru", "vn"]
SUFFIX = re.compile(r"^([A-Za-z0-9_]+?)_(cn|de|en|es|fr|ja|ko|ru|vn)=")
PLACEHOLDERS = ["{TaskForceName}", "{FlagshipName}", "{CommanderRank}", "{CommanderName}",
                "\\n", "<size=", "</size>", "<LineBreak/>", "Title=", "Body=", "ButtonText=",
                "PopupStyle=", "Template=", "From=", "To=", "Subj="]
PATH_KEYS = {"FilePath", "MissionImage", "TileImagePath", "AssetsPath"}

# The game does not localize TaskForceNameOptions: whatever the player picks in
# the builder is one shared Latin string for every language. A language written
# in another script may therefore spell the formation out instead of using the
# {TaskForceName} placeholder. Where it does, the literal below must appear
# wherever English used the placeholder.
TASKFORCE_LITERAL = {"ru": "КУГ «Ключевская»"}


class Text:
    """Text file that keeps its BOM and line endings."""

    def __init__(self, path, create=False):
        self.path = path
        if create and not path.exists():
            self.bom, self.nl, self.lines = False, "\r\n", []
            return
        raw = path.read_bytes()
        self.bom = raw.startswith(b"\xef\xbb\xbf")
        text = raw[3:].decode("utf-8") if self.bom else raw.decode("utf-8")
        self.nl = "\r\n" if "\r\n" in text else "\n"
        self.lines = text.replace("\r\n", "\n").split("\n")

    def save(self):
        data = self.nl.join(self.lines).encode("utf-8")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_bytes((b"\xef\xbb\xbf" if self.bom else b"") + data)


def sections(lines):
    """Yield (name, header_index, body_start, body_end) for every [section]."""
    heads = [i for i, l in enumerate(lines) if l.startswith("[")]
    for n, i in enumerate(heads):
        end = heads[n + 1] if n + 1 < len(heads) else len(lines)
        name = lines[i][1:lines[i].index("]")]
        yield name, i, i + 1, end


def find_section(lines, name):
    for sname, head, start, end in sections(lines):
        if sname == name:
            return head, start, end
    return None


def key_of(line):
    return line.split("=", 1)[0] if "=" in line and not line.startswith(";") else None


def strip_trailing_blank(body):
    while body and not body[-1].strip():
        body = body[:-1]
    return body


# ---------------------------------------------------------------- extract

def extract(outdir):
    out = pathlib.Path(outdir) / "en"
    (out / "missions").mkdir(parents=True, exist_ok=True)

    t = Text(CAMP / "campaign.ini")
    lines = []
    for name, head, start, end in sections(t.lines):
        if name == "Language_en":
            lines += [t.lines[head]] + strip_trailing_blank(t.lines[start:end]) + [""]
        elif re.fullmatch(r"Mission\d+", name):
            keys = [l for l in t.lines[start:end] if re.match(r"[A-Za-z]+_en=", l)]
            lines += [t.lines[head]] + keys + [""]
    (out / "campaign_keys.ini").write_text("\n".join(lines), encoding="utf-8")

    t = Text(CAMP / "commander_settings.ini")
    lines = []
    for name, head, start, end in sections(t.lines):
        if re.fullmatch(r"Ribbon_m\d+", name):
            keys = [l for l in t.lines[start:end] if re.match(r"[A-Za-z]+_en=", l)]
            lines += [t.lines[head]] + keys + [""]
    (out / "commander_keys.ini").write_text("\n".join(lines), encoding="utf-8")

    t = Text(ROOT / "_info.ini")
    head, start, end = find_section(t.lines, "Language_en")
    body = strip_trailing_blank(t.lines[start:end])
    (out / "info.ini").write_text("\n".join([t.lines[head]] + body + [""]), encoding="utf-8")

    for path in sorted(MISSIONS.glob("*.ini")):
        t = Text(path)
        head, start, end = find_section(t.lines, "Language_en")
        body = [l for l in t.lines[start:end]
                if not (SUFFIX.match(l) and SUFFIX.match(l).group(2) != "en")]
        body = strip_trailing_blank(body)
        (out / "missions" / path.name).write_text(
            "\n".join([t.lines[head]] + body + [""]), encoding="utf-8")
    print(f"extracted English sources to {out}")


# ---------------------------------------------------------------- merge

def merge_keys(target, loc_lines, lang, section_re):
    """Insert/replace *_lang keys of matching sections of loc_lines into target."""
    loc = {}
    for name, head, start, end in sections(loc_lines):
        loc[name] = [l for l in loc_lines[start:end] if re.match(rf"[A-Za-z]+_{lang}=", l)]
    for name, head, start, end in list(sections(target.lines)):
        if not section_re.fullmatch(name) or name not in loc:
            continue
        body = target.lines[start:end]
        for line in loc[name]:
            key = key_of(line)
            base = key[: -len(lang) - 1]
            existing = [i for i, l in enumerate(body) if key_of(l) == key]
            if existing:
                body[existing[0]] = line
                continue
            anchor = [i for i, l in enumerate(body) if key_of(l) == f"{base}_en"]
            if anchor:
                body.insert(anchor[0] + 1, line)
            else:
                last = len(strip_trailing_blank(body))
                body.insert(last, line)
        target.lines[start:end] = body
        # sections() indexes shift after insertion: restart scan
        return merge_keys_rest(target, loc, lang, section_re, name)
    return


def merge_keys_rest(target, loc, lang, section_re, done_name):
    # Simple approach: iterate until every loc section has been merged.
    pending = [n for n in loc if section_re.fullmatch(n) and n != done_name]
    for name in pending:
        found = find_section(target.lines, name)
        if not found:
            print(f"  warning: section [{name}] not in target, skipped")
            continue
        head, start, end = found
        body = target.lines[start:end]
        for line in loc[name]:
            key = key_of(line)
            base = key[: -len(lang) - 1]
            existing = [i for i, l in enumerate(body) if key_of(l) == key]
            if existing:
                body[existing[0]] = line
                continue
            anchor = [i for i, l in enumerate(body) if key_of(l) == f"{base}_en"]
            if anchor:
                body.insert(anchor[0] + 1, line)
            else:
                body.insert(len(strip_trailing_blank(body)), line)
        target.lines[start:end] = body


def merge_section(target, loc_lines, lang):
    """Replace or insert the [Language_lang] section (after [Language_en])."""
    found = find_section(loc_lines, f"Language_{lang}")
    if not found:
        sys.exit(f"  [Language_{lang}] missing in loc file for {target.path.name}")
    body = strip_trailing_blank(loc_lines[found[1]:found[2]])
    new = [f"[Language_{lang}]"] + body
    have = find_section(target.lines, f"Language_{lang}")
    if have:
        head, start, end = have
        tail = target.lines[start:end]
        blank = len(tail) - len(strip_trailing_blank(tail))
        target.lines[head:end] = new + [""] * blank
        return
    head, start, end = find_section(target.lines, "Language_en")
    tail = target.lines[start:end]
    blank = len(tail) - len(strip_trailing_blank(tail))
    target.lines[end:end] = new + [""] * blank


def read_loc(path):
    return path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").split("\n")


def merge(indir, lang):
    src = pathlib.Path(indir) / lang
    if not src.is_dir():
        sys.exit(f"no folder {src}")

    t = Text(CAMP / "campaign.ini")
    loc = read_loc(src / "campaign_keys.ini")
    merge_section(t, loc, lang)
    merge_keys(t, loc, lang, re.compile(r"Mission\d+"))
    t.save()

    t = Text(CAMP / "commander_settings.ini")
    merge_keys(t, read_loc(src / "commander_keys.ini"), lang, re.compile(r"Ribbon_m\d+"))
    t.save()

    t = Text(ROOT / "_info.ini")
    merge_section(t, read_loc(src / "info.ini"), lang)
    t.save()

    n = 0
    for path in sorted((src / "missions").glob("*.ini")):
        target = MISSIONS / path.name
        if not target.exists():
            print(f"  warning: unknown mission {path.name}, skipped")
            continue
        t = Text(target)
        merge_section(t, read_loc(path), lang)
        t.save()
        n += 1
    print(f"merged {lang}: campaign.ini, commander_settings.ini, _info.ini, {n} missions")


# ---------------------------------------------------------------- check

class Report:
    def __init__(self, lang):
        self.lang, self.errors, self.warnings = lang, [], []

    def error(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)


def is_boilerplate(value):
    """Values that are expected to stay identical: paths, codes, markup, placeholders."""
    stripped = value.strip()
    if stripped.startswith("{Binding") or stripped.startswith("{StaticResource"):
        return True
    if re.search(r"\.(xml|png|jpg|ini)$|^[-0-9.,]+$", stripped):
        return True
    if re.fullmatch(r"[a-zA-Z0-9_./\\-]+", stripped):  # bare path or identifier
        return True
    without = stripped
    for token in re.findall(r"\{[A-Za-z]+\}", stripped):
        without = without.replace(token, "")
    return without.strip() == ""


def compare_values(rep, where, key, en, xx):
    if xx.strip() == "":
        rep.error(f"{where}: {key} is empty")
        return
    for token in PLACEHOLDERS:
        want, got = en.count(token), xx.count(token)
        if token == "{TaskForceName}" and rep.lang in TASKFORCE_LITERAL and want:
            got = min(want, got + xx.count(TASKFORCE_LITERAL[rep.lang]))
        if want != got:
            rep.warn(f"{where}: {key}: '{token}' count {want} in EN vs {got}")
    if (en == xx and len(en) > 30 and key not in PATH_KEYS
            and not is_boilerplate(en) and not stays_identical(rep.lang, en)):
        rep.warn(f"{where}: {key} looks untranslated")


def check_keyed(rep, where, en_lines, xx_lines, lang, section_re, path_check=None):
    """Compare *_en keys of sections with *_lang keys."""
    en_map, xx_map = {}, {}
    for name, head, start, end in sections(en_lines):
        if section_re.fullmatch(name):
            en_map[name] = {key_of(l)[:-3]: l.split("=", 1)[1]
                            for l in en_lines[start:end] if re.match(r"[A-Za-z]+_en=", l)}
    for name, head, start, end in sections(xx_lines):
        if section_re.fullmatch(name):
            xx_map[name] = {key_of(l)[: -len(lang) - 1]: l.split("=", 1)[1]
                            for l in xx_lines[start:end] if re.match(rf"[A-Za-z]+_{lang}=", l)}
    for name, keys in en_map.items():
        have = xx_map.get(name, {})
        for base, en_val in keys.items():
            if base not in have:
                rep.error(f"{where} [{name}]: {base}_{lang} missing")
                continue
            compare_values(rep, f"{where} [{name}]", base, en_val, have[base])
            if path_check and base in PATH_KEYS:
                path_check(rep, f"{where} [{name}] {base}_{lang}", have[base])


def check_path(rep, where, value):
    p = ROOT / value.replace("\\", "/")
    if not p.exists():
        rep.error(f"{where}: missing file {value}")


def check_language_section(rep, where, en_lines, xx_lines, lang, path_check=True):
    en = find_section(en_lines, "Language_en")
    xx = find_section(xx_lines, f"Language_{lang}")
    if not xx:
        rep.error(f"{where}: [Language_{lang}] missing")
        return
    en_keys, xx_keys = {}, {}
    for l in en_lines[en[1]:en[2]]:
        k = key_of(l)
        if not k:
            continue
        m = SUFFIX.match(l)
        if m and m.group(2) != "en":
            continue
        base = k[:-3] if (m and m.group(2) == "en") else k
        en_keys[base] = l.split("=", 1)[1]
    for l in xx_lines[xx[1]:xx[2]]:
        k = key_of(l)
        if not k:
            continue
        m = SUFFIX.match(l)
        if m and m.group(2) != lang:
            rep.warn(f"{where}: stray key {k} in [Language_{lang}]")
            continue
        base = k[: -len(lang) - 1] if m else k
        xx_keys[base] = l.split("=", 1)[1]
    for base, en_val in en_keys.items():
        if base not in xx_keys:
            rep.error(f"{where}: {base} missing in [Language_{lang}]")
            continue
        xx_val = xx_keys[base]
        if base in ("MissionBriefingLeftPane", "MissionBriefingAssetsDirectory"):
            if path_check:
                check_path(rep, f"{where}: {base}", xx_val)
            if base == "MissionBriefingLeftPane" and f"_{lang}.xml" not in xx_val:
                rep.error(f"{where}: MissionBriefingLeftPane must point to BriefingText_{lang}.xml")
            continue
        if re.fullmatch(r"[-0-9.]+|True|False", en_val):
            if en_val != xx_val:
                rep.error(f"{where}: {base} numeric/boolean value changed")
            continue
        compare_values(rep, where, base, en_val, xx_val)
    for base in xx_keys:
        if base not in en_keys:
            rep.warn(f"{where}: extra key {base} in [Language_{lang}]")


# Strings a translation is expected to leave exactly as they are: procedural
# signals of the message form, routing and document control numbers, the
# declassification authorities of the American documents, dates and page
# markers. Everything else that survives translation unchanged is reported.
KEEP_IDENTICAL = [
    "BT", "DECL OADR BT", "KTOF", "ZYUW RUHGOAA0777 0808100",
    "C05084534", "222X1", "SF Narod", "CONPLAN ORANGE 1-4", "SF Klyuchevskaya '88",
    "SF Klyuchevskaya '88: Orel Edition",
    # place names Latin-script languages spell the same way
    "WASHINGTON", "PARIS", "ZURICH", "TOKYO", "CANBERRA",
]
KEEP_IDENTICAL_RE = [
    re.compile(r"^EO 13526"),
    re.compile(r"^[OZP] \d\d \d{4}Z [A-Z]{3} \d\d$"),      # date-time group
    re.compile(r"^\d\d:\d\dZ \(\d\d:\d\dL\)$"),           # zulu / local time
    re.compile(r"^-\d+-$"),                                 # page marker
]
# Words a language shares with English, and the signal words it keeps on purpose.
KEEP_IDENTICAL_LANG = {
    "fr": ["SECRET", "SECRET DECL OADR", "*******S E C R E T*******",
           "FLASH", "FLASH FLASH FLASH"],
    "es": ["FLASH", "FLASH FLASH FLASH", "Vladlen Mikhailov, Director", "25 FEB 1988"],
}


def is_markup(value):
    """Binding expressions, paths, placeholders and numbers - never translated."""
    v = value.strip()
    if v.startswith("{Binding") or v.startswith("{StaticResource"):
        return True
    if re.search(r"\.(xml|png|jpg|ini)$", v) or "/" in v or "\\" in v:
        return True
    without = v
    for token in re.findall(r"\{[A-Za-z]+\}", v):
        without = without.replace(token, "")
    return without.strip(" .,:;-0123456789") == ""


def stays_identical(lang, value):
    if value in KEEP_IDENTICAL or value in KEEP_IDENTICAL_LANG.get(lang, ()):
        return True
    return any(rx.match(value) for rx in KEEP_IDENTICAL_RE)


def xml_texts(path):
    """Human-readable strings of an XML file: text nodes plus Text="..." values."""
    tree = ET.parse(path)
    out = []
    for el in tree.iter():
        for chunk in (el.text, el.tail):
            if chunk and chunk.strip():
                out.append(" ".join(chunk.split()))
        value = el.get("Text")
        if value and value.strip():
            out.append(" ".join(value.split()))
    return out


def check_xml(rep, en_path, xx_path):
    """Well-formedness plus content checks against the English original."""
    if not xx_path.exists():
        rep.error(f"missing {xx_path.relative_to(ROOT)}")
        return
    name = xx_path.relative_to(ROOT)
    try:
        xx = xml_texts(xx_path)
    except ET.ParseError as e:
        rep.error(f"{name}: XML parse error: {e}")
        return
    if not en_path.exists():
        return
    try:
        en = xml_texts(en_path)
    except ET.ParseError:
        return
    if not en:
        return
    if len(xx) != len(en):
        rep.warn(f"{name}: {len(xx)} text nodes vs {len(en)} in English")
    else:
        left = [a for a, b in zip(en, xx)
                if a == b and not is_markup(a) and not stays_identical(rep.lang, a)]
        if left:
            shown = ", ".join(repr(s) for s in sorted(set(left))[:4])
            rep.warn(f"{name}: {len(left)} string(s) left in English: {shown}")
    en_body = [s for s in en if len(s) > 25 and not is_boilerplate(s)
               and not stays_identical(rep.lang, s)]
    if en_body:
        same = sum(1 for s in en_body if s in xx)
        if same == len(en_body):
            rep.error(f"{name}: appears to be the untranslated English file")
        elif same > len(en_body) * 0.5:
            rep.error(f"{name}: {same} of {len(en_body)} English passages left untranslated")
        elif same:
            rep.warn(f"{name}: {same} of {len(en_body)} English passages unchanged")
    en_all, xx_all = " ".join(en), " ".join(xx)
    for token in ("{TaskForceName}", "{FlagshipName}", "{CommanderName}", "{SelectedUnitName}"):
        want, got = en_all.count(token), xx_all.count(token)
        if token == "{TaskForceName}" and rep.lang in TASKFORCE_LITERAL:
            got += xx_all.count(TASKFORCE_LITERAL[rep.lang])
            if got < want:
                rep.error(f"{name}: the formation is named {got} times, {want} in English "
                          f"(use '{{TaskForceName}}' or '{TASKFORCE_LITERAL[rep.lang]}')")
            continue
        if want != got:
            rep.error(f"{name}: '{token}' appears {want} times in English, {got} here")


ASSET_REF = re.compile(r"(?:campaigns|ui|ships)[/\\][A-Za-z0-9_./\\ -]+\.(?:ini|xml|png|jpg)")
GAME_ORIGINAL = (pathlib.Path.home() / ".steam/debian-installation/steamapps/common/Sea Power"
                 / "Sea Power_Data/StreamingAssets/original")


def check_paths():
    """Every asset path referenced anywhere in the mod must resolve, case included.

    The game runs case-insensitively on Windows and case-sensitively on Linux,
    so a wrong-case reference is invisible to most authors and fatal here.
    A reference may also point at a base-game file, which lives in the game's
    own `original` folder rather than in the mod.
    """
    roots = [ROOT] + ([GAME_ORIGINAL] if GAME_ORIGINAL.is_dir() else [])
    missing = {}
    for path in sorted(ROOT.rglob("*")):
        if path.suffix.lower() not in (".ini", ".xml") or not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8-sig", errors="replace")
        except OSError:
            continue
        for ref in set(ASSET_REF.findall(text)):
            rel = ref.replace("\\", "/").lstrip("/")
            if not any((root / rel).exists() for root in roots):
                missing.setdefault(ref, []).append(str(path.relative_to(ROOT)))
    for ref, users in sorted(missing.items()):
        print(f"  MISSING {ref}")
        for u in sorted(set(users))[:3]:
            print(f"          referenced by {u}")
    print(f"paths: {len(missing)} unresolved reference(s)")
    return len(missing)


def check(langs, locdir=None):
    if check_paths():
        print()
    loc = pathlib.Path(locdir) if locdir else None
    en_campaign = Text(CAMP / "campaign.ini").lines
    en_commander = Text(CAMP / "commander_settings.ini").lines
    en_info = Text(ROOT / "_info.ini").lines
    en_roster = Text(CAMP / "unit_roster_descriptions_en.ini").lines
    failed = False
    for lang in langs:
        rep = Report(lang)
        src = (loc / lang) if loc else None

        def pick(default_lines, name):
            if src:
                p = src / name
                return read_loc(p) if p.exists() else None
            return default_lines

        xx = pick(en_campaign, "campaign_keys.ini")
        if xx is None:
            rep.error("campaign_keys.ini missing")
        else:
            check_language_section(rep, "campaign.ini", en_campaign, xx, lang, path_check=False)
            check_keyed(rep, "campaign.ini", en_campaign, xx, lang, re.compile(r"Mission\d+"), check_path)
        xx = pick(en_commander, "commander_keys.ini")
        if xx is None:
            rep.error("commander_keys.ini missing")
        else:
            check_keyed(rep, "commander_settings.ini", en_commander, xx, lang, re.compile(r"Ribbon_m\d+"))
        xx = pick(en_info, "info.ini")
        if xx is None:
            rep.error("info.ini missing")
        else:
            check_language_section(rep, "_info.ini", en_info, xx, lang, path_check=False)

        for path in sorted(MISSIONS.glob("*.ini")):
            en_lines = Text(path).lines
            xx = pick(en_lines, f"missions/{path.name}")
            if xx is None:
                rep.error(f"missions/{path.name}: translation file missing")
                continue
            check_language_section(rep, path.name, en_lines, xx, lang)

        # the mission title must read the same in the mission file and in campaign.ini
        titles = {}
        for path in sorted(MISSIONS.glob("*.ini")):
            lines = pick(Text(path).lines, f"missions/{path.name}")
            if lines is None:
                continue
            found = find_section(lines, f"Language_{lang}")
            if not found:
                continue
            for l in lines[found[1]:found[2]]:
                if key_of(l) == "Name":
                    titles[path.stem] = l.split("=", 1)[1].strip()
                    break
        campaign_lines = pick(en_campaign, "campaign_keys.ini")
        if campaign_lines:
            for name, head, start, end in sections(campaign_lines):
                if not re.fullmatch(r"Mission\d+", name):
                    continue
                comment = campaign_lines[head].partition("#")[2].strip()
                title = next((l.split("=", 1)[1].strip()
                              for l in campaign_lines[start:end]
                              if key_of(l) == f"Name_{lang}"), None)
                if not title or not comment:
                    continue
                stem = next((s for s in titles if s.upper().startswith(comment.upper())), None)
                if stem and titles[stem] and title not in titles[stem]:
                    rep.warn(f"campaign.ini [{name}]: title '{title}' differs from "
                             f"'{titles[stem]}' in the mission file")

        roster = CAMP / f"unit_roster_descriptions_{lang}.ini"
        if not roster.exists():
            rep.error(f"unit_roster_descriptions_{lang}.ini missing")
        else:
            xx_lines = Text(roster).lines
            en_keys = {key_of(l): l.split("=", 1)[1] for l in en_roster if key_of(l)}
            xx_keys = {key_of(l): l.split("=", 1)[1] for l in xx_lines if key_of(l)}
            for k, v in en_keys.items():
                if k not in xx_keys:
                    rep.error(f"unit_roster_descriptions_{lang}.ini: {k} missing")
                else:
                    compare_values(rep, f"unit_roster_descriptions_{lang}.ini", k, v, xx_keys[k])

        for d in sorted((MISSIONS / "Briefings").iterdir()):
            check_xml(rep, d / "BriefingText_en.xml", d / f"BriefingText_{lang}.xml")
        for p in sorted(CAMP.glob("art/update*.xml")):
            check_xml(rep, p, CAMP / "art" / lang / p.name)
        if not (ROOT / f"language_{lang}" / "aircraft_names" / "sf_klyuchevskaya_orel.ini").exists():
            rep.warn(f"language_{lang}/aircraft_names/sf_klyuchevskaya_orel.ini missing")

        print(f"== {lang}: {len(rep.errors)} errors, {len(rep.warnings)} warnings")
        for m in rep.errors:
            print("  ERROR " + m)
        for m in rep.warnings[:40]:
            print("  warn  " + m)
        if len(rep.warnings) > 40:
            print(f"  ... {len(rep.warnings) - 40} more warnings")
        failed |= bool(rep.errors)
    sys.exit(1 if failed else 0)


def main(argv):
    if len(argv) >= 2 and argv[0] == "extract":
        extract(argv[1])
    elif len(argv) == 3 and argv[0] == "merge":
        merge(argv[1], argv[2])
    elif argv and argv[0] == "paths":
        sys.exit(1 if check_paths() else 0)
    elif argv and argv[0] == "check":
        args = argv[1:]
        locdir = None
        if args and args[0] == "--loc":
            locdir, args = args[1], args[2:]
        check(args or LANGS, locdir)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
