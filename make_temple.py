"""
Generates an original, hand-designed South Indian temple gopuram as a tall,
BACKGROUND-TRANSPARENT SVG fragment — not a stock photo, no sky baked in
(the page's own CSS gradient behind it provides the sky, so colors stay in
one place and always match the site theme).

Deliberately tall (400x1300) so that sliding it up within a clipped,
overflow:hidden container travels from the crown at the top down to the
entrance archway at the bottom, with no zoom involved.

Composition borrows two ideas from a reference photo the couple liked
(ornate multi-band tiers, small flanking shrines beside the main entrance)
but is entirely hand-drawn here in the site's own kumkum/gold palette so it
blends with the rest of the page instead of clashing.

Run: python make_temple.py
  -> writes temple.svg            (standalone, viewable file, for previewing)
  -> writes temple_inline.svg     (just the inner markup, no <svg> wrapper —
                                    paste this into index.html's <svg class="hero-bg-svg">)
"""

# W is wider than the tower itself so the two flanking shrines have room to
# sit beside the entrance wall without spilling off the canvas. H has to
# stay tall relative to W (roughly 1:3.4) or a phone-width viewport leaves
# almost no vertical overflow to pan through — see the note on .hero-bg-svg
# in index.html for how that overflow becomes the crown-to-entrance travel.
W = 560
H = 1900

# Vivid multi-tone Tamil gopuram palette (teal + magenta + gold), matching
# the colorful reference photo, instead of the site's kumkum-red UI accent.
# Kept separate from the site's CSS accent color on purpose — the temple is
# richly painted artwork, the UI chrome (buttons/nav) stays single-accent.
TEAL         = "#1E6B6E"
TEAL_DARK    = "#154E50"
TEAL_DEEP    = "#0E3638"
MAGENTA      = "#C23E70"
MAGENTA_DARK = "#8E2A54"
GOLD         = "#D4A017"
GOLD_LIGHT   = "#F1CD6B"
LEAF         = "#4B7447"
LEAF_DARK    = "#2F4E2C"
STONE        = "#C7BEB0"
STONE_DARK   = "#a89b86"
# aliases so the rest of the (already-written) generator code needs no
# structural changes — kumkum-named vars now carry the temple's own colors
KUMKUM       = TEAL
KUMKUM_DARK  = TEAL_DARK
KUMKUM_DEEP  = TEAL_DEEP

parts = []

def rect(x, y, w, h, fill, extra=""):
    parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" {extra}/>')

def trapezoid(y_top, y_bot, w_top, w_bot, fill, extra=""):
    x_tl, x_tr = (W - w_top) / 2, (W + w_top) / 2
    x_bl, x_br = (W - w_bot) / 2, (W + w_bot) / 2
    parts.append(
        f'<polygon points="{x_tl:.1f},{y_top:.1f} {x_tr:.1f},{y_top:.1f} '
        f'{x_br:.1f},{y_bot:.1f} {x_bl:.1f},{y_bot:.1f}" fill="{fill}" {extra}/>'
    )

def circle(cx, cy, r, fill, cls=""):
    cls_attr = f' class="{cls}"' if cls else ""
    parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}"{cls_attr}/>')

def niche(cx, cy, w, h, fill, dot_fill):
    """A small pointed-arch niche suggesting a sculpted deity figure."""
    hw = w / 2
    parts.append(
        f'<path d="M{cx-hw:.1f} {cy+h/2:.1f} L{cx-hw:.1f} {cy-h/6:.1f} '
        f'Q{cx:.1f} {cy-h/2:.1f} {cx+hw:.1f} {cy-h/6:.1f} L{cx+hw:.1f} {cy+h/2:.1f} Z" '
        f'fill="{fill}" opacity="0.95" stroke="{KUMKUM_DEEP}" stroke-width="0.8"/>'
    )
    circle(cx, cy + h * 0.08, h * 0.16, dot_fill)

def mini_kalasha(cx, cy, scale=1.0):
    """A tiny finial pot, echoing the crown, repeated at each tier's corners."""
    r = 3.6 * scale
    parts.append(f'<path d="M{cx-r:.1f} {cy:.1f} Q{cx:.1f} {cy-r*1.9:.1f} {cx+r:.1f} {cy:.1f} Z" fill="{GOLD}"/>')
    circle(cx, cy + r * 0.25, r * 0.55, GOLD_LIGHT)

def shrine(cx, base_y, w, h):
    """A small flanking mini-shrine: magenta-and-gold domed roof + body,
    deliberately a different hue from the main teal tower (matches the
    reference photo's maroon/pink corner shrines)."""
    body_h = h * 0.62
    body_y = base_y - body_h
    rect(cx - w / 2, body_y, w, body_h, MAGENTA_DARK)
    rect(cx - w / 2 - 4, base_y - 6, w + 8, 6, STONE)
    # domed roof
    parts.append(
        f'<path d="M{cx-w/2-4:.1f} {body_y:.1f} Q{cx:.1f} {body_y-h*0.55:.1f} {cx+w/2+4:.1f} {body_y:.1f} Z" fill="{MAGENTA}"/>'
    )
    circle(cx, body_y - h * 0.55, 4, GOLD_LIGHT, cls="diya-glow")
    # doorway
    dw, dh = w * 0.42, body_h * 0.55
    parts.append(
        f'<path d="M{cx-dw/2:.1f} {base_y:.1f} L{cx-dw/2:.1f} {base_y-dh+dw/2:.1f} '
        f'Q{cx:.1f} {base_y-dh-dw/4:.1f} {cx+dw/2:.1f} {base_y-dh+dw/2:.1f} L{cx+dw/2:.1f} {base_y:.1f} Z" '
        f'fill="#3d1428"/>'
    )

# ---------------------------------------------------------------------------
# 1. Finial — kalasham pot + flag at the very top of the tower
#    (no sky/background rect here — the page's own CSS gradient is the sky)
# ---------------------------------------------------------------------------
FIN_Y = 46
parts.append(f'<rect x="{W/2-2:.1f}" y="10" width="4" height="40" fill="{GOLD}"/>')
parts.append(f'<polygon points="{W/2+2:.1f},12 {W/2+34:.1f},22 {W/2+2:.1f},32" fill="{MAGENTA}"/>')
circle(W/2, FIN_Y + 14, 11, GOLD)
circle(W/2, FIN_Y + 30, 15, GOLD_LIGHT)
parts.append(f'<circle cx="{W/2:.1f}" cy="{FIN_Y+30:.1f}" r="15" fill="none" stroke="{KUMKUM_DARK}" stroke-width="2"/>')

# ---------------------------------------------------------------------------
# 2. Tiers — tapering trapezoids with a richer multi-band look: main body +
#    a thin accent band + gold cornice + sculpted niches + a couple of
#    pulsing diya lights, all narrowing toward the crown.
# ---------------------------------------------------------------------------
N_TIERS = 10
TIER_TOP = 140
TIER_BOTTOM = 1574
TOP_W = 86
BASE_W = 336

diya_positions = []

for i in range(N_TIERS):
    f0 = (i / N_TIERS) ** 0.72
    f1 = ((i + 1) / N_TIERS) ** 0.72
    y0 = TIER_TOP + (TIER_BOTTOM - TIER_TOP) * (i / N_TIERS)
    y1 = TIER_TOP + (TIER_BOTTOM - TIER_TOP) * ((i + 1) / N_TIERS)
    w0 = TOP_W + (BASE_W - TOP_W) * f0
    w1 = TOP_W + (BASE_W - TOP_W) * f1

    body = KUMKUM if i % 2 == 0 else KUMKUM_DARK
    trapezoid(y0, y1, w0, w1, body)

    # thin magenta accent band underscoring the niches — the second hue that
    # makes each tier read as multi-toned rather than a flat single color
    band_y = y0 + (y1 - y0) * 0.78
    band_w_top = TOP_W + (BASE_W - TOP_W) * ((i + 0.78) / N_TIERS) ** 0.72
    rect((W - band_w_top) / 2, band_y, band_w_top, 4.2, MAGENTA, 'opacity="0.85"')

    # cornice ledge between tiers, with a tiny finial pot at each outer corner
    rect((W - w1) / 2 - 6, y1 - 5, w1 + 12, 6, GOLD)
    mini_kalasha(W / 2 - w1 / 2 - 3, y1 - 9, scale=0.75 + i * 0.03)
    mini_kalasha(W / 2 + w1 / 2 + 3, y1 - 9, scale=0.75 + i * 0.03)

    # niches along the tier, spaced to its width
    n_niches = max(2, round(w0 / 58))
    usable = w0 * 0.72
    niche_h = (y1 - y0) * 0.5
    niche_w = min(22, usable / n_niches * 0.55)
    cy = y0 + (y1 - y0) * 0.5
    if n_niches == 1:
        xs = [W / 2]
    else:
        xs = [W / 2 - usable / 2 + usable * k / (n_niches - 1) for k in range(n_niches)]

    # thin pilaster ribs between/around the niches, for texture on the tier face
    rib_span = w0 * 0.86
    n_ribs = n_niches + 1
    for k in range(n_ribs):
        rxp = W / 2 - rib_span / 2 + rib_span * k / (n_ribs - 1) if n_ribs > 1 else W / 2
        parts.append(f'<line x1="{rxp:.1f}" y1="{y0+3:.1f}" x2="{rxp:.1f}" y2="{y1-7:.1f}" stroke="{KUMKUM_DEEP}" stroke-width="1" opacity="0.28"/>')

    for x in xs:
        niche(x, cy, niche_w, niche_h, GOLD_LIGHT, KUMKUM_DEEP)

    if i in (1, 3, 5, 7):
        diya_positions.append((W / 2 - w0 * 0.32, y1 - 5))
        diya_positions.append((W / 2 + w0 * 0.32, y1 - 5))

for (dx, dy) in diya_positions:
    circle(dx, dy, 4, GOLD_LIGHT, cls="diya-glow")

# ---------------------------------------------------------------------------
# 3. Base plinth
# ---------------------------------------------------------------------------
PLINTH_Y = TIER_BOTTOM
PLINTH_H = 46
PLINTH_W = BASE_W + 60
rect((W - PLINTH_W) / 2, PLINTH_Y, PLINTH_W, PLINTH_H, STONE)
rect((W - PLINTH_W) / 2, PLINTH_Y, PLINTH_W, 8, GOLD)

# ---------------------------------------------------------------------------
# 4. Entrance wall + arched doorway + two small flanking shrines
# ---------------------------------------------------------------------------
WALL_Y = PLINTH_Y + PLINTH_H
WALL_H = 170
WALL_W = PLINTH_W
# stone, not teal — the reference's base/entrance is neutral masonry, with
# color reserved for the tiers above and the shrines beside it
rect((W - WALL_W) / 2, WALL_Y, WALL_W, WALL_H, STONE_DARK)
rect((W - WALL_W) / 2, WALL_Y, WALL_W, 6, STONE)

SHRINE_W = 64
SHRINE_GAP = 10
for side in (-1, 1):
    shrine(W / 2 + side * (WALL_W / 2 + SHRINE_GAP + SHRINE_W / 2), WALL_Y + WALL_H, SHRINE_W, 108)

DOOR_W = 148
DOOR_X = (W - DOOR_W) / 2
DOOR_TOP = WALL_Y + 34
DOOR_BOTTOM = WALL_Y + WALL_H
parts.append(
    f'<path d="M{DOOR_X:.1f} {DOOR_BOTTOM:.1f} L{DOOR_X:.1f} {DOOR_TOP+40:.1f} '
    f'Q{W/2:.1f} {DOOR_TOP:.1f} {DOOR_X+DOOR_W:.1f} {DOOR_TOP+40:.1f} '
    f'L{DOOR_X+DOOR_W:.1f} {DOOR_BOTTOM:.1f} Z" fill="url(#doorGlow)" '
    f'stroke="{GOLD}" stroke-width="6"/>'
)

# toran garland draped above the arch: leaves + marigolds
GAR_Y = DOOR_TOP + 6
gar_span = DOOR_W + 30
n_scallop = 9
for k in range(n_scallop):
    gx = DOOR_X - 15 + gar_span * k / (n_scallop - 1)
    sway = 10 * (1 - ((k - (n_scallop - 1) / 2) / ((n_scallop - 1) / 2)) ** 2)
    leaf_y = GAR_Y + sway
    parts.append(f'<polygon points="{gx-7:.1f},{leaf_y:.1f} {gx:.1f},{leaf_y+16:.1f} {gx+7:.1f},{leaf_y:.1f}" fill="{LEAF}"/>')
    circle(gx, leaf_y - 6, 5, GOLD)
parts.append(f'<path d="M{DOOR_X-15:.1f} {GAR_Y:.1f} Q{W/2:.1f} {GAR_Y+22:.1f} {DOOR_X+gar_span-15:.1f} {GAR_Y:.1f}" fill="none" stroke="{LEAF_DARK}" stroke-width="3"/>')

# flanking pillar lamps (kombu vilakku), inside the shrines
for side in (-1, 1):
    lx = W / 2 + side * (DOOR_W / 2 + 34)
    lamp_top = WALL_Y + 30
    lamp_bot = WALL_Y + WALL_H - 10
    rect(lx - 4, lamp_top, 8, lamp_bot - lamp_top, GOLD)
    rect(lx - 16, lamp_bot, 32, 10, STONE)
    circle(lx, lamp_top - 8, 10, GOLD_LIGHT, cls="diya-glow")

# ---------------------------------------------------------------------------
# 5. Steps leading up to the threshold
# ---------------------------------------------------------------------------
STEP_Y = WALL_Y + WALL_H
step_w = WALL_W + 50
step_h = (H - STEP_Y) / 3
for s in range(3):
    sw = min(step_w + s * 24, W - 12)
    rect((W - sw) / 2, STEP_Y + s * step_h, sw, step_h + 1, STONE if s % 2 == 0 else STONE_DARK)
rect(0, H - 26, W, 26, "url(#groundGlow)")

# ---------------------------------------------------------------------------
# Assemble — defs (only glows now, no sky) + all shapes
# ---------------------------------------------------------------------------
defs = '''
  <radialGradient id="doorGlow" cx="50%" cy="15%" r="85%">
    <stop offset="0%"  stop-color="#ffdd9a" stop-opacity="0.9"/>
    <stop offset="100%" stop-color="#2a0810" stop-opacity="1"/>
  </radialGradient>
  <radialGradient id="groundGlow" cx="50%" cy="0%" r="70%">
    <stop offset="0%"  stop-color="#ffce7a" stop-opacity="0.55"/>
    <stop offset="100%" stop-color="#ffce7a" stop-opacity="0"/>
  </radialGradient>
'''
inline_body = f'<defs>{defs}</defs>' + "".join(parts)

with open("temple_inline.svg", "w", encoding="utf-8") as f:
    f.write(inline_body)

standalone = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{inline_body}</svg>\n'
with open("temple.svg", "w", encoding="utf-8") as f:
    f.write(standalone)

print("wrote temple.svg and temple_inline.svg —", len(inline_body), "bytes of markup")
