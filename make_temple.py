"""
Generates an original, hand-designed South Indian temple gopuram as a tall
SVG — not a stock photo. Deliberately tall (400x1300) so that panning the
background from y=0% to y=100% during scroll travels from the crown at the
top down to the entrance archway at the bottom, with no zoom involved.

Run: python make_temple.py   ->  writes temple.svg
"""

W = 400
H = 1300

KUMKUM       = "#9E1B32"
KUMKUM_DARK  = "#6E0F20"
KUMKUM_DEEP  = "#4A0C18"
GOLD         = "#D4A017"
GOLD_LIGHT   = "#F1CD6B"
LEAF         = "#4B7447"
LEAF_DARK    = "#2F4E2C"
STONE        = "#C98A3A"

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
        f'fill="{fill}" opacity="0.9"/>'
    )
    circle(cx, cy + h * 0.08, h * 0.16, dot_fill)

# ---------------------------------------------------------------------------
# 1. Sky — cool dark at the crown, warming toward the entrance
# ---------------------------------------------------------------------------
defs = f'''
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%"   stop-color="{KUMKUM_DEEP}"/>
    <stop offset="35%"  stop-color="{KUMKUM_DARK}"/>
    <stop offset="70%"  stop-color="{KUMKUM}"/>
    <stop offset="100%" stop-color="#c9622f"/>
  </linearGradient>
  <radialGradient id="doorGlow" cx="50%" cy="15%" r="85%">
    <stop offset="0%"  stop-color="#ffdd9a" stop-opacity="0.9"/>
    <stop offset="100%" stop-color="#2a0810" stop-opacity="1"/>
  </radialGradient>
  <radialGradient id="groundGlow" cx="50%" cy="0%" r="70%">
    <stop offset="0%"  stop-color="#ffce7a" stop-opacity="0.55"/>
    <stop offset="100%" stop-color="#ffce7a" stop-opacity="0"/>
  </radialGradient>
'''
parts.append(f'<defs>{defs}</defs>')
rect(0, 0, W, H, "url(#sky)")

# ---------------------------------------------------------------------------
# 2. Finial — kalasham pot + flag at the very top of the tower
# ---------------------------------------------------------------------------
FIN_Y = 46
parts.append(f'<rect x="{W/2-2:.1f}" y="10" width="4" height="40" fill="{GOLD}"/>')
parts.append(f'<polygon points="{W/2+2:.1f},12 {W/2+34:.1f},22 {W/2+2:.1f},32" fill="{KUMKUM}"/>')
circle(W/2, FIN_Y + 14, 11, GOLD)
circle(W/2, FIN_Y + 30, 15, GOLD_LIGHT)
circle(W/2, FIN_Y + 30, 15, "none", "")
parts.append(f'<circle cx="{W/2:.1f}" cy="{FIN_Y+30:.1f}" r="15" fill="none" stroke="{KUMKUM_DARK}" stroke-width="2"/>')

# ---------------------------------------------------------------------------
# 3. Tiers — tapering trapezoids, alternating tone, each with niches +
#    a thin gold cornice and a couple of pulsing diya lights
# ---------------------------------------------------------------------------
N_TIERS = 8
TIER_TOP = 108
TIER_BOTTOM = 1010
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

    # cornice ledge between tiers
    rect((W - w1) / 2 - 6, y1 - 5, w1 + 12, 6, GOLD)

    # niches along the tier, spaced to its width
    n_niches = max(2, round(w0 / 58))
    usable = w0 * 0.72
    niche_h = (y1 - y0) * 0.5
    niche_w = min(22, usable / n_niches * 0.55)
    cy = y0 + (y1 - y0) * 0.52
    if n_niches == 1:
        xs = [W / 2]
    else:
        xs = [W / 2 - usable / 2 + usable * k / (n_niches - 1) for k in range(n_niches)]
    for x in xs:
        niche(x, cy, niche_w, niche_h, GOLD_LIGHT, KUMKUM_DEEP)

    if i in (2, 4, 6):
        diya_positions.append((W / 2 - w0 * 0.32, y1 - 5))
        diya_positions.append((W / 2 + w0 * 0.32, y1 - 5))

for (dx, dy) in diya_positions:
    circle(dx, dy, 4, GOLD_LIGHT, cls="diya-glow")

# ---------------------------------------------------------------------------
# 4. Base plinth
# ---------------------------------------------------------------------------
PLINTH_Y = TIER_BOTTOM
PLINTH_H = 46
PLINTH_W = BASE_W + 60
rect((W - PLINTH_W) / 2, PLINTH_Y, PLINTH_W, PLINTH_H, STONE)
rect((W - PLINTH_W) / 2, PLINTH_Y, PLINTH_W, 8, GOLD)

# ---------------------------------------------------------------------------
# 5. Entrance wall + arched doorway
# ---------------------------------------------------------------------------
WALL_Y = PLINTH_Y + PLINTH_H
WALL_H = 170
WALL_W = PLINTH_W
rect((W - WALL_W) / 2, WALL_Y, WALL_W, WALL_H, KUMKUM_DARK)

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

# flanking pillar lamps (kombu vilakku)
for side in (-1, 1):
    lx = W / 2 + side * (DOOR_W / 2 + 34)
    lamp_top = WALL_Y + 30
    lamp_bot = WALL_Y + WALL_H - 10
    rect(lx - 4, lamp_top, 8, lamp_bot - lamp_top, GOLD)
    rect(lx - 16, lamp_bot, 32, 10, STONE)
    circle(lx, lamp_top - 8, 10, GOLD_LIGHT, cls="diya-glow")

# ---------------------------------------------------------------------------
# 6. Steps leading up to the threshold
# ---------------------------------------------------------------------------
STEP_Y = WALL_Y + WALL_H
step_w = WALL_W
step_h = (H - STEP_Y) / 3
for s in range(3):
    sw = step_w + s * 34
    rect((W - sw) / 2, STEP_Y + s * step_h, sw, step_h + 1, STONE if s % 2 == 0 else "#b87a2e")
rect(0, H - 26, W, 26, "url(#groundGlow)")

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
{"".join(parts)}
</svg>
'''

with open("temple.svg", "w", encoding="utf-8") as f:
    f.write(svg)

print("wrote temple.svg", len(svg), "bytes")
