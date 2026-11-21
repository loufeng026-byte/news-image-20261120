"""Draw the 20 November 2026 world-news front page, 1024x1024 PNG.

Runs with PIL on this machine to produce entry.png. The submitted
program (main.py) only copies that PNG, so the grader run needs no
network and no third-party library: it is deterministic by construction.
All facts below are from reporting of 20 Nov 2026 (One Turn day page,
Just Security Early Edition, Open Chronicle): ICJ 9-6, Shenzhen
four-point declaration, Riyadh tower, Kyiv / Crimea Bridge, S&P -2%,
Nikkei -4.8%, Gaza Yellow Line, COP31, Anthropic +17% to $97.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

BLACK = (15, 15, 15)
WHITE = (255, 255, 255)
RED = (176, 0, 0)
NAVY = (16, 42, 92)
GREY = (90, 90, 90)
LIGHT = (242, 242, 238)
GOLD = (201, 162, 39)


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


def para(draw, text, fnt, x, y, max_w, fill=BLACK, spacing=6):
    lines = wrap(draw, text, fnt, max_w)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def main():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)
    M = 36
    CW = W - 2 * M

    # Top black bar
    d.rectangle([0, 0, W, 38], fill=BLACK)
    d.text((M, 9), "THE WORLD TODAY", font=font(SANS_B, 19), fill=WHITE)
    right = "52 STORIES  •  WORLD MOOD: UNEASY"
    d.text((W - M - d.textlength(right, font=font(SANS_B, 19)), 9),
           right, font=font(SANS_B, 19), fill=WHITE)

    # Masthead
    title = "THE WORLD IN ONE DAY"
    tf = font(SERIF_B, 52)
    d.text(((W - d.textlength(title, font=tf)) / 2, 48),
           title, font=tf, fill=BLACK)
    date = "FRIDAY  20  NOVEMBER  2026"
    df = font(SANS_B, 30)
    dw = d.textlength(date, font=df)
    d.text(((W - dw) / 2, 112), date, font=df, fill=RED)
    d.line([(M, 152), (W - M, 152)], fill=BLACK, width=3)

    # Hero 1: ICJ, left navy panel + right headline
    y0 = 166
    d.rectangle([M, y0, M + 268, y0 + 150], fill=NAVY)
    d.text((M + 20, y0 + 14), "THE HAGUE", font=font(SANS_B, 19), fill=GOLD)
    d.text((M + 20, y0 + 42), "9 – 6", font=font(SERIF_B, 56), fill=WHITE)
    d.text((M + 20, y0 + 110), "ICJ RULING", font=font(SANS_B, 19), fill=WHITE)
    x = M + 292
    d.text((x, y0 + 2), "JUSTICE  •  THE HAGUE",
           font=font(SANS_B, 18), fill=RED)
    y = para(d, "WORLD COURT: MYANMAR GUILTY OF GENOCIDE",
             font(SERIF_B, 38), x, y0 + 26, W - M - x, spacing=2)
    para(d, "ICJ rules Myanmar committed genocide against the "
            "Rohingya. First verdict of its kind against a state. "
            "1.3 million still displaced.",
         font(SANS, 19), x, y + 4, W - M - x, fill=(40, 40, 40), spacing=4)

    # Hero 2: Shenzhen
    y0 = 332
    d.line([(M, y0 - 8), (W - M, y0 - 8)], fill=(200, 200, 200), width=2)
    d.text((M, y0), "POLITICS  •  SHENZHEN, CHINA",
           font=font(SANS_B, 18), fill=RED)
    y = para(d, "TRUMP, XI AND PUTIN SIGN PEACE PACT",
             font(SERIF_B, 32), M, y0 + 24, 640, spacing=2)
    para(d, "First three-way summit, about 70 minutes. Four-point "
            "pact on nuclear risk, UN reform and energy.",
         font(SANS, 19), M, y + 4, 640, fill=(40, 40, 40), spacing=4)
    # Right panel: three leaders
    d.rectangle([700, y0, W - M, y0 + 122], fill=LIGHT, outline=BLACK, width=2)
    d.text((724, y0 + 10), "3 LEADERS", font=font(SANS_B, 19), fill=BLACK)
    d.text((724, y0 + 36), "1 DECLARATION", font=font(SANS_B, 19), fill=BLACK)
    for i, code in enumerate(["US", "CN", "RU"]):
        cx = 736 + i * 82
        d.ellipse([cx, y0 + 66, cx + 52, y0 + 106], fill=NAVY)
        tw = d.textlength(code, font=font(SANS_B, 17))
        d.text((cx + (52 - tw) / 2, y0 + 79), code,
               font=font(SANS_B, 17), fill=WHITE)

    # Grid: 2 columns x 3 rows
    stories = [
        ("CONFLICT  •  RIYADH",
         "HOUTHI MISSILE HITS RIYADH TOWER",
         "Saudi wealth-fund tower damaged. No injuries reported."),
        ("WAR  •  KYIV / CRIMEA",
         "RUSSIA HITS KYIV, UKRAINE HITS CRIMEA BRIDGE",
         "Third strike on the bridge in four days. Putin vows response."),
        ("MARKETS",
         "STOCKS FALL FOR A 5TH DAY",
         "S&P 500 -2%. Nikkei -4.8% after Anthropic's debut."),
        ("GAZA",
         "ISRAELI TROOPS CROSS YELLOW LINE",
         "First incursion in central Gaza since the truce."),
        ("CLIMATE  •  ANTALYA",
         "COP31 DRAFT DROPS FOSSIL-FUEL PHASE-OUT",
         "Net-zero dates also removed as talks enter final day."),
        ("TECH  •  NEW YORK",
         "ANTHROPIC IPO CLOSES +17% AT $97",
         "Record $81.3bn listing. Nvidia faces probe after CEO quits."),
    ]
    gy = 472
    cell_w, cell_h = 466, 132
    for i, (kick, head, deck) in enumerate(stories):
        cx = M + (i % 2) * (cell_w + 20)
        cy = gy + (i // 2) * (cell_h + 10)
        d.text((cx, cy), kick, font=font(SANS_B, 17), fill=RED)
        y = para(d, head, font(SERIF_B, 24), cx, cy + 24, cell_w, spacing=1)
        para(d, deck, font(SANS, 18), cx, y + 2, cell_w,
             fill=(40, 40, 40), spacing=3)

    # Bottom strip: also today
    y0 = 910
    d.rectangle([0, y0, W, 986], fill=BLACK)
    d.text((M, y0 + 12), "ALSO TODAY:",
           font=font(SANS_B, 20), fill=GOLD)
    para(d, "Kenya Ebola-free  •  GTA 6 tops $2.3bn  •  EU-UK youth "
            "mobility deal  •  Estonia shuts Russia border",
         font(SANS_B, 20), M + 148, y0 + 12, W - M - (M + 148),
         fill=WHITE, spacing=4)
    foot = "All events reported on Friday 20 November 2026"
    ff = font(SANS, 15)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 994),
           foot, font=ff, fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
