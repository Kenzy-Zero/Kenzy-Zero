"""Shared design system for the Kenzy Zero profile cards.

Tokens follow the SIGNAL palette (deep sea-blue ground, cyan accent) and the
Inter + JetBrains Mono pair. Fonts are embedded in every SVG as base64 woff2
subsets from assets/fonts, so the cards render identically inside GitHub's
image proxy, where no external font can be loaded.
"""
from __future__ import annotations

import base64
import json
import os
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_DIR = os.path.join(ROOT, "assets", "fonts")
ICONS = json.load(open(os.path.join(os.path.dirname(__file__), "icons.json"), encoding="utf-8"))

T = {
    "bg": "#070d12",
    "surface": "#0c151c",
    "card": "#111d26",
    "card2": "#16252f",
    "accent": "#00dbe9",
    "warm": "#7af2fa",
    "lilac": "#ebb2ff",
    "azure": "#4c8dff",
    "hi": "#f2f8fb",
    "text": "#dbe7ee",
    "t2": "#86a0b0",
    "t3": "#5a7282",
    "border": "#1f3240",
    "border2": "#2c4556",
    "green": "#5fc27e",
    "yellow": "#f59e0b",
    "gold": "#f0b429",
}

SANS = "Inter, 'Segoe UI', system-ui, -apple-system, Roboto, sans-serif"
MONO = "'JetBrains Mono', ui-monospace, 'Cascadia Code', Menlo, Consolas, monospace"

W = 1000  # every card shares this width so they align on the page


def _b64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def fonts(*names: str) -> str:
    """Return a <style> block embedding the requested font files.

    names are like "Inter-400" or "JetBrainsMono-500".
    """
    faces = []
    for n in names:
        family, weight = n.rsplit("-", 1)
        family_css = "Inter" if family == "Inter" else "JetBrains Mono"
        data = _b64(os.path.join(FONT_DIR, n + ".woff2"))
        faces.append(
            f"@font-face{{font-family:'{family_css}';font-style:normal;font-weight:{weight};"
            f"src:url(data:font/woff2;base64,{data}) format('woff2');}}"
        )
    return "<style>" + "".join(faces) + "</style>"


def svg(h: int, body: str, font_names: tuple[str, ...], label: str, w: int = W) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-label="{escape(label)}">\n{fonts(*font_names)}\n{body}\n</svg>\n'
    )


def text(x, y, s, *, size=14, fill=T["text"], mono=False, weight=400, anchor="start", ls=0, extra=""):
    fam = MONO if mono else SANS
    ls_attr = f' letter-spacing="{ls}"' if ls else ""
    return (
        f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" font-weight="{weight}" '
        f'fill="{fill}" text-anchor="{anchor}"{ls_attr}{extra}>{escape(s)}</text>'
    )


def rich(x, y, parts, *, size=14, mono=False, weight=400, anchor="start"):
    """One <text> with several coloured <tspan>s. parts = [(string, fill, weight|None), ...]."""
    fam = MONO if mono else SANS
    spans = []
    for p in parts:
        s, fill = p[0], p[1]
        w = p[2] if len(p) > 2 and p[2] else weight
        spans.append(f'<tspan fill="{fill}" font-weight="{w}">{escape(s)}</tspan>')
    return (
        f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" font-weight="{weight}" '
        f'text-anchor="{anchor}">{"".join(spans)}</text>'
    )


def panel(x, y, w, h, fill=T["surface"], stroke=T["border"], rx=2):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="1"/>'


def hairline(x1, y, x2, color=T["border"]):
    return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{color}" stroke-width="1"/>'


def grid_pattern(pid="grid", step=24, color=T["border"], opacity=0.35):
    return (
        f'<pattern id="{pid}" width="{step}" height="{step}" patternUnits="userSpaceOnUse">'
        f'<path d="M {step} 0 L 0 0 0 {step}" fill="none" stroke="{color}" stroke-width="1" opacity="{opacity}"/>'
        f"</pattern>"
    )


def section(num: str, title: str, tag: str, y: int = 30, x: int = 28, right: int = W - 28) -> str:
    """Tactical section header: `01 // WHOAMI` left, `// tag` right, hairline under."""
    out = [
        rich(x, y, [(num, T["accent"], 700), ("  //  ", T["t3"], 400), (title.upper(), T["t2"], 500)], size=12, mono=True),
        text(right, y, "// " + tag, size=11, fill=T["t3"], mono=True, anchor="end"),
        hairline(x, y + 14, right),
    ]
    return "\n".join(out)


def chip(x, y, label, color, *, size=10.5, pad=10, h=22, dot=False):
    """A small mono status chip; dot=True adds a pulsing dot before the label. Returns (svg, width)."""
    lead = 14 if dot else 0
    w = int(len(label) * (size * 0.6 + 0.8) + pad * 2 + lead)
    s = (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="{color}" fill-opacity="0.10" stroke="{color}" stroke-width="1"/>'
        + text(x + pad + lead, y + h / 2 + 3.8, label, size=size, fill=color, mono=True, weight=500, ls=0.8)
    )
    if dot:
        s += (f'<circle cx="{x + pad + 3}" cy="{y + h / 2}" r="2.6" fill="{color}">'
              f'<animate attributeName="opacity" values="1;0.25;1" dur="2.2s" repeatCount="indefinite"/></circle>')
    return s, w


def icon(slug: str, x: float, y: float, size: float = 14, fill: str = T["text"]) -> str:
    d = ICONS[slug]
    k = size / 24.0
    return f'<g transform="translate({x},{y}) scale({k:.4f})"><path d="{d}" fill="{fill}"/></g>'


def marker(x, y, color, size=6):
    return f'<rect x="{x}" y="{y}" width="{size}" height="{size}" fill="{color}"/>'


def write(name: str, content: str) -> None:
    path = os.path.join(ROOT, "assets", name)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"{name:28s} {os.path.getsize(path):>8,d} bytes")
