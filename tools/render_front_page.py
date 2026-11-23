#!/usr/bin/env python3
"""Draws the front page for Monday 23 November 2026 and saves it as entry.png.

Run once on the build machine (needs Pillow and the Noto fonts):
    python3 tools/render_front_page.py
The PNG it writes is committed next to main.ts, which only has to hand it over.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

SIDE = 1024
HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, "..", "entry.png")
FONT_HOME = "/usr/share/fonts/truetype/noto/"

PAPER = (248, 243, 230)
INK = (20, 20, 22)
RED = (196, 36, 28)
SEA = (221, 234, 243)
LAND = (203, 211, 186)
SHORE = (118, 130, 104)
GREY = (92, 92, 96)
GOLD = (214, 164, 40)
WHITE = (255, 255, 255)

DATE_LINE = "MONDAY 23 NOVEMBER 2026"

# number, place label, (lon, lat), headline, icon name
STORIES = [
    (1, "ANTALYA, TÜRKIYE", (30.7, 36.9), "COP31 climate summit ends with no deal", "climate"),
    (2, "BENGHAZI, LIBYA", (20.1, 32.1), "Russian warship sinks after sea-drone strike; UN urges probe", "warship"),
    (3, "WASHINGTON, USA", (-77.0, 38.9), "Democrats win 258 House seats, the most since 1992", "capitol"),
    (4, "STRAIT OF, HORMUZ", (56.4, 26.6), "Tankers struck in Hormuz as attacks on shipping surge", "tanker"),
    (5, "ITURI, DR CONGO", (30.0, 1.6), "Ebola team trapped by fighting; WHO pleads for peace", "ebola"),
    (6, "NEW DELHI, INDIA", (77.2, 28.6), "Nepal PM Balendra Shah holds talks with Modi", "flags"),
    (7, "WELLINGTON, NZ", (174.8, -41.3), "India hunt final-day Test win after record 720-9", "cricket"),
    (8, "ITALY", (12.5, 41.9), "Jeweller Paolo Bulgari dies aged 89", "gem"),
    (9, "SEOUL, SOUTH KOREA", (127.0, 37.5), "Education minister quits over AI exam cheating", "exam"),
]

# Coarse coastlines, (lon, lat) corner by corner. Enough to read as a world map at a glance.
COASTS = [
    # North America
    [(-166, 68), (-156, 71), (-130, 70), (-115, 73), (-95, 74), (-82, 73), (-78, 68), (-64, 60), (-56, 52),
     (-66, 45), (-70, 42), (-75, 36), (-81, 31), (-80, 26), (-83, 29), (-90, 30), (-97, 27), (-97, 20),
     (-91, 18), (-87, 21), (-83, 10), (-78, 8), (-85, 11), (-92, 15), (-105, 20), (-110, 24), (-114, 30),
     (-118, 34), (-124, 41), (-124, 48), (-131, 55), (-140, 60), (-150, 60), (-160, 57), (-166, 62)],
    # Greenland
    [(-45, 60), (-22, 70), (-20, 80), (-40, 83), (-60, 81), (-70, 77), (-55, 70), (-52, 64)],
    # South America
    [(-78, 8), (-72, 12), (-62, 11), (-52, 5), (-50, 0), (-36, -6), (-39, -14), (-41, -22), (-48, -27),
     (-56, -36), (-62, -40), (-66, -47), (-68, -54), (-74, -52), (-74, -42), (-71, -30), (-70, -18),
     (-76, -14), (-81, -5), (-80, 1)],
    # Europe and Asia in one sweep
    [(-9, 37), (-9, 43), (-2, 44), (-4, 48), (2, 51), (8, 54), (9, 57), (5, 59), (5, 62), (13, 67),
     (22, 71), (30, 70), (41, 67), (44, 68), (60, 69), (70, 73), (85, 74), (105, 78), (115, 74),
     (140, 73), (160, 70), (180, 68), (180, 65), (172, 61), (163, 58), (157, 52), (156, 58), (143, 59),
     (135, 54), (141, 48), (132, 43), (128, 38), (127, 35), (122, 39), (118, 38), (121, 31), (120, 25),
     (110, 21), (107, 17), (109, 12), (105, 9), (100, 13), (100, 7), (104, 2), (101, 3), (98, 9),
     (97, 16), (91, 22), (86, 20), (80, 15), (78, 8), (73, 16), (72, 21), (67, 24), (61, 25),
     (59, 22), (55, 17), (45, 13), (43, 13), (39, 21), (35, 28), (35, 32), (36, 36), (30, 36), (27, 37),
     (26, 40), (23, 38), (22, 37), (20, 40), (14, 45), (12, 44), (18, 40), (16, 38), (10, 44), (3, 43),
     (0, 39), (-5, 36)],
    # Africa
    [(-17, 15), (-17, 21), (-10, 29), (-6, 35), (10, 37), (11, 33), (20, 32), (25, 32), (33, 31),
     (35, 28), (37, 21), (43, 12), (51, 12), (48, 5), (41, -2), (39, -8), (40, -15), (35, -24),
     (32, -29), (26, -34), (19, -34), (15, -27), (12, -17), (13, -8), (9, -1), (9, 4), (4, 6),
     (-4, 5), (-8, 4), (-13, 8)],
    # Madagascar
    [(44, -16), (49, -13), (50, -16), (47, -25), (44, -23)],
    # Australia
    [(114, -22), (122, -18), (130, -12), (136, -12), (137, -16), (142, -11), (146, -19), (153, -26),
     (150, -37), (144, -38), (138, -35), (131, -31), (123, -34), (115, -34)],
    # New Zealand, north then south island
    [(173, -35), (178, -38), (175, -41.5), (173, -39)],
    [(172.5, -41), (174, -42), (170, -46.5), (166.5, -45.5)],
    # Japan
    [(130, 32), (135, 34), (140, 35), (142, 40), (141, 45), (145, 44), (141, 41), (139, 38), (133, 35.5)],
    # Britain and Ireland
    [(-5, 50), (1, 51), (0, 54), (-2, 58), (-5, 58), (-3, 54), (-5, 52)],
    [(-10, 52), (-6, 52), (-6, 55), (-10, 54)],
    # Iceland
    [(-24, 65), (-14, 66), (-14, 64), (-22, 63.5)],
    # Sumatra, Borneo, Java, New Guinea
    [(95, 5), (103, 0), (106, -6), (102, -4), (97, 2)],
    [(109, 1), (117, 7), (118, 1), (116, -4), (110, -3)],
    [(106, -6), (114, -7), (114, -8.5), (106, -7.5)],
    [(131, -1), (141, -3), (150, -6), (147, -9), (141, -9), (138, -7), (133, -4)],
    # Sri Lanka
    [(80, 9.5), (82, 7), (80.5, 6)],
]


def face(name, px):
    return ImageFont.truetype(FONT_HOME + name + ".ttf", px)


def width_of(pen, words, font):
    box = pen.textbbox((0, 0), words, font=font)
    return box[2] - box[0]


def shrink_to(pen, words, name, px, limit):
    """Largest size not above px at which the words fit inside limit pixels."""
    font = face(name, px)
    while width_of(pen, words, font) > limit and px > 8:
        px -= 1
        font = face(name, px)
    return font


def break_lines(pen, words, font, limit):
    rows, row = [], ""
    for word in words.split():
        trial = (row + " " + word).strip()
        if width_of(pen, trial, font) <= limit or not row:
            row = trial
        else:
            rows.append(row)
            row = word
    if row:
        rows.append(row)
    return rows


def centred(pen, mid_x, top, words, font, colour):
    pen.text((mid_x - width_of(pen, words, font) / 2, top), words, font=font, fill=colour)


# ---------------------------------------------------------------- masthead

def masthead(pen):
    pen.rectangle([0, 0, SIDE, 104], fill=INK)
    kicker = face("NotoSans-CondensedBold", 21)
    centred(pen, SIDE / 2, 5, "THE WORLD IN ONE DAY  ·  NINE STORIES, ONE FRONT PAGE", kicker, (232, 214, 170))
    big = shrink_to(pen, DATE_LINE, "NotoSansDisplay-CondensedBlack", 84, SIDE - 60)
    centred(pen, SIDE / 2, 20, DATE_LINE, big, WHITE)
    pen.rectangle([0, 104, SIDE, 110], fill=RED)


# ---------------------------------------------------------------- lead story

def lead_story(pen):
    left = 28
    tag = face("NotoSans-CondensedBold", 24)
    pen.ellipse([left, 124, left + 34, 158], fill=RED)
    centred(pen, left + 17, 124, "1", face("NotoSans-CondensedBlack", 25), WHITE)
    pen.text((left + 44, 124), "CLIMATE  ·  ANTALYA, TÜRKIYE", font=tag, fill=RED)
    head = shrink_to(pen, "CLIMATE TALKS", "NotoSerif-CondensedBlack", 86, 640)
    pen.text((left - 2, 146), "CLIMATE TALKS", font=head, fill=INK)
    pen.text((left - 2, 146 + head.size * 0.9), "COLLAPSE", font=head, fill=RED)
    # the deck must clear the map frame below, so it is held to two rows
    deck = face("NotoSerif-CondensedBold", 24)
    rows = break_lines(pen, "COP31 ends with no deal as nations split over fossil fuels. "
                            "UN chief Guterres: \"deeply disappointed\".", deck, 650)
    y = 146 + head.size * 1.8 + 22
    for row in rows[:2]:
        pen.text((left, y), row, font=deck, fill=INK)
        y += 29
    lead_picture(pen, 850, 250)


def lead_picture(pen, cx, cy):
    """A warming globe beside a thermometer, crossed by a NO DEAL stamp."""
    r = 92
    pen.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 176, 214), outline=INK, width=4)
    blobs = [
        [(-70, -40), (-30, -66), (-8, -42), (-22, -8), (-52, 4), (-74, -14)],
        [(-28, 10), (-6, 22), (-12, 62), (-30, 74), (-40, 40)],
        [(8, -60), (52, -66), (74, -30), (60, 6), (30, 18), (20, -14), (2, -30)],
        [(34, 34), (62, 30), (66, 54), (44, 64)],
    ]
    for blob in blobs:
        pen.polygon([(cx + dx, cy + dy) for dx, dy in blob], fill=(128, 160, 96), outline=(60, 86, 50))
    for k in range(3):
        y0 = cy - r - 16 - k * 9
        pen.arc([cx - 56 + k * 16, y0, cx - 16 + k * 16, y0 + 30], 200, 340, fill=RED, width=4)
    # thermometer
    tx = cx - r - 46
    pen.rounded_rectangle([tx - 13, cy - 96, tx + 13, cy + 50], radius=13, fill=WHITE, outline=INK, width=4)
    pen.ellipse([tx - 26, cy + 34, tx + 26, cy + 86], fill=RED, outline=INK, width=4)
    pen.rectangle([tx - 6, cy - 66, tx + 6, cy + 46], fill=RED)
    for k in range(5):
        pen.line([tx + 13, cy - 70 + k * 22, tx + 24, cy - 70 + k * 22], fill=INK, width=3)
    # stamp, drawn on its own layer so it can sit at an angle
    stamp = Image.new("RGBA", (300, 96), (0, 0, 0, 0))
    ink = ImageDraw.Draw(stamp)
    ink.rounded_rectangle([4, 4, 295, 91], radius=12, fill=(255, 255, 255, 235), outline=RED + (255,), width=8)
    word = face("NotoSansDisplay-CondensedBlack", 70)
    box = ink.textbbox((0, 0), "NO DEAL", font=word)
    ink.text(((300 - (box[2] - box[0])) / 2 - box[0], (96 - (box[3] - box[1])) / 2 - box[1]),
             "NO DEAL", font=word, fill=RED + (255,))
    stamp = stamp.rotate(11, resample=Image.BICUBIC, expand=True)
    pen._image.paste(stamp, (int(cx - stamp.width / 2 - 14), int(cy - stamp.height / 2 + 26)), stamp)


# ---------------------------------------------------------------- world map

MAP_BOX = (20, 384, 1004, 712)
LON_SPAN = (-172.0, 184.0)
LAT_SPAN = (79.0, -57.0)


def spot(lon, lat):
    x0, y0, x1, y1 = MAP_BOX
    fx = (lon - LON_SPAN[0]) / (LON_SPAN[1] - LON_SPAN[0])
    fy = (lat - LAT_SPAN[0]) / (LAT_SPAN[1] - LAT_SPAN[0])
    return x0 + fx * (x1 - x0), y0 + fy * (y1 - y0)


def world_map(pen):
    x0, y0, x1, y1 = MAP_BOX
    pen.rectangle(MAP_BOX, fill=SEA)
    for lon in range(-150, 181, 30):
        pen.line([spot(lon, LAT_SPAN[0]), spot(lon, LAT_SPAN[1])], fill=(203, 220, 232), width=1)
    for lat in range(-30, 61, 30):
        pen.line([spot(LON_SPAN[0], lat), spot(LON_SPAN[1], lat)], fill=(203, 220, 232), width=1)
    for coast in COASTS:
        pen.polygon([spot(lon, lat) for lon, lat in coast], fill=LAND, outline=SHORE)
    pen.rectangle(MAP_BOX, outline=INK, width=3)
    label = face("NotoSans-CondensedBold", 19)
    pen.rectangle([x0, y1 - 28, x0 + 322, y1], fill=INK)
    pen.text((x0 + 10, y1 - 27), "WHERE THE DAY'S NEWS HAPPENED", font=label, fill=WHITE)
    # nudges keep the crowded Mediterranean pins apart; a thin leader ties each to its true spot
    nudge = {1: (30, -20), 2: (-22, 26), 8: (-30, -26), 4: (26, 18), 5: (0, 0), 6: (10, -4)}
    digit = face("NotoSans-CondensedBlack", 24)
    for number, _place, (lon, lat), _head, _icon in STORIES:
        px, py = spot(lon, lat)
        dx, dy = nudge.get(number, (0, 0))
        bx, by = px + dx, py + dy
        if dx or dy:
            pen.line([px, py, bx, by], fill=INK, width=2)
            pen.ellipse([px - 4, py - 4, px + 4, py + 4], fill=INK)
        pen.ellipse([bx - 17, by - 17, bx + 17, by + 17], fill=RED, outline=WHITE, width=3)
        centred(pen, bx, by - 17, str(number), digit, WHITE)


# ---------------------------------------------------------------- small pictures

def icon_warship(pen, x, y):
    sea_y = y + 44
    hull = [(x + 4, y + 30), (x + 60, y + 14), (x + 52, y + 40), (x + 14, y + 50)]
    pen.polygon(hull, fill=GREY, outline=INK)
    pen.polygon([(x + 24, y + 22), (x + 40, y + 17), (x + 38, y + 6), (x + 28, y + 9)], fill=GREY, outline=INK)
    pen.line([x + 33, y + 6, x + 31, y - 4], fill=INK, width=2)
    for k in range(4):
        pen.arc([x - 2 + k * 17, sea_y, x + 15 + k * 17, sea_y + 14], 180, 360, fill=(40, 96, 150), width=3)
    burst = [(x + 50, y + 2), (x + 55, y + 10), (x + 64, y + 6), (x + 60, y + 16), (x + 68, y + 22),
             (x + 58, y + 24), (x + 56, y + 32), (x + 50, y + 24), (x + 42, y + 26), (x + 46, y + 16)]
    pen.polygon(burst, fill=(240, 150, 30), outline=RED)


def icon_capitol(pen, x, y):
    pen.rectangle([x + 2, y + 40, x + 66, y + 54], fill=WHITE, outline=INK, width=2)
    pen.rectangle([x + 16, y + 28, x + 52, y + 40], fill=WHITE, outline=INK, width=2)
    pen.pieslice([x + 18, y + 6, x + 50, y + 50], 180, 360, fill=(52, 96, 170), outline=INK, width=2)
    pen.line([x + 34, y + 6, x + 34, y - 3], fill=INK, width=3)
    for k in range(6):
        pen.line([x + 9 + k * 10, y + 42, x + 9 + k * 10, y + 53], fill=INK, width=2)


def icon_tanker(pen, x, y):
    pen.polygon([(x, y + 30), (x + 68, y + 30), (x + 60, y + 46), (x + 8, y + 46)], fill=(150, 56, 40), outline=INK)
    pen.rectangle([x + 46, y + 14, x + 60, y + 30], fill=WHITE, outline=INK, width=2)
    pen.rectangle([x + 8, y + 23, x + 40, y + 30], fill=GREY, outline=INK)
    flame = [(x + 22, y + 22), (x + 14, y + 10), (x + 21, y + 12), (x + 24, y - 2), (x + 32, y + 10),
             (x + 36, y + 5), (x + 36, y + 22)]
    pen.polygon(flame, fill=(240, 150, 30), outline=RED)
    for k in range(4):
        pen.arc([x - 2 + k * 18, y + 44, x + 16 + k * 18, y + 58], 180, 360, fill=(40, 96, 150), width=3)


def icon_ebola(pen, x, y):
    pen.rounded_rectangle([x + 2, y + 4, x + 46, y + 50], radius=6, fill=WHITE, outline=INK, width=2)
    pen.rectangle([x + 19, y + 12, x + 29, y + 42], fill=RED)
    pen.rectangle([x + 9, y + 22, x + 39, y + 32], fill=RED)
    cx, cy = x + 54, y + 38
    for k in range(8):
        a = k * math.pi / 4
        pen.line([cx, cy, cx + 15 * math.cos(a), cy + 15 * math.sin(a)], fill=(70, 120, 60), width=3)
    pen.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=(118, 168, 84), outline=(40, 80, 40), width=2)


def icon_flags(pen, x, y):
    # Nepal: two stacked crimson pennants with a blue edge
    pen.line([x + 4, y, x + 4, y + 56], fill=INK, width=3)
    pen.polygon([(x + 6, y + 2), (x + 30, y + 20), (x + 6, y + 20)], fill=(200, 16, 46), outline=(0, 56, 148))
    pen.polygon([(x + 6, y + 20), (x + 30, y + 42), (x + 6, y + 42)], fill=(200, 16, 46), outline=(0, 56, 148))
    # India: saffron, white, green with the wheel
    pen.line([x + 38, y, x + 38, y + 56], fill=INK, width=3)
    pen.rectangle([x + 40, y + 4, x + 70, y + 14], fill=(255, 153, 51))
    pen.rectangle([x + 40, y + 14, x + 70, y + 24], fill=WHITE)
    pen.rectangle([x + 40, y + 24, x + 70, y + 34], fill=(19, 136, 8))
    pen.rectangle([x + 40, y + 4, x + 70, y + 34], outline=INK)
    pen.ellipse([x + 51, y + 15, x + 59, y + 23], outline=(0, 0, 128), width=2)


def icon_cricket(pen, x, y):
    for k in range(3):
        pen.rectangle([x + 4 + k * 9, y + 10, x + 8 + k * 9, y + 54], fill=(214, 180, 120), outline=INK)
    pen.line([x + 3, y + 9, x + 27, y + 9], fill=INK, width=3)
    pen.polygon([(x + 40, y + 50), (x + 60, y + 14), (x + 68, y + 18), (x + 50, y + 55)], fill=(226, 196, 138),
                outline=INK)
    pen.line([x + 63, y + 15, x + 70, y + 2], fill=INK, width=5)
    pen.ellipse([x + 30, y + 26, x + 44, y + 40], fill=RED, outline=INK)


def icon_gem(pen, x, y):
    pen.ellipse([x + 12, y + 22, x + 56, y + 58], outline=GOLD, width=6)
    top = [(x + 20, y + 10), (x + 28, y), (x + 40, y), (x + 48, y + 10), (x + 34, y + 28)]
    pen.polygon(top, fill=(150, 214, 236), outline=INK)
    pen.line([x + 20, y + 10, x + 48, y + 10], fill=INK, width=1)
    pen.line([x + 28, y, x + 34, y + 28], fill=INK, width=1)
    pen.line([x + 40, y, x + 34, y + 28], fill=INK, width=1)


def icon_exam(pen, x, y):
    pen.rectangle([x + 4, y + 2, x + 44, y + 56], fill=WHITE, outline=INK, width=2)
    for k in range(5):
        pen.line([x + 10, y + 12 + k * 9, x + 38, y + 12 + k * 9], fill=GREY, width=2)
    pen.rounded_rectangle([x + 32, y + 24, x + 70, y + 52], radius=5, fill=INK)
    pen.text((x + 39, y + 23), "AI", font=face("NotoSans-CondensedBlack", 22), fill=WHITE)
    pen.line([x + 6, y + 4, x + 42, y + 54], fill=RED, width=3)


ICONS = {
    "warship": icon_warship, "capitol": icon_capitol, "tanker": icon_tanker, "ebola": icon_ebola,
    "flags": icon_flags, "cricket": icon_cricket, "gem": icon_gem, "exam": icon_exam,
}


# ---------------------------------------------------------------- story cards

def story_cards(pen):
    top, card_w, card_h, gap = 720, 240, 134, 8
    head_font = face("NotoSerif-CondensedBold", 20)
    digit = face("NotoSans-CondensedBlack", 24)
    for slot, (number, place, _where, head, icon) in enumerate(STORIES[1:]):
        col, row = slot % 4, slot // 4
        x = 20 + col * (card_w + gap)
        y = top + row * (card_h + gap)
        pen.rectangle([x, y, x + card_w, y + card_h], fill=WHITE, outline=INK, width=2)
        pen.ellipse([x + 8, y + 8, x + 42, y + 42], fill=RED)
        centred(pen, x + 25, y + 8, str(number), digit, WHITE)
        ICONS[icon](pen, x + 52, y + 6)
        # place name: split at the comma, each half shrunk until it fits beside the icon
        for k, part in enumerate(place.split(", ")):
            place_font = shrink_to(pen, part, "NotoSans-CondensedBold", 19, card_w - 134)
            pen.text((x + 128, y + 9 + k * 22), part, font=place_font, fill=RED)
        for k, part in enumerate(break_lines(pen, head, head_font, card_w - 16)[:3]):
            pen.text((x + 9, y + 60 + k * 22), part, font=head_font, fill=INK)


def footer(pen):
    pen.rectangle([0, 1004, SIDE, SIDE], fill=INK)
    centred(pen, SIDE / 2, 1004, "World news of Monday 23 November 2026, as reported that day by news agencies",
            face("NotoSans-CondensedBold", 15), (232, 214, 170))


def main():
    sheet = Image.new("RGB", (SIDE, SIDE), PAPER)
    pen = ImageDraw.Draw(sheet)
    masthead(pen)
    lead_story(pen)
    world_map(pen)
    story_cards(pen)
    footer(pen)
    sheet.save(TARGET, format="PNG", optimize=True)
    print("wrote", os.path.normpath(TARGET), os.path.getsize(TARGET), "bytes")


if __name__ == "__main__":
    main()
