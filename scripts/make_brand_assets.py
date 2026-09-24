#!/usr/bin/env python3
"""Generate the banner and footer SVGs in the profile's paper-and-ink style.

    assets/banner.svg        assets/banner-dark.svg
    assets/footer.svg        assets/footer-dark.svg

The style is a hand-drawn notebook: warm paper, ink outlines, a hard un-blurred
offset shadow, a dot-grid texture, a highlighter-yellow label pill and a dashed
rule. Everything is authored here rather than by hand so the light and dark
variants can never drift apart.

Fonts are deliberately system-only: an SVG loaded through <img> renders in
secure static mode and cannot fetch a webfont, so a Google font would silently
fall back.

Run locally:  python scripts/make_brand_assets.py
"""

from __future__ import annotations

from pathlib import Path

from palette import HAND, PALETTE, SANS

ASSETS = Path(__file__).resolve().parent.parent / "assets"

NAME = "Canyon-Li"
TAGLINE = "AI Agent Developer"
SUBHEAD = "Python / TypeScript · Building Peregrine"
COLOPHON = "✦ Canyon-Li · AI Agent Developer ✦"

BANNER_W, BANNER_H = 1200, 310
BANNER_CARD_H = 276
RADIUS = 26
SHADOW_X, SHADOW_Y = 14, 16
STROKE = 3
PAD = 64


def banner(theme: str) -> str:
    p = PALETTE[theme]
    card_w = BANNER_W - 2 * STROKE - SHADOW_X
    divider_y = 102
    right = STROKE + card_w - PAD  # right edge of the padded content column

    # Light dots read as a faint texture on cream; on dark paper the same
    # opacity turns into confetti, so pull them back.
    dot_a, dot_b = (0.20, 0.45) if theme == "light" else (0.16, 0.22)

    # Three ink-stroked dots, echoing the reference style's window decoration.
    dots = "".join(
        f'<circle cx="{right - 44 + i * 20}" cy="64" r="5.5" '
        f'fill="none" stroke="{p["ink"]}" stroke-width="2.5"/>'
        for i in range(3)
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{BANNER_W}" height="{BANNER_H}" \
viewBox="0 0 {BANNER_W} {BANNER_H}" fill="none" role="img" aria-label="{NAME} — {TAGLINE}">
  <defs>
    <pattern id="dot-a" width="29" height="29" patternUnits="userSpaceOnUse">
      <circle cx="4" cy="4" r="1.7" fill="{p["purple"]}" opacity="{dot_a}"/>
    </pattern>
    <pattern id="dot-b" width="37" height="37" patternUnits="userSpaceOnUse">
      <circle cx="29" cy="11" r="1.7" fill="{p["yellow"]}" opacity="{dot_b}"/>
    </pattern>
    <clipPath id="card">
      <rect x="{STROKE}" y="{STROKE}" width="{card_w}" height="{BANNER_CARD_H}" rx="{RADIUS}"/>
    </clipPath>
  </defs>

  <!-- hard offset shadow, then the card itself -->
  <rect x="{STROKE + SHADOW_X}" y="{STROKE + SHADOW_Y}" width="{card_w}" \
height="{BANNER_CARD_H}" rx="{RADIUS}" fill="{p["purple"]}"/>
  <rect x="{STROKE}" y="{STROKE}" width="{card_w}" height="{BANNER_CARD_H}" \
rx="{RADIUS}" fill="{p["paper"]}" stroke="{p["ink"]}" stroke-width="{STROKE}"/>

  <g clip-path="url(#card)">
    <rect x="{STROKE}" y="{STROKE}" width="{card_w}" height="{BANNER_CARD_H}" fill="url(#dot-a)"/>
    <rect x="{STROKE}" y="{STROKE}" width="{card_w}" height="{BANNER_CARD_H}" fill="url(#dot-b)"/>
  </g>

  <!-- label pill, tilted a touch, with its own hard shadow -->
  <g transform="rotate(-1.5 {PAD} 64)">
    <rect x="{PAD + 3}" y="49" width="228" height="36" rx="7" fill="{p["ink"]}"/>
    <rect x="{PAD}" y="46" width="228" height="36" rx="7" fill="{p["yellow2"]}" \
stroke="{p["ink"]}" stroke-width="2"/>
    <text x="{PAD + 114}" y="70" text-anchor="middle" font-family='{SANS}' \
font-size="16" font-weight="700" fill="{p["ink"]}" letter-spacing="0.6">{TAGLINE}</text>
  </g>

  {dots}

  <line x1="{PAD}" y1="{divider_y}" x2="{right}" y2="{divider_y}" \
stroke="{p["line"]}" stroke-width="2" stroke-dasharray="9 8"/>

  <text x="{PAD}" y="196" font-family='{SANS}' font-size="74" font-weight="800" \
fill="{p["ink"]}" letter-spacing="-1.5">{NAME}</text>
  <text x="{PAD}" y="244" font-family='{SANS}' font-size="21" \
fill="{p["muted"]}">{SUBHEAD}</text>
</svg>
"""


def footer(theme: str) -> str:
    p = PALETTE[theme]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="112" \
viewBox="0 0 1200 112" fill="none" role="img" aria-label="{COLOPHON}">
  <line x1="{PAD}" y1="8" x2="{1200 - PAD}" y2="8" stroke="{p["line"]}" \
stroke-width="2" stroke-dasharray="9 8"/>
  <text x="600" y="72" text-anchor="middle" font-family='{HAND}' font-size="26" \
fill="{p["muted"]}">{COLOPHON}</text>
</svg>
"""


def main() -> int:
    ASSETS.mkdir(exist_ok=True)
    for theme in ("light", "dark"):
        suffix = "" if theme == "light" else "-dark"
        (ASSETS / f"banner{suffix}.svg").write_text(banner(theme), encoding="utf-8")
        (ASSETS / f"footer{suffix}.svg").write_text(footer(theme), encoding="utf-8")
    print("wrote banner/footer (light + dark) to assets/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
