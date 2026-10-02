#!/usr/bin/env python3
"""Build mod/<folder>/<unit>.ini from the game's own file and tools/patches/<folder>/<unit>.ini.

The mod changes a few keys of base-game units: the Yak-38 gun loadout, the Tu-95RT
AEW loadout, the MiG-23A loadouts. A unit file in a mod replaces the game's file
whole, so the mod ships the game's current file with the patch keys applied, and
nothing else differs. Re-run this after every game update.

The game's #!extend directive would avoid the copies, but 0.8.3 does not apply it
reliably: the startup preloader opens files in parallel while the extend registry
is still being filled, and a file opened then is cached without its extension.

  make_unit_files.py [<StreamingAssets/original dir>]
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PATCHES = ROOT / "tools" / "patches"
MOD = ROOT / "mod"
DEFAULT_ORIGINAL = (pathlib.Path.home() / ".steam/debian-installation/steamapps/common/Sea Power"
                    / "Sea Power_Data/StreamingAssets/original")
HEADER = re.compile(r"^\[([^\]]*)\]")


def read_text(path):
    raw = path.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    text = raw[3:].decode("utf-8") if bom else raw.decode("utf-8")
    nl = "\r\n" if "\r\n" in text else "\n"
    return bom, nl, text.replace("\r\n", "\n").split("\n")


def key_of(line):
    t = line.strip()
    if not t or t.startswith(("#", ";", "//", "[")) or "=" not in t:
        return None
    return t.split("=", 1)[0].strip().lower()


def parse_patch(lines):
    sections, current = [], None
    for line in lines:
        m = HEADER.match(line.strip())
        if m:
            current = (m.group(1), [])
            sections.append(current)
        elif current is not None and key_of(line):
            k, v = line.strip().split("=", 1)
            current[1].append((k.strip(), v.strip()))
    return sections


def section_spans(lines):
    heads = [(i, HEADER.match(l.strip()).group(1)) for i, l in enumerate(lines) if HEADER.match(l.strip())]
    spans = []
    for n, (i, name) in enumerate(heads):
        end = heads[n + 1][0] if n + 1 < len(heads) else len(lines)
        spans.append((name, i, end))
    return spans


def last_content(lines, start, end):
    last = start
    for i in range(start + 1, end):
        if lines[i].strip():
            last = i
    return last


def apply(lines, patch):
    for name, entries in patch:
        spans = section_spans(lines)
        found = next((s for s in spans if s[0] == name), None)
        if found:
            _, start, end = found
            for k, v in entries:
                hit = next((i for i in range(start + 1, end) if key_of(lines[i]) == k.lower()), None)
                if hit is not None:
                    lines[hit] = f"{k}={v}"
                else:
                    at = last_content(lines, start, end) + 1
                    lines.insert(at, f"{k}={v}")
                    end += 1
            continue
        prefix = re.match(r"^\D*\d*", name).group(0)
        same = [s for s in spans if s[0].startswith(prefix) and s[0] != name] if prefix else []
        anchor = same[-1] if same else spans[-1]
        at = last_content(lines, anchor[1], anchor[2]) + 1
        lines[at:at] = ["", f"[{name}]"] + [f"{k}={v}" for k, v in entries]
    return lines


def effective(lines):
    """The game's reading: first occurrence of a section and of a key wins; values are trimmed."""
    out, seen, cur = {}, set(), None
    for line in lines:
        t = line.strip()
        m = HEADER.match(t)
        if m:
            name = m.group(1)
            if re.match(r"^[ =\-*]", name) or name in seen:
                cur = None
                continue
            seen.add(name)
            cur = out.setdefault(name, {})
            continue
        if cur is not None and "=" in t:
            k, v = t.split("=", 1)
            cur.setdefault(k.strip().lower(), "=".join(x.strip() for x in v.split("=")))
    return out


def main():
    original = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_ORIGINAL
    failed = False
    for patch_path in sorted(PATCHES.glob("*/*.ini")):
        rel = patch_path.relative_to(PATCHES)
        bom, nl, base = read_text(original / rel)
        patch = parse_patch(read_text(patch_path)[2])
        result = apply(list(base), patch)
        expected = effective(base)
        for name, entries in patch:
            for k, v in entries:
                expected.setdefault(name, {})[k.lower()] = v
        if effective(result) != expected:
            failed = True
            print(f"  {rel}: result does not read as game file + patch")
            continue
        out = MOD / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes((b"\xef\xbb\xbf" if bom else b"") + nl.join(result).encode("utf-8"))
        changed = sum(len(e) for _, e in patch)
        print(f"  {rel}: {changed} keys applied to the game's file")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
