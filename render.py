#!/usr/bin/env python3
"""Render the 22 November 2026 world-news front page to entry.png.

Build-time only: the entry ships the pre-rendered entry.png and a
stdlib-only main.py that copies it to /output. Run: python3 render.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "assets", "fonts")
W, H = 1024, 1024
PAPER = (248, 244, 232)
INK = (25, 25, 25)
MUTED = (90, 86, 76)
RED = (163, 22, 33)
NAVY = (31, 58, 95)
TEAL = (15, 118, 110)
GOLD = (176, 132, 40)
RULE = (180, 172, 152)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)   # noqa: E731
SERIF = lambda s: font("DejaVuSerif.ttf", s)         # noqa: E731
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)     # noqa: E731
SANS = lambda s: font("DejaVuSans.ttf", s)            # noqa: E731


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(draw, text, fnt, max_w, max_lines):
    """Wrap and cap to max_lines, ellipsising the last line if cut."""
    lines = wrap(draw, text, fnt, max_w)
    if len(lines) <= max_lines:
        return lines
    lines = lines[:max_lines]
    while lines and draw.textlength(lines[-1] + " …", font=fnt) > max_w:
        lines[-1] = lines[-1][:-1].rstrip()
    lines[-1] = (lines[-1] + " …").strip()
    return lines


def draw_panel(draw, x, y, w, h, kicker, kcolor, headline, deck,
               hsize=26, dsize=17, hlines=2, dlines=3):
    draw.rectangle([x, y, x + w, y + h], outline=RULE, width=2)
    draw.rectangle([x, y, x + w, y + 4], fill=kcolor)
    tx, ty = x + 16, y + 18
    draw.text((tx, ty), kicker, font=SANS_B(15), fill=kcolor)
    ty += 26
    for ln in fit(draw, headline, SERIF_B(hsize), w - 32, hlines):
        draw.text((tx, ty), ln, font=SERIF_B(hsize), fill=INK)
        ty += hsize + 6
    ty += 4
    for ln in fit(draw, deck, SANS(dsize), w - 32, dlines):
        draw.text((tx, ty), ln, font=SANS(dsize), fill=MUTED)
        ty += dsize + 6


def gulf_art():
    """Lead art: night Gulf sea, missile arcs, tanker silhouette."""
    art = Image.new("RGB", (380, 276), (16, 32, 54))
    d = ImageDraw.Draw(art)
    # sky glow + stars
    for sx, sy, r in [(40, 30, 2), (120, 18, 2), (210, 36, 2), (300, 22, 2),
                      (370, 44, 2), (80, 60, 1), (260, 58, 1), (340, 70, 1)]:
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(220, 220, 200))
    # missile arcs (orange trails)
    for x0, y0, x1, y1 in [(30, 250, 200, 60), (90, 250, 280, 40),
                           (160, 250, 360, 70)]:
        d.arc([x0 - 90, y0 - 190, x1 + 90, y1 + 190], start=200, end=340,
              fill=(255, 140, 40), width=5)
        d.ellipse([x1 - 5, y1 - 5, x1 + 5, y1 + 5], fill=(255, 200, 90))
    # sea
    d.rectangle([0, 210, 380, 276], fill=(10, 42, 66))
    for wx in range(0, 380, 28):
        d.line([wx, 226 + (wx % 3) * 4, wx + 18, 226 + (wx % 3) * 4],
               fill=(70, 130, 160), width=2)
    # tanker silhouette
    d.rectangle([150, 176, 330, 210], fill=(8, 8, 10))
    d.rectangle([180, 156, 210, 176], fill=(8, 8, 10))
    d.rectangle([300, 164, 316, 176], fill=(8, 8, 10))
    d.line([316, 164, 316, 150], fill=(8, 8, 10), width=3)
    # smoke plume
    for cx, cy, r in [(250, 150, 14), (262, 132, 18), (276, 112, 22)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 110, 100))
    return art


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead ---
    d.text((16, 14), "MAKE.FUN  ·  WORLD NEWS IN ONE IMAGE",
           font=SANS_B(15), fill=RED)
    d.text((W - 16 - d.textlength("SUNDAY EDITION", font=SANS_B(15)), 14),
           "SUNDAY EDITION", font=SANS_B(15), fill=MUTED)
    d.text((16, 36), "THE WORLD IN ONE PAGE", font=SERIF_B(58), fill=INK)
    d.text((16, 100), "SUNDAY, 22 NOVEMBER 2026", font=SANS_B(22), fill=INK)
    d.text((W - 16 - d.textlength("SIX STORIES · ONE DAY", font=SANS_B(16)), 104),
           "SIX STORIES · ONE DAY", font=SANS_B(16), fill=MUTED)
    d.line([16, 132, W - 16, 132], fill=INK, width=3)
    d.line([16, 137, W - 16, 137], fill=INK, width=1)

    # --- lead: Gulf ---
    lx, ly, lw, lh = 16, 150, 992, 276
    d.rectangle([lx, ly, lx + lw, ly + lh], outline=RULE, width=2)
    img.paste(gulf_art(), (lx + 2, ly + 2))
    tx = lx + 398
    ty = ly + 14
    d.text((tx, ty), "THE GULF IGNITES", font=SANS_B(16), fill=RED)
    ty += 28
    for ln in fit(d, "Iran hits US base in Kuwait, tankers hit off Oman",
                  SERIF_B(34), lw - 398 - 16, 2):
        d.text((tx, ty), ln, font=SERIF_B(34), fill=INK)
        ty += 40
    ty += 6
    deck = ("Tehran's missiles reach a US air base and Bahrain as the "
            "Gulf attacks widen. Two tankers are hit near Oman and an "
            "ADNOC vessel is attacked in the Strait of Hormuz.")
    for ln in fit(d, deck, SANS(18), lw - 398 - 16, 4):
        d.text((tx, ty), ln, font=SANS(18), fill=MUTED)
        ty += 24

    # --- row 2: two panels ---
    y2, h2 = 442, 196
    draw_panel(d, 16, y2, 488, h2, "WAR SPILLS INTO POLAND", RED,
               "Russian missiles crash in Poland; Kyiv hit by 400 drones",
               "Warsaw calls the border crash a provocation as Moscow "
               "unleashes one of the war's biggest aerial barrages.",
               hsize=25, dsize=16, hlines=2, dlines=3)
    draw_panel(d, 520, y2, 488, h2, "THE BIG THREE MEET", NAVY,
               "Trump hails a 'momentous' summit with Xi and Putin",
               "The Shenzhen trilateral ends with few results. Vance "
               "refuses to back the president's Iran strikes.",
               hsize=25, dsize=16, hlines=2, dlines=3)

    # --- row 3: three panels ---
    y3, h3, w3 = 654, 196, 322
    draw_panel(d, 16, y3, w3, h3, "CLIMATE TALKS STALL", TEAL,
               "COP31 deadlocked over fossil fuels",
               "Negotiators run into overtime with no final deal in sight.",
               hsize=24, dsize=16, hlines=2, dlines=3)
    draw_panel(d, 351, y3, w3, h3, "PERU SHAKEN", GOLD,
               "Magnitude 6.9 quake strikes the Andes",
               "A strong tremor rattles Peru; no casualties reported at first.",
               hsize=24, dsize=16, hlines=2, dlines=3)
    draw_panel(d, 686, y3, w3, h3, "BALTIC ON EDGE", NAVY,
               "Drones hit a Russian cargo ship",
               "Finland tightens security after the attack in the Baltic Sea.",
               hsize=24, dsize=16, hlines=2, dlines=3)

    # --- footer ticker ---
    fy = 866
    d.line([16, fy, W - 16, fy], fill=INK, width=2)
    d.text((16, fy + 12), "ALSO TODAY", font=SANS_B(16), fill=RED)
    ticker = ("'El Chapo Isidro' arrested — 11 killed in Sinaloa violence  ·  "
              "Bolsonaro in ICU  ·  Cyclone Akvan disrupts flights  ·  "
              "Oil down 3% as markets slide  ·  Japan to train with Indian forces")
    for ln in fit(d, ticker, SANS(16), W - 32, 3):
        d.text((16, fy + 38), ln, font=SANS(16), fill=INK)
        fy += 22
    d.line([16, 986, W - 16, 986], fill=RULE, width=1)
    d.text((16, 994), "Drawn from the day's reporting · 22 November 2026",
           font=SANS(13), fill=MUTED)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "JPEG", quality=92)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
