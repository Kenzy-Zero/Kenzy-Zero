"""Render every static card of the profile README into assets/.

    python tools/build.py

The dynamic card (signals.svg) is rendered by tools/signals.py, daily, by a
GitHub Action. Everything here is deterministic: the same source gives the
same bytes, so a rebuild with no design change is a no-op in git.
"""
from __future__ import annotations

import math
import random

from kz import (MONO, SANS, T, W, chip, grid_pattern, hairline, icon, marker, panel,
                rich, section, svg, text, write)

# ----------------------------------------------------------------------------
# hero
# ----------------------------------------------------------------------------

def _hexagon(cx, cy, r):
    pts = []
    for i in range(6):
        a = math.radians(60 * i)  # flat-top
        pts.append(f"{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}")
    return " ".join(pts)


def hero() -> str:
    H = 320
    rnd = random.Random(2026)
    out = ["<defs>",
           grid_pattern("hgrid", 28, T["border"], 0.45),
           '<linearGradient id="wm" x1="0" y1="0" x2="1" y2="0">'
           f'<stop offset="0" stop-color="{T["warm"]}"/><stop offset="0.55" stop-color="{T["accent"]}"/>'
           f'<stop offset="1" stop-color="{T["azure"]}"/></linearGradient>',
           '<linearGradient id="fade" x1="0" y1="0" x2="1" y2="0">'
           '<stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.35" stop-color="#fff" stop-opacity="1"/></linearGradient>',
           '<mask id="mfade"><rect x="520" y="0" width="480" height="320" fill="url(#fade)"/></mask>',
           '<radialGradient id="glow" cx="0.82" cy="0.5" r="0.5">'
           f'<stop offset="0" stop-color="{T["accent"]}" stop-opacity="0.14"/><stop offset="1" stop-color="{T["accent"]}" stop-opacity="0"/></radialGradient>',
           "</defs>",
           f'<rect width="{W}" height="{H}" fill="{T["bg"]}"/>',
           f'<rect width="{W}" height="{H}" fill="url(#hgrid)"/>',
           f'<rect width="{W}" height="{H}" fill="url(#glow)"/>',
           f'<rect width="{W}" height="2" fill="url(#wm)"/>']

    # --- map motif (right): an H3-like hex field, a drive-time polygon, a route, pings
    g = ['<g mask="url(#mfade)">']
    r = 19
    dx = 1.5 * r
    dy = math.sqrt(3) * r
    for col in range(14):
        for row in range(10):
            cx = 560 + col * dx
            cy = 20 + row * dy + (dy / 2 if col % 2 else 0)
            v = rnd.random()
            op = 0.0
            if v > 0.86:
                op = 0.55 + 0.45 * rnd.random()
            elif v > 0.62:
                op = 0.12 + 0.2 * rnd.random()
            fill = f'fill="{T["accent"]}" fill-opacity="{op:.2f}"' if op else 'fill="none"'
            g.append(f'<polygon points="{_hexagon(cx, cy, r - 1.5)}" {fill} stroke="{T["border2"]}" stroke-opacity="0.55" stroke-width="1"/>')
    # drive-time polygon (azure, dashed)
    poly = []
    for i in range(14):
        a = math.radians(i * 360 / 14)
        rr = 78 + 22 * math.sin(3 * a + 0.7) + 10 * math.cos(5 * a)
        poly.append(f"{780 + rr * 1.25 * math.cos(a):.1f},{160 + rr * 0.85 * math.sin(a):.1f}")
    g.append(f'<polygon points="{" ".join(poly)}" fill="{T["azure"]}" fill-opacity="0.08" stroke="{T["azure"]}" stroke-width="1.4" stroke-dasharray="5 4"/>')
    # route (lilac)
    g.append(f'<polyline points="600,268 660,236 702,244 742,204 790,196 836,150 882,138 930,96 972,74" fill="none" stroke="{T["lilac"]}" stroke-width="1.6" stroke-opacity="0.9"/>')
    # pings
    for (px, py) in [(742, 204), (836, 150), (930, 96), (684, 120), (872, 232), (612, 190)]:
        g.append(f'<circle cx="{px}" cy="{py}" r="9" fill="{T["accent"]}" fill-opacity="0.18"/>')
        g.append(f'<circle cx="{px}" cy="{py}" r="3.2" fill="{T["warm"]}"/>')
    # a "home" marker (gold, the one colour that is not chrome: it is a data mark)
    g.append(f'<rect x="783" y="155" width="10" height="10" fill="{T["gold"]}" transform="rotate(45 788 160)"/>')
    g.append("</g>")
    out += g

    # --- copy (left)
    out.append(text(40, 64, "// BIG DATA   ·   LOCATION INTELLIGENCE   ·   OPEN-SOURCE TOOLS", size=12, fill=T["t2"], mono=True, weight=500, ls=2.2))
    out.append(f'<text x="36" y="150" font-family="{SANS}" font-size="78" font-weight="800" letter-spacing="-1.5" fill="url(#wm)">KENZY ZERO</text>')
    out.append(f'<rect x="40" y="166" width="120" height="3" fill="{T["accent"]}"/>')
    out.append(text(40, 206, "I turn large-scale movement into decisions,", size=19, fill=T["hi"], weight=400))
    out.append(text(40, 232, "and build the tools to do it.", size=19, fill=T["hi"], weight=400))
    # status chips
    x = 40
    s, w = chip(x, 266, "ONLINE", T["green"], dot=True); out.append(s); x += w + 8
    s, w = chip(x, 266, "CREATOR OF KENZE", T["gold"]); out.append(s); x += w + 8
    s, w = chip(x, 266, "BUILDING SINCE MAY 2026", T["t2"]); out.append(s)
    return svg(H, "\n".join(out), ("Inter-400", "Inter-800", "JetBrainsMono-500"), "Kenzy Zero. Big data and location intelligence, and the open-source tools to do it.")


# ----------------------------------------------------------------------------
# 01 whoami
# ----------------------------------------------------------------------------

def whoami() -> str:
    H = 262
    out = [f'<rect width="{W}" height="{H}" fill="{T["bg"]}"/>',
           section("01", "whoami", "a terminal, because kenze is one")]
    # terminal
    x, y, w, h = 28, 62, W - 56, 180
    out.append(panel(x, y, w, h, T["card"], T["border"]))
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="30" rx="2" fill="{T["card2"]}"/>')
    out.append(f'<rect x="{x}" y="{y + 20}" width="{w}" height="10" fill="{T["card2"]}"/>')
    for i, cx in enumerate((x + 18, x + 36, x + 54)):
        out.append(f'<circle cx="{cx}" cy="{y + 15}" r="4.5" fill="{T["border2"]}"/>')
    out.append(text(x + w / 2, y + 19, "kenzy@zero: ~", size=11.5, fill=T["t3"], mono=True, anchor="middle"))
    ty = y + 58
    out.append(rich(x + 24, ty, [("$ ", T["accent"], 700), ("whoami", T["text"], 400)], size=14, mono=True))
    ty += 28
    out.append(rich(x + 24, ty, [("kenzy-zero", T["hi"], 700), ("   big data & location intelligence   ", T["t2"], 400), ("creator of kenze", T["gold"], 500)], size=14, mono=True))
    ty += 32
    out.append(rich(x + 24, ty, [("» ", T["accent"], 700), ("Day job: large-scale movement data, from raw device pings to the footfall,", T["text"], 400)], size=13.5, mono=True))
    ty += 21
    out.append(text(x + 44, ty, "audiences and maps that real decisions get made on.", size=13.5, fill=T["text"], mono=True))
    ty += 27
    out.append(rich(x + 24, ty, [("» ", T["accent"], 700), ("Side job: the open-source tools I wished existed while doing it. kenze came first.", T["text"], 400)], size=13.5, mono=True))
    ty += 30
    out.append(rich(x + 24, ty, [("$ ", T["accent"], 700)], size=14, mono=True))
    out.append(f'<rect x="{x + 42}" y="{ty - 12}" width="8" height="15" fill="{T["accent"]}"><animate attributeName="opacity" values="1;1;0;0" dur="1.1s" repeatCount="indefinite"/></rect>')
    return svg(H, "\n".join(out), ("JetBrainsMono-400", "JetBrainsMono-500", "JetBrainsMono-700"), "whoami: big data and location intelligence, creator of kenze")


# ----------------------------------------------------------------------------
# 02 what I do
# ----------------------------------------------------------------------------

def _icon_pin(x, y, c):
    return (f'<path d="M{x+12} {y+2} a8 8 0 0 0 -8 8 c0 6 8 14 8 14 s8 -8 8 -14 a8 8 0 0 0 -8 -8z" fill="none" stroke="{c}" stroke-width="1.6"/>'
            f'<circle cx="{x+12}" cy="{y+10}" r="2.6" fill="{c}"/>')


def _icon_engines(x, y, c):
    return (f'<rect x="{x+2}" y="{y+4}" width="9" height="16" rx="1" fill="none" stroke="{c}" stroke-width="1.6"/>'
            f'<rect x="{x+13}" y="{y+4}" width="9" height="16" rx="1" fill="none" stroke="{c}" stroke-width="1.6"/>'
            f'<line x1="{x+4.5}" y1="{y+9}" x2="{x+8.5}" y2="{y+9}" stroke="{c}" stroke-width="1.6"/>'
            f'<line x1="{x+15.5}" y1="{y+9}" x2="{x+19.5}" y2="{y+9}" stroke="{c}" stroke-width="1.6"/>'
            f'<line x1="{x+4.5}" y1="{y+13}" x2="{x+8.5}" y2="{y+13}" stroke="{c}" stroke-width="1.6"/>'
            f'<line x1="{x+15.5}" y1="{y+13}" x2="{x+19.5}" y2="{y+13}" stroke="{c}" stroke-width="1.6"/>')


def _icon_map(x, y, c):
    return (f'<path d="M{x+2} {y+6} l6 -3 l8 3 l6 -3 v15 l-6 3 l-8 -3 l-6 3z" fill="none" stroke="{c}" stroke-width="1.6" stroke-linejoin="round"/>'
            f'<line x1="{x+8}" y1="{y+3}" x2="{x+8}" y2="{y+18}" stroke="{c}" stroke-width="1.2" opacity="0.7"/>'
            f'<line x1="{x+16}" y1="{y+6}" x2="{x+16}" y2="{y+21}" stroke="{c}" stroke-width="1.2" opacity="0.7"/>')


def _icon_check(x, y, c):
    s = ""
    for i, yy in enumerate((y + 5, y + 12, y + 19)):
        s += f'<rect x="{x+2}" y="{yy-3}" width="6" height="6" rx="1" fill="none" stroke="{c}" stroke-width="1.5"/>'
        s += f'<line x1="{x+11}" y1="{yy}" x2="{x+22}" y2="{yy}" stroke="{c}" stroke-width="1.5" opacity="{0.9 if i < 2 else 0.5}"/>'
    s += f'<path d="M{x+3} {y+5} l2 2 l3 -4" fill="none" stroke="{c}" stroke-width="1.5"/>'
    s += f'<path d="M{x+3} {y+12} l2 2 l3 -4" fill="none" stroke="{c}" stroke-width="1.5"/>'
    return s


def whatido() -> str:
    H = 352
    out = [f'<rect width="{W}" height="{H}" fill="{T["bg"]}"/>',
           section("02", "what I do", "the whole path: raw files to shipped product")]
    out.append(text(28, 80, "Large-scale location and movement data, end to end. The raw files, the cleaning that decides whether", size=15.5, fill=T["text"]))
    out.append(text(28, 103, "a number can be trusted, the analysis, the maps, and the product it all ships in.", size=15.5, fill=T["text"]))

    tiles = [
        (_icon_pin, "Movement data at scale",
         ["Billions of raw device pings, cleaned", "and turned into footfall, catchments,", "home and work areas, audiences."], T["accent"]),
        (_icon_engines, "Two engines, one rule set",
         ["DuckDB on a laptop. PySpark on a", "cluster. The same cleaning rules,", "proven to give the same answer."], T["azure"]),
        (_icon_map, "Maps people can use",
         ["Indoor store polygons, drive-time", "areas, story maps, dashboards that", "filter the map as you click."], T["lilac"]),
        (_icon_check, "The unglamorous part",
         ["De-duplication, sink detection, time", "zones, determinism, run logs. Done", "properly, every single time."], T["green"]),
    ]
    x0, y0, tw, th, gap = 28, 130, 226, 192, 13
    for i, (ic, title, lines, col) in enumerate(tiles):
        x = x0 + i * (tw + gap)
        out.append(panel(x, y0, tw, th, T["card"], T["border"]))
        out.append(f'<rect x="{x}" y="{y0}" width="{tw}" height="2" fill="{col}"/>')
        out.append(f'<rect x="{x + 18}" y="{y0 + 20}" width="36" height="36" rx="2" fill="{col}" fill-opacity="0.10" stroke="{col}" stroke-opacity="0.35"/>')
        out.append(ic(x + 24, y0 + 26, col))
        out.append(text(x + 18, y0 + 90, title, size=15.5, fill=T["hi"], weight=600))
        for j, ln in enumerate(lines):
            out.append(text(x + 18, y0 + 116 + j * 20, ln, size=12.3, fill=T["t2"]))
        out.append(text(x + 18, y0 + th - 14, f"0{i + 1}", size=10.5, fill=col, mono=True, weight=700, ls=1))
    return svg(H, "\n".join(out), ("Inter-400", "Inter-600", "JetBrainsMono-500", "JetBrainsMono-700"), "What I do")


# ----------------------------------------------------------------------------
# 03 building: project cards
# ----------------------------------------------------------------------------

def _project(num, name, status, status_color, subtitle, desc_lines, features, right, H, header=None, color=None):
    color = color or status_color
    out = [f'<rect width="{W}" height="{H}" fill="{T["bg"]}"/>']
    top = 0
    if header:
        out.append(section("03", "building", header))
        top = 62
    x, y, w, h = 28, top, W - 56, H - top - 12 if header else H - 24
    if not header:
        y = 12
    out.append(panel(x, y, w, h, T["surface"], T["border"]))
    out.append(f'<rect x="{x}" y="{y}" width="3" height="{h}" fill="{color}"/>')
    # name + status
    out.append(text(x + 28, y + 46, name, size=30, fill=T["hi"], weight=800))
    nw = len(name) * 30 * 0.58
    s, cw = chip(x + 28 + nw + 16, y + 26, status, status_color)
    out.append(s)
    out.append(text(x + w - 16, y + h - 12, num, size=10.5, fill=T["t3"], mono=True, ls=1, anchor="end"))
    out.append(text(x + 28, y + 76, subtitle, size=16, fill=T["text"], weight=600))
    for i, ln in enumerate(desc_lines):
        out.append(text(x + 28, y + 102 + i * 20, ln, size=13.2, fill=T["t2"]))
    # features: two columns
    fy = y + 102 + len(desc_lines) * 20 + 14
    colw = 290
    for i, f in enumerate(features):
        cx = x + 28 + (i % 2) * colw
        cy = fy + (i // 2) * 24
        out.append(marker(cx, cy - 7, color, 6))
        out.append(text(cx + 14, cy, f, size=12.6, fill=T["text"], mono=True))
    # right panel
    out.append(right(x + w - 340, y + 24, 316, h - 48))
    return out


def _shell_panel(x, y, w, h):
    o = [panel(x, y, w, h, T["card"], T["border2"])]
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="26" rx="2" fill="{T["card2"]}"/>')
    o.append(f'<rect x="{x}" y="{y + 18}" width="{w}" height="8" fill="{T["card2"]}"/>')
    o.append(text(x + w / 2, y + 17, "kenze", size=11, fill=T["t3"], mono=True, anchor="middle"))
    lines = [
        [("kenze > ", T["gold"], 700), ("load sales.parquet", T["hi"], 400)],
        [("  60,000,000 rows · opened in 0.4 s", T["t2"], 400)],
        [("kenze > ", T["gold"], 700), ("filter city = 'Lon", T["hi"], 400), ("don'", T["t3"], 400)],
        [("  autocomplete: real values, exact counts", T["t2"], 400)],
        [("kenze > ", T["gold"], 700), ("plot amount --by city", T["hi"], 400)],
        [("  London  ████████████  41%", T["accent"], 400)],
        [("  Paris   ███████       24%", T["accent"], 400)],
        [("  Tokyo   ████          13%", T["accent"], 400)],
        [("kenze > ", T["gold"], 700), ("run clean.csv", T["hi"], 400)],
        [("  streamed through DuckDB · no OOM ✓", T["green"], 400)],
    ]
    ty = y + 50
    for ln in lines:
        o.append(rich(x + 16, ty, ln, size=12, mono=True))
        ty += 19.5
    return "\n".join(o)


def card_kenze() -> str:
    H = 362
    out = _project(
        "03.1", "kenze", "LIVE ON PYPI", T["gold"],
        "Big-file data prep that never runs out of memory.",
        ["An interactive shell and a one-line CLI for CSV, Parquet, JSON and Excel files too big",
         "for pandas. DuckDB does the heavy lifting; kenze auto-sizes memory so the job never",
         "crashes. No SQL to learn, no lock-in: every recipe ejects to plain SQL or Python."],
        ["40 commands, no SQL", "autocomplete knows your values",
         "live preview on every step", "model-ready in one step",
         "PDF / HTML client reports", "Excel, GeoJSON, s3:// in and out"],
        _shell_panel, H, header="shipped · in development · next",
    )
    return svg(H, "\n".join(out), ("Inter-400", "Inter-600", "Inter-800", "JetBrainsMono-400", "JetBrainsMono-500", "JetBrainsMono-700"), "kenze: big-file data prep that never runs out of memory")


def _hub_panel(x, y, w, h):
    c = T["lilac"]
    o = [panel(x, y, w, h, T["card"], T["border2"])]
    # a grid (messy file) on the left
    gx, gy = x + 18, y + 26
    for r in range(7):
        for col in range(5):
            op = 0.9 if (r + col) % 3 else 0.35
            fill = c if (r == 0) else T["t3"]
            o.append(f'<rect x="{gx + col * 24}" y="{gy + r * 16}" width="21" height="12" rx="1" fill="{fill}" fill-opacity="{op if r else 0.9}"/>')
    o.append(text(gx, gy + 7 * 16 + 20, "big messy file", size=10.5, fill=T["t2"], mono=True))
    # arrow
    ax = x + 150
    o.append(f'<line x1="{ax}" y1="{y + h / 2 - 10}" x2="{ax + 34}" y2="{y + h / 2 - 10}" stroke="{c}" stroke-width="1.6"/>')
    o.append(f'<path d="M{ax + 28} {y + h / 2 - 16} l7 6 l-7 6" fill="none" stroke="{c}" stroke-width="1.6"/>')
    # a document on the right
    dx, dy = x + 206, y + 24
    o.append(f'<rect x="{dx}" y="{dy}" width="92" height="118" rx="2" fill="{T["card2"]}" stroke="{c}" stroke-opacity="0.6"/>')
    o.append(f'<rect x="{dx + 12}" y="{dy + 14}" width="44" height="6" rx="1" fill="{T["hi"]}"/>')
    o.append(f'<rect x="{dx + 12}" y="{dy + 28}" width="68" height="3" rx="1" fill="{T["t3"]}"/>')
    o.append(f'<rect x="{dx + 12}" y="{dy + 36}" width="60" height="3" rx="1" fill="{T["t3"]}"/>')
    for i, hgt in enumerate((22, 34, 16, 28, 40)):
        o.append(f'<rect x="{dx + 12 + i * 13}" y="{dy + 96 - hgt}" width="9" height="{hgt}" fill="{c}" fill-opacity="{0.45 + i * 0.12}"/>')
    o.append(f'<rect x="{dx + 12}" y="{dy + 104}" width="68" height="3" rx="1" fill="{T["t3"]}"/>')
    o.append(text(dx, dy + 118 + 20, "client-ready PDF", size=10.5, fill=T["t2"], mono=True))
    o.append(text(x + w - 14, y + h - 12, "nothing leaves the machine", size=10, fill=T["t3"], mono=True, anchor="end"))
    return "\n".join(o)


def card_kenzehub() -> str:
    H = 300
    out = _project(
        "03.2", "Kenzehub", "IN DEVELOPMENT · PRIVATE", T["lilac"],
        "Big messy files in, a client-ready document out.",
        ["A local-first desktop app (Tauri + DuckDB) that opens files far bigger than Excel can,",
         "lets you shape and check them in a grid, and writes a finished PDF, Word or HTML report.",
         "No account, no upload, no server. The export is fully offline too."],
        ["opens files Excel cannot", "edit and check in a grid",
         "PDF · Word · HTML out", "zero scripts in the export",
         "thousands of tests", "public once it is polished"],
        _hub_panel, H,
    )
    return svg(H, "\n".join(out), ("Inter-400", "Inter-600", "Inter-800", "JetBrainsMono-400", "JetBrainsMono-500"), "Kenzehub: big messy files in, a client-ready document out")


def _plan_panel(x, y, w, h):
    c = T["azure"]
    o = [panel(x, y, w, h, T["card"], T["border2"])]
    # floor plan outline
    px, py = x + 18, y + 26
    o.append(f'<rect x="{px}" y="{py}" width="118" height="104" fill="none" stroke="{T["t2"]}" stroke-width="1.4"/>')
    for (rx, ry, rw, rh, lab) in [(0, 0, 44, 40, "101"), (44, 0, 40, 40, "102"), (84, 0, 34, 58, "103"), (0, 40, 30, 64, "104"), (30, 58, 88, 46, "105")]:
        o.append(f'<rect x="{px + rx}" y="{py + ry}" width="{rw}" height="{rh}" fill="{c}" fill-opacity="0.07" stroke="{T["t2"]}" stroke-width="0.9"/>')
        o.append(text(px + rx + rw / 2, py + ry + rh / 2 + 3, lab, size=8.5, fill=T["t2"], mono=True, anchor="middle"))
    o.append(text(px, py + 104 + 20, "vector PDF floor plan", size=10.5, fill=T["t2"], mono=True))
    ax = x + 150
    o.append(f'<line x1="{ax}" y1="{y + h / 2 - 10}" x2="{ax + 34}" y2="{y + h / 2 - 10}" stroke="{c}" stroke-width="1.6"/>')
    o.append(f'<path d="M{ax + 28} {y + h / 2 - 16} l7 6 l-7 6" fill="none" stroke="{c}" stroke-width="1.6"/>')
    # json-ish output
    jx, jy = x + 204, y + 28
    lines = [[("{", T["t2"])], [('  "type"', c), (": ", T["t2"]), ('"Feature"', T["hi"])],
             [('  "unit"', c), (": ", T["t2"]), ('"105"', T["hi"])],
             [('  "category"', c), (": ", T["t2"]), ('"retail"', T["hi"])],
             [('  "geometry"', c), (": {…}", T["t2"])], [("}", T["t2"])]]
    for i, ln in enumerate(lines):
        o.append(rich(jx, jy + 10 + i * 16, ln, size=10.5, mono=True))
    o.append(text(jx, jy + 10 + 6 * 16 + 10, "IMDF ✓  GeoJSON ✓", size=10.5, fill=T["green"], mono=True))
    o.append(text(x + w - 14, y + h - 12, "offline · validated against the spec", size=10, fill=T["t3"], mono=True, anchor="end"))
    return "\n".join(o)


def card_kenzeplan() -> str:
    H = 300
    out = _project(
        "03.3", "kenzeplan", "EARLY BUILD", T["azure"],
        "A vector PDF floor plan in, IMDF and GeoJSON out, fully offline.",
        ["Reads the shapes and unit labels from the plan, joins them to a tenant list, georeferences",
         "the floor and writes the OGC IMDF standard, validated locally. On known ground truth it",
         "recovers 9 units in 10, with 99.7% attached to the right shape. Clean-room, from scratch."],
        ["PDF vectors to polygons", "labels joined to tenants",
         "georeferenced floors", "IMDF validated locally",
         "no upload, no account", "DXF input is next"],
        _plan_panel, H,
    )
    return svg(H, "\n".join(out), ("Inter-400", "Inter-600", "Inter-800", "JetBrainsMono-400", "JetBrainsMono-500"), "kenzeplan: a vector PDF floor plan in, IMDF and GeoJSON out")


def next_up() -> str:
    H = 118
    c = T["green"]
    out = [f'<rect width="{W}" height="{H}" fill="{T["bg"]}"/>', panel(28, 12, W - 56, H - 24, T["surface"], T["border"])]
    out.append(f'<rect x="28" y="12" width="3" height="{H - 24}" fill="{c}"/>')
    out.append(text(56, 50, "K-Series", size=22, fill=T["hi"], weight=800))
    s, _ = chip(56 + 22 * 0.58 * 8 + 14, 32, "NEXT · GROUNDWORK", c)
    out.append(s)
    out.append(text(56, 80, "The mobility data layer: a GeoParquet profile plus the movement verbs (cleaning, home, work, dwell, trips, catchments),", size=13.2, fill=T["t2"]))
    out.append(text(56, 98, "built on kenze's engine. Starts once Kenzehub is out.", size=13.2, fill=T["t2"]))
    out.append(text(W - 44, 98, "03.4", size=10.5, fill=T["t3"], mono=True, anchor="end", ls=1))
    return svg(H, "\n".join(out), ("Inter-400", "Inter-800", "JetBrainsMono-500"), "Next up: K-Series, the mobility data layer")


# ----------------------------------------------------------------------------
# 04 stack
# ----------------------------------------------------------------------------

def stack() -> str:
    rows = [
        ("DATA", T["accent"], [("Python", "python"), ("DuckDB", "duckdb"), ("PySpark", "apachespark"), ("pandas", "pandas"), ("Parquet", None), ("Arrow", None), ("Excel in / out", None)]),
        ("GEO", T["azure"], [("GeoPandas", None), ("PostGIS", "postgresql"), ("H3", None), ("GeoParquet", None), ("MapLibre", "maplibre"), ("Kepler.gl", None), ("Overture Maps", None), ("Turf.js", None)]),
        ("APP", T["lilac"], [("TypeScript", "typescript"), ("React", "react"), ("Tauri", "tauri"), ("Node.js", "nodedotjs"), ("FastAPI", "fastapi"), ("DuckDB-wasm", "duckdb")]),
        ("INFRA", T["green"], [("AWS S3", "amazons3"), ("Git", "git"), ("GitHub Actions", "githubactions"), ("WSL · Linux", None), ("PowerShell", None)]),
    ]
    H = 62 + len(rows) * 46 + 10
    out = [f'<rect width="{W}" height="{H}" fill="{T["bg"]}"/>', section("04", "stack", "what the work is actually done in")]
    y = 72
    for label, col, items in rows:
        out.append(text(28, y + 20, label, size=11, fill=col, mono=True, weight=700, ls=1.6))
        x = 96
        for name, slug in items:
            cw = int(len(name) * 12.5 * 0.6 + 44 + (0 if slug else -8))
            out.append(f'<rect x="{x}" y="{y}" width="{cw}" height="30" rx="2" fill="{T["card"]}" stroke="{T["border"]}"/>')
            if slug:
                out.append(icon(slug, x + 11, y + 8, 14, T["text"]))
                out.append(text(x + 33, y + 19.5, name, size=12.5, fill=T["text"], mono=True))
            else:
                out.append(marker(x + 12, y + 12, col, 6))
                out.append(text(x + 26, y + 19.5, name, size=12.5, fill=T["text"], mono=True))
            x += cw + 8
        y += 46
    return svg(H, "\n".join(out), ("JetBrainsMono-400", "JetBrainsMono-500", "JetBrainsMono-700"), "Stack")


# ----------------------------------------------------------------------------
# 06 connect chips (one file each so every chip is its own link)
# ----------------------------------------------------------------------------

def link_chip(slug: str | None, label: str, handle: str) -> str:
    w, h = 200, 46
    out = [panel(0.5, 0.5, w - 1, h - 1, T["card"], T["border2"])]
    out.append(f'<rect x="0.5" y="0.5" width="3" height="{h - 1}" fill="{T["accent"]}"/>')
    if slug:
        out.append(icon(slug, 14, 15, 16, T["hi"]))
    else:
        out.append(text(14, 29, "in", size=15, fill=T["hi"], weight=800))
    out.append(text(42, 19, label.upper(), size=9.5, fill=T["t3"], mono=True, weight=500, ls=1.4))
    out.append(text(42, 35, handle, size=11, fill=T["hi"], mono=True, weight=500))
    return svg(h, "\n".join(out), ("Inter-800", "JetBrainsMono-500"), f"{label}: {handle}", w=w)


def footer() -> str:
    H = 56
    out = [f'<rect width="{W}" height="{H}" fill="{T["bg"]}"/>',
           '<defs><linearGradient id="fl" x1="0" y1="0" x2="1" y2="0">'
           f'<stop offset="0" stop-color="{T["accent"]}" stop-opacity="0"/><stop offset="0.5" stop-color="{T["accent"]}"/>'
           f'<stop offset="1" stop-color="{T["accent"]}" stop-opacity="0"/></linearGradient></defs>',
           f'<rect x="0" y="0" width="{W}" height="1" fill="url(#fl)"/>',
           f'<circle cx="40" cy="32" r="3" fill="{T["accent"]}"><animate attributeName="opacity" values="1;0.2;1" dur="2.4s" repeatCount="indefinite"/></circle>',
           text(54, 36, "STILL SHIPPING", size=11, fill=T["t2"], mono=True, weight=500, ls=2),
           text(W / 2, 36, "KENZY ZERO", size=11, fill=T["t3"], mono=True, weight=500, ls=3, anchor="middle"),
           text(W - 40, 36, "GITHUB.COM/KENZY-ZERO  ·  2026", size=11, fill=T["t2"], mono=True, weight=500, ls=1.6, anchor="end")]
    return svg(H, "\n".join(out), ("JetBrainsMono-500",), "Still shipping")


def main() -> None:
    write("hero.svg", hero())
    write("whoami.svg", whoami())
    write("whatido.svg", whatido())
    write("card-kenze.svg", card_kenze())
    write("card-kenzehub.svg", card_kenzehub())
    write("card-kenzeplan.svg", card_kenzeplan())
    write("next-up.svg", next_up())
    write("stack.svg", stack())
    write("link-github.svg", link_chip("github", "GitHub", "github.com/Kenzy-Zero"))
    write("link-linkedin.svg", link_chip(None, "LinkedIn", "in/kenzy-zero"))
    write("link-x.svg", link_chip("x", "X", "@kenzy_zero"))
    write("link-reddit.svg", link_chip("reddit", "Reddit", "u/kenzy_zero"))
    write("link-devto.svg", link_chip("devdotto", "dev.to", "dev.to/kenzyzero"))
    write("link-email.svg", link_chip("gmail", "Email", "kenzy.zero.k0@gmail.com"))
    write("link-pypi.svg", link_chip("pypi", "PyPI", "pypi.org/project/kenze"))
    write("footer.svg", footer())


if __name__ == "__main__":
    main()
