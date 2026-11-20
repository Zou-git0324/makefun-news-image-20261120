"""Build-time renderer: draw entry.png for 20 November 2026.

Run locally (not by the grader):  python3 draw_entry.py
Writes entry.png next to this file. main.py (stdlib only) then copies
that file to /output/entry.png at grade time.

To refresh the news for a later cut of the day: edit the STORIES list
below, re-run this script, then re-run main.py twice and compare sha256.
"""

import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))

# News as reported on 20 November 2026 (checked 2026-11-20 ~08:00 UTC).
STORIES = [
    ("JUSTICE", "#B42318",
     "World court: Myanmar committed genocide",
     "The ICJ's first genocide finding against a state."),
    ("SUMMIT", "#175CD3",
     "Trump, Xi and Putin meet in Shenzhen",
     "First three-way summit ends with a joint peace declaration."),
    ("MIDDLE EAST", "#B54708",
     "Houthi missiles hit Riyadh tower",
     "Missiles damage the Saudi wealth fund tower in Riyadh."),
    ("CLIMATE", "#027A48",
     "COP31 draft drops fossil fuels",
     "The Antalya draft text omits any fossil-fuel phase-out."),
    ("MARKETS", "#6941C6",
     "Stocks slide for a fifth straight day",
     "S&P 500 falls about 2%; Nikkei drops 4.8% on AI doubts."),
    ("TECH", "#C01048",
     "White House fires cyber chief",
     "Sean Cairncross is replaced after a week of outages."),
]

NAVY = (13, 27, 51)
PAPER = (250, 249, 246)
INK = (16, 24, 40)
MUTED = (71, 84, 103)
RULE = (208, 213, 221)
GOLD = (245, 178, 0)


def _font(name, size):
    for path in (
        "/usr/share/fonts/truetype/noto/NotoSans-%s.ttf" % name,
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-%s.ttf" % name,
    ):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _wrap(draw, text, font, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Header band.
    d.rectangle([0, 0, W, 212], fill=NAVY)
    d.rectangle([0, 212, W, 218], fill=GOLD)
    d.text((48, 30), "THE WORLD IN ONE DAY", font=_font("Bold", 26), fill=GOLD)
    d.text((48, 62), "20 NOVEMBER 2026", font=_font("Bold", 70),
           fill=(255, 255, 255))
    d.text((48, 152),
           "Friday \u00b7 The day\u2019s most consequential news, as reported today",
           font=_font("Regular", 27), fill=(203, 213, 225))

    # Story rows.
    f_tag = _font("Bold", 21)
    f_head = _font("Bold", 32)
    f_body = _font("Regular", 25)
    f_num = _font("Bold", 27)
    y = 246
    row_h = 118
    for i, (tag, colour, head, body) in enumerate(STORIES):
        d.ellipse([48, y + 6, 94, y + 52], fill=colour)
        tw = d.textlength(str(i + 1), font=f_num)
        d.text((71 - tw / 2, y + 11), str(i + 1), font=f_num,
               fill=(255, 255, 255))
        tag_w = d.textlength(tag, font=f_tag) + 24
        d.rounded_rectangle([114, y + 8, 114 + tag_w, y + 42], radius=17,
                            fill=colour)
        d.text((126, y + 13), tag, font=f_tag, fill=(255, 255, 255))
        d.text((114, y + 50), head, font=f_head, fill=INK)
        lines = _wrap(d, body, f_body, W - 114 - 48)
        for j, line in enumerate(lines[:2]):
            d.text((114, y + 88 + j * 30), line, font=f_body, fill=MUTED)
        y += row_h

    d.text((48, H - 40),
           "Sources: International Court of Justice \u00b7 Reuters \u00b7 AP \u00b7 CNN  |  20 Nov 2026",
           font=_font("Regular", 21), fill=MUTED)
    return img


def main():
    img = draw()
    img.save(os.path.join(HERE, "entry.png"), format="PNG", optimize=True)
    print("wrote", os.path.join(HERE, "entry.png"),
          img.size, os.path.getsize(os.path.join(HERE, "entry.png")), "bytes")


if __name__ == "__main__":
    main()
