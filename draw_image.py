#!/usr/bin/env python3
"""Poster for Friday 20 November 2026 — built at build time with Pillow.

The day's four lead stories (all reported 20 Nov 2026):
  * Ukraine struck the Kerch Bridge for the third time this week;
    rail traffic stopped and Putin promised a response.
  * Houthi missiles damaged the Public Investment Fund tower in
    Riyadh; four targets were claimed.
  * Stocks fell for a fifth straight session in the US while Taiwan's
    index plunged more than 2,200 points intraday.
  * Kenya discharged its last Ebola patient, 37 days after its
    first case.
Ticker items: the US Senate rejected an Iran war-powers resolution
51-48; President Herzog asked Eisenkot to form Israel's next
government; a tanker burned after hitting a mine in the Strait of
Hormuz.

The shipped program is main.ts; it copies the finished entry.png to
/output at run time. Text is drawn here so every word stays exact.
"""
from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
PAPER = (250, 246, 236)
CARD = (255, 255, 255)
EDGE = (198, 194, 180)
TEXT = (26, 30, 40)
SUB = (74, 80, 94)
BANNER = (16, 40, 88)
GOLD = (255, 214, 90)
CRIMSON = (176, 32, 32)
FOREST = (16, 118, 60)
SKY = (58, 128, 198)
AMBER = (245, 160, 20)
STEEL = (92, 100, 117)
LAMP = (250, 215, 90)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def fnt(path, px):
    return ImageFont.truetype(path, px)


def shrink(draw, s, limit, start, path=FB):
    px = start
    while px > 18:
        f = fnt(path, px)
        if draw.textlength(s, font=f) <= limit:
            return f
        px -= 2
    return fnt(path, px)


def centred(draw, cx, y, s, f, colour):
    draw.text((cx - draw.textlength(s, font=f) / 2, y), s, font=f, fill=colour)


def globe(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(30, 110, 200), outline=CARD, width=4)
    draw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=CARD, width=3)
    draw.line([cx - r, cy, cx + r, cy], fill=CARD, width=3)
    draw.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 0, 180, fill=CARD, width=3)
    draw.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 180, 360, fill=CARD, width=3)


def glyph_bridge(draw, ox, oy):
    draw.rectangle([ox, oy + 94, ox + 150, oy + 112], fill=SKY)
    for wx in range(ox + 14, ox + 140, 36):
        draw.arc([wx, oy + 97, wx + 22, oy + 110], 0, 180, fill=CARD, width=3)
    draw.rectangle([ox + 4, oy + 68, ox + 146, oy + 77], fill=TEXT)
    for tx in (ox + 34, ox + 112):
        draw.rectangle([tx, oy + 10, tx + 10, oy + 94], fill=TEXT)
    cable = [(ox + 6, oy + 68), (ox + 39, oy + 14), (ox + 75, oy + 52),
             (ox + 117, oy + 14), (ox + 144, oy + 68)]
    draw.line(cable, fill=TEXT, width=4, joint="curve")
    bx, by = ox + 75, oy + 58
    star = []
    for i in range(10):
        ang = -90 + i * 36
        rad = 25 if i % 2 == 0 else 10
        import math
        star.append((bx + rad * math.cos(math.radians(ang)),
                     by + rad * math.sin(math.radians(ang))))
    draw.polygon(star, fill=AMBER, outline=CRIMSON)


def glyph_tower(draw, ox, oy):
    draw.rectangle([ox + 48, oy + 20, ox + 104, oy + 112], fill=STEEL)
    draw.rectangle([ox + 68, oy + 6, ox + 84, oy + 20], fill=STEEL)
    for col in (ox + 57, ox + 74, ox + 90):
        for row in (oy + 32, oy + 53, oy + 74, oy + 94):
            draw.rectangle([col, row, col + 9, row + 11], fill=LAMP)
    draw.line([ox + 2, oy + 6, ox + 50, oy + 42], fill=CRIMSON, width=6)
    draw.polygon([(ox + 52, oy + 44), (ox + 38, oy + 30), (ox + 60, oy + 27)], fill=CRIMSON)
    draw.ellipse([ox + 43, oy + 35, ox + 67, oy + 59], fill=AMBER, outline=CRIMSON, width=3)


def glyph_falling(draw, ox, oy):
    draw.line([ox + 8, oy + 104, ox + 142, oy + 104], fill=TEXT, width=5)
    draw.line([ox + 8, oy + 104, ox + 8, oy + 10], fill=TEXT, width=5)
    path = [(ox + 16, oy + 22), (ox + 52, oy + 44), (ox + 84, oy + 38), (ox + 126, oy + 86)]
    draw.line(path, fill=CRIMSON, width=8, joint="curve")
    draw.polygon([(ox + 126, oy + 100), (ox + 140, oy + 78), (ox + 116, oy + 76)], fill=CRIMSON)
    for cx, cy in ((ox + 52, oy + 44), (ox + 84, oy + 38)):
        draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=CRIMSON)


def glyph_medical(draw, ox, oy):
    cx, cy, r = ox + 75, oy + 58, 47
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=CARD, outline=FOREST, width=6)
    draw.rectangle([cx - 11, cy - 30, cx + 11, cy + 30], fill=FOREST)
    draw.rectangle([cx - 30, cy - 11, cx + 30, cy + 11], fill=FOREST)
    draw.arc([cx - r - 9, cy - r - 9, cx + r + 9, cy + r + 9], 295, 65, fill=FOREST, width=6)


STORIES = [
    ("KERCH BRIDGE HIT AGAIN", CRIMSON, "3rd strike this week",
     ["Ukraine hits Crimea bridge.", "Rail halted; Putin vows reply."], glyph_bridge),
    ("RIYADH UNDER FIRE", BANNER, "PIF tower damaged",
     ["Houthi missiles hit Riyadh.", "Four targets claimed."], glyph_tower),
    ("MARKETS SLIDE", CRIMSON, "5th straight fall",
     ["S&P down again; Asia sinks.", "Taiwan plunges 2,200+ pts."], glyph_falling),
    ("EBOLA: LAST PATIENT OUT", FOREST, "Kenya clears outbreak",
     ["Last patient discharged,", "37 days after first case."], glyph_medical),
]


def card(draw, rect, story):
    kicker, band, headline, sublines, glyph = story
    x0, y0, x1, y1 = rect
    room = (x1 - x0) - 44
    draw.rounded_rectangle(rect, radius=18, fill=CARD, outline=EDGE, width=3)
    draw.rounded_rectangle([x0, y0, x1, y0 + 46], radius=18, fill=band)
    draw.rectangle([x0, y0 + 30, x1, y0 + 46], fill=band)
    draw.text((x0 + 22, y0 + 8), kicker, font=shrink(draw, kicker, room, 27), fill=CARD)
    glyph(draw, x0 + 24, y0 + 58)
    draw.text((x0 + 22, y0 + 182), headline,
              font=shrink(draw, headline, room, 38), fill=TEXT)
    yy = y0 + 232
    for s in sublines:
        draw.text((x0 + 22, yy), s, font=shrink(draw, s, room, 30, FR), fill=SUB)
        yy += 38


def build():
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, SIZE, 168], fill=BANNER)
    globe(d, 86, 84, 52)
    centred(d, 560, 18, "WORLD NEWS", fnt(FB, 74), CARD)
    centred(d, 560, 102, "Friday  •  20 November 2026", fnt(FB, 42), GOLD)
    d.rectangle([0, 168, SIZE, 174], fill=GOLD)

    margin, gap, top = 28, 16, 184
    pw = (SIZE - 2 * margin - gap) // 2
    ph = 330
    spots = [
        [margin, top, margin + pw, top + ph],
        [margin + pw + gap, top, SIZE - margin, top + ph],
        [margin, top + ph + gap, margin + pw, top + 2 * ph + gap],
        [margin + pw + gap, top + ph + gap, SIZE - margin, top + 2 * ph + gap],
    ]
    for rect, story in zip(spots, STORIES):
        card(d, rect, story)

    fy = top + 2 * ph + 2 * gap
    d.rounded_rectangle([margin, fy, SIZE - margin, SIZE - 24], radius=16, fill=TEXT)
    t1 = "ALSO: Senate rejects Iran war-powers 51–48"
    t2 = "Herzog taps Eisenkot  •  Hormuz tanker burns"
    centred(d, SIZE // 2, fy + 14, t1, shrink(d, t1, SIZE - 2 * margin - 40, 29), CARD)
    centred(d, SIZE // 2, fy + 58, t2, shrink(d, t2, SIZE - 2 * margin - 40, 29), GOLD)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    build()
