# Revisione per uso personale

Riferimenti ufficiali consultati il 28 ottobre 2026:

- https://gjs.guide/extensions/review-guidelines/review-guidelines.html
- https://gjs.guide/extensions/review-guidelines/best-practices.html

Conservare la provenienza AI, ma solo nella documentazione di progetto. I file
sorgente e di runtime portano esclusivamente l’SPDX `GPL-3.0-or-later`: le
[review guidelines](https://gjs.guide/extensions/review-guidelines/review-guidelines.html)
indicano come motivi di rifiuto i «commenti che sembrano prompt LLM o altre
indicazioni di output AI». L’autore resta responsabile della comprensione e della
manutenzione del JavaScript: nessuna submission senza questa revisione.

Lo ZIP non contiene avvisi AI, prompt, note di provenienza o documentazione:
`README.md`, questo file e `docs/` restano nel repository e non nel bundle.
Le precedenti review locali suggeriscono di
verificare API, cleanup e semplicità, non di nascondere la provenienza del codice
al repository.

Controllare prima di ogni consegna:

1. API reali GNOME 50, niente compatibilità speculativa o metodi inventati.
2. Niente flag lifecycle `_enabled`/`_destroyed` o optional call su API garantite.
3. Catch solo ai confini che possono fallire: spawn/letture/wait, JSON, avvio GUI.
   I fallimenti dati hanno codici locali, senza log dei messaggi upstream.
4. Timer rimossi accanto alla sostituzione; cancellabili, segnali e processi
   liberati dal proprietario. Non terminare GUI o agent durante disable.
5. Risposte obsolete invalidate prima della distruzione degli actor.
6. ZIP con elenco esplicito, directory dei moduli conservate, licenza e schema XML.
7. Test GJS e Shell separati dai test hardware reali; limiti dichiarati.

Shexli 0.2.1 sul pacchetto ha dato zero finding, errori e warning. La mancanza di
`manual_review` non evita la revisione umana dei subprocessi: l’unica esecuzione
runtime è la CLI ufficiale in lettura con argv fisso, limiti, timeout e reaping.
Gli argv configurabili nel costruttore del provider servono ai test; non sono
esposti da preferenze o input del menu. Nessun `sh -c` o interpolazione di nomi.
