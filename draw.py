#!/usr/bin/env python3
"""Draw the front page for the news-image-20261123 (MAIN) entry.

A one-day newspaper front page for Monday 23 November 2026, drawn with
Pillow from the day's reported news. No network, no downloaded assets:
every line and shape is drawn here. Output: art.png, 1024x1024, < 1 MiB.

Stories were picked to cover the day across regions and fields:
US politics, world markets, Mexico, Turkey, climate, the Middle East,
Europe, Africa, South America, Asia, science and sport.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 30
CW = W - 2 * MARGIN  # content width: 964

NAVY = (22, 38, 77)
RED = (178, 28, 28)
INK = (18, 18, 18)
GREY = (90, 90, 90)
PAPER = (253, 252, 247)
PANEL = (238, 241, 246)
RULE = (40, 40, 40)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, fill=INK):
    """Draw wrapped text; returns the y just below the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def hline(draw, x0, x1, y, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def ballot_box(draw, x, y, w, h):
    """A ballot box with a ballot and a check mark, drawn in navy/red."""
    draw.rectangle([x, y, x + w, y + h], fill=PANEL, outline=NAVY, width=2)
    bx, by = x + w // 2 - 34, y + 12
    draw.polygon([(bx, by + 52), (bx + 68, by + 40), (bx + 68, by - 6),
                  (bx, by + 6)], fill=(255, 255, 255), outline=NAVY)
    draw.line([(bx + 14, by + 26), (bx + 28, by + 40), (bx + 52, by + 8)],
              fill=RED, width=5)
    box_x, box_y, box_w, box_h = x + 52, y + 56, w - 104, 46
    draw.rectangle([box_x, box_y, box_x + box_w, box_y + box_h],
                   fill=NAVY, outline=NAVY)
    draw.rectangle([box_x + 18, box_y - 6, box_x + box_w - 18, box_y + 2],
                   fill=(255, 255, 255))
    draw.text((box_x + 16, box_y + 12), "VOTE", font=font(SANS_B, 22),
              fill=(255, 255, 255))
    draw.text((x + 14, y + h - 26), "DEMOCRATS 258  \u00b7  HOUSE MAJORITY",
              font=font(SANS_B, 15), fill=NAVY)


def market_chart(draw, x, y, w, h):
    """A plunging market line with a red arrow, on a white panel."""
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255),
                   outline=NAVY, width=2)
    pad = 12
    ix0, iy0, ix1, iy1 = x + pad, y + pad, x + w - pad, y + h - pad
    for gy in range(4):
        gy_y = iy0 + (iy1 - iy0) * gy / 3
        draw.line([(ix0, gy_y), (ix1, gy_y)], fill=(220, 220, 220), width=1)
    pts = [(0.00, 0.12), (0.14, 0.22), (0.26, 0.18), (0.40, 0.42),
           (0.52, 0.38), (0.66, 0.66), (0.78, 0.60), (0.90, 0.86),
           (1.00, 0.94)]
    xy = [(ix0 + px * (ix1 - ix0), iy0 + py * (iy1 - iy0)) for px, py in pts]
    draw.line(xy, fill=RED, width=4, joint="curve")
    ex, ey = xy[-1]
    draw.polygon([(ex, ey), (ex - 12, ey - 2), (ex - 2, ey + 10)], fill=RED)
    draw.text((x + 12, y + 8), "NIKKEI", font=font(SANS_B, 15), fill=NAVY)
    draw.text((ix1 - 78, iy1 - 26), "-5.06%", font=font(SANS_B, 22),
              fill=RED)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0, x1 = MARGIN, W - MARGIN

    # --- masthead: navy band with the paper's name -----------------------
    d.rectangle([x0, 20, x1, 124], fill=NAVY)
    name = "THE 23"
    f_name = font(SERIF_B, 82)
    name_w = d.textlength(name, font=f_name)
    rd = font(SERIF_B, 40)
    total = name_w + d.textlength("rd", font=rd)
    nx = x0 + (CW - total) // 2
    d.text((nx, 30), name, font=f_name, fill=(255, 255, 255))
    d.text((nx + name_w, 36), "rd", font=rd, fill=(255, 255, 255))
    small = font(SANS_B, 13)
    d.text((x0 + 14, 102), "ONE DAY'S WORLD NEWS, IN FULL", font=small,
           fill=(200, 210, 235))
    right = "EST. 23 NOV 2026"
    d.text((x1 - 14 - d.textlength(right, font=small), 102), right,
           font=small, fill=(200, 210, 235))

    # --- date line --------------------------------------------------------
    hline(d, x0, x1, 132, width=4, fill=RED)
    date = "MONDAY, 23 NOVEMBER 2026"
    f_date = font(SANS_B, 26)
    d.text(((W - d.textlength(date, font=f_date)) // 2, 140), date,
           font=f_date, fill=RED)
    hline(d, x0, x1, 174, width=2)

    # --- deck -------------------------------------------------------------
    deck = ("Democrats take the House, markets slide on AI fears, and a cartel "
            "kingpin falls \u2014 the world in one page.")
    para(d, x0 + 60, 182, deck, font(SERIF_I, 21), CW - 120, 27,
         fill=(50, 50, 50))
    hline(d, x0, x1, 244, width=2)

    # --- lead story (left) + markets (right) ------------------------------
    ly = 256
    lw = 620
    d.text((x0, ly), "UNITED STATES  \u00b7  WASHINGTON",
           font=font(SANS_B, 16), fill=RED)
    y = para(d, x0, ly + 26, "DEMOCRATS TAKE THE HOUSE",
             font(SERIF_B, 50), lw, 56)
    y = para(d, x0, y + 4,
             "A recount in North Carolina confirms Chuck Hubbard's win, "
             "giving Democrats at least 258 seats \u2014 their best result "
             "since 1992.",
             font(SANS, 19), lw, 25)
    ballot_box(d, x0, y + 10, lw, 140)

    rx = x0 + lw + 24
    rw = x1 - rx
    d.text((rx, ly), "MARKETS  \u00b7  TOKYO & NEW YORK",
           font=font(SANS_B, 16), fill=RED)
    y2 = para(d, rx, ly + 26, "AI FEARS SINK STOCKS WORLDWIDE",
              font(SERIF_B, 30), rw, 36)
    y2 = para(d, rx, y2 + 4,
              "Nikkei plunges 5.06% and the S&P 500 falls 3.7% as investors "
              "question AI valuations.",
              font(SANS, 17), rw, 23)
    market_chart(d, rx, y2 + 8, rw, 120)

    hline(d, x0, x1, 634, width=2)

    # --- second row: Mexico + Turkey --------------------------------------
    sy = 646
    col_w = (CW - 24) // 2
    d.text((x0, sy), "MEXICO  \u00b7  SINALOA", font=font(SANS_B, 16), fill=RED)
    y = para(d, x0, sy + 24, "\u2018EL CHAPO ISIDRO\u2019 CAPTURED",
             font(SERIF_B, 29), col_w, 34)
    para(d, x0, y + 2,
         "FBI most-wanted cartel leader Fausto Isidro Meza Flores is arrested "
         "in Guasave after years on the run.",
         font(SANS, 16), col_w, 21)

    tx = x0 + col_w + 24
    d.text((tx, sy), "TURKEY  \u00b7  ISTANBUL", font=font(SANS_B, 16),
           fill=RED)
    y = para(d, tx, sy + 24, "THOUSANDS MARCH ON MEDIA TAKEOVER",
             font(SERIF_B, 29), col_w, 34)
    para(d, tx, y + 2,
         "Crowds rally in Istanbul against a government takeover of "
         "independent media outlets.",
         font(SANS, 16), col_w, 21)

    hline(d, x0, x1, 814, width=2)

    # --- the world in brief ------------------------------------------------
    by = 824
    d.text((x0, by), "THE WORLD IN BRIEF", font=font(SERIF_B, 24), fill=NAVY)
    d.text((x1 - d.textlength("12 STORIES", font=font(SANS_B, 15)), by + 6),
           "12 STORIES", font=font(SANS_B, 15), fill=GREY)
    hline(d, x0, x1, 858, width=1, fill=GREY)

    brief = [
        ("CLIMATE \u00b7 ANTALYA", "COP31 ends with no deal on fossil fuels."),
        ("MIDDLE EAST \u00b7 GAZA", "War left widespread contamination."),
        ("EUROPE \u00b7 ROME", "Italy probes ex-police chief's death."),
        ("EUROPE \u00b7 BRUSSELS", "Airports shut in austerity strike."),
        ("AFRICA \u00b7 KIGALI", "Five EU states back Rwanda centres."),
        ("S. AMERICA \u00b7 BRAS\u00cdLIA", "Bolsonaro in intensive care."),
        ("ASIA \u00b7 MUMBAI", "Tata Steel buys $1.67bn pipe stake."),
        ("TECH \u00b7 SILICON VALLEY", "Nvidia affair linked to Beijing spies."),
        ("SCIENCE \u00b7 AI SAFETY", "AI outpacing safety tests."),
        ("SPORT \u00b7 PORTIM\u00c3O", "M\u00e1rquez wins eighth MotoGP title."),
        ("EUROPE \u00b7 COPENHAGEN", "Russia plotted rapper killing."),
        ("DIPLOMACY \u00b7 ABU DHABI", "Mediators to Moscow."),
    ]
    iy = 866
    bcol_w = (CW - 24) // 2
    f_tag = font(SANS_B, 15)
    f_txt = font(SANS, 15)
    for i, (tag, text) in enumerate(brief):
        col = 0 if i < 6 else 1
        row = i % 6
        bx = x0 + col * (bcol_w + 24)
        byy = iy + row * 20
        line = tag + " \u2014 " + text
        if d.textlength(line, font=f_txt) > bcol_w:
            raise SystemExit(f"brief line too wide: {line}")
        d.text((bx, byy), tag + " \u2014 ", font=f_tag, fill=RED)
        tw = d.textlength(tag + " \u2014 ", font=f_tag)
        d.text((bx + tw, byy), text, font=f_txt, fill=INK)

    # --- footer ------------------------------------------------------------
    hline(d, x0, x1, 990, width=2)
    foot = ("All stories were reported on Monday 23 November 2026. "
            "Sources: Reuters, AP, AFP, BBC.")
    d.text(((W - d.textlength(foot, font=font(SANS, 13))) // 2, 998),
           foot, font=font(SANS, 13), fill=GREY)
    return img


if __name__ == "__main__":
    page = build()
    page.save("art.png", optimize=True)
    print("saved art.png", page.size)
