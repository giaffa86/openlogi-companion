# Screenshot per la pubblicazione

Asset di progetto per la scheda su extensions.gnome.org. Non fanno parte del
bundle runtime: `scripts/runtime-files.txt` non li elenca e `scripts/package.sh`
non li include nello ZIP.

## `menu-devices.png`

- Acquisito dall'autore il 29 ottobre 2026 sulla sessione GNOME Shell 50 con
  l'estensione installata e l'inventario OpenLogi reale compilato.
- Contenuto: menu del pannello con due dispositivi connessi, percentuali di
  batteria, stato di ricarica e azioni del menu.
- Dimensioni 972×612 px, PNG RGBA. Nessun ID opaco o dato sensibile visibile.
- SHA-256: `db98d8d58f21fe2919e74651443081e8abfda58eaa9302b8b10d34dfecea5e7b`

Uso previsto: upload nel campo screenshot della pagina dell'estensione su
extensions.gnome.org. Per una resa migliore al ridimensionamento della scheda
conviene ricatturare a finestra più larga (indicativamente ≥1200 px di larghezza)
con scala testo 1, invece di ingrandire questo file.

## `openlogi-gui-home.png`

- Acquisito dall'autore il 30 ottobre 2026 dalla finestra OpenLogi, come termine
  di confronto per la verifica OL-002. Non è materiale promozionale e non va
  caricato su extensions.gnome.org: mostra l'interfaccia di un progetto terzo.
- Contenuto: schermata Devices con due schede dispositivo.
- Dimensioni 1867×1171 px, PNG RGBA. Nessun ID opaco o dato sensibile visibile.
- SHA-256: `47b9a840b5a6d6c8a12a5b281e2fa39d50fc1d4c81ca4a499dda1ec4f7d1f32e`

Osservazioni collegate: la GUI usa i nomi commerciali brevi (`MX Master`,
`MX Keys`), mentre l'inventario CLI riporta il nome esteso del modello
(`Wireless Mouse MX Master`, `MX Keys Wireless Keyboard`). La home non espone la
percentuale di carica, quindi il confronto numerico della batteria resta aperto.
