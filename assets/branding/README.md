# OpenLogi Companion visual identity

Generated with AI for personal use on October 29, 2026. GPL-3.0-or-later.
Independent mark: a mouse inside an open circle. No affiliation with OpenLogi,
Logitech or GNOME.

- `openlogi-companion-logo.png`: transparent raster logo generated with the
  built-in image_gen tool; kept as a project asset outside the bundle.
- `../../icons/openlogi-companion-symbolic.svg`: a vector adaptation of the
  concept, drawn with AI assistance on a 16×16 grid. The panel uses this
  symbolic variant, recolored by the GNOME theme through St.Icon.

## Final logo prompt

```text
Use case: logo-brand
Asset type: standalone transparent logo for OpenLogi Companion, an independent personal GNOME extension monitoring peripherals and battery.
Primary request: Create one polished minimal original emblem: a clean upright computer mouse silhouette nested inside an open circular ring, with the opening at the upper right. The mouse has a single short wheel mark. Soft precise geometric curves, friendly utilitarian design, strong negative space.
Style/medium: flat vector-like brand mark, one solid near-black ink color, no gradients, no 3D, no texture.
Composition: a single centered emblem with generous transparent margins, square canvas.
Text: none.
Constraints: actual transparent background; original identity, no existing Logitech or GNOME trademarks; avoid tiny details, extra wireless waves, battery symbols, shadows, presentation boards and mockups.
```

## Symbolic adaptation specification

Keep the mouse, the wheel cutout and the circle opening at the upper right.
Use one symbolic color, a transparent background and SVG geometry on a 16×16
grid. Simplify the raster for panel readability, without text or shadows.

**Fills only, no `stroke`.** Shell symbolic recoloring applies `fill` to every
path, so a stroked arc with `fill="none"` becomes a solid disc, a defect observed
on October 30, 2026. The circle is therefore a ring represented by a closed path
with `fill-rule="evenodd"`; the wheel is a hole in the same path as the mouse.
`tests/check-package.py` rejects a symbolic icon with `stroke` or `fill="none"`.
