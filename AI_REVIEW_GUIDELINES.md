# Revisione per uso personale

Riferimenti ufficiali consultati il 28 ottobre 2026:

- https://gjs.guide/extensions/review-guidelines/review-guidelines.html
- https://gjs.guide/extensions/review-guidelines/best-practices.html

Conservare l’avviso AI: la manutenzione richiede la comprensione del JavaScript.
Non preparare una submission EGO eliminando soltanto l’avviso. È prevista la
condivisione dei sorgenti sperimentali su GitHub, non una pubblicazione EGO.
Le precedenti review locali suggeriscono di
verificare API, cleanup e semplicità, non di nascondere la provenienza del codice.

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
