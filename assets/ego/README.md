# Icona per la pagina extensions.gnome.org

Generata con assistenza AI per uso personale. GPL-3.0-or-later.
Marchio originale (mouse in un cerchio aperto), nessuna affiliazione con
OpenLogi, Logitech o GNOME.

- `icon-256.png` (256×256) e `icon-128.png` (128×128): PNG RGBA, piastra scura
  arrotondata con emblema chiaro, così da restare leggibile sia su schede chiare
  sia scure. L'icona trasparente e monocroma non sarebbe visibile su fondo scuro.
- Rigenerazione: `python3 scripts/make-ego-icon.py`, che parte da
  `assets/branding/openlogi-companion-logo.png` e non modifica il logo.

Uso previsto: campo icona del modulo di pubblicazione su extensions.gnome.org.
Questi file non sono nel bundle: `scripts/runtime-files.txt` non li elenca. La
variante usata nella Shell resta `icons/openlogi-companion-symbolic.svg`, che
viene ricolorata dal tema.
