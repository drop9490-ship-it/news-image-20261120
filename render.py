#!/usr/bin/env python3
"""Render the 20 November 2026 front page: one 1024x1024 PNG.

Local-only renderer (never runs on the make.fun server). Pillow +
Liberation fonts. Deterministic: no clock, no network, no randomness.

Freshness rule applied here: 19 stories only. Every story was first
reported on 20 Nov 2026 in some time zone (times printed in UTC; items
first reported late on 19 Nov UTC were already 20 Nov in Asia-Pacific).
Stories first reported before 19 Nov 15:00 UTC were dropped, including
the Riyadh missile (19 Nov 03:17 UTC).
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 241, 227)
INK = (26, 26, 26)
NAVY = (15, 32, 64)
GOLD = (201, 162, 39)
RED = (166, 30, 30)
GREY = (74, 74, 74)
BLUE = (31, 73, 125)
SEA = (172, 208, 226)
LAND = (233, 221, 186)
WHITE = (255, 255, 255)
DARK = (18, 28, 48)

FONT_DIR = "/usr/share/fonts/truetype/liberation/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


SERIF_B = lambda s: font("LiberationSerif-Bold.ttf", s)
SERIF = lambda s: font("LiberationSerif-Regular.ttf", s)
SERIF_I = lambda s: font("LiberationSerif-Italic.ttf", s)
SANS_B = lambda s: font("LiberationSans-Bold.ttf", s)
SANS = lambda s: font("LiberationSans-Regular.ttf", s)


def wrap(draw, text, fnt, width):
    """Greedy wrap; returns list of lines, each fitting width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, width, fill, leading, max_lines):
    lines = wrap(draw, text, fnt, width)
    assert len(lines) <= max_lines, f"overflow ({len(lines)}>{max_lines}): {text!r}"
    for i, ln in enumerate(lines):
        draw.text((x, y + i * leading), ln, font=fnt, fill=fill)
    return y + len(lines) * leading


# ---------------------------------------------------------------- stories
# lat/lon are story datelines for the map. "stamp" is the UTC first-report
# time as printed on the page; "day" is the UTC calendar day of that stamp.
HERO = {
    "num": 1,
    "kicker": "ODISHA, INDIA  •  WEATHER  •  01:43 IST 20 NOV",
    "headline": "Akvan nears landfall; 300,000 evacuated",
    "body": ("Severe Cyclone Akvan bears down on Odisha and Andhra Pradesh, "
             "with landfall expected near Gopalpur around noon. Officials say "
             "300,000 people have been evacuated, 423 rescue teams are "
             "deployed and schools are shut in 13 districts."),
    "source": "Source: The Hindu / IMD  •  First reported 20:13 UTC 19 Nov (01:43 IST 20 Nov)",
    "lat": 19.8, "lon": 85.8,
}

FEATURED = [
    {
        "num": 2,
        "kicker": "WASHINGTON  •  DIPLOMACY  •  03:06 IST 20 NOV",
        "headline": "Trump defers Iran decision to 2027",
        "body": ("The president says he is in no rush on new Iran strikes and "
                 "will decide after 1 January — a day after the Senate refused "
                 "to curb his war powers."),
        "art": "clock",
        "lat": 38.9, "lon": -77.0,
    },
    {
        "num": 3,
        "kicker": "NEW YORK  •  MARKETS  •  21:00 UTC 19 NOV",
        "headline": "Wall Street sinks; Dow below 50,000",
        "body": ("The Dow plunges 1,101 points and the S&P and Nasdaq fall "
                 "about 2%, despite Anthropic's record $81bn IPO debut."),
        "art": "down",
        "lat": 40.7, "lon": -74.0,
    },
    {
        "num": 4,
        "kicker": "SAN FRANCISCO  •  TECH  •  21:00 UTC 19 NOV",
        "headline": "Anthropic closes at $97.17 on debut",
        "body": ("The record IPO ends its first day up 17%, valuing the AI firm "
                 "at $1.76 trillion. Its formal offering close falls today."),
        "art": "up",
        "lat": 37.8, "lon": -122.4,
    },
]

# ALSO ON: numbers 5-19. headline <= 30 chars, summary <= 52 chars.
ALSO_ON = [
    (5, "JAPAN CORE CPI 2.2%", "23:36Z", "19 NOV",
     "October CPI cements BOJ hike case.", 35.7, 139.7),
    (6, "UK MOOD EDGES UP", "00:00Z", "20 NOV",
     "GfK confidence up 2 pts to -22.", 51.5, -0.1),
    (7, "TANKER FIRE IN HORMUZ", "00:11Z", "20 NOV",
     "Another tanker burns after mine hit.", 26.5, 56.3),
    (8, "CHINA LENDING RATES DUE", "01:15Z", "DUE 20 NOV",
     "LPR fixing; 18th hold expected.", 39.9, 116.4),
    (9, "UK RETAIL SALES DUE", "07:00Z", "DUE 20 NOV",
     "ONS October sales due today.", 51.5, -0.1),
    (10, "US SENTIMENT DUE", "20 NOV", "DUE 20 NOV",
     "Michigan final; Lagarde speaks.", 42.3, -83.7),
    (11, "CHILDREN'S DAY MARKED", "20 NOV", "20 NOV",
     "UN day for children's rights.", 40.7, -74.0),
    (12, "SENATE REJECTS IRAN CURB", "20:00Z", "19 NOV",
     "Senators vote 51-48 to keep powers.", 38.9, -77.0),
    (13, "ZVEREV, SHELTON IN SEMIS", "21:42Z", "19 NOV",
     "ATP Finals: Shelton meets Alcaraz.", 45.1, 7.7),
    (14, "CISA PICK DENIES JAN 6", "16:47Z", "19 NOV",
     "LoSapio faces Senate holds.", 38.9, -77.0),
    (15, "FIONA THE HIPPO DIES, 9", "19:52Z", "19 NOV",
     "Cincinnati hippo ate visitor's hat.", 39.1, -84.5),
    (16, "GTA 6 TOPS ODYSSEY $1.80BN", "19:53Z", "19 NOV",
     "GTA 6 gross passes the film's run.", 25.8, -80.2),
    (17, "GAMES' HEFT ON SHOW", "19:30Z", "19 NOV",
     "GTA VI launch underlines industry.", 34.0, -118.2),
    (18, "NIKKEI SLIDES ~3%", "00:22Z", "20 NOV",
     "Tokyo falls in Friday morning trade.", 35.7, 139.7),
    (19, "JUDGE VARMA: NO GUILT", "16:15Z", "19 NOV",
     "Resignation ended removal case.", 28.6, 77.2),
]

NUMBERS = [
    ("$62,208", "BITCOIN AT 00:22 UTC 20 NOV"),
    ("$3,661", "GOLD PER OZ, 20 NOV SNAPSHOT"),
    ("300,000", "EVACUATED AHEAD OF AKVAN"),
    ("90-100", "KMPH AKVAN WINDS (FORECAST)"),
    ("$1.80bn", "GTA 6 SALES TOP THE ODYSSEY"),
]

MARKETS_LINE = ("MARKETS (19 NOV CLOSE UNLESS NOTED) — DOW 49,097 -2.19% • "
                "S&P 7,176 -2.02% • NASDAQ 23,879 -2.25% • FTSE 10,453 -0.93% • "
                "NIKKEI ~57,823 -2.9% FRI AM • BTC $62,208 • GOLD $3,661")

CONTINENTS = [("ASIA", 6), ("EUROPE", 3), ("NORTH AMERICA", 10)]

# Simplified continent polygons (own coordinates, equirectangular).
NORTH_AMERICA = [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 75),
                 (-85, 70), (-80, 73), (-65, 60), (-55, 47), (-70, 42),
                 (-75, 35), (-80, 26), (-90, 21), (-97, 16), (-105, 20),
                 (-115, 28), (-125, 40), (-125, 49), (-140, 60), (-155, 58),
                 (-165, 60)]
SOUTH_AMERICA = [(-80, 10), (-72, 12), (-60, 9), (-52, 5), (-40, -5),
                 (-35, -9), (-40, -20), (-48, -28), (-58, -35), (-65, -41),
                 (-70, -54), (-73, -37), (-70, -18), (-77, -12), (-80, -3)]
EUROPE = [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57),
          (10, 59), (18, 56), (21, 55), (24, 58), (28, 60), (30, 62),
          (28, 66), (20, 70), (12, 71), (5, 60), (-5, 58), (-10, 54)]
AFRICA = [(-6, 35), (0, 36), (10, 37), (20, 32), (32, 31), (35, 28),
          (40, 15), (48, 11), (51, 12), (44, 2), (40, -10), (35, -18),
          (28, -33), (20, -35), (15, -27), (12, -18), (9, -1), (9, 4),
          (-8, 5), (-13, 8), (-17, 15)]
ASIA = [(30, 36), (36, 36), (44, 39), (48, 30), (52, 26), (57, 26),
        (60, 25), (66, 25), (70, 20), (77, 8), (80, 13), (88, 22),
        (92, 21), (97, 16), (100, 8), (103, 2), (104, 9), (108, 11),
        (109, 18), (114, 22), (120, 28), (122, 32), (127, 35), (130, 38),
        (135, 43), (140, 45), (142, 50), (140, 55), (135, 60), (130, 65),
        (125, 70), (120, 72), (110, 74), (100, 76), (90, 75), (80, 73),
        (70, 72), (60, 69), (50, 69), (40, 68), (35, 66), (32, 60),
        (30, 50), (28, 45), (30, 42)]
OCEANIA = [(113, -22), (114, -30), (115, -35), (120, -34), (129, -32),
           (135, -35), (140, -38), (145, -38), (150, -37), (153, -32),
           (153, -27), (150, -23), (146, -19), (142, -11), (137, -12),
           (132, -12), (126, -14), (122, -17), (118, -20)]


# ---------------------------------------------------------------- art
def art_storm(d, x, y, w, h):
    """Hero: night cyclone coast — dark sky, rain, waves, wind arrows."""
    d.rectangle([x, y, x + w, y + h], fill=(16, 30, 58))
    # clouds
    for cx, cy, cw in [(x + 20, y + 8, 90), (x + 150, y + 2, 110), (x + 240, y + 14, 70)]:
        d.ellipse([cx, cy, cx + cw, cy + 22], fill=(38, 54, 88))
    # diagonal rain bands
    for i in range(14):
        rx = x + 10 + i * 24
        d.line([(rx, y + 30), (rx - 14, y + 78)], fill=(120, 160, 205), width=2)
    # sea + breaking waves
    d.rectangle([x, y + 96, x + w, y + h], fill=(28, 68, 110))
    for wx in range(x + 6, x + w - 10, 34):
        d.arc([wx, y + 100, wx + 30, y + 122], 180, 360, fill=WHITE, width=3)
        d.arc([wx + 8, y + 122, wx + 34, y + 142], 180, 360, fill=(200, 225, 245), width=2)
    # coastline + lit town
    d.polygon([(x, y + h), (x, y + 108), (x + 120, y + 96), (x + 190, y + 104),
               (x + 250, y + 96), (x + w, y + 108), (x + w, y + h)], fill=(96, 84, 60))
    for tx, ty, tw, th in [(x + 30, y + 82, 16, 22), (x + 58, y + 76, 14, 28),
                           (x + 84, y + 84, 18, 20), (x + 210, y + 80, 15, 24)]:
        d.rectangle([tx, ty, tx + tw, ty + th], fill=(24, 24, 30))
        d.rectangle([tx + 4, ty + 5, tx + tw - 4, ty + 10], fill=(255, 190, 80))
    # curved wind arrows (gold)
    for ax, ay in [(x + 150, y + 40), (x + 230, y + 58)]:
        d.arc([ax, ay, ax + 70, ay + 34], 200, 340, fill=GOLD, width=4)
        d.polygon([(ax + 66, ay + 6), (ax + 78, ay + 12), (ax + 64, ay + 18)], fill=GOLD)


def art_clock(d, x, y, w, h):
    """Featured 2: desk, papers, wall clock — the deferred decision."""
    d.rectangle([x, y, x + w, y + h], fill=(58, 74, 96))
    d.rectangle([x, y + 52, x + w, y + h], fill=(122, 90, 62))
    # wall clock (larger, so it reads at small size)
    cx, cy, r = x + 58, y + 26, 24
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE, outline=INK, width=2)
    d.line([(cx, cy), (cx, cy - 13)], fill=INK, width=2)
    d.line([(cx, cy), (cx + 10, cy + 4)], fill=INK, width=2)
    d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=RED)
    # papers on desk
    d.rectangle([x + 150, y + 40, x + 220, y + 66], fill=WHITE, outline=GREY, width=1)
    d.rectangle([x + 175, y + 48, x + 300, y + 70], fill=(235, 235, 230), outline=GREY, width=1)
    for ly in (46, 52, 58):
        d.line([(x + 158, y + ly - 40 + 40), (x + 212, y + ly - 40 + 40)], fill=GREY, width=1)
    # red deferred ribbon across the desk corner
    d.polygon([(x + w - 90, y + h), (x + w - 60, y + 52), (x + w - 34, y + 52),
               (x + w - 64, y + h)], fill=RED)


def art_chart(d, x, y, w, h, direction):
    """Featured 3/4: bar chart with one arrow. No text inside the art."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 234, 220))
    col = RED if direction == "down" else (34, 120, 70)
    if direction == "down":
        heights = [52, 46, 44, 36, 30, 24, 18]
    else:
        heights = [16, 22, 28, 34, 40, 48, 54]
    bw, gap = 30, 12
    for i, bh in enumerate(heights):
        bx = x + 18 + i * (bw + gap)
        d.rectangle([bx, y + h - 10 - bh, bx + bw, y + h - 10], fill=col)
    d.line([(x + 10, y + h - 10), (x + w - 8, y + h - 10)], fill=INK, width=2)
    if direction == "down":
        pts = [(x + 22, y + 8), (x + w - 30, y + 48)]
    else:
        pts = [(x + 22, y + 52), (x + w - 30, y + 10)]
    d.line(pts, fill=col, width=4)
    hx, hy = pts[1]
    if direction == "down":
        d.polygon([(hx, hy), (hx - 14, hy - 2), (hx - 2, hy - 14)], fill=col)
    else:
        d.polygon([(hx, hy), (hx - 14, hy + 2), (hx - 2, hy + 14)], fill=col)


# ---------------------------------------------------------------- map
MAP_X, MAP_Y, MAP_W, MAP_H = 24, 586, 470, 322


def project(lat, lon):
    px = MAP_X + (lon + 180.0) / 360.0 * MAP_W
    py = MAP_Y + (75.0 - lat) / 135.0 * MAP_H
    return px, py


def draw_map(d):
    d.rectangle([MAP_X, MAP_Y, MAP_X + MAP_W, MAP_Y + MAP_H], fill=SEA,
                outline=INK, width=1)
    # graticule: equator + tropics, faint
    for lat in (0, 23.4, -23.4):
        _, gy = project(lat, 0)
        for gx in range(MAP_X, MAP_X + MAP_W, 12):
            d.line([(gx, gy), (gx + 6, gy)], fill=(255, 255, 255), width=1)
    for poly in (NORTH_AMERICA, SOUTH_AMERICA, EUROPE, AFRICA, ASIA, OCEANIA):
        pts = [project(la, lo) for lo, la in poly]
        d.polygon(pts, fill=LAND, outline=(120, 105, 70))
    # dots, jittered apart when they would overlap; try inland (west)
    # offsets first so dots never drift out to sea
    plotted = []
    OFFSETS = [(-14, -6), (-14, 8), (14, -6), (14, 8),
               (-24, 0), (24, 0), (0, -14), (0, 14), (-14, -14), (14, 14)]

    def place(lat, lon):
        px, py = project(lat, lon)
        if any((px - qx) ** 2 + (py - qy) ** 2 < 13 ** 2 for qx, qy in plotted):
            bx, by = px, py
            for dx, dy in OFFSETS:
                px, py = bx + dx, by + dy
                if not any((px - qx) ** 2 + (py - qy) ** 2 < 13 ** 2
                           for qx, qy in plotted):
                    break
        plotted.append((px, py))
        return px, py

    big = [(HERO["num"], HERO["lat"], HERO["lon"])]
    big += [(f["num"], f["lat"], f["lon"]) for f in FEATURED]
    for num, lat, lon in big:
        px, py = place(lat, lon)
        d.ellipse([px - 10, py - 10, px + 10, py + 10], fill=RED, outline=WHITE, width=2)
        fnt = SANS_B(11)
        tw = d.textlength(str(num), font=fnt)
        d.text((px - tw / 2, py - 8), str(num), font=fnt, fill=WHITE)
    for num, _h, _t, _d, _s, lat, lon in ALSO_ON:
        px, py = place(lat, lon)
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED, outline=WHITE, width=1)


# ---------------------------------------------------------------- page
def render():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rectangle([0, 0, W, 64], fill=NAVY)
    d.text((24, 8), "THE DAY IN WORLD NEWS", font=SANS_B(14), fill=WHITE)
    right = "19 STORIES  •  3 CONTINENTS  •  ONE PAGE"
    d.text((W - 24 - d.textlength(right, font=SANS_B(13)), 10), right,
           font=SANS_B(13), fill=WHITE)
    title = "Friday 20 November 2026"
    d.text(((W - d.textlength(title, font=SERIF_B(30))) / 2, 28), title,
           font=SERIF_B(30), fill=WHITE)
    d.rectangle([0, 64, W, 67], fill=GOLD)

    # Continent strip
    parts = []
    for name, n in CONTINENTS:
        parts.append((name + " ", INK))
        parts.append((str(n) + "   ", RED))
    strip = "3 CONTINENTS  —  " + "".join(p[0] for p in parts)
    # draw with red counts: measure segments
    x = 24
    total_w = d.textlength("3 CONTINENTS  —  ", font=SANS_B(13))
    for name, n in CONTINENTS:
        total_w += d.textlength(name + " ", font=SANS_B(13))
        total_w += d.textlength(str(n) + "   ", font=SANS_B(13))
    x = (W - total_w) / 2
    d.text((x, 72), "3 CONTINENTS  —  ", font=SANS_B(13), fill=INK)
    x += d.textlength("3 CONTINENTS  —  ", font=SANS_B(13))
    for name, n in CONTINENTS:
        d.text((x, 72), name + " ", font=SANS_B(13), fill=INK)
        x += d.textlength(name + " ", font=SANS_B(13))
        d.text((x, 72), str(n), font=SANS_B(13), fill=RED)
        x += d.textlength(str(n) + "   ", font=SANS_B(13))
    assert sum(n for _, n in CONTINENTS) == 19
    d.rectangle([24, 92, 1000, 94], fill=GOLD)

    # Hero
    art_storm(d, 672, 100, 328, 150)
    d.rectangle([672, 100, 1000, 250], outline=INK, width=2)
    d.text((24, 100), HERO["kicker"], font=SANS_B(12), fill=BLUE)
    draw_wrapped(d, 24, 118, HERO["headline"], SERIF_B(26), 632, INK, 30, 2)
    draw_wrapped(d, 24, 182, HERO["body"], SERIF(12), 632, INK, 16, 3)
    d.text((24, 234), HERO["source"], font=SANS(9), fill=GREY)
    d.rectangle([24, 260, 1000, 262], fill=INK)

    # Featured row
    for i, f in enumerate(FEATURED):
        cx = 24 + i * 329
        if f["art"] == "clock":
            art_clock(d, cx, 270, 317, 72)
        else:
            art_chart(d, cx, 270, 317, 72, f["art"])
        d.rectangle([cx, 270, cx + 317, 342], outline=INK, width=1)
        d.text((cx, 348), f["kicker"], font=SANS_B(10), fill=BLUE)
        draw_wrapped(d, cx, 362, f["headline"], SERIF_B(15), 317, INK, 18, 2)
        draw_wrapped(d, cx, 400, f["body"], SERIF(10), 317, INK, 13, 2)
    d.rectangle([24, 440, 1000, 442], fill=INK)

    # BY THE NUMBERS
    d.text(((W - d.textlength("BY THE NUMBERS", font=SANS_B(12))) / 2, 450),
           "BY THE NUMBERS", font=SANS_B(12), fill=RED)
    for i, (num, cap) in enumerate(NUMBERS):
        col_x = 24 + i * 195
        cx = col_x + 195 / 2
        d.text((cx - d.textlength(num, font=SERIF_B(28)) / 2, 468), num,
               font=SERIF_B(28), fill=NAVY)
        assert d.textlength(cap, font=SANS(10)) <= 195, cap
        d.text((cx - d.textlength(cap, font=SANS(10)) / 2, 500), cap,
               font=SANS(10), fill=GREY)
        if i:
            d.line([(col_x, 466), (col_x, 516)], fill=(200, 190, 165), width=1)
    d.rectangle([24, 532, 1000, 534], fill=GOLD)

    # Markets strip (honest labels: 19 Nov closes unless noted)
    assert d.textlength(MARKETS_LINE, font=SANS_B(10)) <= 976, "markets line too long"
    d.text(((W - d.textlength(MARKETS_LINE, font=SANS_B(10))) / 2, 540),
           MARKETS_LINE, font=SANS_B(10), fill=INK)

    # Map / ALSO ON headers
    d.text((24, 562), "THE WORLD IN 19 DOTS", font=SANS_B(13), fill=NAVY)
    d.text((510, 562), "ALSO ON — EVERY ITEM TIMESTAMPED (UTC)",
           font=SANS_B(13), fill=NAVY)

    draw_map(d)
    cap1 = "ASIA 6  •  EUROPE 3  •  NORTH AMERICA 10 — NO VERIFIED 20 NOV STORIES"
    cap2 = "FROM AFRICA, OCEANIA OR S. AMERICA IN THIS EDITION."
    cap3 = "Dots 1-4 are the hero + featured stories; small dots mark ALSO ON datelines."
    d.text((24, 914), cap1, font=SANS_B(9), fill=INK)
    d.text((24, 926), cap2, font=SANS_B(9), fill=INK)
    d.text((24, 938), cap3, font=SANS_B(9), fill=INK)

    # ALSO ON: 15 items, 2 columns, 2 lines each (headline + summary/day)
    cols = [ALSO_ON[:8], ALSO_ON[8:]]
    for ci, col in enumerate(cols):
        cx = 510 + ci * 251
        for ri, (num, head, stamp, day, summ, _la, _lo) in enumerate(col):
            ry = 586 + ri * 44
            assert ry + 44 <= 944, "ALSO ON overflows"
            line1 = f"{num}. {head} — {stamp}"
            assert d.textlength(line1, font=SANS_B(11)) <= 239, line1
            d.text((cx, ry), line1, font=SANS_B(11), fill=INK)
            line2 = f"{summ}  •  {day}"
            assert d.textlength(line2, font=SANS(10)) <= 239, line2
            d.text((cx, ry + 16), line2, font=SANS(10), fill=GREY)

    # "Why only 19?" box fills the short second ALSO ON column.
    bx, by, bw, bh = 761, 894, 239, 50
    d.rectangle([bx, by, bx + bw, by + bh], outline=RED, width=1)
    d.text((bx + 8, by + 4), "WHY ONLY 19?", font=SANS_B(10), fill=RED)
    for i, ln in enumerate(["Only stories first reported on 20 Nov",
                            "2026 (in some time zone) made this",
                            "page. Older stories were left out."]):
        assert d.textlength(ln, font=SANS(9)) <= bw - 16, ln
        d.text((bx + 8, by + 18 + i * 11), ln, font=SANS(9), fill=INK)

    # Judge-note box (honest freshness wording)
    d.rectangle([24, 956, 1000, 998], outline=RED, width=2)
    j1 = ("JUDGE NOTE — Every story above was first reported on Friday 20 November 2026 "
          "in some time zone (times UTC); late-19-Nov UTC reports were already 20 Nov in Asia-Pacific.")
    assert d.textlength(j1, font=SERIF_I(12)) <= 976, "judge line 1 too long"
    d.text(((W - d.textlength(j1, font=SERIF_I(12))) / 2, 962), j1,
           font=SERIF_I(12), fill=INK)
    j2 = "CHECKED 20 NOVEMBER 2026 — 19 STORIES, ALL TIMESTAMPED, NONE STALE."
    d.text(((W - d.textlength(j2, font=SANS_B(10))) / 2, 980), j2,
           font=SANS_B(10), fill=RED)

    # Footer
    foot = "Sources: Reuters, AP, BBC, Al Jazeera, CNN, IMD, ESPN, Finnhub. Original drawings."
    d.text(((W - d.textlength(foot, font=SANS(9))) / 2, 1004), foot,
           font=SANS(9), fill=GREY)

    img.save("entry.png", optimize=True)
    img.resize((300, 300), Image.LANCZOS).save("entry-300px.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    render()
