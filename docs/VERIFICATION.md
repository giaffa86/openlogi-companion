# Verifica del 28 ottobre 2026

## Preparazione dei sorgenti per GitHub

Nota aggiornata con assistenza AI per uso personale. Preparazione locale
completata; nessun repository remoto creato e nessun push eseguito.

Successivamente autorizzata la creazione del repository e del primo commit
soltanto in locale. Il passaggio al remoto resta rimandato alla verifica con
dispositivi reali collegati, come registrato in `OPEN_ITEMS.md`. I test sintetici
riportati sotto non soddisfano questa condizione.

- README aggiornato per il progetto sperimentale, con istruzioni dalla radice
  del repository, dipendenze di build/verifica e limiti hardware/API espliciti.
- Rimossi i percorsi personali e i riferimenti a progetti locali dalla
  documentazione destinata alla condivisione. Conservati avvisi AI, licenza,
  risultati storici, prove residue e piano upstream.
- `.gitignore` esclude ZIP, cataloghi compilati, `gschemas.compiled`, ambienti
  Python, cache, configurazioni locali degli agenti e file temporanei.
- Gli script di packaging e sync creano la directory dei cataloghi prima di
  compilarli, così funzionano anche senza una directory `locale/` preesistente.
- Regole di esclusione verificate con Git in una copia temporanea separata:
  31 file sorgente/documentazione selezionati, senza gli artefatti esclusi.
  Da questi soli file, senza `locale/` e `dist/`, `./scripts/package.sh` ha
  rigenerato lo ZIP superando il confronto tra manifest, contenuti e import.

Controlli rieseguiti dopo le modifiche:

```text
SHEXLI=/tmp/shexli-venv/bin/shexli ./scripts/verify.sh
  61 controlli GJS superati; ZIP e traduzioni verificati
  Shexli: 0 finding, 0 errori, 0 warning
./tests/nested.sh
  42 controlli Shell isolati superati; backend sintetico
```

Lo scanner inizialmente mancava: predisposto in un venv sotto `/tmp` con le
versioni fissate documentate sotto. Il sandbox ha impedito il download e il bind
del bus D-Bus del test; download e test Shell sono riusciti con esecuzione
autorizzata fuori dal sandbox, mantenendo bus e dati di test separati dall’host.
Anche questa esecuzione ha prodotto gli avvisi ambientali AT-SPI/PipeWire/Adw già
descritti sotto, senza errori JS del companion nel log della Shell isolata.
Screenshot generati dal runner; nessuna nuova ispezione visiva in questa verifica
documentale. Nessuna installazione o ricarica nella sessione host e nessuna nuova
prova con hardware o GUI OpenLogi reali. Il sync verso la sessione host non è
stato eseguito.

## Ambiente e provenienza

Ricontrollati localmente:

```text
rpm -q openlogi gnome-shell gjs
openlogi-0.8.18-1.x86_64
gnome-shell-50.5-1.fc44.x86_64
gjs-1.88.1-2.fc44.x86_64
openlogi --version → openlogi 0.8.18
```

La Shell headless ha riportato Mutter 50.6. Nessuna altra versione Shell viene
indicata come compatibile. Gli script non aggiornano pacchetti o servizi.

Codice ufficiale scaricato in `/tmp/openlogi-upstream-0818` con:

```bash
git clone --depth 1 --branch v0.8.18 https://github.com/AprilNEA/OpenLogi.git /tmp/openlogi-upstream-0818
git -C /tmp/openlogi-upstream-0818 rev-parse HEAD
```

Tag annotato `v0.8.18`: `9fb08172f1e4ca9f1b83374fe1532cec3580cc69`;
commit effettivo: `d9fd33aca1639c377af25b8fe89ee89c6120f187`.
La rete del sandbox ha inizialmente dato `Could not resolve host: github.com`;
il clone è riuscito con esecuzione autorizzata fuori dal sandbox. Non si è usato
`master` per dedurre il contratto della release installata.

Fonti lette nel clone, riferimenti pubblici della stessa release:

- [USAGE.md, automation API](https://github.com/AprilNEA/OpenLogi/blob/v0.8.18/docs/USAGE.md)
- [Proiezione JSON e codici errore](https://github.com/AprilNEA/OpenLogi/blob/v0.8.18/crates/openlogi-cli/src/cmd/api/output.rs)
- [Comando api devices](https://github.com/AprilNEA/OpenLogi/blob/v0.8.18/crates/openlogi-cli/src/cmd/api.rs)
- [Tipi dispositivo e batteria](https://github.com/AprilNEA/OpenLogi/blob/v0.8.18/crates/openlogi-core/src/device.rs)
- [Launcher Linux](https://github.com/AprilNEA/OpenLogi/blob/v0.8.18/packaging/linux/desktop/openlogi.desktop)
- [Vocabolario deep link](https://github.com/AprilNEA/OpenLogi/blob/v0.8.18/crates/openlogi-core/src/brand.rs)
- [Bootstrap GUI e single instance](https://github.com/AprilNEA/OpenLogi/blob/v0.8.18/crates/openlogi-desktop/src/main.rs)
- [IPC agent](https://github.com/AprilNEA/OpenLogi/blob/v0.8.18/crates/openlogi-ipc/src/lib.rs)

Conferme: envelope schema 1; successo exit 0, errore runtime exit 1 e sintassi
exit 2; `inventory` scanning/ready/unavailable; campi nullable e ID opachi non
persistenti. BatteryLevel critical/low/good/full/unknown e BatteryStatus
charging/charging_slow/discharging/full/error/unknown. Nessuna sottoscrizione
pubblica di inventario o interfaccia D-Bus supportata individuata nei documenti
API e nel relativo codice. L’estensione upstream per finestra attiva non è
un servizio di inventario. Scelta: CLI asincrona, nessun protocollo IPC interno.

Il desktop file installato coincide nei campi consumati con upstream:
`openlogi.desktop`, `Exec=openlogi-desktop`,
`StartupWMClass=org.openlogi.openlogi`. Il WM_CLASS differisce dal nome del file.
Il vocabolario deep link non contiene selezione dispositivo; `on_open_urls` nel
bootstrap non prova la registrazione Linux. Il processo GUI secondario può uscire
per single-instance: non è sufficiente lanciare nuovamente il binario per dare focus.

Consultate il 28 ottobre le [Review Guidelines](https://gjs.guide/extensions/review-guidelines/review-guidelines.html)
e [Best Practices](https://gjs.guide/extensions/review-guidelines/best-practices.html).
Conservato l’avviso AI. La revisione locale ha incluso riferimenti di sviluppo
esterni al repository; nessun modulo o documento privato è incluso nel bundle.
La successiva preparazione dei sorgenti per GitHub non estende la copertura
delle prove né costituisce una submission EGO.

## Inventario reale

Nel sandbox `openlogi api devices` ha restituito exit 1, schema 1,
`agent_unavailable`, con errore IPC `Operation not permitted (os error 1)`.
Questo non dimostra che l’agent sia spento.

La stessa CLI in lettura, autorizzata fuori dal sandbox, ha restituito:

```json
{"schema_version":1,"ok":true,"data":{"inventory":"ready","devices":[]}}
```

Exit 0. L’output è stato sintetizzato prima della stampa per non esporre ID o
nomi hardware. È una prova di comunicazione con l’agent e di inventario vuoto in
quel momento, non una prova di compatibilità o incompatibilità delle periferiche.
Nessun dispositivo reale o stato batteria è stato osservato. Nessun servizio,
configurazione privata, pacchetto o regola udev è stato modificato.

## Controlli indipendenti e provider GJS

Comando riproducibile dalla radice del progetto:

```bash
SHEXLI=/tmp/shexli-venv/bin/shexli ./scripts/verify.sh
```

Il controllo esegue parsing sintattico ESM con Node (senza dipendenze Node),
`bash -n`, validazione JSON, limite 200 colonne JS/CSS, test GJS,
`msgfmt --check`, `glib-compile-schemas --strict --dry-run schemas`, build ZIP,
confronto esatto manifest/contenuti/import relativi e Shexli.
Catalogo italiano controllato anche con estrazione `xgettext` e `msgcmp`:
nessun messaggio UI mancante. Caricamento gettext GJS con `LC_ALL=it_IT.UTF-8`
verificato: `Battery unavailable` diventa `Batteria non disponibile`.
Il syntax check Node non prova le API GJS: queste vengono esercitate nei test
provider e nella Shell isolata.

`gjs -m tests/test.js`: **61 controlli superati** con dati sintetici e figli CLI
Python reali. Copertura:

- Otto dispositivi con ID null/duplicati, nomi uguali/lunghi, 0/100%, livello senza
  percentuale, ricarica lenta, luce senza batteria e offline con lettura precedente.
- Stati scanning/unavailable/ready vuoto e distinzione zero/null.
- JSON vuoto/malformato, envelope invalido, schema sconosciuto, tipi invalidi,
  percentuali fuori intervallo, exit status incoerente.
- CLI assente, agent irraggiungibile, version mismatch, handshake failure,
  timeout API, codice errore ignoto, sintassi CLI incompatibile.
- Output stdout e stderr oltre 1 MiB, timeout finito, drenaggio simultaneo dei due
  stream senza deadlock. Lo stderr non è accumulato in memoria.
- Refresh sovrapposti accorpati nello stesso Promise, cancellazione durante
  teardown, figlio terminato e raccolto (`get_if_signaled`), nuova istanza dopo
  teardown. Timeout e limite rilasciano l’identità della richiesta.

## Shell isolata e preferenze

Comando: `./tests/nested.sh`. Il primo tentativo nel sandbox ha fallito prima
dell’avvio: `Failed to bind socket … Operation not permitted`. Le prove sono
poi riuscite con esecuzione autorizzata fuori dal sandbox, mantenendo l’isolamento.

Il runner crea un bus D-Bus nuovo, XDG_RUNTIME_DIR/DATA_HOME/CONFIG_HOME separati,
backend GSettings keyfile e monitor virtuale 1280×720, quindi avvia:

```bash
gnome-shell --headless --virtual-monitor 1280x720 --debug-control
```

Non inoltra l’indirizzo del bus host. La CLI finta legge soltanto una fixture
sintetica; il launcher OpenLogi è mascherato e poi sostituito da una GUI GTK di
test nella sola directory XDG temporanea. Il helper Eval è locale ai test e
non è presente nel manifest runtime. Lo script arresta e raccoglie il PID della
Shell creata, non cerca processi tramite pattern. Non installa né ricarica
estensioni nella sessione host.

La prima serie completata ha superato **37 controlli**, con:

- Otto righe comprese le duplicate; nessun 84% offline nel dettaglio.
- Menu, focus delle righe e nomi accessibili, larghezza limitata.
- Percentuale 0 e 100, rifiuto ID ambigui/offline, righe riutilizzate a refresh
  immutato, reset della scelta quando il dispositivo scompare.
- Errore reale della CLI finta: snapshot e righe cancellati, retry dopo riapertura
  rapida del menu; nessuna percentuale corrente dopo errore.
- Disable mentre è pendente un figlio ritardato, riferimenti e timer rimossi,
  tre cicli enable/disable/enable e ripristino delle otto righe.
- Preferenza live che crea/rimuove il polling.
- 200 dispositivi, temi prefer-light/prefer-dark, scala testo 1 e 1,5; menu entro
  lo schermo e lista scorrevole in tutte e quattro le combinazioni.
- Apertura e chiusura delle vere preferenze GTK dell’estensione.

Screenshot delle quattro combinazioni acquisiti tramite Screenshot D-Bus della
Shell isolata; ispezionati visivamente chiaro 1,5 e scuro 1. Testo troncato,
scorrimento, contrasto del tema e indicatori di focus osservabili. La finestra di
benvenuto Fedora sullo sfondo appartiene soltanto alla nuova sessione di test.
Scala testo non equivale a scala monitor frazionaria. Nessuna prova con screen
reader o navigazione fisica completa; il bus AT-SPI ha dato `Permission denied`.

La serie estesa del launcher ha inizialmente rilevato la mancata attivazione della
finestra sintetica minimizzata. Correzione: preferire la finestra di `Shell.App`,
poi cercare il WM_CLASS dichiarato dal launcher se il desktop ID è diverso;
attivare la finestra con `Main.activateWindow`. In assenza di finestra, usare
`Shell.App.activate()` per l’avvio. La serie finale estesa ha superato **42 controlli**, inclusi applicazione assente,
avvio da chiusa, finestra già aperta senza duplicati e ripristino da minimizzata,
tutti sulla sola GUI sintetica. Evidenze e screenshot sono stati conservati
nella directory temporanea stampata dal runner (`results.txt`, `shell.log` e PNG);
nessun errore JS del companion nel relativo `shell.log`. Questi artefatti locali
non sono distribuiti con i sorgenti e possono non essere più disponibili.
Non equivale a una prova della GUI OpenLogi reale.

Avvisi ambientali osservati: AT-SPI non avviabile, PipeWire non collegato,
permission store geolocation vuoto, authentication agent indisponibile e warning
GI su Adw.PreferencesWindow. Non equivalgono a errori dell’estensione. I log completi
restano in `/tmp`; non vengono copiati nel progetto o nel pacchetto.

## Pacchetto, licenza e revisione

`scripts/runtime-files.txt` contiene gli undici file runtime esatti. Lo ZIP
conserva `shell/`, schema XML, catalogo `.mo` e LICENSE GPLv3. Confrontati tutti
i byte con i sorgenti e risolti gli import relativi. Esclusi `gschemas.compiled`,
script, test, prompt, documentazione, directory agent e altri dati locali.

Shexli **0.2.1**, tree-sitter **0.25.2**, tree-sitter-javascript **0.25.0**:
**zero finding, zero errori, zero warning**. Nessun crash su questa combinazione;
lo scanner non è stato modificato. Non è stato usato tree-sitter 0.26.0, segnalato
come problematico nei riferimenti locali.

Nessun finding `manual_review` per i subprocessi; valutazione esplicita: il provider
esegue la sola CLI ufficiale con argv fisso e privilegi utente, budget condiviso,
timeout, cancellazione, terminazione e wait non cancellabile. Non esegue input
hardware o nomi dispositivo. I costruttori parametrizzabili servono al backend
sintetico dei test e non sono esposti nelle preferenze.

Non è una certificazione EGO o un audit dell’RPM OpenLogi. La revisione della
manutenibilità resta responsabilità dell’autore prima di qualsiasi pubblicazione.

## Prove residue e comandi utente

Vedere [OPEN_ITEMS.md](OPEN_ITEMS.md) per la selezione pagina dispositivo
**non soddisfatta**, la GUI OpenLogi reale non collaudata e le verifiche hardware.
Per riprodurre controlli in un terminale senza restrizioni sandbox:

```bash
# Dalla radice del repository:
SHEXLI=/tmp/shexli-venv/bin/shexli ./scripts/verify.sh
./tests/nested.sh
openlogi --version
openlogi api devices
```

Se il venv non esiste, predisporlo esplicitamente senza alterare lo scanner:

```bash
python3 -m venv /tmp/shexli-venv
/tmp/shexli-venv/bin/pip install shexli==0.2.1 tree-sitter==0.25.2 tree-sitter-javascript==0.25.0
```

Per test interattivi significativi: `dbus-run-session -- gnome-shell --devkit`
con `mutter-devkit` disponibile, copia del runtime nel relativo XDG isolato e
backend sintetico come nel runner. Non esporre il bus host al devkit.
