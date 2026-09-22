#!/usr/bin/env python3
"""Draws the placeholder castle sprites. Usage: make_castle_art.py <output-dir>"""
import math, os, random, sys
from PIL import Image

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)


def H(s, a=255):
    s = s.lstrip("#")
    return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16), a)


CLEAR = (0, 0, 0, 0)


class Cv:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.img = Image.new("RGBA", (w, h), CLEAR)

    def px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.img.putpixel((x, y), c)

    def get(self, x, y):
        return self.img.getpixel((x, y))

    def rect(self, x, y, w, h, c):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.px(xx, yy, c)

    def save(self, name):
        self.img.save(os.path.join(OUT, name))


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


# ------------------------------------------------------------------ palettes
# Sunny sandstone: index 0 = brightest highlight ... 4 = deepest shade
STONE = [H("#f8efd6"), H("#ecdcb8"), H("#dcc9a0"), H("#c4ae84"), H("#a8916a")]
MORTAR = [H("#cdbf97"), H("#b9a97f"), H("#a4936b"), H("#8b7b5c"), H("#6f6149")]
BACKWALL = H("#8f7c58")          # dark stone seen through battlement gaps
TONES = [2, 2, 1, 2, 3, 2, 1, 2]  # per-brick tone variety (index into STONE)


def brick_color(x, y_global, tile_w, bw=8, bh=4, seed=0, level_fn=None):
    """Colour of one pixel of a running-bond brick wall."""
    course = y_global // bh
    offset = (bw // 2) if course % 2 else 0
    xx = (x + offset) % tile_w
    bi = xx // bw
    lx = xx % bw
    ly = y_global % bh
    level = level_fn(x) if level_fn else 0
    if lx == bw - 1 or ly == bh - 1:
        return MORTAR[clamp(2 + level, 0, 4)]
    tone = TONES[(course * 5 + bi * 3 + seed) % len(TONES)]
    idx = tone
    if ly == 0:
        idx -= 1
    elif ly == bh - 2:
        idx += 1
    return STONE[clamp(idx + level, 0, 4)]


def tower_level(x):
    """Cylinder shading: lit on the left, shadowed on the right."""
    if x < 3:
        return -1
    if x < 22:
        return 0
    if x < 28:
        return 1
    return 2


# ------------------------------------------------------------------ tower
def make_tower_body():
    cv = Cv(32, 32)
    for y in range(32):
        for x in range(32):
            cv.px(x, y, brick_color(x, y + 24, 32, seed=3, level_fn=tower_level))
    cv.save("tower-body.png")


def make_tower_cap():
    cv = Cv(32, 24)
    merlons = [(0, 5), (9, 5), (18, 5), (27, 5)]  # (x, width) -> 5 wide, 4-wide gaps
    in_merlon = lambda x: any(mx <= x < mx + mw for mx, mw in merlons)
    for y in range(24):
        for x in range(32):
            if y < 8:
                if in_merlon(x):
                    c = brick_color(x, y, 32, seed=3, level_fn=tower_level)
                    if y == 0:
                        c = STONE[clamp(0 + max(tower_level(x), 0), 0, 4)]
                    cv.px(x, y, c)
                elif y >= 4:
                    cv.px(x, y, BACKWALL)
            elif y == 8:
                cv.px(x, y, STONE[clamp(0 + max(tower_level(x), 0), 0, 4)])
            elif y == 9:
                cv.px(x, y, STONE[clamp(1 + tower_level(x), 0, 4)])
            elif y == 10:
                cv.px(x, y, STONE[4])
            else:
                cv.px(x, y, brick_color(x, y, 32, seed=3, level_fn=tower_level))
    cv.save("tower-cap.png")


def blob(cv, cx, cy, rx, ry, pal, rng=None):
    """A small leaf: ellipse lit from the upper left. pal = [hi, light, mid, dark]."""
    for dy in range(-ry - 1, ry + 2):
        for dx in range(-rx - 1, rx + 2):
            d = (dx / (rx + 0.5)) ** 2 + (dy / (ry + 0.5)) ** 2
            if d > 1.0:
                continue
            t = (dx / (rx + 0.5) + dy / (ry + 0.5)) / 2
            if d > 0.72:
                idx = 3
            elif t < -0.42:
                idx = 0
            elif t < -0.05:
                idx = 1
            elif t < 0.4:
                idx = 2
            else:
                idx = 3
            x, y = cx + dx, (cy + dy) % cv.h
            cv.px(x, y, pal[idx])


def make_tower_ivy():
    cv = Cv(32, 64)
    rng = random.Random(42)
    STEM, STEM_HI = H("#3b5a29"), H("#5b8237")
    LEAF = [H("#c4f08a"), H("#8fd451"), H("#5aa93b"), H("#356f2a")]

    vines = [
        (lambda y: 25 + 2.2 * math.sin(2 * math.pi * y / 64 * 2 + 0.6), +1),
        (lambda y: 6 + 2.2 * math.sin(2 * math.pi * y / 64 * 1 + 2.4), -1),
        (lambda y: 15 + 1.6 * math.sin(2 * math.pi * y / 64 * 3 + 1.1), 0),
    ]
    for vi, (fx, _) in enumerate(vines):
        thin = vi == 2
        for y in range(64):
            x = round(fx(y))
            cv.px(x, y, STEM)
            if not thin:
                cv.px(x - 1, y, STEM_HI)
        # leaves along the vine
        y = rng.randint(0, 3)
        side = 1
        while y < 64:
            x = round(fx(y))
            r = 2 if thin else rng.choice([2, 2, 3])
            off = r + 1 + rng.randint(0, 1)
            blob(cv, x + side * off, y + rng.randint(-1, 1), r, max(1, r - 1), LEAF)
            if rng.random() < 0.45:  # a second leaf on the other side
                blob(cv, x - side * (off + 1), y + 2, r - 1 if r > 2 else r, 1, LEAF)
            side = -side
            y += rng.randint(3, 5) if not thin else rng.randint(6, 9)
        # a couple of denser clumps
        for _ in range(0 if thin else 3):
            cy = rng.randint(0, 63)
            cx = round(fx(cy))
            for _ in range(4):
                blob(cv, cx + rng.randint(-4, 4), cy + rng.randint(-3, 3), 2, 2, LEAF)
    cv.save("tower-ivy.png")


def make_tower_window():
    cv = Cv(8, 14)
    L, B, S, D = STONE[1], STONE[2], STONE[3], STONE[4]
    K, K2 = H("#2a2a38"), H("#454d6b")
    for y in range(14):
        for x in range(8):
            if (x in (0, 7) and y < 2):
                continue
            if y == 0 and x in (1, 6):
                continue
            if y == 0:
                c = STONE[0]
            elif x == 0:
                c = L
            elif x == 7 or y == 13:
                c = D if x == 7 else S
            elif y >= 12:
                c = L
            else:
                c = B
            cv.px(x, y, c)
    # the slit itself
    for y in range(3, 12):
        cv.px(3, y, K2 if y > 8 else K)
        cv.px(4, y, K)
    cv.px(3, 2, K)
    cv.px(4, 2, K)
    cv.save("tower-window.png")


def make_banner():
    cv = Cv(16, 32)
    ROD, ROD_HI = H("#5b3a1a"), H("#8a5a2b")
    BL = [H("#4a82de"), H("#2f5fb3"), H("#234a8f")]
    GOLD, GOLD_HI, GOLD_DK = H("#f2b322"), H("#ffe27a"), H("#b87a10")
    for x in range(16):
        cv.px(x, 0, ROD_HI)
        cv.px(x, 1, ROD)
    cv.px(0, 0, GOLD_HI)
    cv.px(15, 0, GOLD_HI)
    for y in range(2, 32):
        notch = max(0, (y - 24)) * 1.15 if y >= 25 else -1
        for x in range(1, 15):
            if abs(x - 7.5) < notch:
                continue
            c = BL[0] if x < 5 else BL[1] if x < 11 else BL[2]
            if x in (1, 14):
                c = GOLD if x == 1 else GOLD_DK
            cv.px(x, y, c)
        if y == 3:
            for x in range(2, 14):
                cv.px(x, y, GOLD_HI if x < 8 else GOLD)
    # tail trim
    for y in range(25, 32):
        for x in range(1, 15):
            if cv.get(x, y)[3] and cv.get(x, y) != CLEAR and (
                (x + 1 < 16 and cv.get(x + 1, y)[3] == 0) or (x - 1 >= 0 and cv.get(x - 1, y)[3] == 0)
            ):
                cv.px(x, y, GOLD)
    # emblem: a gold coin
    coin = ["..GGG..", ".GHYYG.", "GHYYYDG", "GYYYYDG", "GYYYDDG", ".GDDDG.", "..GGG.."]
    pal = {"G": GOLD, "H": GOLD_HI, "Y": H("#ffd54a"), "D": GOLD_DK}
    for j, row in enumerate(coin):
        for i, ch in enumerate(row):
            if ch != ".":
                cv.px(4 + i, 9 + j, pal[ch])
    cv.save("tower-banner.png")


# ------------------------------------------------------------------ wall
def make_wall_body():
    cv = Cv(32, 32)
    for y in range(32):
        for x in range(32):
            cv.px(x, y, brick_color(x, y + 24, 32, seed=1))
    cv.save("wall-body.png")


def make_wall_top():
    cv = Cv(12, 8)
    for y in range(8):
        for x in range(12):
            if y < 6:
                if x < 8:
                    c = brick_color(x, y, 12, bw=8, seed=5)
                    if y == 0:
                        c = STONE[0]
                    cv.px(x, y, c)
                elif y >= 3:
                    cv.px(x, y, BACKWALL)
            elif y == 6:
                cv.px(x, y, STONE[0])
            else:
                cv.px(x, y, STONE[3])
    cv.save("wall-top.png")


def make_panel_frame():
    cv = Cv(16, 16)
    DARK = H("#3b2412")
    WOOD, HI, LO = H("#8a5a2b"), H("#b47d3c"), H("#6a4420")
    IRON, IRON_HI, RIVET = H("#5b6570"), H("#9aa6b2"), H("#e3e9ee")
    for y in range(16):
        for x in range(16):
            d = min(x, y, 15 - x, 15 - y)
            if d >= 4:
                continue
            corner = (x < 4 or x > 11) and (y < 4 or y > 11)
            if corner:
                cx, cy = (x if x < 4 else x - 12), (y if y < 4 else y - 12)
                if min(cx, cy, 3 - cx, 3 - cy) == 0 and (cx in (0, 3) or cy in (0, 3)):
                    # outline only on the outward-facing sides
                    outward = (x == 0 or y == 0 or x == 15 or y == 15)
                    c = DARK if outward else IRON
                else:
                    c = IRON
                if (cx, cy) == (1, 1) or (x > 11 and y < 4 and (cx, cy) == (2, 1)) or (y > 11 and x < 4 and (cx, cy) == (1, 2)) or (x > 11 and y > 11 and (cx, cy) == (2, 2)):
                    c = RIVET
                elif c == IRON and (cx + cy) <= 2 and d > 0:
                    c = IRON_HI if (cx == 1 or cy == 1) and d == 1 else IRON
                cv.px(x, y, c)
                continue
            along = x if (y < 4 or y > 11) else y
            if d == 0:
                c = DARK
            elif d == 1:
                c = HI if (y == 1 or x == 1) else LO
            elif d == 2:
                c = LO if along % 4 == 1 else WOOD
            else:
                c = DARK
            cv.px(x, y, c)
    cv.save("panel-frame.png")


def make_parchment():
    cv = Cv(16, 16)
    rng = random.Random(9)
    cv.rect(0, 0, 16, 16, H("#f5e6c0"))
    for _ in range(16):
        cv.px(rng.randint(0, 15), rng.randint(0, 15), H("#ecd9a8"))
    for _ in range(7):
        cv.px(rng.randint(0, 15), rng.randint(0, 15), H("#fbf0d2"))
    for _ in range(3):
        x, y = rng.randint(0, 13), rng.randint(0, 15)
        cv.px(x, y, H("#e6d09b"))
        cv.px(x + 1, y, H("#e6d09b"))
    cv.save("parchment.png")


def make_gate():
    W, Hh = 40, 44
    cv = Cv(W, Hh)
    cx, arch_cy = 19.5, 19.0
    OUT_R, IN_R, IN_HALF = 19.6, 13.4, 13.0
    DARK = H("#6f6149")

    def inside_outer(x, y):
        if abs(x - cx) > 19.5:
            return False
        if y >= arch_cy:
            return True
        return math.hypot(x - cx, y - arch_cy) <= OUT_R

    def inside_door(x, y):
        if abs(x - cx) > IN_HALF:
            return False
        if y >= arch_cy:
            return True
        return math.hypot(x - cx, y - arch_cy) <= IN_R

    wood, wood_hi, wood_dk = H("#8a5a2b"), H("#a8703a"), H("#5b3a1a")
    iron, iron_hi, stud = H("#4a525b"), H("#7a8794"), H("#c9d2da")
    for y in range(Hh):
        for x in range(W):
            if not inside_outer(x, y):
                continue
            edge = any(not inside_outer(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if inside_door(x, y):
                lx = x - 7
                c = wood
                if lx % 4 == 3:
                    c = wood_dk
                elif lx % 4 == 0:
                    c = wood_hi
                if y - arch_cy < -9:  # shadow under the arch
                    c = H("#4a2f17") if lx % 4 != 3 else H("#33200f")
                if y in (16, 17, 30, 31):  # iron straps
                    c = iron_hi if y in (16, 30) else iron
                    if x % 6 == 3 and y in (16, 30):
                        c = stud
                if x in (19, 20):
                    c = H("#2b1a0b")
                if (x, y) in ((17, 26), (22, 26), (17, 27), (22, 27), (18, 27), (21, 27)):
                    c = iron_hi
                cv.px(x, y, c)
            else:
                if y >= arch_cy:
                    c = brick_color(x, y, 40, bw=7, bh=4, seed=2)
                else:
                    ang = math.atan2(y - arch_cy, x - cx)  # -pi .. 0 across the top
                    seg = int((ang + math.pi) / (math.pi / 11))
                    edge_seg = abs(((ang + math.pi) / (math.pi / 11)) - round((ang + math.pi) / (math.pi / 11))) < 0.09
                    c = MORTAR[2] if edge_seg else (STONE[1] if seg % 2 else STONE[2])
                if edge:
                    c = DARK
                cv.px(x, y, c)
    # stone threshold
    for x in range(4, 36):
        cv.px(x, 42, STONE[0])
        cv.px(x, 43, STONE[3])
    cv.save("gate.png")


def make_torch():
    cv = Cv(32, 16)
    iron, iron_hi = H("#4a525b"), H("#8b98a5")
    wood, wood_dk = H("#8a5a2b"), H("#5b3a1a")
    for f in range(2):
        ox = f * 16
        # bracket + cup
        cv.rect(ox + 7, 14, 2, 2, iron)
        cv.rect(ox + 5, 11, 6, 1, iron_hi)
        cv.rect(ox + 6, 12, 4, 2, iron)
        cv.px(ox + 6, 12, iron_hi)
        # stick
        cv.rect(ox + 7, 8, 2, 3, wood)
        cv.px(ox + 8, 9, wood_dk)
        cv.px(ox + 7, 10, wood_dk)
        # flame
        height = 9 if f == 0 else 8
        lean = -1 if f == 0 else 1
        base_y = 8
        for i in range(height):
            hw = 2.3 * math.sin(math.pi * (i + 1.0) / (height + 1.0)) ** 0.8 + 0.4
            cxf = 7.5 + lean * (i / height) * 1.6
            y = base_y - i
            for x in range(int(round(cxf - hw)), int(round(cxf + hw)) + 1):
                d = abs(x - cxf) / max(hw, 0.5)
                v = i / height
                if d < 0.4 and v < 0.55:
                    c = H("#fff6b0")
                elif d < 0.65 and v < 0.8:
                    c = H("#ffd54a")
                elif d < 0.9:
                    c = H("#ffab2e")
                else:
                    c = H("#ff7a1a")
                cv.px(ox + x, y, c)
        cv.px(ox + (5 if f == 0 else 10), 1 + f, H("#ffd54a"))
    cv.save("torch.png")


# ------------------------------------------------------------------ scenery
def make_sun():
    cv = Cv(24, 24)
    c0 = 11.5
    RAY = H("#ffd23f")
    for y in range(24):
        for x in range(24):
            d = math.hypot(x - c0, y - c0)
            if d <= 6.6:
                t = ((x - c0) + (y - c0)) / 12
                c = H("#fff6a8") if t < -0.45 else H("#ffe45c") if t < 0.35 else H("#ffcf3a")
                cv.px(x, y, c)
    for dx, dy, w, h in [(10, 1, 2, 3), (10, 20, 2, 3), (1, 10, 3, 2), (20, 10, 3, 2)]:
        cv.rect(dx, dy, w, h, RAY)
    for dx, dy in [(4, 4), (18, 4), (4, 18), (18, 18)]:
        cv.rect(dx, dy, 2, 2, RAY)
    cv.save("sun.png")


def make_clouds():
    cv = Cv(96, 40)
    W_, SH = H("#ffffff"), H("#d3e6f5")

    def cloud(cx, cy, rw):
        mask = set()
        lumps = [(0, 0, rw, rw * 0.32), (-rw * 0.45, -2, rw * 0.5, rw * 0.3), (rw * 0.3, -3, rw * 0.45, rw * 0.32)]
        for lx, ly, rx, ry in lumps:
            for y in range(int(cy + ly - ry - 1), int(cy + ly + ry + 2)):
                for x in range(int(cx + lx - rx - 1), int(cx + lx + rx + 2)):
                    if ((x - cx - lx) / max(rx, 1)) ** 2 + ((y - cy - ly) / max(ry, 1)) ** 2 <= 1:
                        mask.add((x, y))
        bottom = max(y for _, y in mask)
        for x, y in mask:
            cv.px(x, y, SH if y >= bottom - 1 else W_)

    cloud(18, 14, 14)
    cloud(58, 24, 20)
    cloud(86, 9, 8)
    cv.save("sky-clouds.png")


def make_grass():
    cv = Cv(16, 12)
    tops = [3, 2, 3, 1, 2, 3, 2, 1, 3, 2, 1, 2, 3, 2, 3, 2]
    for x in range(16):
        for y in range(12):
            if y < tops[x]:
                continue
            depth = y - tops[x]
            if y == 11:
                c = H("#6b4a2b")
            elif depth == 0:
                c = H("#9be066")
            elif depth < 3:
                c = H("#6dbb4a")
            elif depth < 6:
                c = H("#4f9a3a")
            else:
                c = H("#3d7f2f")
            cv.px(x, y, c)
    cv.save("grass.png")


# ------------------------------------------------------------------ hoard
def make_coin():
    rows = [
        ".KKKK.",
        "KYGGOK",
        "KGGOOK",
        "KODDDK",
        ".KKKK.",
    ]
    pal = {"K": H("#6b3f08"), "Y": H("#fff3a8"), "G": H("#ffd54a"), "O": H("#f2b322"), "D": H("#c98a12")}
    cv = Cv(6, 5)
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch != ".":
                cv.px(i, j, pal[ch])
    cv.save("coin.png")


def make_gems():
    cv = Cv(15, 5)
    shape = [".KKK.", "KHMMK", "KMMSK", ".KSK.", "..K.."]
    sets = [
        (H("#ffb3ad"), H("#e0453a"), H("#a02620")),
        (H("#a8d4ff"), H("#3a8fe0"), H("#1f5aa0")),
        (H("#a8f5c8"), H("#3ad07a"), H("#1d8a4d")),
    ]
    for g, (hi, mid, sh) in enumerate(sets):
        pal = {"K": H("#2a1a12"), "H": hi, "M": mid, "S": sh}
        for j, row in enumerate(shape):
            for i, ch in enumerate(row):
                if ch != ".":
                    cv.px(g * 5 + i, j, pal[ch])
    cv.save("gems.png")


def make_sparkle():
    rows = [
        "...W...",
        "...W...",
        "..WYW..",
        "WWYYYWW",
        "..WYW..",
        "...W...",
        "...W...",
    ]
    pal = {"W": H("#fffbe0"), "Y": H("#ffe27a")}
    cv = Cv(7, 7)
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch != ".":
                cv.px(i, j, pal[ch])
    cv.save("sparkle.png")


if __name__ == "__main__":
    make_tower_body()
    make_tower_cap()
    make_tower_ivy()
    make_tower_window()
    make_banner()
    make_wall_body()
    make_wall_top()
    make_panel_frame()
    make_parchment()
    make_gate()
    make_torch()
    make_sun()
    make_clouds()
    make_grass()
    make_coin()
    make_gems()
    make_sparkle()
    print("wrote", len(os.listdir(OUT)), "sprites to", OUT)
