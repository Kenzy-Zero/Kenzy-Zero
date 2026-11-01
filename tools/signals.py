"""Render assets/signals.svg from the GitHub GraphQL contribution calendar.

    GH_TOKEN=... python tools/signals.py

Runs daily in .github/workflows/signals.yml with the workflow's own token.
Private repositories count toward the numbers (GitHub's "include private
contributions" setting is on); their names never appear anywhere.
On any API failure the script exits non-zero and the previous card stays.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys
import urllib.request

from kz import T, W, hairline, panel, rich, section, svg, text, write

LOGIN = "Kenzy-Zero"
QUERY = """
query($login:String!, $from:DateTime!, $to:DateTime!) {
  user(login:$login) {
    contributionsCollection(from:$from, to:$to) {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount weekday } }
      }
    }
    repositories(ownerAffiliations: OWNER) { totalCount }
  }
}
"""


def fetch() -> dict:
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        sys.exit("GH_TOKEN is not set")
    to = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
    frm = to - dt.timedelta(days=364)
    body = json.dumps({"query": QUERY, "variables": {"login": LOGIN, "from": frm.isoformat(), "to": to.isoformat()}}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql", data=body,
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json", "User-Agent": "kenzy-zero-profile"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.load(r)
    if "errors" in data or not data.get("data", {}).get("user"):
        sys.exit(f"GraphQL error: {json.dumps(data)[:500]}")
    return data["data"]["user"]


def streaks(days: list[dict]) -> tuple[int, int, int]:
    longest = run = 0
    for d in days:
        run = run + 1 if d["contributionCount"] > 0 else 0
        longest = max(longest, run)
    i = len(days) - 1
    if days[i]["contributionCount"] == 0:
        i -= 1  # today may still be empty
    current = 0
    while i >= 0 and days[i]["contributionCount"] > 0:
        current += 1
        i -= 1
    active = sum(1 for d in days if d["contributionCount"] > 0)
    return current, longest, active


def render(user: dict) -> str:
    cal = user["contributionsCollection"]["contributionCalendar"]
    weeks = cal["weeks"]
    days = [d for w in weeks for d in w["contributionDays"]]
    total = cal["totalContributions"]
    current, longest, active = streaks(days)
    repos = user["repositories"]["totalCount"]
    today = days[-1]["date"]
    peak = max(d["contributionCount"] for d in days)

    H = 322
    out = [f'<rect width="{W}" height="{H}" fill="{T["bg"]}"/>',
           section("05", "signals", f"updated {today} · includes private work")]

    # ---- stats (left)
    stats = [
        (f"{total:,}", "CONTRIBUTIONS", "last 12 months", T["accent"]),
        (f"{current}", "CURRENT STREAK", "days in a row", T["warm"]),
        (f"{longest}", "LONGEST STREAK", "days in a row", T["azure"]),
        (f"{active}", "ACTIVE DAYS", f"of {len(days)} · peak {peak} in a day", T["lilac"]),
    ]
    x0, y0 = 28, 64
    bw, bh, gap = 176, 96, 10
    for i, (num, label, sub, col) in enumerate(stats):
        x = x0 + (i % 2) * (bw + gap)
        y = y0 + (i // 2) * (bh + gap)
        out.append(panel(x, y, bw, bh, T["card"], T["border"]))
        out.append(f'<rect x="{x}" y="{y}" width="{bw}" height="2" fill="{col}"/>')
        out.append(text(x + 16, y + 52, num, size=34, fill=T["hi"], weight=800))
        out.append(text(x + 16, y + 70, label, size=10, fill=col, mono=True, weight=700, ls=1.4))
        out.append(text(x + 16, y + 84, sub, size=10, fill=T["t3"], mono=True))

    # ---- heatmap (right)
    hx, hy = 424, 72
    cell, cgap = 8.0, 2.4
    step = cell + cgap
    # colour ramp by quantile of non-zero days
    nz = sorted(d["contributionCount"] for d in days if d["contributionCount"] > 0)
    def q(p):
        return nz[min(len(nz) - 1, int(p * len(nz)))] if nz else 1
    t1, t2, t3 = q(0.25), q(0.5), q(0.8)
    def shade(n):
        if n <= 0:
            return T["card2"], 1.0
        if n <= t1:
            return T["accent"], 0.28
        if n <= t2:
            return T["accent"], 0.5
        if n <= t3:
            return T["accent"], 0.75
        return T["warm"], 1.0
    month_marks = []
    last_month = None
    for wi, w in enumerate(weeks):
        for d in w["contributionDays"]:
            col, op = shade(d["contributionCount"])
            x = hx + wi * step
            y = hy + d["weekday"] * step
            out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell}" height="{cell}" rx="1.5" fill="{col}" fill-opacity="{op}"/>')
            m = d["date"][:7]
            if m != last_month and d["weekday"] == 0 or (last_month is None):
                if m != last_month:
                    month_marks.append((x, dt.date.fromisoformat(d["date"]).strftime("%b")))
                    last_month = m
    for x, m in month_marks[1:]:
        out.append(text(x, hy - 10, m, size=9.5, fill=T["t3"], mono=True))
    for wd, lab in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        out.append(text(hx - 8, hy + wd * step + 8, lab, size=9, fill=T["t3"], mono=True, anchor="end"))
    # legend
    lx = hx + len(weeks) * step - 6 * 14 - 30
    ly = hy + 7 * step + 16
    out.append(text(lx - 10, ly + 8, "less", size=9.5, fill=T["t3"], mono=True, anchor="end"))
    for i, (col, op) in enumerate([(T["card2"], 1), (T["accent"], 0.28), (T["accent"], 0.5), (T["accent"], 0.75), (T["warm"], 1)]):
        out.append(f'<rect x="{lx + i * 14}" y="{ly}" width="{cell}" height="{cell}" rx="1.5" fill="{col}" fill-opacity="{op}"/>')
    out.append(text(lx + 5 * 14 + 4, ly + 8, "more", size=9.5, fill=T["t3"], mono=True))

    # ---- footer line
    out.append(hairline(28, H - 34, W - 28))
    out.append(rich(28, H - 14, [("▣ ", T["accent"], 700), (f"{repos} repositories, 2 public. ", T["t2"], 400),
                                 ("The rest stay private until they are polished enough to show.", T["t3"], 400)], size=10.5, mono=True))
    out.append(text(W - 28, H - 14, "rendered daily by a GitHub Action", size=9.5, fill=T["t3"], mono=True, anchor="end"))
    return svg(H, "\n".join(out), ("Inter-800", "JetBrainsMono-400", "JetBrainsMono-500", "JetBrainsMono-700"), f"Signals: {total:,} contributions in the last 12 months")


if __name__ == "__main__":
    write("signals.svg", render(fetch()))
