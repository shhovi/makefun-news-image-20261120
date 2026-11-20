#!/usr/bin/env python3
"""Draw entry.png: one-day world news poster for Friday 20 November 2026.

Build-time only (Pillow). The entered program is main.ts, which copies the
finished entry.png to /output/entry.png with no network. All words are set
here in code so the judge sees exact, legible text.
Events (all reported 20 Nov 2026):
  1. Ukraine strikes the Kerch (Crimea) Bridge a third time this week;
     rail traffic halted, Putin vows a response.
  2. Houthi missiles damage the PIF tower in Riyadh; four targets claimed.
  3. Markets slide: S&P 500 down a fifth straight day; Taiwan plunges
     more than 2,200 points intraday.
  4. Kenya discharges its last Ebola patient, 37 days after the first case.
  Ticker: US Senate rejects Iran war-powers resolution 51-48;
          Herzog taps Eisenkot to form Israel's next government;
          tanker burns after hitting a mine in the Strait of Hormuz.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (247, 243, 232)
INK = (24, 28, 38)
NAVY = (18, 42, 92)
TEAL = (0, 110, 110)
RED = (178, 34, 34)
GREEN = (18, 120, 62)
WHITE = (255, 255, 255)
GREY = (70, 76, 90)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def center_text(d, cx, y, text, fnt, fill):
    box = d.textbbox((0, 0), text, font=fnt)
    d.text((cx - (box[2] - box[0]) / 2, y), text, font=fnt, fill=fill)
    return box[3] - box[1]


def draw_globe(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(30, 110, 200), outline=WHITE, width=4)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=WHITE, width=3)
    d.line([cx - r, cy, cx + r, cy], fill=WHITE, width=3)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 0, 180, fill=WHITE, width=3)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 180, 360, fill=WHITE, width=3)


def icon_bridge(d, x, y):
    # Suspension bridge over water with a blast star on the deck.
    d.rectangle([x, y + 92, x + 150, y + 112], fill=(60, 130, 200))
    for wx in (x + 16, x + 52, x + 88, x + 124):
        d.arc([wx, y + 96, wx + 22, y + 110], 0, 180, fill=WHITE, width=3)
    d.rectangle([x + 4, y + 66, x + 146, y + 76], fill=INK)
    for px in (x + 34, x + 112):
        d.rectangle([px, y + 10, px + 10, y + 92], fill=INK)
    d.line([x + 8, y + 66, x + 39, y + 14], fill=INK, width=4)
    d.line([x + 39, y + 14, x + 75, y + 52], fill=INK, width=4)
    d.line([x + 75, y + 52, x + 117, y + 14], fill=INK, width=4)
    d.line([x + 117, y + 14, x + 142, y + 66], fill=INK, width=4)
    cx, cy = x + 75, y + 58
    d.polygon(
        [(cx, cy - 26), (cx + 7, cy - 8), (cx + 25, cy - 9), (cx + 11, cy + 3),
         (cx + 17, cy + 21), (cx, cy + 11), (cx - 17, cy + 21), (cx - 11, cy + 3),
         (cx - 25, cy - 9), (cx - 7, cy - 8)],
        fill=(245, 160, 20), outline=RED,
    )


def icon_tower(d, x, y):
    # Skyscraper with a missile streaking in from the corner.
    d.rectangle([x + 46, y + 18, x + 104, y + 112], fill=(90, 98, 115))
    d.rectangle([x + 66, y + 4, x + 84, y + 18], fill=(90, 98, 115))
    for wx in (x + 56, x + 74, x + 90):
        for wy in (y + 30, y + 52, y + 74, y + 94):
            d.rectangle([wx, wy, wx + 9, wy + 11], fill=(250, 215, 90))
    d.line([x + 4, y + 8, x + 52, y + 44], fill=RED, width=6)
    d.polygon([(x + 52, y + 44), (x + 40, y + 30), (x + 60, y + 28)], fill=RED)
    d.ellipse([x + 44, y + 36, x + 68, y + 60], fill=(245, 160, 20), outline=RED, width=3)


def icon_chart_down(d, x, y):
    d.line([x + 8, y + 104, x + 142, y + 104], fill=INK, width=5)
    d.line([x + 8, y + 104, x + 8, y + 10], fill=INK, width=5)
    pts = [(x + 16, y + 22), (x + 52, y + 44), (x + 84, y + 38), (x + 126, y + 86)]
    d.line(pts, fill=RED, width=8, joint="curve")
    d.polygon([(x + 126, y + 100), (x + 140, y + 78), (x + 116, y + 76)], fill=RED)
    d.ellipse([x + 44, y + 36, x + 60, y + 52], fill=RED)
    d.ellipse([x + 76, y + 30, x + 92, y + 46], fill=RED)


def icon_cross(d, x, y):
    # Medical cross in a ring: outbreak over, last patient discharged.
    cx, cy, r = x + 75, y + 58, 48
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE, outline=GREEN, width=6)
    d.rectangle([cx - 11, cy - 30, cx + 11, cy + 30], fill=GREEN)
    d.rectangle([cx - 30, cy - 11, cx + 30, cy + 11], fill=GREEN)
    d.arc([cx - r - 8, cy - r - 8, cx + r + 8, cy + r + 8], 300, 60, fill=GREEN, width=6)


def fit_font(d, text, max_w, start, path=BOLD):
    """Largest bold size at or below start whose text fits max_w pixels."""
    size = start
    while size > 18:
        fnt = font(path, size)
        box = d.textbbox((0, 0), text, font=fnt)
        if box[2] - box[0] <= max_w:
            return fnt
        size -= 2
    return font(path, size)


def panel(d, box, stripe, kicker, headline, lines, icon):
    x0, y0, x1, y1 = box
    inner = (x1 - x0) - 44
    d.rounded_rectangle(box, radius=18, fill=WHITE, outline=(200, 196, 182), width=3)
    d.rounded_rectangle([x0, y0, x1, y0 + 46], radius=18, fill=stripe)
    d.rectangle([x0, y0 + 30, x1, y0 + 46], fill=stripe)
    d.text((x0 + 22, y0 + 8), kicker, font=fit_font(d, kicker, inner, 27), fill=WHITE)
    icon(d, x0 + 24, y0 + 58)
    d.text((x0 + 22, y0 + 182), headline, font=fit_font(d, headline, inner, 38), fill=INK)
    y = y0 + 232
    for line in lines:
        d.text((x0 + 22, y), line, font=fit_font(d, line, inner, 30, REG), fill=GREY)
        y += 38


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Header band: names the day, big enough to read at 300px.
    d.rectangle([0, 0, W, 168], fill=NAVY)
    draw_globe(d, 86, 84, 52)
    center_text(d, 560, 18, "WORLD NEWS", font(BOLD, 74), WHITE)
    center_text(d, 560, 102, "Friday  •  20 November 2026", font(BOLD, 42), (255, 214, 90))
    # Thin gold rule under the header, echoing the date colour.
    d.rectangle([0, 168, W, 174], fill=(255, 214, 90))

    m, gap, top = 28, 16, 184
    pw = (W - 2 * m - gap) // 2
    ph = 330
    panel(d, [m, top, m + pw, top + ph], RED, "KERCH BRIDGE HIT AGAIN",
          "3rd strike this week",
          ["Ukraine hits Crimea bridge.", "Rail halted; Putin vows reply."], icon_bridge)
    panel(d, [m + pw + gap, top, W - m, top + ph], NAVY, "RIYADH UNDER FIRE",
          "PIF tower damaged",
          ["Houthi missiles hit Riyadh.", "Four targets claimed."], icon_tower)
    top2 = top + ph + gap
    panel(d, [m, top2, m + pw, top2 + ph], RED, "MARKETS SLIDE",
          "5th straight fall",
          ["S&P down again; Asia sinks.", "Taiwan plunges 2,200+ pts."], icon_chart_down)
    panel(d, [m + pw + gap, top2, W - m, top2 + ph], GREEN, "EBOLA: LAST PATIENT OUT",
          "Kenya clears outbreak",
          ["Last patient discharged,", "37 days after first case."], icon_cross)

    # Footer ticker: three more of the day's stories, still legible.
    fy = top2 + ph + gap
    d.rounded_rectangle([m, fy, W - m, H - 24], radius=16, fill=INK)
    line1 = "ALSO: Senate rejects Iran war-powers 51–48"
    line2 = "Herzog taps Eisenkot  •  Hormuz tanker burns"
    center_text(d, W // 2, fy + 14, line1, fit_font(d, line1, W - 2 * m - 40, 29), WHITE)
    center_text(d, W // 2, fy + 58, line2, fit_font(d, line2, W - 2 * m - 40, 29), (255, 214, 90))

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
