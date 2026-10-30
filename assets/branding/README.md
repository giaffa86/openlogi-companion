# Identità visiva OpenLogi Companion

Generata con AI per uso personale il 29 ottobre 2026. GPL-3.0-or-later.
Marchio indipendente: mouse dentro un cerchio aperto. Nessuna affiliazione
con OpenLogi, Logitech o GNOME.

- `openlogi-companion-logo.png`: logo raster trasparente generato con lo
  strumento integrato image_gen; conservato come asset di progetto, fuori dal bundle.
- `../../icons/openlogi-companion-symbolic.svg`: adattamento vettoriale del
  concetto, disegnato con assistenza AI sulla griglia 16×16. Il pannello usa
  questa variante simbolica, ricolorata dal tema GNOME tramite St.Icon.

## Prompt finale del logo

```text
Use case: logo-brand
Asset type: standalone transparent logo for OpenLogi Companion, an independent personal GNOME extension monitoring peripherals and battery.
Primary request: Create one polished minimal original emblem: a clean upright computer mouse silhouette nested inside an open circular ring, with the opening at the upper right. The mouse has a single short wheel mark. Soft precise geometric curves, friendly utilitarian design, strong negative space.
Style/medium: flat vector-like brand mark, one solid near-black ink color, no gradients, no 3D, no texture.
Composition: a single centered emblem with generous transparent margins, square canvas.
Text: none.
Constraints: actual transparent background; original identity, no existing Logitech or GNOME trademarks; avoid tiny details, extra wireless waves, battery symbols, shadows, presentation boards and mockups.
```

## Specifica dell’adattamento simbolico

Conservare mouse, rotella in negativo e cerchio aperto in alto a destra.
Usare un solo colore simbolico, fondo trasparente e geometria SVG a 16×16.
Semplificare il raster per la leggibilità nel pannello, senza scritte o ombre.

**Solo riempimenti, nessun `stroke`.** Il recolouring simbolico della Shell
applica `fill` a tutti i path, quindi un arco tracciato con `stroke` e
`fill="none"` viene riempito e diventa un disco pieno (difetto osservato il
30 ottobre 2026). Il cerchio è perciò un anello come path chiuso con
`fill-rule="evenodd"`, la rotella un foro nello stesso path del mouse.
`tests/check-package.py` rifiuta un’icona simbolica con `stroke` o
`fill="none"`.

