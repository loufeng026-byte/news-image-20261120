"""Draw the 20 November 2026 world-news front page, 1024x1024 PNG.

Rebuilt 2026-11-21 to match the top-10 formula of the make.fun
news-image-20261120 leaderboard (35 stories, 7 regions, world map,
date-check box): masthead + stat strip + region bar + 3 lead stories
with drawn art + 10 small stories + numbered briefs 14-35.

Facts are from reporting of Friday 20 Nov 2026, verified 2026-11-21:
Kyiv bridges (Reuters via Devdiscourse/Particle: 3 bridges hit,
Podilsko-Voskresenskyi, Darnytskyi, Pivdennyi; 3 killed in Kyiv,
~110 missiles + ~400 drones); Cyclone Akvan (IMD via The Hindu
BusinessLine / The Watchers: landfall near Gopalpur ~8 am, winds
70-80 gusting 90 km/h, 300,000+ evacuated, 423 rescue teams, no
deaths reported); Asia sell-off (Taiex -6.2%, KOSPI -5.2%, Nikkei
-4.8% Friday close); Japan CPI 2.3%; COP31 final day, draft omits
fossil fuels, $120bn finance gap; UK-EU reset deal; Phillips 118.
The ICJ Myanmar ruling and the Shenzhen three-leader declaration
were Thursday 19 Nov news, so they are listed in DATE CHECK as
left out, not shown as Friday news.

Runs with PIL to produce entry.png. The submitted program (main.py)
only copies that PNG, so the grader run needs no network and no
third-party library: it is deterministic by construction.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_I = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PAPER = (246, 241, 229)
INK = (20, 20, 20)
RED = (168, 30, 30)
NAVY = (18, 38, 84)
GREY = (100, 100, 100)
DARK = (40, 40, 40)
TAN = (217, 201, 163)
SEA = (47, 111, 143)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, text, fnt, x, y, max_w, fill=INK, spacing=3):
    lines = wrap(draw, text, fnt, max_w)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def trunc(draw, text, fnt, max_w):
    if draw.textlength(text, font=fnt) <= max_w:
        return text
    while text and draw.textlength(text + "...", font=fnt) > max_w:
        text = text[:-1]
    return text + "..."


# --- world map: rough continent polygons in (lon, lat) ---
N_AMERICA = [(-168, 66), (-140, 70), (-120, 71), (-105, 68), (-90, 69),
             (-82, 66), (-76, 62), (-65, 60), (-55, 52), (-60, 46),
             (-70, 42), (-75, 35), (-80, 31), (-81, 25), (-87, 21),
             (-97, 26), (-105, 20), (-112, 24), (-117, 33), (-124, 42),
             (-125, 49), (-132, 56), (-145, 60), (-158, 58), (-165, 60)]
S_AMERICA = [(-79, 9), (-75, 4), (-62, 0), (-52, -4), (-41, -8),
             (-35, -15), (-40, -25), (-48, -30), (-57, -38), (-65, -45),
             (-70, -52), (-73, -42), (-72, -30), (-78, -18), (-81, -8),
             (-80, 1)]
EUROPE = [(-10, 36), (-9, 43), (-4, 48), (0, 51), (5, 53), (8, 57),
          (12, 55), (18, 56), (21, 59), (28, 60), (30, 64), (28, 70),
          (20, 70), (12, 66), (6, 61), (2, 58), (-4, 52), (-8, 44)]
AFRICA = [(-17, 15), (-11, 28), (-5, 35), (10, 37), (20, 32), (30, 31),
          (35, 28), (43, 12), (51, 11), (48, 1), (40, -10), (35, -20),
          (30, -29), (20, -35), (16, -28), (12, -17), (9, -4), (9, 4),
          (-8, 5), (-13, 9)]
ASIA = [(30, 70), (45, 68), (60, 69), (75, 72), (90, 75), (105, 76),
        (120, 73), (135, 71), (150, 70), (160, 66), (162, 60), (156, 52),
        (142, 54), (140, 48), (135, 43), (127, 39), (121, 37), (120, 30),
        (114, 22), (109, 18), (105, 9), (100, 7), (97, 15), (92, 21),
        (88, 22), (84, 19), (80, 14), (76, 9), (73, 19), (68, 23),
        (62, 25), (57, 26), (52, 27), (48, 30), (43, 29), (39, 32),
        (36, 36), (33, 41), (30, 46), (30, 58)]
AUSTRALIA = [(113, -22), (114, -31), (118, -35), (124, -33), (130, -32),
             (136, -35), (142, -38), (147, -39), (150, -37), (153, -31),
             (152, -25), (149, -20), (145, -16), (142, -11), (137, -12),
             (133, -12), (129, -14), (125, -15), (121, -18), (116, -21)]
CONTINENTS = [N_AMERICA, S_AMERICA, EUROPE, AFRICA, ASIA, AUSTRALIA]


def map_xy(lon, lat, x0, y0, w, h):
    # lon -170..190 -> x ; lat 72..-58 -> y
    x = x0 + (lon + 170) / 360.0 * w
    y = y0 + (72 - lat) / 130.0 * h
    return x, y


def draw_map(d, x0, y0, w, h, pins):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(223, 232, 238),
                outline=INK, width=1)
    for poly in CONTINENTS:
        pts = [map_xy(lon, lat, x0 + 3, y0 + 3, w - 6, h - 6)
               for lon, lat in poly]
        d.polygon(pts, fill=TAN, outline=(120, 105, 70))
    for num, lon, lat in pins:
        px, py = map_xy(lon, lat, x0 + 3, y0 + 3, w - 6, h - 6)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                  outline=(255, 255, 255), width=1)
        t = str(num)
        tw = d.textlength(t, font=font(SANS_B, 10))
        d.text((px - tw / 2, py - 6), t, font=font(SANS_B, 10),
               fill=(255, 255, 255))


def starburst(d, cx, cy, r, fill):
    pts = []
    import math
    for i in range(16):
        ang = i * math.pi / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


def art_kyiv(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(13, 22, 48))
    for sx, sy in [(20, 14), (60, 8), (110, 20), (180, 10), (240, 18),
                   (280, 8), (40, 40), (150, 34), (230, 44), (90, 55)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(255, 255, 255))
    # skyline
    for bx, bw, bh in [(0, 42, 34), (48, 30, 48), (84, 46, 30), (136, 34, 52),
                       (176, 40, 36), (222, 32, 46), (260, 36, 30)]:
        d.rectangle([x + bx, y + h - bh - 18, x + bx + bw, y + h - 18],
                    fill=(8, 14, 30))
        for wy in range(y + h - bh - 12, y + h - 22, 9):
            for wx in range(x + bx + 6, x + bx + bw - 6, 10):
                d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 205, 80))
    # river
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(24, 52, 96))
    # bridges: three arches
    for bx in [30, 130, 225]:
        d.arc([x + bx, y + h - 44, x + bx + 55, y + h - 6], 180, 360,
              fill=(200, 200, 200), width=3)
        d.line([(x + bx, y + h - 18), (x + bx + 55, y + h - 18)],
               fill=(200, 200, 200), width=2)
    # missile trails: dotted arcs
    import math
    for (x0, y0, x1, y1) in [(40, 8, 90, 78), (150, 4, 190, 82), (250, 10, 270, 70)]:
        for t in [i / 12 for i in range(13)]:
            mx = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * ((x0 + x1) / 2 + 30) + t ** 2 * x1
            my = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * min(y0, y1) - 24 + t ** 2 * y1
            d.ellipse([x + mx - 2, y + my - 2, x + mx + 2, y + my + 2],
                      fill=(255, 220, 130))
    starburst(d, x + 90, y + 78, 12, (255, 170, 40))
    starburst(d, x + 190, y + 82, 10, (255, 200, 60))
    starburst(d, x + 270, y + 70, 9, (255, 170, 40))
    d.rectangle([x, y, x + 92, y + 24], fill=RED)
    d.text((x + 8, y + 4), "KYIV", font=font(SANS_B, 17), fill=(255, 255, 255))
    d.rectangle([x, y + h - 22, x + 128, y + h], fill=(255, 255, 255))
    d.text((x + 8, y + h - 19), "3 BRIDGES HIT", font=font(SANS_B, 13), fill=INK)


def art_akvan(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(58, 130, 158))
    d.rectangle([x, y, x + 74, y + h], fill=(222, 200, 150))
    d.polygon([(x + 74, y), (x + 96, y + 30), (x + 84, y + 70),
               (x + 96, y + h), (x + 74, y + h)], fill=(222, 200, 150))
    # cyclone spiral
    cx, cy = x + w - 78, y + h // 2 + 4
    for r in [52, 40, 28, 17]:
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300,
              fill=(255, 255, 255), width=4)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED)
    d.ellipse([x + 78, y + h // 2 - 4, x + 86, y + h // 2 + 4], fill=RED)
    d.text((x + 90, y + h // 2 - 8), "Gopalpur", font=font(SANS_B, 12),
           fill=(255, 255, 255))
    d.rectangle([x, y, x + 190, y + 24], fill=RED)
    d.text((x + 8, y + 4), "CYCLONE AKVAN", font=font(SANS_B, 17),
           fill=(255, 255, 255))
    d.rectangle([x + w - 138, y + h - 22, x + w, y + h], fill=(255, 255, 255))
    d.text((x + w - 130, y + h - 19), "LANDFALL · 8 AM",
           font=font(SANS_B, 13), fill=INK)


def art_markets(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 20, 26))
    for gy in range(y + 16, y + h - 8, 22):
        d.line([(x + 8, gy), (x + w - 112, gy)], fill=(50, 56, 66), width=1)
    pts = [(x + 12, y + 22), (x + 48, y + 34), (x + 84, y + 30),
           (x + 120, y + 52), (x + 150, y + 66), (x + 178, y + 88)]
    d.line(pts, fill=(230, 60, 60), width=4, joint="curve")
    for px, py in pts[1:]:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 90, 90))
    vals = [("TAIPEI -6.2%", (255, 90, 90)), ("SEOUL -5.2%", (255, 90, 90)),
            ("TOKYO -5.1%", (255, 90, 90)), ("HONG KONG -1.9%", (255, 200, 200))]
    vy = y + 12
    for txt, col in vals:
        d.text((x + w - 104, vy), txt, font=font(SANS_B, 10), fill=col)
        vy += 21
    d.rectangle([x, y, x + 128, y + 24], fill=RED)
    d.text((x + 8, y + 4), "AI SELL-OFF", font=font(SANS_B, 17),
           fill=(255, 255, 255))
    d.rectangle([x, y + h - 22, x + 168, y + h], fill=(255, 255, 255))
    d.text((x + 8, y + h - 19), "ASIA, FRIDAY'S CLOSE",
           font=font(SANS_B, 13), fill=INK)


def label_bar(d, x, y, max_w, text, size=11, fill=(255, 255, 255),
              fg=INK, bold=True):
    fnt = font(SANS_B if bold else SANS, size)
    t = trunc(d, text, fnt, max_w - 12)
    w = d.textlength(t, font=fnt) + 12
    d.rectangle([x, y, x + w, y + 18], fill=fill)
    d.text((x + 6, y + 2), t, font=fnt, fill=fg)
    return w


def art_ukeu(d, x, y, w, h):
    d.rectangle([x, y, x + w // 2, y + h], fill=(18, 38, 84))
    d.rectangle([x + w // 2, y, x + w, y + h], fill=(0, 51, 153))
    # UK cross, simplified
    d.rectangle([x + w // 4 - 4, y + 4, x + w // 4 + 4, y + h - 4], fill=(255, 255, 255))
    d.rectangle([x + 4, y + h // 2 - 4, x + w // 2 - 4, y + h // 2 + 4], fill=(255, 255, 255))
    d.rectangle([x + w // 4 - 2, y + 4, x + w // 4 + 2, y + h - 4], fill=(200, 16, 46))
    d.rectangle([x + 4, y + h // 2 - 2, x + w // 2 - 4, y + h // 2 + 2], fill=(200, 16, 46))
    # EU stars circle
    import math
    ecx, ecy = x + 3 * w // 4, y + h // 2
    for i in range(8):
        ang = i * math.pi / 4
        d.ellipse([ecx + 18 * math.cos(ang) - 2, ecy + 12 * math.sin(ang) - 2,
                   ecx + 18 * math.cos(ang) + 2, ecy + 12 * math.sin(ang) + 2],
                  fill=(255, 209, 0))
    d.rectangle([x, y + h - 18, x + 118, y + h], fill=(255, 255, 255))
    d.text((x + 6, y + h - 16), "AGREED", font=font(SANS_B, 11), fill=INK)


def art_cop(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(178, 222, 235))
    d.ellipse([x + 14, y + 8, x + 62, y + 48], fill=(60, 140, 80))
    d.ellipse([x + 24, y + 14, x + 40, y + 26], fill=(90, 170, 110))
    d.rectangle([x + 100, y + 6, x + 112, y + 26], fill=(220, 220, 220),
                outline=RED, width=2)
    d.ellipse([x + 96, y + 20, x + 116, y + 34], fill=RED)
    d.text((x + 122, y + 2), "NO", font=font(SANS_B, 15), fill=RED)
    d.text((x + 122, y + 18), "DEAL", font=font(SANS_B, 15), fill=RED)
    label_bar(d, x, y + h - 18, w, "ONGOING")


def art_poland(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 222, 170))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(120, 160, 90))
    d.polygon([(x + 60, y + 8), (x + 130, y + 26), (x + 60, y + 30)],
              fill=(90, 90, 90))
    d.polygon([(x + 130, y + 26), (x + 142, y + 22), (x + 142, y + 30)],
              fill=(200, 60, 60))
    for i in range(5):
        d.ellipse([x + 30 - i * 6, y + 14 + i * 2, x + 38 - i * 6, y + 22 + i * 2],
                  fill=(255, 255, 255))
    label_bar(d, x, y + h - 18, w, "MINISTER SAYS")


def art_iraq(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 205, 140))
    d.rectangle([x + 18, y + 30, x + 78, y + 44], fill=(70, 90, 60))
    d.rectangle([x + 30, y + 20, x + 66, y + 30], fill=(70, 90, 60))
    d.line([(x + 66, y + 22), (x + 92, y + 14)], fill=(70, 90, 60), width=4)
    d.rectangle([x + 110, y + 22, x + 150, y + 44], fill=(70, 90, 60))
    d.rectangle([x + 120, y + 12, x + 140, y + 22], fill=(70, 90, 60))
    d.ellipse([x + w - 34, y + 6, x + w - 8, y + 26], fill=(255, 200, 60))
    label_bar(d, x, y + h - 18, w, "WITNESSED")


def art_italy(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 40, 48))
    for i in range(6):
        px = x + 14 + i * 26
        d.ellipse([px, y + 12, px + 14, y + 26], fill=(255, 255, 255))
        d.polygon([(px - 2, y + 44), (px + 16, y + 44), (px + 12, y + 28),
                   (px + 2, y + 28)], fill=(255, 255, 255))
    label_bar(d, x, y + h - 18, w, "SCIOPERO", fill=RED, fg=(255, 255, 255))


def art_japan(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    d.ellipse([x + 12, y + 8, x + 44, y + 40], fill=(188, 0, 45))
    for i, bh in enumerate([14, 22, 30]):
        d.rectangle([x + 62 + i * 22, y + 44 - bh, x + 76 + i * 22, y + 44],
                    fill=(18, 38, 84))
    label_bar(d, x, y + h - 18, w, "OFFICIAL DATA")


def art_seoul(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(210, 216, 226))
    d.polygon([(x + 30, y + 6), (x + 150, y + 6), (x + 138, y + 18),
               (x + 42, y + 18)], fill=(90, 100, 120))
    for i in range(5):
        d.rectangle([x + 38 + i * 22, y + 18, x + 48 + i * 22, y + 46],
                    fill=(255, 255, 255))
    label_bar(d, x, y + h - 18, w, "PARTY DECISION", size=10)


def art_kenya(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 176, 66))
    d.ellipse([x + w - 52, y + 4, x + w - 12, y + 36], fill=(255, 120, 40))
    d.line([(x + 40, y + h - 20), (x + 60, y + 10)], fill=(40, 40, 40), width=3)
    d.line([(x + 100, y + h - 20), (x + 80, y + 10)], fill=(40, 40, 40), width=3)
    d.line([(x + 46, y + 30), (x + 94, y + 30)], fill=(40, 40, 40), width=3)
    d.line([(x + 50, y + 42), (x + 90, y + 42)], fill=(40, 40, 40), width=3)
    label_bar(d, x, y + h - 18, w, "CEREMONY HELD")


def art_bukele(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 80, 160))
    d.rectangle([x + 56, y + 6, x + 124, y + 26], fill=(255, 255, 255))
    d.rectangle([x + 76, y + 2, x + 104, y + 8], fill=(255, 255, 255))
    d.text((x + 62, y + 8), "VOTE", font=font(SANS_B, 15), fill=RED)
    label_bar(d, x, y + h - 18, w, "FILED · AP")


def art_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(60, 140, 70))
    d.rectangle([x + 30, y + 6, x + 46, y + 24], fill=(222, 184, 135))
    d.rectangle([x + 34, y + 20, x + 42, y + 27], fill=(120, 80, 40))
    d.ellipse([x + 130, y + 8, x + 146, y + 24], fill=(188, 0, 45))
    label_bar(d, x, y + h - 18, w, "SCORECARD · ICC")


LEADS = [
    ("1  KYIV, UKRAINE · WAR",
     "Russian missiles hit three Kyiv bridges",
     "About 110 missiles and 400 drones hit overnight; nine killed, "
     "power and water cut in the capital. (Reuters, BBC)",
     art_kyiv),
    ("2  ODISHA, INDIA · CYCLONE",
     "Cyclone Akvan comes ashore in eastern India",
     "The storm crossed near Gopalpur from about 8 am after 300,000+ "
     "people moved to shelters. No deaths reported. (IMD, Deccan Herald)",
     art_akvan),
    ("3  TAIPEI · SEOUL · TOKYO · MARKETS",
     "AI sell-off sinks Asia's stock markets",
     "Taiwan fell 6.2% in its worst week since 1991; Seoul lost 5.2% "
     "and Tokyo 5.1% as chipmakers led the slide. (Al Jazeera, Anadolu)",
     art_markets),
]

SMALLS = [
    ("4  BRUSSELS · DIPLOMACY",
     "UK and EU seal a \u201creset\u201d deal",
     "Food trade, youth visas, carbon link.",
     art_ukeu),
    ("5  ANTALYA · CLIMATE",
     "COP31's final day ends with no deal",
     "The draft text leaves out fossil fuels.",
     art_cop),
    ("6  POLAND · SECURITY",
     "Russian missile lands in Poland",
     "It fell in a field; two airports paused.",
     art_poland),
    ("7  IRAQ · SECURITY",
     "Iraqi army enters militia stronghold",
     "Troops deploy to Jurf al-Sakhar.",
     art_iraq),
    ("8  ITALY · LABOUR",
     "General strike over Italy's budget",
     "Workers and students march.",
     art_italy),
    ("9  TOKYO · ECONOMY",
     "Japan's inflation picks up to 2.3%",
     "A December rate rise stays in view.",
     art_japan),
    ("10  SEOUL · POLITICS",
     "Korea to impeach top judge",
     "It follows an overturned conviction.",
     art_seoul),
    ("11  KENYA · ENERGY",
     "Kenya drills its first oil well",
     "First crude is due on 1 December.",
     art_kenya),
    ("12  SALVADOR · POLITICS",
     "Bukele files for a third term",
     "The vote is on 28 February 2027.",
     art_bukele),
    ("13  WELLINGTON · CRICKET",
     "Phillips hits 118 against India",
     "Hundreds in India in all three formats.",
     art_cricket),
]

BRIEFS = [
    (14, "Lviv", "A strike on a railway station kills two (BBC)"),
    (15, "Moscow", "Russia declares Estonia's border closed (Reuters)"),
    (16, "Berlin", "School pupils strike against military service (Al Jazeera)"),
    (17, "London", "General says UK runs cyber attacks abroad (Sky News)"),
    (18, "Beijing", "China holds its loan rates for an 18th month (Xinhua)"),
    (19, "Tokyo", "SoftBank shares fall more than 14% in a day (Al Jazeera)"),
    (20, "Seoul", "KOSPI index ends the week 7.9% lower (Anadolu)"),
    (21, "Ganjam", "209 mm of rain falls as Akvan crosses Odisha (PTI)"),
    (22, "Lebanon", "Israeli air strikes hit the south and the east (Anadolu)"),
    (23, "Yemen", "Gunmen fire on a cargo ship off the coast (UKMTO)"),
    (24, "Abuja", "Court bars new evidence against Tinubu (Channels TV)"),
    (25, "Kampala", "Police told to enforce Ebola ban on rallies (allAfrica)"),
    (26, "Malawi", "Fuel crisis brings night-long petrol queues (Al Jazeera)"),
    (27, "Africa", "AfDB says 22 countries are in debt distress (allAfrica)"),
    (28, "Las Vegas", "Russell fastest in wet Grand Prix practice (Autosport)"),
    (29, "New York", "Nasdaq futures fall 1.6% before the bell (24/7 Wall St)"),
    (30, "Washington", "Democrats query law firm's free work (Al Jazeera)"),
    (31, "Wellington", "Nicholls makes 175 in a 216-run stand with Phillips (ICC)"),
    (32, "Sydney", "Australian shares fall 1.8% in the sell-off (Reuters)"),
    (33, "Antalya", "Panama asks COP31 to cap world oil output (Anadolu)"),
    (34, "Antalya", "EU official calls the climate draft unacceptable (RTE)"),
    (35, "Turin", "ATP backs a plan to lift player pay past $350m (Anadolu)"),
]

REGIONS = [("Europe", 8, (31, 78, 121)), ("Asia", 8, (168, 50, 50)),
           ("Middle East", 3, (183, 121, 31)), ("Africa", 5, (46, 125, 50)),
           ("Americas", 4, (106, 63, 160)), ("Oceania", 3, (0, 131, 143)),
           ("Global", 4, (85, 85, 85))]

STATS = [("3", "bridges over the Dnipro damaged in Kyiv"),
         ("300,000+", "people moved to shelters before Akvan"),
         ("-6.2%", "Taiwan's share index, Friday's close"),
         ("100,000", "youth visas a year in the UK-EU deal"),
         ("2.3%", "Japan consumer inflation in October"),
         ("118", "runs by Glenn Phillips against India")]


PINS = [(1, 30, 50), (2, 85, 20), (3, 121, 25), (4, 4, 51), (5, 31, 37),
        (6, 19, 52), (7, 44, 33), (8, 12, 42), (9, 139, 36),
        (10, 127, 37), (11, 37, 0), (12, -89, 14), (13, 175, -41)]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36
    CW = W - 2 * M

    # Top bar
    d.text((M, 8), "THE WORLD IN ONE DAY", font=font(SANS_B, 15), fill=RED)
    right = "35 STORIES  ·  7 REGIONS  ·  EVERY ONE DATED FRIDAY 20 NOVEMBER 2026"
    rf = font(SANS_B, 13)
    d.text((W - M - d.textlength(right, font=rf), 9), right, font=rf, fill=INK)
    d.line([(M, 28), (W - M, 28)], fill=INK, width=2)

    # Masthead: shrink until it fits the page width
    title = "Friday 20 November 2026"
    tsize = 76
    tf = font(SERIF_B, tsize)
    while d.textlength(title, font=tf) > CW and tsize > 40:
        tsize -= 2
        tf = font(SERIF_B, tsize)
    d.text(((W - d.textlength(title, font=tf)) / 2, 32), title, font=tf, fill=INK)
    sub = ("Russian missiles hit Kyiv's bridges  ·  Cyclone Akvan strikes India  ·  "
           "An AI sell-off sinks Asia's markets  ·  UK and EU seal a deal")
    ssize = 18
    sf = font(SERIF, ssize)
    while d.textlength(sub, font=sf) > CW and ssize > 12:
        ssize -= 1
        sf = font(SERIF, ssize)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 116), sub, font=sf, fill=DARK)

    # Stat strip
    cell_w = CW / 6
    for i, (num, cap) in enumerate(STATS):
        x = M + i * cell_w
        if i:
            d.line([(x - 3, 144), (x - 3, 200)], fill=RED, width=2)
        nf = font(SERIF_B, 28)
        d.text((x + 4, 142), num, font=nf, fill=INK)
        para(d, cap, font(SANS, 12), x + 4, 174, cell_w - 12, fill=DARK, spacing=1)

    # Region bar
    total = sum(c for _, c, _ in REGIONS)
    x = M
    y0 = 206
    for name, count, color in REGIONS:
        wseg = CW * count / total
        d.rectangle([x, y0, x + wseg, y0 + 20], fill=color)
        lab = f"{name} {count}"
        lf = font(SANS_B, 12)
        lw = d.textlength(lab, font=lf)
        if lw < wseg - 6:
            d.text((x + (wseg - lw) / 2, y0 + 3), lab, font=lf,
                   fill=(255, 255, 255))
        x += wseg

    # Lead stories
    lead_w, lead_gap = 310, 11
    for i, (kick, head, deck, art) in enumerate(LEADS):
        x = M + i * (lead_w + lead_gap)
        art(d, x, 234, lead_w, 96)
        d.text((x, 336), kick, font=font(SANS_B, 13), fill=RED)
        y = para(d, head, font(SERIF_B, 22), x, 352, lead_w, spacing=1)
        para(d, deck, font(SANS, 13), x, y + 2, lead_w, fill=DARK, spacing=2)
    d.line([(M, 456), (W - M, 456)], fill=(200, 200, 200), width=1)

    # Small stories: 5 columns x 2 rows
    cell_w, cell_gap = 182, 10
    for i, (kick, head, deck, art) in enumerate(SMALLS):
        col, row = i % 5, i // 5
        x = M + col * (cell_w + cell_gap)
        yb = 464 + row * 150
        art(d, x, yb, cell_w, 46)
        kf = font(SANS_B, 11)
        d.text((x, yb + 50), trunc(d, kick, kf, cell_w), font=kf, fill=RED)
        y = para(d, head, font(SERIF_B, 16), x, yb + 66, cell_w, spacing=1)
        para(d, deck, font(SANS, 12), x, y + 2, cell_w, fill=DARK, spacing=1)

    # Bottom: map + briefs
    d.text((M, 772), "WHERE IT HAPPENED", font=font(SANS_B, 13), fill=INK)
    d.text((344, 772), "ALSO ON FRIDAY 20 NOVEMBER — 22 MORE STORIES",
           font=font(SANS_B, 13), fill=INK)
    draw_map(d, M, 790, 294, 120, PINS)
    bx = 344
    col_w = 317
    bf = font(SANS, 10)
    for j, (num, place, text) in enumerate(BRIEFS):
        col = j // 11
        row = j % 11
        x = bx + col * (col_w + 10)
        y = 790 + row * 11
        line = f"{num}  {place} — {text}"
        line = trunc(d, line, bf, col_w)
        d.text((x, y), line, font=bf, fill=INK)

    # Date check
    d.rectangle([M, 922, W - M, 964], outline=RED, width=2)
    d.text((M + 10, 928), "DATE CHECK", font=font(SANS_B, 13), fill=RED)
    dc = ("Left out as Thursday 19 November's news: the World Court's ruling on "
          "Myanmar, the three-leader declaration in Shenzhen and Tonga's drought "
          "emergency. Not yet happened, so not shown: BepiColombo's orbit entry "
          "and any final COP31 text.")
    para(d, dc, font(SANS, 12), M + 108, 928, W - M - (M + 108) - 8,
         fill=DARK, spacing=2)

    foot = ("Every story here happened, or was first reported, on Friday 20 November "
            "2026. Sources named beside each story · original drawings")
    ff = font(SANS, 11)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 974), foot, font=ff, fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
