#!/usr/bin/python3
# SPDX-License-Identifier: GPL-3.0-or-later.
"""Generate the square icon used on the extensions.gnome.org page.

The page renders icons as rounded squares on both light and dark cards, so the
emblem is placed in near-white over an opaque dark plate instead of being
shipped as a transparent black glyph. Run from the repository root:

    python3 scripts/make-ego-icon.py

Output goes to assets/ego/ and is never part of the extension bundle.
"""
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'assets/branding/openlogi-companion-logo.png'
OUTPUT = ROOT / 'assets/ego'
SIZES = (128, 256)
PLATE = (28, 26, 32, 255)
GLYPH = (246, 245, 244, 255)


def emblem() -> Image.Image:
    """White emblem with the original alpha channel, cropped to its bounds."""
    logo = Image.open(SOURCE).convert('RGBA')
    white = Image.new('RGBA', logo.size, GLYPH)
    white.putalpha(logo.getchannel('A'))
    return white.crop(white.getbbox())


def build(size: int, glyph: Image.Image) -> Image.Image:
    canvas = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    radius = round(size * 0.22)
    draw.rounded_rectangle((0, 0, size - 1, size - 1), radius=radius, fill=PLATE)
    target = round(size * 0.66)
    scale = target / max(glyph.size)
    scaled = glyph.resize((round(glyph.width * scale), round(glyph.height * scale)), Image.LANCZOS)
    canvas.alpha_composite(scaled, ((size - scaled.width) // 2, (size - scaled.height) // 2))
    return canvas


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    glyph = emblem()
    for size in SIZES:
        path = OUTPUT / f'icon-{size}.png'
        build(size, glyph).save(path, optimize=True)
        print(f'{path.relative_to(ROOT)} {path.stat().st_size} bytes')


if __name__ == '__main__':
    main()
