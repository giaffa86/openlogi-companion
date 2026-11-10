# Verifiche locali

## Autorizzazione alla sincronizzazione GitHub — 10 novembre 2026

Nota aggiornata con assistenza AI. Dopo la creazione da parte dell’autore del
repository pubblico `https://github.com/giaffa86/openlogi-companion.git`,
l’autore ha chiesto esplicitamente di sincronizzarlo con il progetto locale.
Il connettore GitHub ha confermato repository accessibile, permessi di push e
assenza di branch prima del primo invio. La richiesta autorizza commit e push
dei sorgenti e supera il rinvio al remoto annotato nelle sezioni storiche.

Aggiornati README, `AGENTS.md` e `OPEN_ITEMS.md` per distinguere questo passaggio
dalle release e dalla submission EGO, ancora subordinate alle verifiche residue.
Il controllo dell’estensione resta quello dell’ultima modifica: 64 controlli GJS,
14 dello script di sessione, 94 Shell isolati e Shexli pulito. Questa
sincronizzazione non aggiunge prove hardware né installa o ricarica la sessione
host. ZIP e file generati, note private e configurazioni locali restano esclusi
dal repository tramite `.gitignore`; il bundle runtime mantiene il manifest
esplicito.

## Righe dispositivo di sola consultazione — 10 novembre 2026

Modifica realizzata con assistenza AI su richiesta dell’autore: disabilitare il
click sulle periferiche, fuorviante finché non esiste apertura contestuale.

- `DeviceRow` non riceve più un callback di apertura e non collega `activate`.
  La riga usa `reactive: false` e `can_focus: false`: il componente GNOME
  disabilita anche gesto di click e hover. Le puntine conservano reattività e
  focus, senza rendere inattivi i controlli figli.
- Il testo accessibile della riga descrive dispositivo e stato. Ogni puntina
  annuncia anche nome e batteria della propria periferica, per conservare il
  contesto quando il focus arriva direttamente al pulsante.
- L’apertura generale resta nell’azione **Mostra la finestra di OpenLogi**.
  Aggiornati messaggio del menu, metadati, README e catalogo italiano (40 messaggi).
- Promemoria persistente in `AGENTS.md` e OL-001 di `OPEN_ITEMS.md`: ricontrollare
  prossime release e issue upstream #1375; considerare un contributo alla
  richiesta esistente prima di aprirne una nuova. Nessun invio su GitHub.

Verifiche eseguite:

- `SHEXLI=/tmp/shexli-venv/bin/shexli ./scripts/verify.sh`: 64 controlli GJS,
  14 dello script di sessione, ZIP corrispondente al manifest, catalogo italiano
  e template allineati su 40 messaggi; Shexli senza finding, errori o warning.
- `./tests/nested.sh`: **94 controlli** Shell superati con backend sintetico.
  Verificati righe non reattive, focus e hover disabilitati, gesti di click
  inattivi, nomi accessibili delle puntine e focus sui pulsanti nei quattro
  casi tema chiaro/scuro e scala testo 1/1,5. Restano superate le prove di
  puntine multiple, tacche e avvio/attivazione della GUI sintetica.
- Evidenze in `/tmp/openlogi-nested-5tPXlH`; nessun errore JavaScript o di parsing
  del tema nel log Shell. Ispezionato il menu chiaro a scala 1,5 della serie
  precedente (`/tmp/openlogi-nested-YYR5Gi`): righe prive di highlight, testo
  informativo e puntina con focus visibile; l’ultima serie aggiunge solo il
  contesto nei nomi accessibili dei pulsanti.
- Pacchetto aggiornato in
  `dist/openlogi-companion@giaffa86.shell-extension.zip`, con sole risorse runtime
  previste dal manifest. Nessun test, documento locale o schema compilato.

Nessuna installazione o ricarica della sessione host e nessuna pubblicazione.
Le verifiche hardware, screen reader e DPI reali restano quelle ancora aperte in
`OPEN_ITEMS.md`.

## Apertura contestuale, controllo OpenLogi 0.9.0 — 10 novembre 2026

Verifica aggiornata con assistenza AI su richiesta dell’autore. La versione
locale è `openlogi 0.9.0`, RPM `openlogi-0.9.0-1.x86_64`. Consultati i sorgenti
ufficiali fissati al tag v0.9.0, non dedotti dal ramo di sviluppo:

- [Release v0.9.0](https://github.com/AprilNEA/OpenLogi/releases/tag/v0.9.0),
  pubblicata il 3 novembre 2026, commit indicato `a5b507e`.
- [`brand.rs`](https://github.com/AprilNEA/OpenLogi/blob/v0.9.0/crates/openlogi-core/src/brand.rs):
  `DeeplinkCommand` offre soltanto Show, OpenSettings, OpenAbout, CheckForUpdates
  e Quit. Non contiene un identificatore o comando per selezionare il device;
  `parse_url` ignora path e query, quindi `show?device=…` rimane un semplice Show.
- [`main.rs`](https://github.com/AprilNEA/OpenLogi/blob/v0.9.0/crates/openlogi-desktop/src/main.rs):
  guardia single-instance con uscita se la GUI è già attiva, senza inoltro di
  URL; nessun parsing di argomenti per aprire una periferica.
- [`openlogi.desktop`](https://github.com/AprilNEA/OpenLogi/blob/v0.9.0/packaging/linux/desktop/openlogi.desktop):
  `Exec=openlogi-desktop`, nessun `%u`, MIME handler o azione per dispositivo.
  Confermato anche leggendo il launcher installato in `/usr/share/applications`.
- [Documentazione CLI](https://github.com/AprilNEA/OpenLogi/blob/v0.9.0/docs/USAGE.md):
  non documenta navigazione nella GUI per dispositivo. I selettori delle API
  hardware non costituiscono un’azione di navigazione.
- [Issue #1375](https://github.com/AprilNEA/OpenLogi/issues/1375): richiesta
  equivalente già aperta; stato e commento letti tramite il connettore GitHub.
  Nessuna issue, PR o risposta inviata.

Esito: la v0.9.0 non aggiunge l’apertura contestuale richiesta. Il companion
continua ad aprire la finestra generale. Aggiornati OL-001 e il punto 3 della
checklist in `OPEN_ITEMS.md`; prima di proporre un’API va considerata la richiesta
upstream esistente.

Solo verifica documentale e letture locali di versione, RPM e desktop file:
nessuna esecuzione di diagnostiche hardware, modifica a OpenLogi o attivazione
della GUI. Le prove reali residue di OL-002 restano aperte. Nessuna modifica al
runtime del companion o allo ZIP già creato; non occorre ripetere i test runtime
per questo aggiornamento documentale.

## Tacche batteria e puntine multiple — 10 novembre 2026

Modifica realizzata con assistenza AI per uso personale, su richiesta dell’autore
con riferimento visivo di tastiera e mouse affiancati nel pannello.

- Le puntine diventano scelte indipendenti in un `Set` in memoria, in ordine di
  selezione. Ogni dispositivo ha la propria icona e lettura; nessuna media o
  persistenza degli ID. Rimuovere una puntina non modifica le altre.
- La chiave UI `battery-bar`, booleana e predefinita a `false`, alterna le
  percentuali con tacche verticali proporzionali. Le preferenze esistenti
  `show-percentage` e `hide-logo` sono conservate; testo e catalogo italiano
  aggiornati per più dispositivi (41 messaggi).
- Tacca verde sopra il 20%, ambra fino al 20%, rossa fino al 10%. Lo 0% è una
  traccia vuota; una lettura assente non produce una tacca. Livelli qualitativi
  e stato di carica restano nel dettaglio e nei nomi accessibili, senza inventare
  percentuali. Un dispositivo in carica senza lettura mantiene la sua icona.
- Gli actor del pannello vengono riusati durante refresh e cambio modalità,
  distrutti alla rimozione e liberati al teardown. Scomparsa, disconnessione,
  ID ambiguo o perdita del supporto batteria rimuovono solo la puntina coinvolta;
  errore, scansione o disabilitazione azzerano tutte le scelte.
- Il runner disattiva la finestra di benvenuto soltanto nel suo profilo
  GSettings temporaneo, così non oscura le acquisizioni grafiche.

Verifiche eseguite:

- `SHEXLI=/tmp/shexli-venv/bin/shexli ./scripts/verify.sh`: 64 controlli GJS,
  14 controlli dello script di sessione, ZIP dal manifest esplicito, traduzioni e
  template allineati; Shexli 0.2.1 con tree-sitter 0.25.2/0.25.0 senza finding,
  errori o warning. Scanner installato soltanto nel venv temporaneo `/tmp`.
- `./tests/nested.sh`: **92 controlli** Shell superati con backend sintetico.
  Coperti tre pin simultanei, rimozione indipendente, ordine, riuso degli actor,
  cambio live numero/tacca, zero e lettura assente, barra piena e proporzionale,
  soglie colore, ripristino dopo occultamento, perdita selettiva di dispositivi
  assenti/offline/ambigui e cleanup con due puntine attive. Tacche visibili anche
  nei temi chiaro/scuro a scala testo 1 e 1,5.
- Evidenze finali in `/tmp/openlogi-nested-PJR4Q7`; ispezionati visivamente il
  pannello con tastiera e mouse e le preferenze. Nessun errore JavaScript o di
  parsing del tema nel log Shell; restano gli avvisi ambientali AT-SPI/PipeWire/
  Adw già osservati. Il primo avvio nel sandbox non poteva creare il socket
  D-Bus; il runner è riuscito con esecuzione autorizzata mantenendo bus e profilo
  separati dalla sessione host.

Nessuna installazione o ricarica nella sessione host, né pubblicazione remota.
La nuova modalità e i pin multipli non sono stati provati con dispositivi reali.
Restano i limiti di `OPEN_ITEMS.md`, inclusi avvio/ripristino della GUI reale,
lettore di schermo, DPI frazionari e multi-monitor.

## Preferenza per nascondere il marchio nel pannello — 31 ottobre 2026

Modifica realizzata con assistenza AI per uso personale, su richiesta
dell’autore: poter nascondere il logo dell’estensione nella barra superiore
quando un dispositivo è fissato.

- Nuova chiave GSettings `hide-logo` (booleana, default `false`), additiva e
  indipendente da `show-percentage`; nessun dato di dispositivo viene salvato.
- `prefs.js` aggiunge una seconda `Adw.SwitchRow` legata con
  `Gio.SettingsBindFlags.DEFAULT`, quindi nessun segnale GTK da disconnettere a
  mano.
- `shell/indicator.js` conserva il riferimento all’icona del marchio
  (`this._logo`), azzerato in `destroy()`. Il marchio viene nascosto solo se il
  dispositivo fissato è **effettivamente mostrato** nel pannello: altrimenti il
  pulsante resterebbe vuoto. Il pulsante continua a esporre un nome accessibile
  con nome del dispositivo e percentuale.
- Il segnale delle preferenze passa da `changed::show-percentage` a `changed`,
  così entrambe le chiavi aggiornano pannello e timer con un solo handler.
- Traduzione italiana portata a 39 messaggi; template rigenerato.

Verifiche eseguite:

- `SHEXLI=/tmp/shexli-venv/bin/shexli ./scripts/verify.sh` superato: sintassi,
  limiti di riga, 64 controlli GJS, 14 dello script di sessione, ZIP dal
  manifest, catalogo italiano caricato, template allineato su 39 messaggi e
  Shexli 0.2.1 con tree-sitter 0.25.2/0.25.0 senza finding, errori o warning
  (venv ricreato in `/tmp` con le versioni fissate).
- `./tests/nested.sh`: **63 controlli** Shell (erano 56). Nuovi: marchio
  nascosto con dispositivo fissato e mostrato, nome accessibile invariato,
  logo ripristinato disattivando la preferenza, applicazione della modifica
  senza refresh manuale, logo sempre presente con ID ambiguo, dispositivo
  offline e `show-percentage` disattivato.
- Evidenze in `/tmp/openlogi-nested-0k0qDv`: `pinned-percentage.png` (marchio +
  icona tastiera + `0%`) e `pinned-no-logo.png` (icona tastiera + `100%`, senza
  marchio), ritagli del pannello ispezionati.
- Nessuna installazione o ricarica nella sessione host.

Restano aperti i punti di `OPEN_ITEMS.md`, invariati: confronto numerico della
batteria con la GUI, click con app chiusa/minimizzata, raggruppamento finestra,
accessibilità con lettore di schermo e DPI/multi-monitor. La nuova preferenza non
è stata provata con dispositivi reali collegati.

## Correzioni della review dello script di sessione — 30 ottobre 2026

Correzioni realizzate con assistenza AI dopo la revisione dei commit locali:

- lettura centralizzata dello stato con `LC_ALL=C LANGUAGE=C`, confrontando
  `ACTIVE`/`INACTIVE` invece di `ENABLED`;
- risposte JSON non leggibili, envelope senza successo, schema incompatibile o
  inventario senza una lista di dispositivi producono `FAIL`, senza conteggio `?`;
- il teardown controlla sia l'esito di `disable` sia lo stato `INACTIVE` prima
  della ricerca dei processi; tenta poi il ripristino e verifica `ACTIVE`.
  Anche gli errori di riabilitazione producono `FAIL`.

`tests/test-session-check.sh`, incluso in `scripts/verify.sh`, copre 14 casi con
comandi simulati, senza contattare la Shell host o la CLI reale. Lo script di
sessione viene caricato solo per le sue funzioni. Queste prove non chiudono i
limiti hardware e di sessione reale elencati in `OPEN_ITEMS.md`.

Verifiche eseguite: `SHEXLI=/tmp/shexli-venv/bin/shexli ./scripts/verify.sh`
superato (64 controlli GJS, 14 dello script, ZIP e traduzioni; Shexli senza
finding, errori o warning). `./tests/nested.sh`: 56 controlli Shell superati,
backend sintetico; evidenze in `/tmp/openlogi-nested-nas5FZ`, avvisi ambientali
AT-SPI/PipeWire/Adw già noti. Nessuna installazione o ricarica nella sessione host.

## Script di sessione e stato dell’installazione — 30 ottobre 2026

Aggiunto `scripts/session-check.sh` per le verifiche manuali, deliberatamente
fuori da `verify.sh` e da `tests/nested.sh` perché installa file e toglie/rimette
l’estensione nella sessione dell’autore:

- senza argomenti confronta uno per uno i file elencati in
  `scripts/runtime-files.txt` con la copia installata, poi riporta stato,
  versione della CLI, numero di dispositivi (senza ID) e righe di log pertinenti;
- `--install` rigenera il `.mo` e sincronizza i file runtime;
- `--teardown` disabilita l’estensione dopo `DELAY` secondi, con il menu aperto,
  verifica che non restino processi `openlogi api devices` e la riabilita;
- `--all` concatena i passi; `-h` mostra l’uso.

Prima esecuzione nella sessione reale: tutti i file installati risultano diversi
dal repository, quindi la copia in uso è quella precedente alle correzioni di
oggi. Questo spiega perché il refresh live non si osservava e perché la puntina
seguiva ancora la vecchia regola della percentuale. Stato riportato:
`Enabled: No`, `State: INACTIVE`, nessuna installazione di sistema: l’estensione
non era abilitata al momento del controllo.

Dato raccolto dalla stessa esecuzione: `openlogi --version` risponde
`openlogi 0.8.19`, non 0.8.18, e l’inventario reale (2 dispositivi) è leggibile
con schema 1. Il contratto resta verificato sul tag v0.8.18; nessuna nuova
verifica hardware per la 0.8.19 oltre a quanto già osservato.

## Puntina e icona del tipo nel pannello — 30 ottobre 2026

Difetto segnalato dall’autore: la puntina del mouse era scomparsa dalla riga.
Causa: `pinnable` richiedeva `battery.percentage !== null`, quindi un dispositivo
in carica senza lettura (`Battery unavailable · Charging`) perdeva la puntina
anche se la selezione era ancora valida.

Correzione:

- la puntina ora dipende solo dalla scelta: ID univoco, dispositivo online e
  supporto batteria (`battery !== null`); una lettura mancante non la nasconde;
  l’icona del tipo viene mostrata sempre e la percentuale solo se esiste;
- nel pannello, dopo l’icona dell’estensione compaiono l’icona del tipo del
  dispositivo fissato (mouse, tastiera, …) e la percentuale quando disponibile;
  il nome accessibile del pulsante include nome dispositivo e valore;
- mappa delle icone di tipo centralizzata in `shell/deviceRow.js` (`kindIcon`),
  usata sia dalle righe sia dal pannello;
- stringhe aggiornate: «Show the pinned device in the panel» (preferenza),
  «Remove this device from the panel» (puntina), «Select a device in OpenLogi.
  Pin a device in the panel for this session.» (intestazione menu), più
  descrizione della chiave GSettings; traduzione italiana a 37 messaggi;
- fixture sintetica estesa con `charging-no-reading`, un mouse in carica senza
  percentuale, per coprire la regressione.

Verifiche:

- `SHEXLI=/tmp/shexli-venv/bin/shexli ./scripts/verify.sh`: 64 controlli GJS
  (erano 61), ZIP, catalogo italiano, template e Shexli tutti verdi;
- `./tests/nested.sh`: **56 controlli** Shell (erano 48). Nuovi: puntina visibile
  e reattiva su dispositivo senza lettura, puntina che sopravvive a un refresh,
  nessuna puntina su un dispositivo senza batteria, icona di tipo corretta con e
  senza percentuale, nome accessibile del pannello;
- evidenze: `/tmp/openlogi-nested-i6QndI/pinned-kind-icon.png` (mouse senza
  percentuale: icona del topo, nessun valore) e `pinned-percentage.png`
  (tastiera con `0%`), ritagli del pannello ispezionati.

## Icona simbolica del pannello — 30 ottobre 2026

Difetto segnalato dall’autore: nel pannello compariva un pallino bianco al posto
del marchio. Riprodotto ingrandendo lo screenshot della sessione reale.

Causa: l’SVG usava due path con `stroke` e `fill="none"`. Il recolouring
simbolico della Shell/GTK impone `fill` su tutti i path, quindi l’arco del
cerchio veniva riempito e diventava un disco pieno che copriva il mouse.

Correzione in `icons/openlogi-companion-symbolic.svg`:

- cerchio come anello chiuso (due archi, `fill-rule="evenodd"`), niente `stroke`;
- mouse come capsula con la rotella ritagliata nello stesso path tramite evenodd;
- unico colore `#2e3436`, che il tema sostituisce; nessuna modifica al nome o al
  percorso del file, quindi il manifest runtime resta invariato.

Verifiche:

- resa raster a 16, 22 e 32 px ispezionata: anello e mouse distinti, senza fusione;
- `./tests/nested.sh`: 48 controlli superati e screenshot
  `/tmp/openlogi-nested-LViwg2`; ritaglio del pannello ispezionato a tema chiaro e
  scuro a scala testo 1, icona riconoscibile in entrambi (prima era un disco);
- `tests/check-package.py` ora rifiuta un’icona `-symbolic.svg` con `stroke` o
  `fill="none"`, così il difetto non può tornare;
- `SHEXLI=/tmp/shexli-venv/bin/shexli ./scripts/verify.sh` superato.

L’icona quadrata per la pagina EGO è un PNG e non è toccata da questo difetto.

## Icona EGO e marchi — 30 ottobre 2026

Modifica realizzata con assistenza AI per uso personale.

- `scripts/make-ego-icon.py` genera `assets/ego/icon-256.png` e `icon-128.png`
  dal logo esistente: piastra scura arrotondata (raggio 22%) con emblema chiaro
  al 66% del lato, per leggibilità su schede chiare e scure della pagina EGO.
  Nessuna modifica al logo o all’SVG simbolico usato dalla Shell.
- `assets/ego/README.md` documenta rigenerazione e uso; `assets/` non è nel
  manifest runtime, quindi l’icona non entra nello ZIP.
- `README.md` ha ora la sezione «Marchi e indipendenza»: nessuna affiliazione,
  marchio originale, nessun media di terzi nel repository o nel bundle, nomi
  commerciali dei dispositivi solo a runtime.
- Verifica visiva delle due dimensioni: emblema centrato, margini regolari,
  nessun artefatto di ridimensionamento.

`verify.sh` non è influenzato (nessun file runtime o di test modificato);
`nested.sh` non rieseguito in questo passaggio.

## Pulizia per la revisione — 30 ottobre 2026

Modifica realizzata con assistenza AI per uso personale, su richiesta esplicita
dell’autore, in deroga alla precedente regola «conservare l’avviso AI nei file
generati».

- Rimossi dagli header di tutti i file (runtime, test, script, CSS) i commenti
  `Generated with AI for personal use` e `Do NOT upload to extensions.gnome.org`:
  le review EGO li elencano fra gli indicatori di output AI. Resta solo
  `SPDX-License-Identifier: GPL-3.0-or-later`.
- Provenienza AI conservata nella documentazione: `README.md`,
  `AI_REVIEW_GUIDELINES.md`, `AGENTS.md`, `assets/branding/README.md` e questo
  file. Aggiornate le regole di progetto di conseguenza.
- `metadata.json`: rimosso `version` (deprecato, impostato da EGO), aggiunto
  `url` verso il repository previsto e descrizione estesa su requisiti, sola
  lettura, comportamento del click e indipendenza.
- `tests/check-package.py` ora rifiuta un bundle con `version` o senza `url`
  `https://`.

Limite noto: `url` punta a `https://github.com/giaffa86/openlogi-companion`, che
non esiste ancora. Il link va creato prima di qualsiasi upload su EGO.

Verifiche: `SHEXLI=/tmp/shexli-venv/bin/shexli ./scripts/verify.sh` superato
(sintassi, 61 controlli GJS, ZIP dal manifest, catalogo italiano, template,
Shexli senza finding). `./tests/nested.sh` non rieseguito in questo passaggio:
non sono cambiati `shell/`, la UI o il polling.

## Sessione reale e refresh del menu — 30 ottobre 2026

Modifica realizzata con assistenza AI per uso personale, sulla base delle
osservazioni dell’autore nella sessione GNOME Shell 50 con dispositivi reali
collegati.

### Riscontri della sessione reale

- L’inventario reale è arrivato e il menu ha elencato due dispositivi con
  batteria e stato di ricarica; evidenza in `assets/screenshots/menu-devices.png`.
- Il click sulla riga e l’azione di apertura portano alla **finestra generale** di
  OpenLogi, che richiede ancora la selezione manuale del dispositivo: è il
  comportamento previsto da OL-001, non un difetto introdotto dal companion.
- I nomi non coincidono con la home della GUI, che usa i nomi commerciali brevi
  (`MX Master`, `MX Keys`) mentre la CLI riporta il nome esteso del modello.
- La home della GUI non mostra la percentuale di carica: il confronto numerico
  della batteria con OpenLogi resta non eseguito (evidenza
  `assets/screenshots/openlogi-gui-home.png`).

### Etichette

`Open OpenLogi` ripeteva il verbo nel nome dell’applicazione. L’azione del menu
diventa `Show OpenLogi window` / `Mostra la finestra di OpenLogi`, coerente con
`Main.activateWindow` e con l’apertura della finestra generale. Il nome
accessibile della riga diventa `Select the device in the OpenLogi app`. Le
vecchie stringhe sono state rimosse da `po/it.po` e dal modello; nessun filtro
aggiunto sul bus, nessuna intercettazione di notifiche.

### Refresh live a menu aperto

Difetto osservato: con il pannello aperto i dati non si aggiornavano, perché il
timer di polling esisteva solo con la preferenza `show-percentage` attiva e con
intervallo minimo di 60 s. Il polling ora dipende dalla visibilità del menu:

- menu aperto: 5 s, con backoff `10 → 20 → 40 → 60` s in caso di errori (tetto 60 s);
- menu chiuso: nessun timer, salvo la preferenza `show-percentage` attiva, che
  mantiene il poll lento `60 → 900` s;
- una sola richiesta pendente, timeout 5 s, cancellazione e reaping invariati;
- le righe vengono riusate quando l’inventario non cambia, quindi focus e scroll
  non vengono persi a ogni aggiornamento.

### Traduzioni

Lingua sorgente: inglese (i `msgid`). Italiano: `po/it.po` compilato in
`locale/it/LC_MESSAGES/openlogi-companion.mo`, che è anche il percorso atteso da
GNOME Shell per `gettext-domain: openlogi-companion` in `metadata.json`. Ogni
altra lingua cade sull’inglese. Lo ZIP contiene solo il catalogo compilato: le
regole EGO elencano `.po` e `.pot` fra i file non necessari alla submission.

Controlli aggiunti a `scripts/verify.sh`:

- il catalogo compilato esiste nel percorso del dominio dichiarato;
- `msgfmt --statistics` su `po/it.po` non riporta voci non tradotte o fuzzy;
- il catalogo si carica davvero e restituisce `Mostra la finestra di OpenLogi`
  per `Show OpenLogi window` (verifica con il modulo `gettext` di Python, perché
  il typelib `Gettext` non è installato su questa macchina);
- `po/openlogi-companion.pot` è allineato ai sorgenti (37 messaggi).

Stringhe aggiornate in questo passaggio: sottotitolo delle preferenze
(`Aggiorna ogni 60 secondi mentre è mostrata nel pannello, con attesa maggiore
dopo errori.`) e descrizione della chiave GSettings, entrambe coerenti con il
polling 5 s a menu aperto. Restano in inglese, non tradotte, solo le stringhe di
marca `OpenLogi Companion` del pannello.

### Verifiche eseguite sui sorgenti modificati

- `SHEXLI=/tmp/shexli-venv/bin/shexli ./scripts/verify.sh`: sintassi, limiti di
  riga, 61 controlli GJS, ZIP dal manifest esplicito e `msgcmp` superato su 37
  messaggi tradotti; Shexli 0.2.1 con tree-sitter 0.25.2 e tree-sitter-javascript 0.25.0
  senza finding, errori o warning.
- `./tests/nested.sh`: **48 controlli** Shell superati con backend sintetico (erano
  42), incluso il refresh live a menu aperto con inventario cambiato nel finto
  CLI, il ritorno al poll lento alla chiusura e l’apertura della finestra delle
  preferenze con il nuovo sottotitolo. Evidenze e screenshot
  `/tmp/openlogi-nested-swZqwi`; menu scuro a scala testo 1 ispezionato, etichetta
  `Show OpenLogi window` visibile, avvisi ambientali AT-SPI/PipeWire invariati.
- Nessuna installazione o ricarica nella sessione host durante queste verifiche.

Restano aperti i punti di `OPEN_ITEMS.md`: confronto numerico batteria con la GUI,
click con app chiusa e minimizzata, raggruppamento finestra, accessibilità con
lettore di schermo e DPI/multi-monitor.

## Screenshot del menu con dispositivi — 29 ottobre 2026

Nota aggiunta con assistenza AI per uso personale. L'autore ha segnalato il
funzionamento corretto dell'estensione nella sessione GNOME Shell 50 reale, con
menu funzionante e dispositivi mostrati, e ha fornito lo screenshot acquisito.
L'immagine è conservata come `assets/screenshots/menu-devices.png` (972×612,
SHA-256 `db98d8d5…5e7b`), con provenienza e uso previsto nel relativo README.
Mostra due dispositivi connessi con batteria e stato di ricarica, senza ID o
dati sensibili. Resta un'evidenza visiva fornita dall'autore, non una
riacquisizione automatica: non sostituisce le prove in `tests/nested.sh` né
aggiunge verifiche hardware oltre a quanto annotato in `OPEN_ITEMS.md`. L'asset
non è nel manifest runtime e quindi non entra nello ZIP.

## Logo e icona — 29 ottobre 2026

Modifica realizzata con assistenza AI per uso personale. Logo PNG generato con
image_gen, con canale alfa verificato, in `assets/branding/`; prompt e provenienza
nel relativo README. Adattamento SVG simbolico su griglia 16×16 in `icons/`,
caricato da `St.Icon` tramite `Gio.FileIcon`. Il tema Shell ne determina il colore.
Il manifest runtime include soltanto l’SVG, senza PNG, prompt o documentazione.

Verifiche eseguite sui sorgenti modificati:

- `SHEXLI=/tmp/shexli-venv/bin/shexli ./scripts/verify.sh`: 61 controlli GJS,
  ZIP e traduzioni superati; Shexli senza finding, errori o warning.
- `./tests/nested.sh`: 42 controlli Shell superati con backend sintetico.
  Il bind D-Bus inizialmente negato nel sandbox è riuscito con esecuzione
  autorizzata fuori dal sandbox. Evidenze in `/tmp/openlogi-nested-IgFqBv`.
  Screenshot scuro a scala testo 1 ispezionato; nessun errore di caricamento
  dell’icona nel log. Restano gli avvisi ambientali AT-SPI/PipeWire/Adw già noti.

Nessuna installazione o ricarica nella sessione host. Nessuna prova hardware o
della GUI OpenLogi reale aggiunta; restano tutti i limiti in `OPEN_ITEMS.md`.

## Verifica del 28 ottobre 2026

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

`scripts/runtime-files.txt` contiene l’elenco esatto dei file runtime. Lo ZIP
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
