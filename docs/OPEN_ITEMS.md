# Limiti e verifiche aperte

## Punto di ripresa concordato — 28 ottobre 2026

Nota aggiornata con assistenza AI per uso personale.

Al momento del punto di ripresa non erano disponibili dispositivi collegati.
Le prove hardware restano in attesa; l’inventario vuoto osservato non dimostra
incompatibilità. Alla ripresa, seguire questa checklist:

**Pubblicazione remota rimandata:** i sorgenti e il commit Git locale possono
essere preparati ora. Creazione del repository GitHub, push e release restano
da fare soltanto dopo la verifica dell’estensione con dispositivi reali collegati,
inclusi inventario/batteria e apertura della GUI descritti nei punti 1 e 2.
Registrare qui e in `VERIFICATION.md` i risultati prima di riprendere il passaggio
al remoto. La preparazione locale non autorizza la pubblicazione anticipata.
Il 30 ottobre 2026 i punti 1 e 2 sono stati provati con dispositivi reali e sono
chiusi solo in parte: restano il confronto numerico della batteria con la GUI e le
prove con OpenLogi chiuso e minimizzato. La pubblicazione resta quindi rimandata.

1. [x] Inventario reale osservato il 30 ottobre 2026: due dispositivi con
   batteria nel menu, con GUI OpenLogi aperta sugli stessi due dispositivi.
   Confronto numerico della batteria eseguito con la pagina dispositivo della
   GUI: coerente. **Nota non bloccante:** la CLI riporta il nome esteso del
   modello (`Wireless Mouse MX Master`, `MX Keys Wireless Keyboard`), la home
   della GUI i nomi brevi (`MX Master`, `MX Keys`); non è un difetto.
2. [x] Click sulla riga e azione Apri provati nella sessione reale: portano
   **entrambi alla finestra generale**, come previsto da OL-001. **Parziale:**
   mancano le prove con OpenLogi chiuso e minimizzato e del raggruppamento della
   finestra (OL-002).
3. [ ] Controllare release successive alla v0.8.18, documentazione e issue upstream
   per eventuali interfacce pubbliche già disponibili o richieste equivalenti.
   Questo controllo può essere svolto anche senza hardware.
4. [ ] Se il limite persiste, preparare una richiesta upstream concreta per
   identità pubblica stabile e azione di apertura della pagina dispositivo,
   includendo gestione di GUI già avviata ed errori espliciti. La proposta non è
   stata inviata; questa nota non autorizza l’invio.
5. [ ] Integrare la selezione diretta solo dopo verifica dell’interfaccia pubblica.
   Nel frattempo mantenere l’apertura generale e la puntina soltanto in memoria
   (OL-001 e OL-004).

## OL-001: apertura diretta della pagina dispositivo, requisito non soddisfatto

OpenLogi v0.8.18 non offre un’azione pubblica verificata per selezionare un
dispositivo nella GUI. `brand.rs` definisce comandi generici `show` e
`open-settings`, senza selezione dispositivo; `main.rs` registra `on_open_urls`
ma questo non dimostra la registrazione Linux. Il file desktop non dichiara
un protocol handler. Non vengono inventati deep link, flag o metodi D-Bus.

Il companion chiama il launcher `openlogi.desktop` e attiva una sua finestra esistente con
`Main.activateWindow`, oppure ne avvia una con `Shell.App.activate()`:
click sulla riga e azione Apri usano la **finestra generale**. Il testo del menu e
il nome accessibile della riga richiedono di selezionare il dispositivo nell’app.
Il pulsante a puntina modifica soltanto la visualizzazione del pannello.

Conferma empirica del 30 ottobre 2026: nella sessione reale con due dispositivi
collegati, sia il click sulla riga sia l’azione di apertura hanno mostrato la
finestra generale e non la pagina del dispositivo.

Proposta upstream, separata e non inviata: introdurre un’azione Linux pubblica e
versionata `OpenDevice`, tramite desktop action/D-Bus o deep link registrato,
con identità pubblica stabile del dispositivo e metodo di risoluzione alla route
corrente. Un ID nullo/duplicato deve produrre un errore, mai selezionare la prima
corrispondenza. GUI chiusa: avvio e applicazione della selezione dopo inventario
pronto; GUI aperta/minimizzata: inoltro all’istanza esistente, selezione e focus.
Il client deve poter distinguere successo, dispositivo assente/offline, identità
ambigua e inventario non pronto. Evitare seriali in URL/log pubblici. Fino alla
verifica di questa interfaccia, la selezione diretta resta non implementata.

## OL-002: periferiche reali e integrazione con la GUI OpenLogi

Prima osservazione con dispositivi reali il 30 ottobre 2026: inventario `ready`
con due dispositivi connessi (mouse e tastiera), batteria e stato di ricarica
mostrati correttamente nel menu; nessun errore nel log della Shell. Evidenze in
`assets/screenshots/`.

Chiuso il 30 ottobre 2026: **confronto numerico della batteria** con la pagina
dispositivo di OpenLogi, coerente con la riga del menu (la home della GUI non
espone la percentuale). Osservato anche il caso reale «Battery unavailable ·
Charging» senza lettura: prima della correzione la puntina spariva, ora resta
fissabile e il pannello mostra l’icona del tipo.

Limiti residui:

- Nomi: la CLI espone il nome esteso del modello, la home della GUI il nome
  commerciale breve. Il companion non rinomina nulla e non deduce alias.
- Avvio della GUI: provati solo con OpenLogi già aperto. Restano chiuso,
  minimizzato e raggruppamento finestra (GPUI reale, `StartupWMClass`).
- Altri modelli (es. G515, Keys-To-Go 2) non sono disponibili all’autore: sono
  periferiche di terzi, quindi nessuna compatibilità è dichiarata e la loro
  verifica non è un requisito di pubblicazione.
- Non sono state avviate GUI reali o installate estensioni nella sessione host
  durante le build; la prova reale è stata fatta dall’autore.

Il percorso Shell di avvio/attivazione è testato con un’app GTK sintetica e il
medesimo desktop ID/StartupWMClass in una sessione separata. Non è una prova di
OpenLogi GPUI.

Per chiudere il punto, dopo installazione esplicita del companion:

```bash
openlogi --version
openlogi api devices
gnome-extensions info openlogi-companion@giaffa86
journalctl --user -b -o cat /usr/bin/gnome-shell
```

Non condividere l’output dell’inventario senza oscurare gli ID. Con dispositivi
reali connessi, confrontare nomi, connessione e batteria con OpenLogi, quindi
provare riga e Apri con app chiusa/aperta/minimizzata. Verificare che il click
porti alla finestra generale e richieda ancora la selezione manuale. Provare
riavvio della sola estensione con richieste pendenti, senza fermare l’agent.
Non usare `openlogi list` per aggirare l’assenza dell’inventario.

## OL-005: blocchi per una eventuale submission EGO

Ricognizione del 30 ottobre 2026 sulle
[review guidelines](https://gjs.guide/extensions/review-guidelines/review-guidelines.html).
Lavori preparatori eseguiti; la pubblicazione resta rimandata alle verifiche di
OL-002, OL-003 e alla creazione del repository remoto.

- **Avviso AI negli header.** Risolto il 30 ottobre 2026: gli header dei file
  contengono solo `SPDX-License-Identifier: GPL-3.0-or-later`. La provenienza AI
  resta documentata in `README.md`, `AI_REVIEW_GUIDELINES.md` e `docs/`. Resta a
  carico dell’autore poter spiegare e mantenere il codice: le linee guida
  respingono comunque le submission non giustificabili.
- **`metadata.json`.** Sistemato: `version` rimosso, `url` aggiunto
  (`https://github.com/giaffa86/openlogi-companion`) e `description` estesa con
  requisiti, sola lettura, click e indipendenza. **Aperto:** il repository non
  esiste ancora, quindi l’URL va creato e verificato prima dell’upload;
  `tests/check-package.py` rifiuta un bundle con `version` o senza `url` https.
- **Necessità del subprocess.** Non eliminabile con i vincoli attuali: l’unica
  interfaccia pubblica documentata è `openlogi api devices`. Sono esclusi per
  regola di progetto IPC interno, HID diretto, `openlogi list`, daemon aggiuntivi
  e lettura di `config.toml`. La motivazione da usare nella submission è in
  `README.md` e in questo file: CLI ufficiale in sola lettura, argv fisso, nessuna
  shell, timeout, limiti, cancellazione e reaping.
- **Marchio.** Chiarito il 30 ottobre 2026: dichiarazione di indipendenza nella
  `description` di `metadata.json`, in `README.md` (sezione «Marchi e
  indipendenza») e nella nota privata `private/ego-subprocess.md`. Il marchio è
  originale, e nel bundle non ci sono media di terzi. **Aperto:** la scelta del
  nome resta dell’autore. Le linee guida EGO elencano «nomi di marchio» fra i
  contenuti protetti privi di permesso: `OpenLogi Companion` può quindi essere
  contestato in review. Alternative pronte, da usare solo se richiesto: nome
  neutro (es. «Wireless Peripheral Battery») con OpenLogi citato nella sola
  descrizione.
- **Icona della scheda EGO.** Pronta: `assets/ego/icon-256.png` e `icon-128.png`,
  piastra scura arrotondata con emblema chiaro per restare leggibili su schede
  chiare e scure, rigenerabili con `scripts/make-ego-icon.py`. Si caricano dal
  modulo web, non dallo ZIP. Resta da valutarne la resa sulla scheda reale dopo
  l’upload.
- **Screenshot.** `assets/screenshots/menu-devices.png` è pronto; conviene
  ricatturare a ≥1200 px di larghezza. `openlogi-gui-home.png` non va caricato.
- **File non necessari.** Le regole EGO elencano `.po`, `.pot`, script di build e
  media inutilizzati: lo ZIP attuale contiene solo runtime, icona, schema,
  catalogo compilato e `LICENSE`, quindi è già conforme su questo punto.
- **Lingua.** Inglese come sorgente, italiano come catalogo compilato; le altre
  lingue cadono sull’inglese. Un eventuale portale di traduzione EGO lavora sui
  sorgenti del repository, non sullo ZIP.
- **Accessibilità.** Restano le prove con lettore di schermo e i DPI frazionari
  descritti in OL-003.

## OL-003: accessibilità e layout residui

Coperto dai test automatici nella Shell isolata: focus programmatico delle righe,
nomi accessibili, troncamento, scrolling, 200 dispositivi, temi chiaro/scuro,
scala testo 1 e 1,5 su monitor virtuale 1280×720, conservazione di focus e
scorrimento durante il refresh live a menu aperto.

**Non coperto — test manuali rimandati dall’autore**, che li eseguirà con la
checklist locale non versionata `private/accessibility-tests.md`: lettore di
schermo (Orca), navigazione fisica Tab/frecce, interazione touch, DPI frazionari,
multi-monitor e monitor molto piccoli. Il bus AT-SPI nella sessione isolata ha
segnalato `Permission denied`; non dimostra incompatibilità, ma la prova con il
lettore di schermo resta assente e non va considerata coperta.

## OL-004: identità e copertura API

Nessun favorito persistente fino a un’identità pubblica stabile verificata.
ID opachi attuali soltanto in memoria; se mancanti o duplicati non si può fissare
il dispositivo nel pannello. La puntina non richiede una lettura di batteria
valida: un dispositivo online con supporto batteria resta fissabile anche senza
percentuale, e il pannello mostra almeno l’icona del tipo. Non si deduplicano le
righe. I cambi della route richiedono una nuova scelta. Non è possibile ricostruire in modo affidabile la stessa periferica
fisica da nomi o ID riutilizzati dall’upstream.

L’API inventario della release include luci ma non webcam. Non implementati
sottoscrizione eventi, notifiche batteria, controlli hardware o modifica profili.
Il profilo corrente della CLI deve coincidere con quello dell’agent; il companion
non legge o cambia configurazioni private per forzarne la corrispondenza.
