#!/usr/bin/env python3
"""Fetch the third-party profile cards, recolour them to the profile's paper/ink
palette and give them a hand-drawn frame (ink outline + hard offset shadow).

Outputs six self-hosted SVGs into assets/:

    assets/stats-{light,dark}.svg
    assets/streak-{light,dark}.svg
    assets/trophies-{light,dark}.svg

Self-hosting means the cards follow the page palette and can react to
prefers-color-scheme, which the upstream services do not support (dooboo
hardcodes a #26272D background; streak has no dark variant wiring).

Run locally:   python scripts/theme_cards.py
In CI:         .github/workflows/theme-cards.yml
"""

from __future__ import annotations

import re
import sys
import time
import urllib.request
from pathlib import Path

from palette import PALETTE

USER = "Canyon-Li"
ASSETS = Path(__file__).resolve().parent.parent / "assets"

# --------------------------------------------------------------------------
# Recolour maps. Keys are the colours dooboo/strea  emit; values are palette
# tokens. Replacements are single-pass, so no colour can be rewritten twice.
# --------------------------------------------------------------------------
STATS_MAP = {
    "light": {
        # card surface + text
        "#26272D": "#fffaf0",  # background
        "#FFFFFF": "#282522",  # primary text / icons / rank-1 bar
        "#646569": "#70695f",  # subtitle + percentage labels
        # language-bar prominence ramp, rank 2..6 (bright -> recedes into paper)
        "#96979B": "#4a443c",
        "#6F7073": "#6b6459",
        "#4D4E51": "#8c8477",
        "#3D3D41": "#aba295",
        "#36363A": "#c9c0b0",
        "#2E2F32": "#d8cdbb",
        # full-width activity gradient: purple -> lavender -> yellow
        "#AE7BFA": "#8e7bb8",
        "#6489E7": "#b9a8d8",
        "#78EDFD": "#f2d778",
        # avatar gradient: sepia -> purple family
        "#654747": "#6b5a8e",
        "#976A35": "#8e7bb8",
        "#957D61": "#a293c9",
        "#B79E78": "#b7a8da",
        "#8F7C5F": "#9d8cc4",
        "#CDB89F": "#e9e1f2",
    },
    "dark": {
        "#26272D": "#2d271f",
        "#FFFFFF": "#eee6d8",
        "#646569": "#a89e8d",
        "#96979B": "#c4bbab",
        "#6F7073": "#a89e8d",
        "#4D4E51": "#8a8172",
        "#3D3D41": "#6b6458",
        "#36363A": "#554e42",
        "#2E2F32": "#4a4234",
        "#AE7BFA": "#b7a8da",
        "#6489E7": "#8e7bb8",
        "#78EDFD": "#d9c069",
        "#654747": "#4a3f66",
        "#976A35": "#8e7bb8",
        "#957D61": "#7a6a9e",
        "#B79E78": "#9d8cc4",
        "#8F7C5F": "#6b5a8e",
        "#CDB89F": "#b7a8da",
    },
}

TROPHY_MAP = {
    "light": {
        "#26272D": "#fffaf0",
        "#FFFFFF": "#282522",  # achievement ring
        "#FFE713": "#f2d778",  # gold
        "#F29F23": "#e8c15c",
        "#FF7A00": "#d9b34a",
        "#CFCFCF": "#e9e1f2",  # silver -> pale lavender
        "#8F8F8F": "#c4b8d8",
        "#8D8D8D": "#d8cdbb",  # inner hairline
        "#F4A93A": "#70695f",  # tier label
    },
    "dark": {
        "#26272D": "#2d271f",
        "#FFFFFF": "#eee6d8",
        "#FFE713": "#d9c069",
        "#F29F23": "#b89a45",
        "#FF7A00": "#8a7330",
        "#CFCFCF": "#3c3449",
        "#8F8F8F": "#5a4e6e",
        "#8D8D8D": "#4a4234",
        "#F4A93A": "#a89e8d",
    },
}

# --------------------------------------------------------------------------
# Frame geometry — generous radius + hard, un-blurred offset shadow.
# --------------------------------------------------------------------------
STROKE = 2.5
SHADOW_X = 9
SHADOW_Y = 10
RADIUS = 16

COLOR_ATTR = re.compile(r'\b(fill|stroke|stop-color)="(#[0-9A-Fa-f]{3,6})"')
COLOR_CSS = re.compile(
    r'\b(stop-color\s*:\s*|fill\s*:\s*|color\s*:\s*|stroke\s*:\s*)(#[0-9A-Fa-f]{3,6})'
)
SVG_OPEN = re.compile(r"<svg\b[^>]*>", re.S)
NAMESPACE = re.compile(r'\s(xmlns(?::[\w-]+)?)="([^"]*)"')
ROOT_VIEWBOX = re.compile(
    r'<svg\b[^>]*?viewBox="([-\d.]+)\s+([-\d.]+)\s+([\d.]+)\s+([\d.]+)"', re.S
)
TILES = re.compile(
    r'<svg x="([\d.]+)" y="([\d.]+)" width="(\d+)" height="(\d+)" '
    r'viewBox="0 0 \d+ \d+" fill="none"'
)


def fetch(url: str, attempts: int = 4) -> str:
    """GET an SVG, retrying transient TLS/connection drops.

    These hosts intermittently abort the handshake mid-run
    (SSL: UNEXPECTED_EOF_WHILE_READING), which is worth a retry rather than
    abandoning the whole refresh.
    """
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; profile-card-themer/1.0)",
            "Accept": "image/svg+xml,image/*,*/*",
        },
    )
    last: Exception | None = None
    for attempt in range(attempts):
        if attempt:
            time.sleep(2 * attempt)
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                body = resp.read().decode("utf-8", "replace")
            if "<svg" not in body:
                raise RuntimeError(f"did not return SVG ({len(body)} bytes)")
            return body
        except Exception as exc:  # noqa: BLE001 — retry any transport error
            last = exc
    raise RuntimeError(f"{url}: {last}")


def recolour(src: str, mapping: dict[str, str]) -> str:
    """Single-pass colour substitution so one colour is never remapped twice."""

    def attr(m: re.Match[str]) -> str:
        return f'{m.group(1)}="{mapping.get(m.group(2).upper(), m.group(2))}"'

    def css(m: re.Match[str]) -> str:
        return f"{m.group(1)}{mapping.get(m.group(2).upper(), m.group(2))}"

    src = COLOR_ATTR.sub(attr, src)
    src = COLOR_CSS.sub(css, src)
    return src


def opaque_background(src: str) -> str:
    """Neutralise dooboo's own backdrop so the frame supplies the surface.

    dooboo paints both cards through one `.backgroundColor` class, so blanking
    that declaration is enough and leaves the hairline strokes intact. streak is
    a no-op here — it takes its background from the `background=` query
    parameter, which is already transparent.
    """
    src = re.sub(r"(\.backgroundColor\s*\{\s*fill\s*:\s*)#[0-9A-Fa-f]{3,6}",
                 r"\1none", src)
    return src


def static_card(src: str) -> str:
    """Freeze entrance animations to their finished state.

    Both services draw the card blank and fade it in — dooboo with SMIL, streak
    with CSS. Left alone the card is only populated while an animation is
    running, so anything that does not play them (a static renderer, a proxy
    that strips SMIL) shows an empty frame. Committing the finished state
    instead makes the asset deterministic.
    """
    # dooboo: SMIL
    src = re.sub(r"<animate\b[^>]*?/>", "", src)
    src = re.sub(r"<animate\b[^>]*?>.*?</animate\s*>", "", src, flags=re.S)

    # Reveal everything those animations used to fade in.
    src = re.sub(r'\sopacity="0"', ' opacity="1"', src)

    # dooboo's placeholder skeleton loops forever (repeatCount="indefinite");
    # with its animation gone it would sit on top of the data. Hide the group
    # after the blanket reveal above so it keeps opacity 0.
    src = src.replace(
        '<g id="currentStatsShapeLoading">',
        '<g id="currentStatsShapeLoading" opacity="0">',
        1,
    )

    # streak: CSS animations in inline styles
    src = re.sub(r"animation\s*:\s*[^;'\"]+;?", "", src)
    src = re.sub(r"(style='[^']*?)opacity:\s*0\b", r"\1opacity: 1", src)
    return src


def frame(src: str, theme: str, width: float, height: float) -> str:
    """Wrap the card body in an ink outline with a hard offset shadow."""
    p = PALETTE[theme]
    out_w = width + 2 * STROKE + SHADOW_X
    out_h = height + 2 * STROKE + SHADOW_Y

    open_tag = SVG_OPEN.search(src)
    if not open_tag:
        raise RuntimeError("no <svg> element found")

    # Carry over every namespace the original root declared. The stats card
    # still uses xlink:href after its animations are stripped, and an `unbound
    # prefix` error makes the whole document fail to parse — Chrome then paints
    # the frame with nothing inside it.
    ns = " ".join(f'{k}="{v}"' for k, v in NAMESPACE.findall(open_tag.group(0)))
    if not ns:
        ns = 'xmlns="http://www.w3.org/2000/svg"'

    attrs = (
        f"<svg {ns} "
        f'viewBox="-{STROKE} -{STROKE} {out_w:g} {out_h:g}" '
        f'width="{out_w:g}" height="{out_h:g}">'
    )
    prelude = (
        f'<g transform="translate({STROKE:g},{STROKE:g})">'
        f'<rect x="{SHADOW_X}" y="{SHADOW_Y}" width="{width:g}" height="{height:g}" '
        f'rx="{RADIUS}" fill="{p["purple"]}"/>'
        f'<rect x="0" y="0" width="{width:g}" height="{height:g}" rx="{RADIUS}" '
        f'fill="{p["paper2"]}" stroke="{p["ink"]}" stroke-width="{STROKE:g}"/>'
    )

    head = src[: open_tag.start()]
    body = src[open_tag.end():]
    # drop the original document's own closing tag; we re-close the wrapper
    body = re.sub(r"</svg\s*>\s*$", "", body.rstrip()) + "</g>"

    return f"{head}{attrs}{prelude}{body}</svg>\n"


def inner_size(src: str, default: tuple[float, float]) -> tuple[float, float]:
    """Tight bounding box of the drawn content.

    dooboo always lays trophies out on a 124px grid and pads the viewBox to a
    fixed 620px width, which leaves ~40% dead space on the right whenever the
    account holds fewer than five trophies. Measuring the actual tiles keeps the
    strip centred instead of hugging the left edge.

    Only a full-height row of tiles counts: the stats card also contains a
    nested 32px icon <svg>, which would otherwise be mistaken for a tile and
    shrink the card to a fraction of its real size.
    """
    m = ROOT_VIEWBOX.search(src)
    if not m:
        return default
    width, height = float(m.group(3)), float(m.group(4))

    tiles = [t for t in TILES.findall(src) if float(t[3]) == height]
    if len(tiles) > 1:
        width = max(float(x) + float(w) for x, _, w, _ in tiles)
    return width, height


def streak_url(theme: str) -> str:
    """streak-stats accepts colours as query parameters, so skip substitution."""
    p = PALETTE[theme]
    return (
        "https://streak-stats.demolab.com/"
        f"?user={USER}"
        "&hide_border=true"
        "&border_radius=14"
        "&background=00000000"
        f"&stroke={p['line'].lstrip('#')}"
        f"&ring={p['purple'].lstrip('#')}"
        f"&fire={p['yellow'].lstrip('#')}"
        f"&currStreakNum={p['ink'].lstrip('#')}"
        f"&currStreakLabel={p['purple'].lstrip('#')}"
        f"&sideNums={p['ink'].lstrip('#')}"
        f"&sideLabels={p['muted'].lstrip('#')}"
        f"&dates={p['muted'].lstrip('#')}"
    )


def build() -> list[str]:
    """Build all six cards in memory, then write them.

    Nothing touches the disk until every fetch has succeeded. Upstreams drop
    connections often enough that a mid-run failure is routine, and writing as
    we go would leave a half-updated assets/ — some cards fresh, others missing
    — which the README already links to.
    """
    # (filename, svg text, one-line report)
    plan: list[tuple[str, str, str]] = []

    for theme in ("light", "dark"):
        def note(kind: str, w: float, h: float) -> str:
            return f"{kind}-{theme}.svg  {w:g}x{h:g} -> {w + 14:g}x{h + 15:g}"

        # ---- stats -------------------------------------------------------
        raw = fetch(f"https://stats.dooboo.io/api/github-stats-advanced?login={USER}")
        w, h = inner_size(raw, (350.0, 208.0))
        body = static_card(recolour(opaque_background(raw), STATS_MAP[theme]))
        plan.append((f"stats-{theme}.svg", frame(body, theme, w, h), note("stats", w, h)))

        # ---- trophies ----------------------------------------------------
        raw = fetch(f"https://stats.dooboo.io/api/github-trophies?login={USER}")
        w, h = inner_size(raw, (620.0, 124.0))
        body = static_card(recolour(opaque_background(raw), TROPHY_MAP[theme]))
        plan.append((f"trophies-{theme}.svg", frame(body, theme, w, h), note("trophies", w, h)))

        # ---- streak ------------------------------------------------------
        raw = fetch(streak_url(theme))
        w, h = inner_size(raw, (495.0, 195.0))
        body = static_card(opaque_background(raw))
        plan.append((f"streak-{theme}.svg", frame(body, theme, w, h), note("streak", w, h)))

    for name, svg, _ in plan:
        (ASSETS / name).write_text(svg, encoding="utf-8")
    return [line for _, _, line in plan]


def main() -> int:
    ASSETS.mkdir(exist_ok=True)
    try:
        for line in build():
            print(line)
    except RuntimeError as exc:
        # A flaky upstream must not fail the workflow and lose the last good
        # assets. build() writes nothing until every fetch has succeeded, so
        # bailing here leaves the committed SVGs exactly as they were.
        print(f"::warning::card refresh skipped: {exc}", file=sys.stderr)
        return 0
    print("\nwrote 6 SVGs to assets/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
