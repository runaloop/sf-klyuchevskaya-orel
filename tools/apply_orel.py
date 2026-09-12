#!/usr/bin/env python3
"""Swap TAVKR Minsk (Project 1143) for TAVKR Tbilisi (Project 1160 Orel).

Rewrites the campaign files in place. Idempotent: edit WING / HELOS / PRICES
below and re-run to regenerate mission 01 and the carrier air groups of the
other missions.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1] / "mod"
CAMP = ROOT / "campaigns" / "SF_Klyuchevskaya_88"
MISSIONS = CAMP / "missions"

OLD_SHIP = "wp_takr_kiev"
NEW_SHIP = "wp_cv_orel"
NEW_VARIANT = "Variant3"  # TAVKR Tbilisi, in service 1988
BUY_VARIANT = "Variant2"  # TAVKR Riga, purchasable replacement hull
NEW_TAG = f"{NEW_SHIP}_{NEW_VARIANT}"

# Fixed-wing start air wing of mission 01. Each entry becomes one formation.
# (type, squadron, count, loadout, formation name, position, heading, waypoints)
WING = [
    ("wp_mig-23a", "Squadron5", 8, "Ferry", "1/311 IAP Flight 1",
     "-9.89,10000,65.99", "-179", "-10.5199,10000,38.4439"),
    ("wp_taifun", "Squadron3", 6, "Ferry", "14/3 OKAP Strike",
     "-24.56,1000,65.2", "-72", "-26.9573,1000,65.9811|-11.961,10000,71.3896|-10.9026,10000,42.3992"),
    ("wp_taifun_ew", "Squadron3", 2, "Ferry", "14/5 OKAP EW",
     "-6.2,10000,70.5", "-179", "-10.4,10000,39.5"),
    ("wp_p-42_rldn", "Squadron3", 1, "AEW", "14/4 OKAP AEW",
     "-17.5,8000,76.5", "100", "-10.8,8000,41.5"),
    ("wp_p-42", "Squadron3", 4, "Empty", "14/6 OKAP ASW",
     "-28.5,3000,61.0", "-60", "-11.6,3000,43.5"),
]

# Starting budget per difficulty preset. Moderate buys exactly one Project 1164
# Atlant (Slava, 400) and one Project 956 Sarych (Sovremenny, 235) and nothing
# else, so the screen is thin and the carrier is exposed.
# ShipIncludesAirwing must stay True everywhere: bought separately this air wing
# costs about 2000 points, far beyond any preset.
POINTS = {"Easy": 850, "Moderate": 635, "Difficult": 500}

# Helicopters of mission 01. Positions per airframe, leader carries the waypoints.
HELOS = [
    ("wp_ka-25ts", "Squadron3", "AEW", "AEW Flight 1", "153", "-12.1459,1000,35.4478",
     ["-19.37,1000,49.38"]),
    ("wp_ka-27", "Squadron3", "Empty", "3/396 Flight 1", "153", "-12.4865,1000,36.0523",
     ["-21.82,1000,54.16", "-23.5,1000,54.15", "-20.83,1000,55.51", "-25.18,1000,54.13"]),
]

# Roster additions: unit -> (variants/squadrons, points)
PRICES = {
    NEW_SHIP: (BUY_VARIANT, 600),
    "wp_taifun": ("Squadron3", 65),
    "wp_taifun_ew": ("Squadron3", 120),
    "wp_p-42": ("Squadron3", 65),
}
# Squadrons to add to existing roster / allow-list entries
EXTRA_SQUADRONS = {
    "wp_mig-23a": ["Squadron5", "Squadron6"],
    "wp_p-42_rldn": ["Squadron3"],
}

DESCRIPTIONS = {
    NEW_SHIP: (
        "[AllowedVessels]",
        OLD_SHIP,
        "The Project 1160 OREL-class is the Soviet Navy's first true fleet carrier, with catapults, "
        "arresting gear and a capacity of up to 60 aircraft: MiG-23A FLOGGER fighters, Ko-45 strike "
        "and EW aircraft, P-42 ASW and P-42RLDN AEW aircraft, plus Ka-27 HELIX helicopters. She gives "
        "the task force real fleet air defense, stand-off strike and an airborne radar picture. She also "
        "mounts 16x SS-N-19 SHIPWRECK anti-ship missiles, SA-N-7 and SA-N-4 SAMs and CIWS, but she is "
        "the most valuable hull in the fleet and a replacement is extremely expensive, so keep her escorted.",
    ),
    "wp_taifun": (
        "[AllowedAircraft]",
        "wp_mig-23a",
        "The Ko-45 is a subsonic carrier-based attack aircraft, the Soviet answer to the A-6 INTRUDER. "
        "It carries a heavy stand-off anti-ship and land-attack load with precision and SEAD options, "
        "and can also fly as a tanker. It is the strike arm of the OREL-class air wing.",
    ),
    "wp_taifun_ew": (
        "[AllowedAircraft]",
        "wp_taifun",
        "The Ko-45E is the electronic warfare version of the Ko-45, in the role of the EA-6 PROWLER. "
        "Its jammer degrades enemy radars and SAM engagements for the strike package, and it can carry "
        "anti-radiation missiles for SEAD. Very few are available, do not risk them needlessly.",
    ),
    "wp_p-42": (
        "[AllowedAircraft]",
        "wp_taifun_ew",
        "The P-42 is a carrier-based ASW and maritime patrol aircraft comparable to the S-3 VIKING. "
        "With sonobuoys and torpedoes it extends the task force's ASW screen far beyond helicopter "
        "range and gives the carrier a long-endurance surface-search platform.",
    ),
}

TEXT_REPLACEMENTS = {
    MISSIONS / "01 FAR EAST DEPARTURE.ini": [
        ("MapSymbol_New1Label_en=TAVKR MINSK", "MapSymbol_New1Label_en=TAVKR TBILISI"),
        ("MapSymbol_New3Label_en=MINSK Arrow", "MapSymbol_New3Label_en=TBILISI Arrow"),
        ("MapSymbol_New6Label_en=MINSK Airgroup", "MapSymbol_New6Label_en=TBILISI Air Wing"),
        ("is to RV with TAVKR MINSK. MINSK airgroup is already airborne, land them aboard the "
         "aviation cruiser. Once airgroup is landed, proceed to exit area.",
         "is to RV with TAVKR TBILISI. TBILISI's air wing is already airborne, land it aboard the "
         "carrier. Once the air wing is landed, proceed to exit area."),
        ("let your aircraft land on MINSK.", "let your aircraft land on TBILISI."),
    ],
    MISSIONS / "05 SUDDEN STRIKE.ini": [("Name=MINSK detected", "Name=TBILISI detected")],
    MISSIONS / "06 SHOCK AND AWE.ini": [("|TAVKR Minsk|", "|TAVKR Tbilisi|")],
    MISSIONS / "07 APEX PREDATORS.ini": [("|TAVKR Minsk|", "|TAVKR Tbilisi|")],
    MISSIONS / "Briefings" / "01" / "BriefingText_en.xml": [
        ("rendezvous with TAKVR MINSK before", "rendezvous with TAVKR TBILISI before"),
        ("Land MINSK's airgroup and proceed", "Land TBILISI's air wing and proceed"),
    ],
    CAMP / "art" / "update1.xml": [
        ("Centered on TAKVR MINSK, it is a powerful task force",
         "Centered on TAVKR TBILISI, the newest Project 1160 carrier of the Pacific Fleet, "
         "it is a powerful task force"),
        ("protect MINSK and defend", "protect TBILISI and defend"),
    ],
    CAMP / "unit_roster_descriptions_en.ini": [
        ("Coupled with MINSK's own 8x SS-N-12s, you can deliver a combined 24x missile salvo",
         "Coupled with TBILISI's own 16x SS-N-19s, you can deliver a combined 32x missile salvo"),
    ],
    CAMP / "campaign.ini": [
        ("|MINSK SAG", "|TBILISI SAG"),
        ("You begin with TAKVR MINSK and its attached airgroup while you build",
         "You begin with TAVKR TBILISI, a Project 1160 Orel-class carrier, and her air wing while you build"),
    ],
}


class Text:
    """Text file that keeps its BOM and line endings."""

    def __init__(self, path):
        self.path = path
        raw = path.read_bytes()
        self.bom = raw.startswith(b"\xef\xbb\xbf")
        text = raw[3:].decode("utf-8") if self.bom else raw.decode("utf-8")
        self.nl = "\r\n" if "\r\n" in text else "\n"
        self.lines = text.replace("\r\n", "\n").split("\n")

    def save(self):
        text = self.nl.join(self.lines)
        data = text.encode("utf-8")
        self.path.write_bytes((b"\xef\xbb\xbf" if self.bom else b"") + data)

    def replace(self, old, new):
        joined = "\n".join(self.lines)
        if old not in joined and new not in joined:
            sys.exit(f"{self.path.name}: text not found: {old[:60]}")
        self.lines = joined.replace(old, new).split("\n")

    def section(self, name):
        """Return (start, end) line indexes of [name] body, end exclusive.

        A header may carry a trailing comment, e.g. "[TaskForceMode] # rules".
        """
        start = next((i for i, l in enumerate(self.lines)
                      if l == f"[{name}]" or l.startswith(f"[{name}] ")), None)
        if start is None:
            return None
        end = start + 1
        while end < len(self.lines) and not self.lines[end].startswith("["):
            end += 1
        return start, end


CARRIER_SECTION = "Taskforce2Vessel2"  # the Orel in mission 01


def unit_block(kind, index, utype, squadron, loadout, tag, position, heading, waypoints, telegraph):
    lines = [
        f"[{kind}{index}]",
        f"Type={utype}",
        f"SquadronReference={squadron}",
        "JoinTaskForce=True",
        "UnlimitedFuel=False",
        f"LoadoutVariant={loadout}",
        "WeaponStatus=Free",
        "CrewSkill=Trained",
        "Morale=3",
        f"CampaignTag={tag}",
        f"RelativePositionInNM={position}",
    ]
    if telegraph:
        lines.append("Telegraph=3")
    lines.append(f"Heading={heading}")
    if waypoints:
        lines.append(f"Waypoints={waypoints}")
    # bind every fly-in unit to the carrier so it knows where it belongs and
    # can recover there; the original mission left them unattached
    lines.append(f"HomeBase={CARRIER_SECTION}")
    return lines


def build_mission01_units():
    aircraft, helos, formations = [], [], []
    counters = {}
    idx = 0
    for utype, sqn, count, loadout, fname, pos, hdg, wps in WING:
        members = []
        for _ in range(count):
            idx += 1
            counters[(utype, sqn)] = counters.get((utype, sqn), 0) + 1
            tag = f"{utype}_{sqn}_{counters[(utype, sqn)]}"
            leader = not members
            aircraft += unit_block("Taskforce2Aircraft", idx, utype, sqn, loadout, tag,
                                   pos, hdg, wps if leader else None, True)
            members.append(f"Taskforce2Aircraft{idx}")
        formations.append(f"{','.join(members)}|{fname}|Vic|0.1|OverrideSpawnPositions")
    idx = 0
    for utype, sqn, loadout, fname, hdg, wps, positions in HELOS:
        members = []
        for pos in positions:
            idx += 1
            counters[(utype, sqn)] = counters.get((utype, sqn), 0) + 1
            tag = f"{utype}_{sqn}_{counters[(utype, sqn)]}"
            leader = not members
            helos += unit_block("Taskforce2Helicopter", idx, utype, sqn, loadout, tag,
                                pos, hdg, wps if leader else None, False)
            members.append(f"Taskforce2Helicopter{idx}")
        formations.append(f"{','.join(members)}|{fname}|Vic|1.5|OverrideSpawnPositions")
    return aircraft, helos, formations


def inline_air_group():
    """CustomAirGroup lines for the carrier anchors of missions 02-10."""
    groups = {}
    for utype, sqn, count, *_ in WING:
        groups.setdefault(utype, []).append(f"{sqn},{count}")
    for utype, sqn, _l, _f, _h, _w, positions in HELOS:
        groups.setdefault(utype, {})
        if isinstance(groups[utype], dict):
            groups[utype][sqn] = groups[utype].get(sqn, 0) + len(positions)
    lines = []
    for utype, val in groups.items():
        if isinstance(val, dict):
            lines.append(f"{utype}=" + "|".join(f"{s},{n}" for s, n in val.items()))
        else:
            lines.append(f"{utype}=" + "|".join(val))
    return lines


def apply_mission01():
    path = MISSIONS / "01 FAR EAST DEPARTURE.ini"
    t = Text(path)
    aircraft, helos, formations = build_mission01_units()
    n_air = sum(1 for l in aircraft if l.startswith("[Taskforce2Aircraft"))
    n_helo = sum(1 for l in helos if l.startswith("[Taskforce2Helicopter"))

    # counts and formations in [Mission]
    s, e = t.section("Mission")
    body = t.lines[s:e]
    body = [l for l in body if not re.match(r"Taskforce2_Formation([2-9]|\d\d+)=", l)]
    out = []
    for l in body:
        if l.startswith("NumberOfTaskforce2Aircraft="):
            l = f"NumberOfTaskforce2Aircraft={n_air}"
        elif l.startswith("NumberOfTaskforce2Helicopters="):
            l = f"NumberOfTaskforce2Helicopters={n_helo}"
        elif l.startswith("Taskforce2_NumberOfFormations="):
            l = f"Taskforce2_NumberOfFormations={1 + len(formations)}"
        out.append(l)
        if l.startswith("Taskforce2_Formation1="):
            out += [f"Taskforce2_Formation{i + 2}={f}" for i, f in enumerate(formations)]
    t.lines[s:e] = out

    # the carrier itself
    s, e = t.section("Taskforce2Vessel2")
    for i in range(s, e):
        l = t.lines[i]
        if l.startswith("Type="):
            t.lines[i] = f"Type={NEW_SHIP}"
        elif l.startswith("VariantReference="):
            t.lines[i] = f"VariantReference={NEW_VARIANT}"
        elif l.startswith("CampaignTag="):
            t.lines[i] = f"CampaignTag={NEW_TAG}"

    # unit blocks
    a0 = t.lines.index("[Taskforce2Aircraft1]")
    a1 = t.lines.index("[NeutralAircraft1]")
    t.lines[a0:a1] = aircraft
    h0 = t.lines.index("[Taskforce2Helicopter1]")
    h1 = t.lines.index("[Taskforce2LandUnit1]")
    t.lines[h0:h1] = helos
    t.save()
    return n_air, n_helo


def apply_anchor(path):
    t = Text(path)
    if "[Taskforce2Vessel1]" not in t.lines:
        return False
    s, e = t.section("Taskforce2Vessel1")
    body = t.lines[s:e]
    if f"Type={OLD_SHIP}" not in body and f"Type={NEW_SHIP}" not in body:
        return False
    out = []
    inserted = False
    for l in body:
        if l.startswith("Type="):
            l = f"Type={NEW_SHIP}"
        elif l.startswith("VariantReference="):
            l = f"VariantReference={NEW_VARIANT}"
        elif re.match(r"wp_[a-z0-9_-]+=", l):
            if not inserted:
                out += inline_air_group()
                inserted = True
            continue
        out.append(l)
    t.lines[s:e] = out
    t.save()
    return True


def merge_list(value, additions, after=None):
    """Merge into 'type,V1,V2|type,...' keeping order; optional insert after a type."""
    entries = []
    for item in value.split("|"):
        parts = item.split(",")
        entries.append([parts[0], parts[1:]])
    index = {e[0]: e for e in entries}
    for utype, variants in additions:
        if utype in index:
            for v in variants:
                if v not in index[utype][1]:
                    index[utype][1].append(v)
        else:
            entry = [utype, list(variants)]
            anchor = after.get(utype) if after else None
            if anchor and anchor in index:
                entries.insert(entries.index(index[anchor]) + 1, entry)
            else:
                entries.append(entry)
            index[utype] = entry
    return "|".join(",".join([e[0]] + e[1]) for e in entries)


def apply_points():
    """Rewrite the starting budget of each difficulty preset and the default."""
    t = Text(CAMP / "campaign.ini")
    for name, points in POINTS.items():
        found = t.section(f"TaskForceModeDifficulty_{name}")
        if not found:
            continue
        start, end = found
        for i in range(start, end):
            if t.lines[i].startswith(("StartingPoints=", "PointCap=")):
                t.lines[i] = t.lines[i].split("=")[0] + f"={points}"
            elif t.lines[i].startswith("ShipIncludesAirwing="):
                t.lines[i] = "ShipIncludesAirwing=True"
    # the [TaskForceMode] defaults mirror the Moderate preset
    start, end = t.section("TaskForceMode")
    for i in range(start, end):
        if t.lines[i].startswith(("StartingPoints=", "PointCap=")):
            t.lines[i] = t.lines[i].split("=")[0] + f"={POINTS['Moderate']}"
    t.save()


def apply_campaign_ini():
    t = Text(CAMP / "campaign.ini")
    additions = [(u, [PRICES[u][0]]) for u in ("wp_taifun", "wp_taifun_ew", "wp_p-42")]
    additions += [(u, v) for u, v in EXTRA_SQUADRONS.items()]
    for i, l in enumerate(t.lines):
        if l.startswith("TaskForceModeAllowedRosterUnits="):
            value = l.split("=", 1)[1]
            adds = list(additions)
            if f"{OLD_SHIP}," in value:
                adds.insert(0, (NEW_SHIP, [BUY_VARIANT]))
            t.lines[i] = "TaskForceModeAllowedRosterUnits=" + merge_list(
                value, adds, after={NEW_SHIP: OLD_SHIP, "wp_taifun": "wp_mig-23a",
                                    "wp_taifun_ew": "wp_taifun", "wp_p-42": "wp_taifun_ew"})
    t.save()


def apply_roster():
    t = Text(CAMP / "player_task_force_roster.ini")
    lines = t.lines
    for i, l in enumerate(lines):
        for utype, squadrons in EXTRA_SQUADRONS.items():
            if l.startswith(f"{utype}="):
                value, cost = l.split("=", 1)[1].split("|")
                have = value.split(",")
                have += [s for s in squadrons if s not in have]
                lines[i] = f"{utype}={','.join(have)}|{cost}"
    for utype, anchor in ((NEW_SHIP, OLD_SHIP), ("wp_taifun", "wp_mig-23a"),
                          ("wp_taifun_ew", "wp_taifun"), ("wp_p-42", "wp_taifun_ew")):
        if any(l.startswith(f"{utype}=") for l in lines):
            continue
        pos = next(i for i, l in enumerate(lines) if l.startswith(f"{anchor}="))
        variants, cost = PRICES[utype]
        lines.insert(pos + 1, f"{utype}={variants}|{cost}")
    t.save()


def apply_descriptions():
    t = Text(CAMP / "unit_roster_descriptions_en.ini")
    for utype, (_section, anchor, text) in DESCRIPTIONS.items():
        existing = [i for i, l in enumerate(t.lines) if l.startswith(f"{utype}=")]
        if existing:
            t.lines[existing[0]] = f"{utype}={text}"
            continue
        pos = next(i for i, l in enumerate(t.lines) if l.startswith(f"{anchor}="))
        t.lines.insert(pos + 1, f"{utype}={text}")
    t.save()


def apply_texts():
    for path, pairs in TEXT_REPLACEMENTS.items():
        t = Text(path)
        for old, new in pairs:
            t.replace(old, new)
        t.save()


def main():
    n_air, n_helo = apply_mission01()
    apply_points()
    anchors = [p.name for p in sorted(MISSIONS.glob("*.ini")) if apply_anchor(p)]
    apply_campaign_ini()
    apply_roster()
    apply_descriptions()
    apply_texts()
    print(f"mission 01: {n_air} aircraft, {n_helo} helicopters")
    print(f"carrier anchors rewritten: {len(anchors)}")
    for line in inline_air_group():
        print("  " + line)


if __name__ == "__main__":
    main()
