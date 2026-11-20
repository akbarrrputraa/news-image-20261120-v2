#!/usr/bin/env python3
"""THE WORLD TODAY - Friday 20 November 2026.
A one-page broadsheet summing up the day's world news, drawn entirely
in code (Pillow). No network, no external images: every pictogram is
drawn with primitives. Deterministic: two runs write identical bytes.

Run:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
Output: $MAKEFUN_OUTPUT_DIR/entry.png  (1024 x 1024, < 1 MiB)
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)   # newsprint cream
INK = (22, 22, 22)
RED = (160, 30, 34)
GREY = (105, 100, 90)
RULE = (60, 58, 52)
LIGHT = (232, 227, 214)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines that fit `width` px."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, leading, fill=INK):
    """Draw wrapped paragraph; return y after last line."""
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=1, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- stories
# Every item below was verified against reporting published 19-20 Nov 2026
# (Reuters, The Times, WSJ, AP/BBC, USA Today, Le Monde, Investor's
# Business Daily, Fox 5 NY). No invented facts: figures are as reported.
LEAD_HEAD = "TRUMP, XI AND PUTIN SIGN PEACE DECLARATION"
LEAD_DECK = "First trilateral summit covers nuclear risk, UN reform and energy"
LEAD_BODY = (
    "The leaders of the United States, China and Russia met in Shenzhen on "
    "Thursday for their first three-way summit and signed a four-point joint "
    "declaration. It covers reducing nuclear risk, reforming the United "
    "Nations and stabilising energy supply. The text does not mention "
    "Ukraine or Iran; Europe and Ukraine were not at the table."
)

# (kicker, headline, body) - 12 grid stories
GRID = [
    ("JUSTICE", "MYANMAR GUILTY OF GENOCIDE, WORLD COURT RULES",
     "The ICJ found Myanmar committed genocide against the Rohingya in "
     "2017, by 9-6 - the first time it has held a state responsible. "
     "Reparations were ordered."),
    ("TECH", "ANTHROPIC'S $81BN DEBUT IS THE BIGGEST IPO EVER",
     "The Claude maker priced at $83, opened at $111.50 and closed at "
     "$97.17, up 17%, valuing it at about $1.3 trillion - the largest "
     "IPO ever."),
    ("MARKETS", "WALL STREET TUMBLES AS AI FEVER BREAKS",
     "The Dow fell 1,101 points, or 2.2%, to 49,097; the S&P 500 lost "
     "2.0% and the Nasdaq 2.3% - the S&P's fifth straight loss."),
    ("CULTURE", "GTA VI: $1.84BN LAUNCH SMASHES RECORDS",
     "Rockstar's GTA VI sold an estimated 19.05m copies by launch day, "
     "Sensor Tower estimates - over double GTA V's first-day haul - "
     "scoring 99 on Metacritic."),
    ("WAR", "KYIV HIT AGAIN AS MISSILE DEBRIS SETS FIRE",
     "Missile debris set fire to a three-storey building in Kyiv's "
     "Obolonskyi district early on Friday, the mayor said. Explosions "
     "were heard across the capital."),
    ("MIDDLE EAST", "HOUTHI MISSILES DAMAGE RIYADH TOWER",
     "Houthi missiles struck Riyadh's financial district, damaging the "
     "Public Investment Fund tower, Saudi Arabia's tallest. Two drones "
     "were downed."),
    ("SPORT", "TRUMP PARDONS PETE ROSE, BASEBALL'S HIT KING",
     "Trump posthumously pardoned Pete Rose, MLB's all-time hits leader "
     "with 4,256, banned for betting on baseball. He died in 2024, "
     "aged 83."),
    ("WORLD", "FIONA THE HIPPO DIES AT 9 AFTER SWALLOWING HAT",
     "Cincinnati Zoo's hippo, a global star since her premature birth in "
     "2017, died after swallowing a visitor's knitted hat. Vets tried "
     "for 11 days."),
    ("CLIMATE", "COP31 DRAFT DROPS ALL FOSSIL-FUEL LANGUAGE",
     "In Antalya, negotiators published a slimmed-down draft deal with "
     "no mention of fossil fuels, removing two references from Monday's "
     "text."),
    ("EUROPE", "COST-OF-LIVING PROTESTS SWEEP EUROPE",
     "Unions rallied across France, Britain, Belgium, Spain, Italy, "
     "Portugal and Greece on Friday over living costs and housing; Italy "
     "held a general strike."),
    ("EUROPE", "ESTONIA TO SHUT ITS BORDER WITH RUSSIA",
     "Estonia said it will close border crossings with Russia from "
     "December after an attempted attack on a defence company."),
    ("SPORT", "TEXANS ROUT COLTS 26-3 ON THURSDAY NIGHT",
     "C.J. Stroud threw three touchdown passes as Houston beat "
     "Indianapolis 26-3 to open NFL Week 11; the Texans are 4-6, the "
     "Colts 3-8."),
]

# (bold lead-in, text) - IN BRIEF column
BRIEF = [
    ("AMD dives:", "shares fell over 7% after a short-seller report questioned its China exposure."),
    ("Japan inflation:", "core inflation hit its highest this year as energy subsidies ended; the Nikkei fell 4.8%."),
    ("Sanctions:", "the US sanctioned the Comancheros gang and Italy's 'Ndrangheta, blocking their US assets."),
    ("Kim meeting:", "Trump told NBC he will meet North Korea's Kim Jong-un \"at some point\"."),
    ("Iran vote:", "the US Senate rejected a war-powers resolution on Iran by 51-48."),
    ("Stacy Keach dies:", "the American actor, star of stage and screen, has died aged 85."),
    ("Paris talks:", "Kamala Harris met Emmanuel Macron in Paris as Europe weighed Ukraine talks."),
    ("Earthquake:", "a 5.6-magnitude quake struck near New Caledonia in the Pacific."),
    ("Drones halt Genoa:", "Genoa airport suspended flights after unidentified drones were detected."),
]

MARKETS = ("DOW 49,097  -2.2%      S&P 500  7,176  -2.0%      "
           "NASDAQ  23,879  -2.3%      NIKKEI  -4.8%      "
           "BRENT $90.05  +0.7%      ANT $97.17  +17%")


# ---------------------------------------------------------------- drawing
def draw_globe(draw, cx, cy, r):
    """Small wireframe globe pictogram, drawn in code."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=2)
    draw.ellipse([cx - r * 0.55, cy - r, cx + r * 0.55, cy + r],
                 outline=INK, width=1)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=INK, width=1)
    draw.line([(cx, cy - r), (cx, cy + r)], fill=INK, width=1)
    draw.arc([cx - r, cy - r * 0.45, cx + r, cy + r * 0.45],
             start=200, end=340, fill=INK, width=1)
    draw.arc([cx - r, cy - r * 0.45, cx + r, cy + r * 0.45],
             start=20, end=160, fill=INK, width=1)


def draw_summit(draw, x, y, w, h):
    """Shenzhen skyline + three leaders' flag bars, drawn in code."""
    # sky
    draw.rectangle([x, y, x + w, y + h], fill=(214, 226, 235),
                   outline=INK, width=2)
    # sun
    draw.ellipse([x + w - 52, y + 12, x + w - 18, y + 46], fill=(214, 140, 40))
    # skyline silhouette
    base = y + h - 58
    towers = [(0, 46), (34, 78), (72, 58), (104, 96), (140, 66),
              (176, 88), (210, 52), (244, 80), (276, 60)]
    for tx, th in towers:
        draw.rectangle([x + tx, base - th, x + tx + 28, base],
                       fill=(52, 68, 86))
    draw.rectangle([x, base, x + w, base + 58], fill=(52, 68, 86))
    # three flag bars: US, China, Russia
    bars = [((178, 34, 52), "USA"), ((192, 28, 28), "CHN"),
            ((255, 255, 255), "RUS")]
    bw, bh = 62, 34
    bx = x + 18
    for i, (col, lab) in enumerate(bars):
        bx_i = bx + i * (bw + 14)
        draw.rectangle([bx_i, base + 8, bx_i + bw, base + 8 + bh],
                       fill=col, outline=INK, width=1)
        if lab == "USA":
            draw.rectangle([bx_i, base + 8, bx_i + 26, base + 8 + 16],
                           fill=(40, 60, 120))
            for s in range(3):
                draw.line([(bx_i, base + 14 + s * 9),
                           (bx_i + bw, base + 14 + s * 9)],
                          fill=(255, 255, 255), width=2)
        elif lab == "CHN":
            draw.ellipse([bx_i + 8, base + 13, bx_i + 20, base + 25],
                         fill=(255, 220, 60))
        else:
            draw.rectangle([bx_i, base + 8 + 11, bx_i + bw, base + 8 + 23],
                           fill=(40, 80, 180))
            draw.rectangle([bx_i, base + 8 + 23, bx_i + bw, base + 8 + bh],
                           fill=(200, 40, 40))
        draw.text((bx_i + 4, base + 8 + bh + 4), lab,
                  font=font(SANS_B, 11), fill=(255, 255, 255))
    draw.text((x + 8, y + 6), "SHENZHEN  •  THE FIRST TRILATERAL SUMMIT",
              font=font(SANS_B, 11), fill=INK)


def draw_market_bars(draw, x, y):
    """Tiny falling-bars pictogram for the markets strip."""
    vals = [26, 22, 30, 18, 24, 14]
    for i, v in enumerate(vals):
        bx = x + i * 11
        draw.rectangle([bx, y + 30 - v, bx + 7, y + 30], fill=(255, 255, 255))
    draw.line([(x - 2, y + 30), (x + 66, y + 30)], fill=(255, 255, 255),
              width=1)


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 26
    R = W - M  # right edge

    # ---- top dateline bar
    f_small = font(SANS_B, 11)
    d.text((M, 12), "FRIDAY, 20 NOVEMBER 2026", font=f_small, fill=INK)
    tag = "THE WORLD IN ONE PAGE"
    d.text((R - d.textlength(tag, font=f_small), 12), tag, font=f_small,
           fill=RED)
    rule(d, M, 34, R, 2)

    # ---- masthead
    f_mast = font(SERIF_B, 62)
    title = "THE WORLD TODAY"
    d.text(((W - d.textlength(title, font=f_mast)) / 2, 40), title,
           font=f_mast, fill=INK)
    f_sub = font(SANS, 12)
    sub = "S U M M I N G   U P   T H E   D A Y ' S   W O R L D   N E W S"
    d.text(((W - d.textlength(sub, font=f_sub)) / 2, 112), sub, font=f_sub,
           fill=GREY)
    rule(d, M, 132, R, 3)
    rule(d, M, 136, R, 1)

    # ---- lead story
    ly = 148
    f_lead = font(SERIF_B, 29)
    y = ly
    for line in wrap(d, LEAD_HEAD, f_lead, 600):
        d.text((M, y), line, font=f_lead, fill=INK)
        y += 36
    y += 2
    f_deck = font(SERIF, 15)
    y = para(d, M, y, LEAD_DECK, f_deck, 600, 20, fill=RED)
    y += 6
    f_body = font(SERIF, 13)
    y = para(d, M, y, LEAD_BODY, f_body, 600, 18)
    # lead pictogram, right of lead text
    draw_summit(d, 656, ly + 2, 342, 176)
    rule(d, M, 336, R, 2)

    # ---- markets strip
    d.rectangle([M, 346, R, 384], fill=INK)
    draw_market_bars(d, M + 12, 352)
    f_mk = font(SANS_B, 11)
    d.text((M + 92, 360), MARKETS, font=f_mk, fill=(255, 255, 255))

    # ---- section headers
    f_sec = font(SANS_B, 13)
    d.text((M, 398), "THE DAY IN FULL", font=f_sec, fill=RED)
    d.text((690, 398), "IN BRIEF", font=f_sec, fill=RED)
    rule(d, M, 418, 664, 1)
    rule(d, 690, 418, R, 1)

    # ---- grid: 2 columns x 6 rows
    col_w = 312
    xs = [M, M + col_w + 14]
    row_h = 88
    f_kick = font(SANS_B, 10)
    f_h = font(SANS_B, 14)
    f_b = font(SERIF, 11)
    for i, (kick, head, body) in enumerate(GRID):
        cx = xs[i % 2]
        cy = 428 + (i // 2) * row_h
        d.text((cx, cy), kick, font=f_kick, fill=RED)
        hy = cy + 15
        lines = wrap(d, head, f_h, col_w)[:2]
        for line in lines:
            d.text((cx, hy), line, font=f_h, fill=INK)
            hy += 16
        para(d, cx, hy + 1, body, f_b, col_w, 13, fill=(40, 38, 34))
        if i % 2 == 0:
            rule(d, cx, cy + row_h - 10, cx + col_w, 1, fill=LIGHT)

    # ---- IN BRIEF column
    f_bf = font(SERIF, 12)
    f_bb = font(SERIF_B, 12)
    by = 428
    for lead_in, text in BRIEF:
        full = lead_in + " " + text
        lines = wrap(d, full, f_bf, 296)
        for li, line in enumerate(lines):
            if li == 0:
                rest = line[len(lead_in):].strip()
                d.text((690, by), lead_in, font=f_bb, fill=INK)
                lx = 690 + d.textlength(lead_in + " ", font=f_bb)
                d.text((lx, by), rest, font=f_bf, fill=INK)
            else:
                d.text((690, by), line, font=f_bf, fill=INK)
            by += 16
        by += 8
        rule(d, 690, by - 4, R, 1, fill=LIGHT)

    # ---- footer
    rule(d, M, 972, R, 2)
    f_ft = font(SANS, 10)
    foot = ("Sources: Reuters  •  The Times  •  Wall Street Journal  •  AP  •  BBC  •  "
            "USA Today  •  Le Monde  •  Investor's Business Daily  —  reporting published 19-20 Nov 2026")
    d.text(((W - d.textlength(foot, font=f_ft)) / 2, 980), foot, font=f_ft,
           fill=GREY)
    f_ft2 = font(SANS_B, 10)
    foot2 = "THE WORLD TODAY  •  20 NOVEMBER 2026  •  PAGE 1 OF 1"
    d.text(((W - d.textlength(foot2, font=f_ft2)) / 2, 998), foot2,
           font=f_ft2, fill=INK)
    return img


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(outdir, exist_ok=True)
    img = render()
    path = os.path.join(outdir, "entry.png")
    img.save(path, format="PNG")
    print(f"wrote {path} {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
