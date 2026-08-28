"""
One-off asset prep: cut the plain-white background out of images.jpg
(the bride & groom illustration) so it can float over the temple photo
as a real transparent PNG instead of a CSS mask hack.

Flood-fills "background-like" (light, low-saturation) pixels starting
only from the image border, so it never eats into light-colored parts
of the illustration itself (the groom's cream shirt, gold jewellery,
etc.) unless they're actually touching the outer edge.
"""
from collections import deque
import numpy as np
from PIL import Image, ImageFilter

SRC = "images.jpg"
OUT = "couple.png"

img = Image.open(SRC).convert("RGB")
arr = np.array(img).astype(np.int16)
h, w, _ = arr.shape

maxc = arr.max(axis=2)
minc = arr.min(axis=2)
sat = maxc - minc
is_bg_like = (minc > 195) & (sat < 30)

visited = np.zeros((h, w), dtype=bool)
q = deque()

def seed(y, x):
    if is_bg_like[y, x] and not visited[y, x]:
        visited[y, x] = True
        q.append((y, x))

for x in range(w):
    seed(0, x)
    seed(h - 1, x)
for y in range(h):
    seed(y, 0)
    seed(y, w - 1)

while q:
    y, x = q.popleft()
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ny, nx = y + dy, x + dx
        if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx] and is_bg_like[ny, nx]:
            visited[ny, nx] = True
            q.append((ny, nx))

alpha = np.where(visited, 0, 255).astype(np.uint8)
alpha_img = Image.fromarray(alpha, mode="L").filter(ImageFilter.GaussianBlur(1.1))

out = img.convert("RGBA")
out.putalpha(alpha_img)

# trim to the illustration's actual bounding box so the PNG has no
# wasted transparent margin (keeps it crisp and easy to size in CSS)
bbox = out.getbbox()
if bbox:
    pad = 6
    l, t, r, b = bbox
    l = max(0, l - pad); t = max(0, t - pad)
    r = min(w, r + pad); b = min(h, b + pad)
    out = out.crop((l, t, r, b))

out.save(OUT)
print("saved", OUT, out.size)
