#!/usr/bin/env python3
"""Render the contribution graph as a space-invader animation (animated SVG).

A small ship flies under the grid from left to right, stops under every
week that has contributions and shoots each green cell, which flashes and
turns empty. When the sweep ends the grid refills and the loop restarts.

Writes a light and a dark SVG into the output directory (default: dist/).
Needs GITHUB_TOKEN (the Actions token is enough) for the GraphQL API.
"""
import json
import os
import sys
import urllib.request

OWNER = os.environ.get("GH_OWNER", "yyoel")
OUT_DIR = sys.argv[1] if len(sys.argv) > 1 else "dist"

# Geometry (px)
CELL, GAP = 11, 3
PITCH = CELL + GAP
COLS, ROWS = 53, 7
PAD_X, PAD_Y = 16, 12
GRID_W, GRID_H = COLS * PITCH - GAP, ROWS * PITCH - GAP
SHIP_Y = PAD_Y + GRID_H + 22  # top of the ship
WIDTH, HEIGHT = GRID_W + 2 * PAD_X, SHIP_Y + 22

# Timing (seconds)
MOVE = 0.09         # ship travel per column
FIRE_GAP = 0.16     # time between shots in one column
BULLET_SPEED = 520  # px/s
FLASH = 0.12        # how long a hit cell flashes
START_HOLD = 0.8    # pause before the ship starts
END_HOLD = 2.0      # pause after the last hit, before the reset

LEVELS = ["NONE", "FIRST_QUARTILE", "SECOND_QUARTILE", "THIRD_QUARTILE", "FOURTH_QUARTILE"]
PALETTES = {
    "light": {
        "cells": ["#ebedf0", "#9be9a8", "#40c463", "#30a14e", "#216e39"],
        "ship": "#0969da", "bullet": "#bf8700", "flash": "#fb8f44",
    },
    "dark": {
        "cells": ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"],
        "ship": "#58a6ff", "bullet": "#e3b341", "flash": "#ffa657",
    },
}

# Pixel-art ship, 11 x 8; '#' is a filled pixel (2px each).
SHIP = [
    ".....#.....",
    "....###....",
    "....###....",
    ".#########.",
    "###########",
    "###########",
    "##.#####.##",
    "#.........#",
]
PX = 2
SHIP_W = len(SHIP[0]) * PX

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        weeks { contributionDays { weekday contributionLevel } }
      }
    }
  }
}
"""


def fetch_grid():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        sys.exit("GITHUB_TOKEN is not set")
    body = json.dumps({"query": QUERY, "variables": {"login": OWNER}}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=body,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.load(resp)
    if "errors" in data:
        sys.exit(f"GraphQL error: {data['errors']}")
    weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    weeks = weeks[-COLS:]
    # grid[col][row] = level index, or None where the calendar has no day
    grid = [[None] * ROWS for _ in weeks]
    for c, week in enumerate(weeks):
        for day in week["contributionDays"]:
            grid[c][day["weekday"]] = LEVELS.index(day["contributionLevel"])
    return grid


def cell_xy(c, r):
    return PAD_X + c * PITCH, PAD_Y + r * PITCH


def ship_x(c):
    """Left edge of the ship when it is centred under column c."""
    return PAD_X + c * PITCH + CELL / 2 - SHIP_W / 2


def plan(grid):
    """Return ship stops, shots and total loop length (all times in seconds)."""
    t = START_HOLD
    stops = [(0.0, ship_x(-2))]  # ship waits just left of the grid
    stops.append((t, ship_x(-2)))
    shots = []  # (col, row, fire_time, hit_time)
    last_hit = t
    for c, col in enumerate(grid):
        t += MOVE
        stops.append((t, ship_x(c)))
        targets = [r for r in range(ROWS - 1, -1, -1) if col[r]]  # bottom row first
        for i, r in enumerate(targets):
            fire = t + i * FIRE_GAP
            dist = SHIP_Y - (cell_xy(c, r)[1] + CELL)
            hit = fire + dist / BULLET_SPEED
            shots.append((c, r, fire, hit))
            last_hit = max(last_hit, hit)
        if targets:
            t += len(targets) * FIRE_GAP
            stops.append((t, ship_x(c)))
    t += MOVE * 3
    stops.append((t, ship_x(COLS + 1)))  # fly off to the right
    total = max(t, last_hit) + END_HOLD
    return stops, shots, total


def pct(t, total):
    return f"{100 * t / total:.3f}%"


def render(grid, theme):
    pal = PALETTES[theme]
    stops, shots, total = plan(grid)
    css, body = [], []

    css.append(
        f"rect.c{{width:{CELL}px;height:{CELL}px;rx:2px}}"
        f".a{{animation-duration:{total:.2f}s;animation-iteration-count:infinite;"
        f"animation-timing-function:linear}}"
    )

    # Static / animated cells
    hit_at = {(c, r): (fire, hit) for c, r, fire, hit in shots}
    for c, col in enumerate(grid):
        for r, level in enumerate(col):
            if level is None:
                continue
            x, y = cell_xy(c, r)
            colour = pal["cells"][level]
            if (c, r) not in hit_at:
                body.append(f'<rect class="c" x="{x}" y="{y}" fill="{colour}"/>')
                continue
            name = f"h{c}_{r}"
            _, hit = hit_at[(c, r)]
            empty = pal["cells"][0]
            css.append(
                f"@keyframes {name}{{0%,{pct(hit, total)}{{fill:{colour}}}"
                f"{pct(hit + 0.02, total)},{pct(hit + FLASH, total)}{{fill:{pal['flash']}}}"
                f"{pct(hit + FLASH + 0.02, total)},{pct(total - 0.6, total)}{{fill:{empty}}}"
                f"100%{{fill:{colour}}}}}"
                f".{name}{{animation-name:{name}}}"
            )
            body.append(f'<rect class="c a {name}" x="{x}" y="{y}" fill="{colour}"/>')

    # Bullets: a 2x6 bolt from the ship nose up to the cell
    nose_y = SHIP_Y - 6
    for c, r, fire, hit in shots:
        name = f"b{c}_{r}"
        bx = PAD_X + c * PITCH + CELL / 2 - 1
        target_y = cell_xy(c, r)[1] + CELL - 6
        dy = target_y - nose_y
        css.append(
            f"@keyframes {name}{{0%,{pct(fire, total)}{{opacity:0;transform:translateY(0)}}"
            f"{pct(fire + 0.02, total)}{{opacity:1;transform:translateY(0)}}"
            f"{pct(hit, total)}{{opacity:1;transform:translateY({dy:.1f}px)}}"
            f"{pct(hit + 0.02, total)},100%{{opacity:0;transform:translateY({dy:.1f}px)}}}}"
            f".{name}{{animation-name:{name}}}"
        )
        body.append(
            f'<rect class="a {name}" x="{bx:.1f}" y="{nose_y}" width="2" height="6" '
            f'fill="{pal["bullet"]}" opacity="0"/>'
        )

    # Ship path: hold, sweep, fly off, then jump back to the start
    frames = [f"{pct(t, total)}{{transform:translateX({x:.1f}px)}}" for t, x in stops]
    frames.append(f"100%{{transform:translateX({ship_x(COLS + 1):.1f}px)}}")
    css.append("@keyframes ship{" + "".join(frames) + "}.ship{animation-name:ship}")
    pixels = "".join(
        f'<rect x="{i * PX}" y="{SHIP_Y + j * PX}" width="{PX}" height="{PX}"/>'
        for j, row in enumerate(SHIP)
        for i, ch in enumerate(row)
        if ch == "#"
    )
    body.append(f'<g class="a ship" fill="{pal["ship"]}">{pixels}</g>')

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}">'
        f"<style>{''.join(css)}</style>"
        f"{''.join(body)}</svg>\n"
    )


def main():
    grid = fetch_grid()
    os.makedirs(OUT_DIR, exist_ok=True)
    for theme, filename in (("light", "space-invaders.svg"), ("dark", "space-invaders-dark.svg")):
        path = os.path.join(OUT_DIR, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(render(grid, theme))
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
