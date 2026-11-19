#!/usr/bin/env python3
"""Draw 'Wednesday 18 November 2026' as a one-page newspaper front page.

Original vector-style artwork, drawn from scratch with Pillow. Every story
on the page happened, or was first reported, on Wednesday 18 November 2026.
Output: entry.png, 1024x1024, deterministic (no randomness, no network).
Run: python3 draw_frontpage.py   -> writes entry.png beside this file.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 227)
INK = (17, 17, 17)
RED = (163, 18, 31)
NAVY = (18, 40, 75)
TEAL = (14, 90, 86)
GOLD = (176, 124, 22)
GREY = (90, 86, 76)
LIGHT = (232, 226, 208)
BLUE = (28, 78, 140)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
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


def para(draw, x, y, text, fnt, max_w, leading, fill=INK, max_lines=None):
    lines = wrap(draw, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def headline(draw, x, y, text, size, max_w, leading=None, fill=INK):
    fnt = font(SERIF_B, size)
    leading = leading or int(size * 1.08)
    return para(draw, x, y, text, fnt, max_w, leading, fill=fill)


def kicker(draw, x, y, num, label, color=RED):
    """Numbered story kicker: '1  ASIA - APEC SUMMIT'."""
    fnt = font(SANS_B, 11)
    draw.text((x, y), str(num), font=font(SANS_B, 13), fill=color)
    draw.text((x + 20, y + 1), label, font=fnt, fill=color)
    return y + 16


def rule(draw, x, y, w, fill=INK, width=1):
    draw.line([(x, y), (x + w, y)], fill=fill, width=width)


# ---------------------------------------------------------------- stories
# (n, region, kicker, headline, deck) for the 11 pictured stories.
TOP = [
    (1, "ASIA", "ASIA - APEC SUMMIT",
     "Xi greets Trump on the tarmac in Shenzhen",
     "A rare airport welcome, and an embrace, from China's leader. The first "
     "three-way summit is set for Thursday."),
    (2, "MIDDLE EAST", "MIDDLE EAST - IRAN WAR",
     "Kuwait, Bahrain intercept Iranian drones",
     "Iran says it aimed at US forces after Tuesday's US strike on Qeshm. "
     "The Gulf states report interceptions."),
    (3, "GLOBAL", "GLOBAL - SPACE - SCIENCE",
     "Voyager 1 is one light-day from Earth",
     "NASA's 1977 probe is the first human-made object to get 25.9 billion "
     "km away: a command sent today arrives tomorrow."),
    (4, "EUROPE", "EUROPE - UKRAINE WAR",
     "Russia fires 141 drones at Ukraine",
     "Seven sites are hit overnight; four die in Odesa."),
    (5, "EUROPE", "EUROPE - UKRAINE AID",
     "EU offers Kyiv a \u20ac45bn loan for 2027",
     "It fills two-thirds of a \u20ac70bn gap."),
    (6, "MIDDLE EAST", "MIDDLE EAST - GAZA",
     "Israeli tanks push into central Gaza",
     "First ground push since last year's ceasefire."),
    (7, "AMERICAS", "AMERICAS - MARKETS",
     "Fed minutes point to more rate hikes",
     "A bigger December rise is floated; Dow -1.1%."),
    (8, "AMERICAS", "AMERICAS - US POLITICS",
     "Jeffries wins Democrats' nod for Speaker",
     "Caucus votes 251-11; first Black Speaker."),
    (9, "ASIA", "ASIA - WEATHER",
     "Cyclone Akvan heads for Odisha",
     "Landfall is forecast for Friday; evacuations begin."),
    (10, "GLOBAL", "GLOBAL - CULTURE",
     "GTA VI on sale after a 13-year wait",
     "Midnight launch starts in New Zealand."),
    (11, "GLOBAL", "GLOBAL - CLIMATE",
     "COP31 splits over fossil-fuel phase-out",
     "Ministers in Antalya face a draft deal."),
]

# Briefs 12-44: short, one-line, in "Also on Wednesday 18 November".
BRIEFS = [
    "UK: inflation climbs to 3.6%, a one-year high",
    "Manila: Trump hails a 'very big' trade deal",
    "Japan: Takaichi makes her first China visit as PM",
    "Seoul: Lee seeks Xi's help on North Korea",
    "Dhaka: wage protests shut 55 garment factories",
    "Kemerovo: 19 die as an An-12 crashes in Siberia",
    "Riyadh: coalition says it downed a Houthi missile",
    "Hormuz: Iran says it shot down a US MQ-9 drone",
    "Berlin: Iran defences, F-16 arms pledged to Kyiv",
    "Kosovo: ex-president Thaci is given 17 months",
    "Stockholm: ECDC - Europe off track on superbugs",
    "Turin: Alcaraz beats Medvedev at the ATP Finals",
    "FIFA: France's Diallo to challenge Infantino",
    "Horn: Ethiopia and Eritrea mass troops at border",
    "DR Congo: WHO keeps Ebola a global emergency",
    "Maputo: opposition leader Mondlane goes on trial",
    "Guinea: 224 jailed over illegal gold mining",
    "Mauritius: December Chagos deadline set for UK",
    "Senegal: migrant boat capsizes off the coast",
    "Ottawa: Carney and Xi agree tariff relief",
    "Caracas: Hegseth visits a defence pact",
    "Haiti: Salvadoran troops raze a gang chief's home",
    "Bogota: Colombia's economy shrinks 0.8% in Q3",
    "Brasilia: Senate passes Lula's $10bn package",
    "Mexico: US trade talks 'very far along'",
    "Peru: Tumbes River passes its red-alert level",
    "New York: Anthropic prices its IPO at $83 a share",
    "Australia: sanctions settler leader Daniella Weiss",
    "Sydney: Tame Impala sweeps the ARIA Awards",
    "PNG: magnitude 6.0 quake shakes Port Moresby",
]

TIMELINE = [
    ("OVERNIGHT", "Drones over Kuwait, Bahrain"),
    ("07:00 UTC", "UK inflation: 3.6%"),
    ("MORNING", "Xi greets Trump in Shenzhen"),
    ("10:16 UTC", "Voyager 1: one light-day"),
    ("AFTERNOON", "EU offers Kyiv \u20ac45bn"),
    ("19:00 UTC", "Fed minutes: more hikes"),
]

REGIONS = [
    ("ASIA", 10, (122, 62, 140)),
    ("EUROPE", 8, (28, 78, 140)),
    ("AMERICAS", 9, (176, 32, 32)),
    ("MIDDLE EAST", 6, (176, 124, 22)),
    ("AFRICA", 3, (14, 90, 86)),
    ("OCEANIA", 2, (60, 110, 70)),
    ("GLOBAL", 3, (90, 86, 76)),
]


# ------------------------------------------------------------- illustrations
def draw_skyline(draw, x, y, w, h):
    """Shenzhen tarmac: dusk sky, skyline, runway, plane, three flags."""
    draw.rectangle([x, y, x + w, y + h], fill=(233, 196, 138))
    draw.ellipse([x + w - 52, y + 8, x + w - 14, y + 46], fill=(214, 120, 40))
    # skyline blocks
    for i, (bx, bw, bh) in enumerate([(0, 26, 52), (30, 18, 70), (52, 30, 44),
                                      (86, 16, 62), (106, 24, 38), (134, 20, 58)]):
        draw.rectangle([x + bx, y + h - 34 - bh, x + bx + bw, y + h - 34],
                       fill=(120, 88, 70) if i % 2 else (96, 70, 58))
    draw.rectangle([x, y + h - 34, x + w, y + h - 22], fill=(90, 90, 92))
    draw.line([(x, y + h - 28), (x + w, y + h - 28)], fill=(250, 250, 250), width=2)
    # plane: fuselage, wing, tail
    px, py = x + 14, y + h - 52
    draw.polygon([(px, py), (px + 62, py), (px + 72, py + 7), (px + 62, py + 11),
                  (px, py + 11)], fill=(240, 244, 248))
    draw.polygon([(px + 34, py + 2), (px + 52, py + 2), (px + 46, py + 16),
                  (px + 38, py + 16)], fill=(190, 200, 210))
    draw.polygon([(px + 58, py - 8), (px + 64, py - 8), (px + 64, py + 2),
                  (px + 58, py + 2)], fill=(163, 18, 31))
    # three small flags on poles
    for i, col in enumerate([(178, 32, 32), (214, 120, 40), (28, 78, 140)]):
        fx = x + 128 + i * 26
        draw.line([(fx, y + h - 34), (fx, y + h - 14)], fill=INK, width=2)
        draw.rectangle([fx, y + h - 34, fx + 18, y + h - 24], fill=col)
    draw.rectangle([x, y + h - 22, x + w, y + h], fill=(163, 18, 31))
    draw.text((x + 8, y + h - 19), "SHENZHEN  •  APEC LEADERS' WEEK",
              font=font(SANS_B, 10), fill=(255, 255, 255))


def draw_gulf(draw, x, y, w, h):
    """Simplified Gulf map: sea, Iran / Kuwait / Bahrain, drone tracks."""
    draw.rectangle([x, y, x + w, y + h], fill=(168, 196, 214))
    # land masses
    draw.polygon([(x + 8, y + 6), (x + w - 8, y + 6), (x + w - 8, y + 34),
                  (x + 130, y + 34), (x + 120, y + 62), (x + 8, y + 62)],
                 fill=(222, 200, 150))
    draw.polygon([(x + 8, y + 66), (x + 150, y + 66), (x + 150, y + h - 8),
                  (x + 8, y + h - 8)], fill=(222, 200, 150))
    draw.text((x + 130, y + 10), "IRAN", font=font(SANS_B, 13), fill=INK)
    draw.text((x + 14, y + 44), "KUWAIT", font=font(SANS_B, 11), fill=INK)
    draw.text((x + 96, y + 78), "BAHRAIN", font=font(SANS_B, 10), fill=INK)
    draw.text((x + 150, y + 78), "THE GULF", font=font(SANS_B, 10), fill=NAVY)
    # drone tracks: dashed red arcs Kuwait -> Gulf
    for k in range(6):
        t = k / 5.0
        dx = x + 40 + t * 110
        dy = y + 46 + int(14 * math.sin(t * math.pi)) - 8
        draw.ellipse([dx - 3, dy - 3, dx + 3, dy + 3], fill=RED)
    draw.polygon([(x + 150, y + 44), (x + 162, y + 50), (x + 150, y + 56)],
                 fill=RED)
    draw.rectangle([x, y + h - 22, x + w, y + h], fill=NAVY)
    draw.text((x + 8, y + h - 19), "KUWAIT  •  BAHRAIN  •  IRAN WAR",
              font=font(SANS_B, 10), fill=(255, 255, 255))


def draw_voyager(draw, x, y, w, h):
    """Deep space: Earth, dashed one-light-day line, Voyager probe."""
    draw.rectangle([x, y, x + w, y + h], fill=(10, 16, 38))
    for sx, sy in [(18, 14), (70, 30), (120, 12), (170, 34), (220, 16),
                   (260, 40), (40, 60), (150, 58), (280, 62)]:
        draw.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(255, 255, 255))
    draw.ellipse([x + 12, y + h - 46, x + 52, y + h - 6], fill=(52, 120, 200))
    draw.ellipse([x + 20, y + h - 40, x + 34, y + h - 28], fill=(90, 170, 110))
    draw.text((x + 12, y + h - 62), "EARTH", font=font(SANS_B, 10), fill=(255, 255, 255))
    # dashed line Earth -> probe
    for k in range(12):
        t = k / 11.0
        dx = x + 56 + t * 200
        dy = y + 52 + int(6 * math.sin(t * 3))
        draw.rectangle([dx, dy, dx + 8, dy + 3], fill=(255, 200, 60))
    # probe: dish + body + boom
    px, py = x + w - 52, y + 34
    draw.line([(px, py + 10), (px + 30, py + 10)], fill=(200, 200, 200), width=3)
    draw.ellipse([px + 28, py, px + 48, py + 20], outline=(255, 255, 255), width=2)
    draw.rectangle([px - 14, py + 4, px + 4, py + 16], fill=(180, 180, 190))
    draw.text((x + 60, y + 8), "1 LIGHT-DAY", font=font(SANS_B, 22), fill=(255, 200, 60))
    draw.text((x + 60, y + 34), "25.9 billion km from Earth",
              font=font(SANS, 11), fill=(255, 255, 255))
    draw.rectangle([x, y + h - 22, x + w, y + h], fill=(163, 18, 31))
    draw.text((x + 8, y + h - 19), "INTERSTELLAR SPACE  •  NASA",
              font=font(SANS_B, 10), fill=(255, 255, 255))


def draw_small_icon(draw, x, y, w, h, kind):
    """One small flat illustration per second-row story."""
    if kind == "drones":
        draw.rectangle([x, y, x + w, y + h], fill=(18, 40, 75))
        for k in range(7):
            dx = x + 16 + k * 26
            dy = y + 22 + (10 if k % 2 else -4)
            draw.ellipse([dx - 4, dy - 4, dx + 4, dy + 4], fill=(255, 200, 60))
            draw.line([(dx, dy), (dx + 18, dy + 12)], fill=(255, 255, 255), width=1)
        draw.text((x + 8, y + h - 20), "141 FIRED  •  126 DOWNED",
                  font=font(SANS_B, 10), fill=(255, 255, 255))
    elif kind == "euro":
        draw.rectangle([x, y, x + w, y + h], fill=(28, 78, 140))
        draw.ellipse([x + 14, y + 10, x + 74, y + 56], fill=(255, 200, 60))
        draw.text((x + 26, y + 14), "\u20ac", font=font(SANS_B, 34), fill=NAVY)
        draw.rectangle([x + 84, y + 8, x + w - 10, y + 32], fill=(255, 255, 255))
        draw.text((x + 90, y + 10), "45bn", font=font(SANS_B, 18), fill=NAVY)
    elif kind == "gaza":
        draw.rectangle([x, y, x + w, y + h], fill=(222, 200, 150))
        draw.line([(x + 10, y + h - 26), (x + w - 10, y + h - 26)],
                  fill=(163, 18, 31), width=4)
        draw.rectangle([x + 40, y + 18, x + 130, y + 44], fill=(90, 100, 80))
        draw.rectangle([x + 60, y + 8, x + 90, y + 20], fill=(70, 80, 62))
        draw.line([(x + 90, y + 14), (x + 150, y + 10)], fill=INK, width=3)
        draw.text((x + 8, y + h - 20), "THE YELLOW LINE",
                  font=font(SANS_B, 10), fill=RED)
    elif kind == "fed":
        draw.rectangle([x, y, x + w, y + h], fill=(246, 241, 227))
        draw.rectangle([x + 20, y + 12, x + 80, y + 52], fill=(200, 200, 190))
        for i in range(4):
            draw.line([(x + 28 + i * 12, y + 20), (x + 28 + i * 12, y + 44)],
                      fill=INK, width=3)
        draw.line([(x + 90, y + 44), (x + 140, y + 30), (x + 190, y + 14)],
                  fill=RED, width=4)
        draw.polygon([(x + 178, y + 8), (x + 196, y + 14), (x + 182, y + 22)],
                     fill=RED)
        draw.text((x + 96, y + h - 20), "DOW -1.1%",
                  font=font(SANS_B, 11), fill=RED)
    elif kind == "speaker":
        draw.rectangle([x, y, x + w, y + h], fill=(18, 40, 75))
        draw.polygon([(x + 60, y + 8), (x + 150, y + 8), (x + 168, y + 30),
                      (x + 42, y + 30)], fill=(240, 240, 230))
        draw.rectangle([x + 52, y + 30, x + 158, y + 52], fill=(240, 240, 230))
        for i in range(5):
            draw.rectangle([x + 60 + i * 20, y + 34, x + 68 + i * 20, y + 52],
                           fill=NAVY)
        draw.text((x + 8, y + h - 20), "251-11  •  CAUCUS VOTE",
                  font=font(SANS_B, 10), fill=(255, 255, 255))
    elif kind == "cyclone":
        draw.rectangle([x, y, x + w, y + h], fill=(14, 90, 86))
        cx, cy = x + w // 2, y + h // 2 - 4
        for r in (34, 26, 18, 10):
            draw.arc([cx - r, cy - r, cx + r, cy + r], 20, 300,
                     fill=(255, 255, 255), width=4)
        draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 200, 60))
        draw.text((x + 8, y + h - 20), "LANDFALL FRI 20 NOV",
                  font=font(SANS_B, 10), fill=(255, 255, 255))
    elif kind == "gta":
        draw.rectangle([x, y, x + w, y + h], fill=(90, 30, 110))
        draw.rounded_rectangle([x + 50, y + 10, x + 160, y + 46], radius=12,
                               fill=(30, 30, 40))
        draw.ellipse([x + 62, y + 22, x + 74, y + 34], fill=(255, 255, 255))
        draw.ellipse([x + 136, y + 22, x + 148, y + 34], fill=(255, 200, 60))
        draw.text((x + 8, y + h - 20), "00:00  •  NEW ZEALAND FIRST",
                  font=font(SANS_B, 10), fill=(255, 255, 255))
    elif kind == "cop":
        draw.rectangle([x, y, x + w, y + h], fill=(176, 124, 22))
        draw.ellipse([x + 60, y + 6, x + 150, y + 58], fill=(120, 180, 120))
        draw.arc([x + 70, y + 12, x + 140, y + 52], 0, 360,
                 fill=(255, 255, 255), width=3)
        draw.text((x + 8, y + h - 20), "ANTALYA  •  DRAFT DEAL",
                  font=font(SANS_B, 10), fill=(255, 255, 255))
    # Caption bar at the foot of every small icon: one solid strip, so the
    # label never collides with the drawing above it.
    labels = {
        "drones": "141 FIRED  •  126 DOWNED",
        "euro": "LOAN  •  REPAY AFTER REPARATIONS",
        "gaza": "THE YELLOW LINE",
        "fed": "DOW -1.1%",
        "speaker": "251-11  •  CAUCUS VOTE",
        "cyclone": "LANDFALL FRI 20 NOV",
        "gta": "00:00  •  NEW ZEALAND FIRST",
        "cop": "ANTALYA  •  DRAFT DEAL",
    }
    draw.rectangle([x, y + h - 22, x + w, y + h], fill=(17, 17, 17))
    draw.text((x + 8, y + h - 18), labels[kind], font=font(SANS_B, 10),
              fill=(255, 255, 255))


def draw_map(draw, x, y, w, h):
    """Stylised world map with numbered pins for stories 1-11."""
    draw.rectangle([x, y, x + w, y + h], fill=(214, 228, 232))
    # rough continent blobs (stylised, not to scale)
    blobs = [
        [(14, 26), (70, 14), (96, 30), (78, 62), (30, 66), (10, 46)],   # N America
        [(86, 78), (118, 70), (128, 92), (104, 108), (88, 94)],          # S America
        [(150, 18), (196, 10), (214, 26), (196, 44), (162, 40)],         # Europe
        [(152, 52), (196, 48), (210, 76), (188, 104), (160, 88)],        # Africa
        [(220, 12), (286, 8), (300, 34), (272, 66), (238, 52)],          # Asia
        [(268, 92), (300, 86), (308, 106), (282, 112)],                  # Oceania
    ]
    for b in blobs:
        draw.polygon([(x + bx, y + by) for bx, by in b], fill=(222, 200, 150),
                     outline=(150, 130, 100))
    # Approximate locations: 1 Shenzhen, 2 Kuwait, 4 Ukraine, 5 Brussels,
    # 6 Gaza, 7 Washington, 8 Washington, 9 Odisha, 10 New Zealand, 11 Antalya.
    # 3 is Voyager 1, in deep space, so it has no pin on Earth.
    pins = [(282, 48), (232, 52), (198, 22), (182, 32), (218, 56),
            (40, 35), (56, 46), (262, 62), (305, 105), (202, 44)]
    pin_nums = [1, 2, 4, 5, 6, 7, 8, 9, 10, 11]
    for i, (px, py) in zip(pin_nums, pins):
        draw.ellipse([x + px - 7, y + py - 7, x + px + 7, y + py + 7],
                     fill=RED, outline=(255, 255, 255), width=1)
        draw.text((x + px - 3, y + py - 6), str(i), font=font(SANS_B, 9),
                  fill=(255, 255, 255))
    draw.text((x + 8, y + h - 18),
              "Numbered pins: stories 1, 2, 4-11  •  3 is in space",
              font=font(SANS, 10), fill=GREY)


# ------------------------------------------------------------------- layout
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 18
    # --- top strip
    d.text((mx, 10), "THE WORLD IN ONE DAY  —  ONE PAGE, ONE DATE",
           font=font(SANS_B, 11), fill=RED)
    d.text((W - mx - 300, 10), "41 STORIES  •  7 REGIONS  •  11 DRAWN",
           font=font(SANS_B, 11), fill=NAVY)
    rule(d, mx, 28, W - 2 * mx, width=2)
    # --- masthead: date box + title
    d.rectangle([mx, 36, mx + 84, 106], fill=RED)
    d.text((mx + 10, 40), "NOV", font=font(SANS_B, 15), fill=(255, 255, 255))
    d.text((mx + 8, 58), "18", font=font(SERIF_B, 30), fill=(255, 255, 255))
    d.text((mx + 10, 90), "WED 2026", font=font(SANS_B, 10), fill=(255, 255, 255))
    d.text((mx + 96, 38), "Wednesday 18 November 2026",
           font=font(SERIF_B, 44), fill=INK)
    d.text((mx + 98, 88),
           "Everything on this page happened, or was first reported, on "
           "Wednesday 18 November 2026.",
           font=font(SERIF, 13), fill=GREY)
    rule(d, mx, 112, W - 2 * mx, width=3)
    # --- region bar
    x = mx
    total_w = W - 2 * mx
    for name, count, col in REGIONS:
        seg = int(total_w * count / 41)
        d.rectangle([x, 118, x + seg - 2, 138], fill=col)
        d.text((x + 6, 122), f"{name} {count}", font=font(SANS_B, 11),
               fill=(255, 255, 255))
        x += seg
    # --- timeline strip
    y = 144
    col_w = (W - 2 * mx) // 6
    for i, (when, what) in enumerate(TIMELINE):
        tx = mx + i * col_w
        d.rectangle([tx, y, tx + col_w - 4, y + 30], fill=LIGHT,
                    outline=(180, 170, 145))
        d.text((tx + 6, y + 2), when, font=font(SANS_B, 9), fill=RED)
        d.text((tx + 6, y + 14), what, font=font(SANS, 10), fill=INK)
    # --- top 3 stories
    y = 182
    col_w = (W - 2 * mx - 16) // 3
    illus = [draw_skyline, draw_gulf, draw_voyager]
    for i, story in enumerate(TOP[:3]):
        sx = mx + i * (col_w + 8)
        n, region, kick, head, deck = story
        illus[i](d, sx, y, col_w, 96)
        kicker(d, sx, y + 100, n, kick)
        yy = headline(d, sx, y + 116, head, 22, col_w)
        para(d, sx, yy + 2, deck, font(SERIF, 11), col_w, 14, max_lines=2)
    # --- second row: stories 4-7, then 8-11
    kinds = ["drones", "euro", "gaza", "fed", "speaker", "cyclone", "gta", "cop"]
    col_w2 = (W - 2 * mx - 24) // 4
    for row in range(2):
        ry = 412 + row * 118
        for c in range(4):
            idx = 3 + row * 4 + c
            story = TOP[idx]
            sx = mx + c * (col_w2 + 8)
            n, region, kick, head, deck = story
            draw_small_icon(d, sx, ry, col_w2, 56, kinds[idx - 3])
            kicker(d, sx, ry + 60, n, kick)
            yy = headline(d, sx, ry + 76, head, 14, col_w2, leading=16)
            # No deck in this row: headline + kicker alone keep the
            # grid clean at thumbnail size; the deck lives in the top row.
    # --- bottom: map + briefs
    y = 656
    rule(d, mx, y, W - 2 * mx, width=2)
    d.text((mx, y + 6), "WHERE IT HAPPENED", font=font(SANS_B, 12), fill=RED)
    d.text((mx + 330, y + 6), "ALSO ON WEDNESDAY 18 NOVEMBER",
           font=font(SANS_B, 12), fill=RED)
    draw_map(d, mx, y + 24, 312, 190)
    # briefs in 3 columns
    bx0 = mx + 330
    bcol_w = (W - mx - bx0 - 6) // 3
    per_col = 10
    for ci in range(3):
        bx = bx0 + ci * (bcol_w + 4)
        by = y + 24
        for j in range(per_col):
            k = ci * per_col + j
            if k >= len(BRIEFS):
                break
            num = 12 + k
            d.text((bx, by), str(num), font=font(SANS_B, 10), fill=RED)
            by = para(d, bx + 22, by, BRIEFS[k], font(SANS, 10), bcol_w - 24,
                      12, max_lines=2)
            by += 3
    # --- footer: date check + sources
    fy = 936
    d.rectangle([mx, fy, W - mx, fy + 44], outline=RED, width=2)
    d.text((mx + 8, fy + 4), "DATE CHECK", font=font(SANS_B, 11), fill=RED)
    para(d, mx + 92, fy + 4,
         "Left out, first reported on Tuesday 17 November: Nvidia's results, "
         "the US strike on Qeshm, the Kerch Bridge collapse. Not yet news on "
         "Wednesday: the Trump-Xi-Putin summit (Thu 19 Nov), Cyclone Akvan's "
         "landfall (Fri 20 Nov).",
         font(SANS, 10), W - mx - 100, 12, max_lines=3)
    d.text((mx, fy + 50),
            "All 41 stories happened, or were first reported, on Wed 18 Nov 2026; "
           "each has two or more sources. Claims are attributed. Original drawings.",
           font=font(SANS, 9), fill=GREY)
    d.text((mx, fy + 63),
           "Sources: Reuters  •  AP  •  AFP  •  DW  •  Al Jazeera  •  NPR  •  CBS  •  "
           "ONS  •  IMD  •  NASA  •  Amnesty  •  WHO",
           font=font(SANS, 9), fill=GREY)
    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
