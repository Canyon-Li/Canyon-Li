"""Single source of truth for the profile's paper-and-ink palette.

Shared by the brand assets (banner, footer) and the third-party card theming so
the two can never drift apart. Mirrors the tokens used by the hand-drawn
"paper notebook" style: warm paper, ink outlines, hard offset shadows and a
purple/yellow accent pair.
"""

PALETTE = {
    "light": {
        "paper": "#f7f1e5",  # page background
        "paper2": "#fffaf0",  # card surface
        "ink": "#282522",  # outlines and primary text
        "muted": "#70695f",  # secondary text
        "purple": "#8e7bb8",  # shadow + emphasis
        "purple2": "#e9e1f2",
        "yellow": "#f2d778",  # highlighter
        "yellow2": "#fff2b8",
        "line": "#d8cdbb",  # dashed rules
    },
    "dark": {
        "paper": "#262019",
        "paper2": "#2d271f",
        "ink": "#eee6d8",
        "muted": "#a89e8d",
        "purple": "#b7a8da",
        "purple2": "#3c3449",
        "yellow": "#d9c069",
        "yellow2": "#453c22",
        "line": "#4a4234",
    },
}

# Handwriting stack, used the way the source style uses it: for the colophon
# and small annotations only, never for body copy. All system fonts — an SVG in
# an <img> is rendered in secure static mode and cannot load a webfont.
HAND = ('"Segoe Print", "Bradley Hand", "Comic Sans MS", '
        '"KaiTi", "STKaiti", cursive')

# Body stack, matched to the reference style's sans.
SANS = ('"Segoe UI", -apple-system, "PingFang SC", "Microsoft YaHei", '
        'system-ui, sans-serif')
