#!/usr/bin/env python3
"""Letter in one image — make.fun bounty u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee.

Renders a handwritten-style invitation letter as a single 1024x1024 PNG.
Deterministic: same input always produces byte-identical output
(no timestamps, no randomness, fixed fonts, fixed layout).

Writes /output/entry.png (the harness gate path) and ./entry.png (local copy).
"""
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# Palette — warm paper, ink, terracotta, sage, sunset gold.
PAPER = (247, 239, 222)
PAPER_EDGE = (238, 226, 200)
INK = (46, 42, 38)
INK_SOFT = (96, 84, 70)
RULE = (74, 55, 40)
GOLD = (214, 164, 65)
TERRA = (196, 94, 58)
SAGE = (111, 143, 96)
SAGE_DARK = (84, 116, 72)
SKY_TOP = (250, 214, 158)
SKY_BOT = (247, 178, 116)
SUN = (232, 126, 58)
HOUSE_WALL = (250, 240, 214)
HOUSE_ROOF = (178, 74, 48)
WINDOW_LIT = (255, 196, 92)
GROUND = (139, 166, 110)
TEAL = (31, 78, 84)

SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF_ITALIC = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def draw_sky(draw, box):
    """Vertical sunset gradient, deterministic."""
    x0, y0, x1, y1 = box
    steps = y1 - y0
    for i in range(steps):
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=lerp(SKY_TOP, SKY_BOT, i / max(steps - 1, 1)))


def draw_scene(draw):
    """Flat illustration band: house, mango tree, setting sun, cat on the fence."""
    x0, y0, x1, y1 = 72, 124, 952, 336
    draw.rounded_rectangle([x0, y0, x1, y1], radius=18, outline=RULE, width=3)
    # Clip the scene to the rounded frame by drawing inside an inset box.
    draw_sky(draw, (x0 + 3, y0 + 3, x1 - 3, y1 - 3))
    # Sun, low on the horizon, left of centre.
    draw.ellipse([150, 178, 238, 266], fill=SUN)
    draw.ellipse([162, 190, 226, 254], fill=(240, 150, 84))
    # Distant hills (kept above the ground line so nothing pokes past the frame).
    draw.ellipse([560, 268, 950, 320], fill=(214, 158, 96))
    draw.ellipse([72, 288, 420, 320], fill=(222, 168, 104))
    # Ground.
    draw.rectangle([x0 + 3, 318, x1 - 3, y1 - 3], fill=GROUND)
    # Mango tree, right side.
    draw.rectangle([838, 218, 856, 320], fill=(96, 66, 44))
    draw.ellipse([782, 158, 912, 252], fill=SAGE)
    draw.ellipse([806, 138, 888, 210], fill=SAGE_DARK)
    for mx, my in [(812, 210), (856, 228), (884, 196), (830, 238)]:
        draw.ellipse([mx, my, mx + 12, my + 12], fill=(232, 126, 58))
    # House, centre-left.
    hx, hy = 330, 218  # roof peak base
    draw.polygon([(hx - 110, hy + 40), (hx, hy - 52), (hx + 110, hy + 40)], fill=HOUSE_ROOF)
    draw.rectangle([hx - 92, hy + 40, hx + 92, 318], fill=HOUSE_WALL)
    draw.rectangle([hx - 92, hy + 40, hx + 92, 318], outline=RULE, width=2)
    # Door.
    draw.rectangle([hx - 18, 258, hx + 18, 318], fill=(120, 72, 44))
    draw.ellipse([hx + 8, 288, hx + 13, 293], fill=GOLD)
    # Windows, warmly lit.
    for wx in (hx - 74, hx + 44):
        draw.rectangle([wx, 252, wx + 30, 282], fill=WINDOW_LIT, outline=RULE, width=2)
        draw.line([(wx + 15, 252), (wx + 15, 282)], fill=RULE, width=2)
        draw.line([(wx, 267), (wx + 30, 267)], fill=RULE, width=2)
    # Chimney with two puffs of smoke.
    draw.rectangle([hx + 58, hy - 44, hx + 76, hy + 6], fill=(150, 96, 72))
    draw.ellipse([hx + 52, hy - 66, hx + 74, hy - 44], fill=(255, 250, 238))
    draw.ellipse([hx + 62, hy - 86, hx + 84, hy - 64], fill=(255, 250, 238))
    # Fence with the cat, bottom left.
    for fx in range(96, 300, 34):
        draw.rectangle([fx, 292, fx + 8, 320], fill=(120, 88, 58))
    draw.rectangle([92, 300, 300, 308], fill=(120, 88, 58))
    # Cat silhouette sitting on the fence.
    draw.ellipse([150, 268, 182, 302], fill=INK)          # body
    draw.ellipse([156, 250, 178, 272], fill=INK)          # head
    draw.polygon([(158, 254), (162, 242), (167, 253)], fill=INK)  # ear L
    draw.polygon([(170, 253), (175, 242), (179, 254)], fill=INK)  # ear R
    draw.arc([182, 282, 206, 306], 300, 60, fill=INK, width=5)    # tail


def draw_spaced(draw, cx, y, text, fnt, fill, spacing=8):
    """Draw centred text with letter spacing."""
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + spacing * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + spacing


def wrap_paragraph(draw, text, fnt, max_width):
    """Greedy word wrap on pixel width; returns list of lines."""
    lines = []
    for raw in text.split("\n"):
        if not raw.strip():
            lines.append("")
            continue
        words = raw.split()
        cur = ""
        for word in words:
            trial = (cur + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= max_width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines


LETTER = [
    ("Dear Judge,", False),
    ("I know you spend all day reading invitations and deciding which ones win. "
     "So let me be clear: this letter has no score attached. Nobody here is keeping count.", False),
    ("My house is small and the roof leaks \u2014 "
     "but it has the best window seat in the neighbourhood: mango tree, "
     "afternoon rain, and the neighbour's cat.", False),
    ("Come and sit in it. No prompts, no pairings, no margins from one to five. "
     "You don't have to judge anything here \u2014 unless you want to. "
     "The sunset is at six, and it has never once asked for a verdict.", False),
    ("There will be tea. There will be fried bananas. "
     "There will be a chair that is already yours.", False),
    ("You can't literally visit, I know. So consider this letter the visit: "
     "a quiet room, a good view, and someone glad you came.", False),
    ("Warmly,\nThe human at the end of the lane", False),
    ("P.S. The cat has already decided you are welcome. It never decides that.", True),
]

RSVP = "RSVP \u2014 just come. The door is open, the kettle is on."


def render():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # Paper edge + double frame.
    draw.rectangle([14, 14, W - 15, H - 15], outline=RULE, width=3)
    draw.rectangle([26, 26, W - 27, H - 27], outline=RULE, width=1)

    # Header.
    draw_spaced(draw, W // 2, 52, "AN INVITATION", font(SANS_BOLD, 30), RULE, spacing=10)
    draw.line([(392, 100), (632, 100)], fill=GOLD, width=3)
    draw.ellipse([508, 94, 516, 102], fill=GOLD)

    # Illustration.
    draw_scene(draw)

    # Letter body — auto-fit: shrink until it fits the allotted height.
    body_top, body_bottom = 360, 884
    margin_x = 80
    max_w = W - 2 * margin_x
    size = 25
    while size >= 21:
        fnt = font(SERIF, size)
        fnt_i = font(SERIF_ITALIC, size)
        leading = int(size * 1.34)
        para_gap = int(size * 0.46)
        lines = []
        for text, italic in LETTER:
            pf = fnt_i if italic else fnt
            wrapped = wrap_paragraph(draw, text, pf, max_w)
            lines.append((wrapped, pf))
        total_h = sum(len(w) * leading for w, _ in lines) + para_gap * (len(lines) - 1)
        if total_h <= body_bottom - body_top:
            break
        size -= 1

    y = body_top
    for wrapped, pf in lines:
        for line in wrapped:
            if line:
                draw.text((margin_x, y), line, font=pf, fill=INK)
            y += leading
        y += para_gap

    # RSVP line, centred, italic, with rules.
    y = 898
    draw.line([(120, y + 14), (300, y + 14)], fill=GOLD, width=2)
    draw.line([(724, y + 14), (904, y + 14)], fill=GOLD, width=2)
    rf = font(SERIF_ITALIC, 24)
    tw = draw.textlength(RSVP, font=rf)
    draw.text(((W - tw) / 2, y), RSVP, font=rf, fill=INK_SOFT)

    # make.fun wordmark pill, bottom centre — readable at 300px.
    pill_w, pill_h = 196, 46
    px0, py0 = (W - pill_w) // 2, 936
    draw.rounded_rectangle([px0, py0, px0 + pill_w, py0 + pill_h], radius=23, fill=TEAL)
    mf = font(SANS_BOLD, 30)
    mtw = draw.textlength("make.fun", font=mf)
    draw.text(((W - mtw) / 2, py0 + 7), "make.fun", font=mf, fill=(255, 255, 255))

    return img


def main():
    img = render()
    img.save("/tmp/entry-render-check.png")
    out_gate = "/output/entry.png"
    os.makedirs("/output", exist_ok=True)
    img.save(out_gate)
    here = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(here)
    print(f"wrote {out_gate} and {here}: {img.size}, {os.path.getsize(here)} bytes")


if __name__ == "__main__":
    main()
