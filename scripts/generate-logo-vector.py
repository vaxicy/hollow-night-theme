#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hollow Night Theme — vector logo candidates (SVG rendered by headless Chromium).

Halloween marks, but drawn as designed emblems rather than clip-art: each mark
carries a gradient fill, a soft drop shadow and at least one highlight, and every
silhouette sits inside a 24–232 safe box so the export never clips.

Playwright screenshots each SVG cell with omit_background=True (true
transparency); PIL only composes the contact sheets, the inline strip and the
official logo/logo.png exported from SELECTED.

Colours come from manifest.json. Change SELECTED and re-run; never hand-copy PNGs.
"""
import json
import math
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
os.chdir(str(ROOT))                      # relative paths only (non-ASCII path safety)

SIZE = 128
CELL = 512
PREVIEW = 256
SELECTED = "01"
CAND_DIR = Path("logo/candidates")
LOGO_OUT = Path("logo/logo.png")

with open("manifest.json", "r", encoding="utf-8") as f:
    _m = json.load(f)
_C, _P = _m["theme"]["colors"], _m["theme"]["properties"]


def hx(vals):
    return "#%02X%02X%02X" % tuple(vals)


INK = hx(_C["frame"])                              # #1A1226 violet black
TOOLBAR = hx(_C["toolbar"])                        # #2B1C3B
BONE = hx(_C["ntp_background"])                    # #F4EDE4
VIOLET = hx(_C["button_background_secondary"])     # #7B4FA8
PUMPKIN = hx(_C["button_background"])              # #F2792B
DEEP_ORANGE = hx(_C["ntp_link"])                   # #A0401E

SHADOW = """
  <filter id="ds" x="-35%%" y="-35%%" width="170%%" height="170%%">
    <feDropShadow dx="0" dy="5" stdDeviation="6" flood-color="%s" flood-opacity=".24"/>
  </filter>""" % INK


def svg_open(body, defs=""):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
            'viewBox="0 0 256 256">%s%s</svg>' % (CELL, CELL, defs, body))


def star(cx, cy, r_out, r_in, fill, opacity=1.0):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(-90 + i * 36)
        pts.append("%.1f %.1f" % (cx + r * math.cos(a), cy + r * math.sin(a)))
    return '<path d="M%s Z" fill="%s" fill-opacity="%.2f"/>' % (" L".join(pts), fill, opacity)


# ------------------------------------------------------------------ candidates
SVG_01 = svg_open("""
<defs>
  <radialGradient id="pk1" cx="38%%" cy="30%%" r="78%%">
    <stop offset="0" stop-color="#FF9A4A"/>
    <stop offset="0.6" stop-color="%s"/>
    <stop offset="1" stop-color="%s"/>
  </radialGradient>
  %s
</defs>
<g filter="url(#ds)">
  <path d="M128 40 C176 40 202 86 202 130 C202 180 170 216 128 216 C86 216 54 180 54 130
           C54 86 80 40 128 40 Z" fill="url(#pk1)"/>
  <path d="M124 40 h10 v-12 q0 -6 -5 -6 t-5 6 z" fill="%s"/>
  <!-- carved face -->
  <path d="M92 112 L118 112 L105 138 Z" fill="%s"/>
  <path d="M138 112 L164 112 L151 138 Z" fill="%s"/>
  <path d="M86 158 Q104 148 118 158 Q128 150 138 158 Q152 148 170 158 Q162 184 128 184
           Q94 184 86 158 Z" fill="%s"/>
</g>
<ellipse cx="96" cy="96" rx="16" ry="24" fill="#FFFFFF" opacity=".20" transform="rotate(-24 96 96)"/>
""" % (PUMPKIN, DEEP_ORANGE, SHADOW, TOOLBAR, INK, INK, INK))

SVG_02 = svg_open("""
<defs>
  <linearGradient id="mn2" x1="0" y1="0" x2="0.6" y2="1">
    <stop offset="0" stop-color="#FFA55C"/>
    <stop offset="1" stop-color="%s"/>
  </linearGradient>
  %s
</defs>
<circle cx="128" cy="118" r="88" fill="url(#mn2)" filter="url(#ds)"/>
<g fill="%s">
  <path d="M96 216 C96 176 108 152 128 152 C148 152 160 176 160 216 Z"/>
  <circle cx="128" cy="130" r="34"/>
  <path d="M104 106 L98 78 L122 96 Z"/>
  <path d="M152 106 L158 78 L134 96 Z"/>
  <path d="M158 200 C186 196 194 170 180 154 C176 172 168 184 152 190 Z"/>
</g>
<g fill="%s">
  <circle cx="118" cy="126" r="5"/>
  <circle cx="140" cy="126" r="5"/>
</g>
""" % (DEEP_ORANGE, SHADOW, TOOLBAR, PUMPKIN))

SVG_03 = svg_open("""
<defs>%s</defs>
<circle cx="128" cy="128" r="100" fill="%s" filter="url(#ds)"/>
<g fill="%s" transform="translate(128 136) scale(1.28) translate(-128 -136)">
  <ellipse cx="128" cy="140" rx="10" ry="13"/>
  <path d="M119 132 l-3 -11 l9 7 Z"/>
  <path d="M137 132 l3 -11 l-9 7 Z"/>
  <path d="M118 134 C102 118 82 116 66 128 C77 130 82 138 84 148 C93 139 100 139 105 146
           C111 137 116 137 120 143 Z"/>
  <path d="M138 134 C154 118 174 116 190 128 C179 130 174 138 172 148 C163 139 156 139 151 146
           C145 137 140 137 136 143 Z"/>
</g>
<g fill="%s">
  <circle cx="124" cy="136" r="2.8"/>
  <circle cx="132" cy="136" r="2.8"/>
</g>
%s
""" % (SHADOW, VIOLET, INK, PUMPKIN,
       star(58, 62, 10, 4.2, BONE, .9) + star(198, 76, 12, 5.0, BONE, .85)
       + star(184, 46, 7, 3.0, BONE, .7)))

SVG_04 = svg_open("""
<defs>
  <linearGradient id="ht4" x1="0" y1="0" x2="0.5" y2="1">
    <stop offset="0" stop-color="%s"/>
    <stop offset="1" stop-color="%s"/>
  </linearGradient>
  %s
</defs>
<g filter="url(#ds)">
  <!-- tall cone -->
  <path d="M128 38 C140 62 156 104 168 138 H88 C100 104 116 62 128 38 Z" fill="url(#ht4)"/>
  <!-- band + buckle -->
  <path d="M92 128 h72 v14 h-72 z" fill="%s"/>
  <rect x="118" y="127" width="20" height="16" rx="3" fill="none" stroke="%s" stroke-width="5"/>
  <!-- wide curved brim -->
  <path d="M44 146 q26 -18 84 -18 q58 0 84 18 q-28 20 -84 20 q-56 0 -84 -20 Z" fill="%s"/>
  <path d="M44 146 q26 -18 84 -18 q58 0 84 18" fill="none" stroke="#FFFFFF"
        stroke-opacity=".22" stroke-width="3"/>
</g>
%s
%s
""" % (PUMPKIN, DEEP_ORANGE, SHADOW, VIOLET, BONE, VIOLET,
       star(104, 88, 9, 3.8, BONE, .95),
       star(152, 72, 6.5, 2.8, BONE, .8)))

SVG_05 = svg_open("""
<defs>
  <mask id="mn5"><rect width="256" height="256" fill="#000"/>
    <circle cx="106" cy="96" r="70" fill="#fff"/>
    <circle cx="138" cy="72" r="60" fill="#000"/>
  </mask>
  %s
</defs>
<circle cx="106" cy="96" r="70" fill="%s" mask="url(#mn5)"/>
<g fill="%s">
  <!-- bare tree: trunk, branches, ground -->
  <path d="M150 206 C154 178 156 156 154 138 C168 132 180 120 186 106 C172 108 158 118 152 130
           C150 118 146 110 140 102 C140 118 142 130 146 140 C138 134 128 132 120 134
           C132 142 142 150 148 158 C146 178 146 194 148 206 Z"/>
  <path d="M118 206 H192" stroke="%s" stroke-width="10" stroke-linecap="round" fill="none"/>
</g>
%s
""" % (SHADOW, PUMPKIN, TOOLBAR, TOOLBAR,
       star(198, 76, 9, 3.8, VIOLET, .92) + star(180, 50, 6.5, 2.8, VIOLET, .78)))

SVG_06 = svg_open("""
<defs>
  <linearGradient id="cc6" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="%s"/>
    <stop offset="0.34" stop-color="%s"/>
    <stop offset="0.35" stop-color="%s"/>
    <stop offset="0.66" stop-color="%s"/>
    <stop offset="0.67" stop-color="%s"/>
    <stop offset="1" stop-color="%s"/>
  </linearGradient>
  %s
</defs>
<g filter="url(#ds)">
  <path d="M128 42 L196 196 q6 14 -8 14 H68 q-14 0 -8 -14 Z" fill="url(#cc6)"/>
</g>
<path d="M92 152 q36 12 72 0" stroke="#FFFFFF" stroke-opacity=".28" stroke-width="4" fill="none"/>
""" % ("#FFB877", PUMPKIN, BONE, BONE, VIOLET, "#5F3A85", SHADOW))

CANDIDATES = [
    ("01", "lantern-face", "Carved pumpkin — the clearest Halloween read", SVG_01),
    ("02", "cat-moon", "Black cat on a pumpkin moon — quiet and graphic", SVG_02),
    ("03", "bat-badge", "Bat in a violet badge with stars — strongest at 32px", SVG_03),
    ("04", "witch-hat", "Witch hat with a star — iconic silhouette", SVG_04),
    ("05", "moon-tree", "Crescent moon over a bare tree — moodiest", SVG_05),
    ("06", "candy-corn", "Candy corn in the palette's three tones", SVG_06),
]


def font(size, bold=False):
    for name in (("segoeuib.ttf", "seguisb.ttf") if bold else ("segoeui.ttf", "segoeuisl.ttf")):
        p = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", name)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def render_cells():
    cells = "".join('<div id="cell%s" style="width:%dpx;height:%dpx">%s</div>' % (num, CELL, CELL, svg)
                    for num, _n, _d, svg in CANDIDATES)
    html = ('<!doctype html><html><head><meta charset="utf-8"><style>'
            'html,body{margin:0;padding:0;background:transparent}'
            '#grid{display:flex;flex-wrap:wrap;width:%dpx}div[id^=cell]{display:block}'
            '</style></head><body><div id="grid">%s</div></body></html>' % (CELL * 3, cells))
    out = {}
    with sync_playwright() as p:
        try:
            b = p.chromium.launch()
        except Exception:
            # bundled headless shell may be missing after a Playwright update
            b = p.chromium.launch(channel="chrome")
        pg = b.new_page(viewport={"width": CELL * 3, "height": CELL * 2})
        pg.set_content(html)
        for num, name, _d, _svg in CANDIDATES:
            path = CAND_DIR / ("%s-%s.png" % (num, name))
            pg.locator("#cell" + num).screenshot(path=str(path), omit_background=True)
            img = Image.open(path).convert("RGBA").resize((PREVIEW, PREVIEW), Image.LANCZOS)
            img.save(path)
            bbox = img.split()[3].getbbox()
            assert bbox, "candidate %s rendered empty" % name
            assert bbox[0] > 6 and bbox[1] > 6 and bbox[2] < PREVIEW - 6 and bbox[3] < PREVIEW - 6, \
                "candidate %s touches the canvas edge: %s" % (name, bbox)
            out[num] = img
            print("candidate %s %s -> alpha bbox %s" % (num, name, bbox))
        b.close()
    return out


def contact_sheet(rendered, bg, txt, sub, path, title):
    cols, rows = 3, 2
    cw, ch = 384, 374
    gap, margin = 28, 40
    W = margin * 2 + cols * cw + (cols - 1) * gap
    H = margin * 2 + 34 + rows * ch + (rows - 1) * gap
    sheet = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(sheet)
    f_title, f_name, f_desc, f_file = font(24, True), font(21, True), font(15), font(14)
    d.text((margin, margin), title, font=f_title, fill=txt)
    y0 = margin + 34
    for i, (num, name, desc, _svg) in enumerate(CANDIDATES):
        r, c = divmod(i, cols)
        x = margin + c * (cw + gap)
        y = y0 + r * (ch + gap)
        big = rendered[num].resize((220, 220), Image.LANCZOS)
        sheet.paste(big, (x + (cw - 220) // 2, y + 14), big)
        d.text((x + 18, y + 250), "%s · %s" % (num, name), font=f_name, fill=txt)
        d.text((x + 18, y + 280), desc, font=f_desc, fill=sub)
        thumb = rendered[num].resize((32, 32), Image.LANCZOS)
        sheet.paste(thumb, (x + 18, y + 330), thumb)
        d.text((x + 60, y + 339), "%s.png  256x256" % name, font=f_file, fill=sub)
        assert y + 300 <= y + 322, "text block collides with the thumbnail row"
    sheet.save(path)
    print("saved:", path, sheet.size)


def inline_strip(rendered, path):
    n, cell, gap, margin = len(CANDIDATES), 108, 22, 30
    W = margin * 2 + n * cell + (n - 1) * gap
    H = margin * 2 + cell + 30
    strip = Image.new("RGB", (W, H), (244, 237, 228))
    d = ImageDraw.Draw(strip)
    f = font(15, True)
    for i, (num, _n, _d, _s) in enumerate(CANDIDATES):
        x = margin + i * (cell + gap)
        img = rendered[num].resize((cell, cell), Image.LANCZOS)
        strip.paste(img, (x, margin), img)
        d.text((x + cell // 2 - 8, margin + cell + 8), num, font=f, fill=(26, 18, 38))
    strip.save(path)
    print("saved:", path, strip.size)


def main():
    CAND_DIR.mkdir(parents=True, exist_ok=True)
    rendered = render_cells()
    contact_sheet(rendered, (244, 237, 228), (26, 18, 38), (128, 108, 130),
                  CAND_DIR / "contact-light.png", "Hollow Night — vector logo candidates (light)")
    contact_sheet(rendered, (26, 18, 38), (244, 237, 228), (168, 140, 150),
                  CAND_DIR / "contact-dark.png", "Hollow Night — vector logo candidates (dark)")
    inline_strip(rendered, CAND_DIR / "inline-strip.png")
    sel = [c for c in CANDIDATES if c[0] == SELECTED][0]
    icon = rendered[sel[0]].resize((SIZE, SIZE), Image.LANCZOS)
    icon.save(LOGO_OUT)
    print("official icon from SELECTED=%s (%s):" % (sel[0], sel[1]), LOGO_OUT, icon.size)


if __name__ == "__main__":
    main()
