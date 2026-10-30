# OpenLogi Companion

- Comunicare in italiano. Progetto indipendente per uso personale, GNOME Shell 50.
- UUID `openlogi-companion@giaffa86`. ESM/GJS, nessuna toolchain Node/TypeScript.
- Provenienza AI documentata in `README.md`, `AI_REVIEW_GUIDELINES.md` e
  `docs/`; i file sorgente e di runtime portano solo l'SPDX
  `GPL-3.0-or-later`. Non reintrodurre avvisi AI nei file distribuiti: le
  review EGO li trattano come indicatori di codice generato. Leggere
  `AI_REVIEW_GUIDELINES.md`.
- `extension.js` collega il lifecycle, `shell/provider.js` possiede i subprocessi,
  `shell/contract.js` valida i dati, `shell/indicator.js` possiede UI e timer.
- GTK/Adw solo in `prefs.js`; St/Clutter/Shell solo nella Shell.
- CLI runtime esclusivamente `['openlogi', 'api', 'devices']`, senza shell.
  Mai usare `openlogi list`, accesso HID, daemon aggiuntivi o IPC interno.
- Timeout 5 s, output condiviso 1 MiB, cancellazione e reaping dei figli posseduti.
  Una richiesta pendente; generazione e identità richiesta proteggono il teardown.
- GSettings contiene solo preferenze UI, mai dispositivi o ID. Pin solo in memoria.
- Nessun `Gio.DBus.session.add_filter`, monkey patch o intercettazione notifiche.
- Verificare con `SHEXLI=/tmp/shexli-venv/bin/shexli ./scripts/verify.sh` e
  `./tests/nested.sh`. Quest’ultimo usa una Shell separata con backend sintetico.
- `scripts/runtime-files.txt` è l’elenco esplicito per sync e ZIP. Non includere
  `gschemas.compiled`, test, prompt, script dev o documentazione locale nel bundle.
- Non installare/ricaricare la sessione host durante i test di build.
- Il click apre la finestra generale: non promettere la pagina del dispositivo.
- Conservare i limiti osservati in `docs/OPEN_ITEMS.md` e `docs/VERIFICATION.md`.
- Git locale autorizzato; creazione del repository remoto, push e release
  rimandati fino alla verifica con dispositivi reali collegati, come da
  `docs/OPEN_ITEMS.md`. Non pubblicare durante la sola preparazione locale.
- Non modificare progetti fratelli, servizi OpenLogi, pacchetti o regole udev.
