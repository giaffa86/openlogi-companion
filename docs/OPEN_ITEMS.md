# Limiti e verifiche aperte

## Pubblicazione dei sorgenti autorizzata — 10 novembre 2026

L’autore ha creato il repository pubblico
[giaffa86/openlogi-companion](https://github.com/giaffa86/openlogi-companion)
e ha chiesto esplicitamente di sincronizzarlo con il progetto locale.
Questa istruzione autorizza commit e push dei sorgenti e supera il precedente
rinvio del passaggio al remoto. Restano aperte le verifiche hardware e GUI sotto
elencate: release e submission EGO continuano a dipendere da OL-002, OL-003 e
OL-005. Nessuna compatibilità aggiuntiva è dichiarata.

## Punto di ripresa concordato — 28 ottobre 2026 (storico)

Nota aggiornata con assistenza AI per uso personale.

Al momento del punto di ripresa non erano disponibili dispositivi collegati.
Le prove hardware restano in attesa; l’inventario vuoto osservato non dimostra
incompatibilità. Alla ripresa, seguire questa checklist:

**Decisione del 28 ottobre, superata per i push dall’autorizzazione sopra:** i sorgenti e il commit Git locale possono
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
2. [x] Prima della disattivazione del click sulle righe, click e azione Apri
   provati nella sessione reale: portano
   **entrambi alla finestra generale**, come previsto da OL-001. **Parziale:**
   mancano le prove dell’azione dedicata con OpenLogi chiuso e minimizzato e del
   raggruppamento della finestra (OL-002).
3. [x] Controllo aggiornato il 10 novembre 2026 sulla v0.9.0, ora installata:
   sorgenti della release, documentazione CLI e launcher Linux non offrono
   l’apertura della pagina dispositivo. Esiste la richiesta equivalente
   [upstream #1375](https://github.com/AprilNEA/OpenLogi/issues/1375), ancora aperta.
   Verifica dei sorgenti e del pacchetto installato, senza prova di apertura GUI.
4. [ ] Se il limite persiste, preparare una richiesta upstream concreta per
   identità pubblica stabile e azione di apertura della pagina dispositivo,
   includendo gestione di GUI già avviata ed errori espliciti. La proposta non è
   stata inviata; questa nota non autorizza l’invio.
   Prima di inviare, coordinarsi con la richiesta equivalente #1375 già esistente.
5. [ ] Integrare la selezione diretta solo dopo verifica dell’interfaccia pubblica.
   Nel frattempo mantenere l’apertura generale e la puntina soltanto in memoria
   (OL-001 e OL-004).

## OL-001: apertura diretta della pagina dispositivo, requisito non soddisfatto

OpenLogi v0.8.18 non offre un’azione pubblica verificata per selezionare un
dispositivo nella GUI. `brand.rs` definisce comandi generici `show` e
`open-settings`, senza selezione dispositivo; `main.rs` registra `on_open_urls`
ma questo non dimostra la registrazione Linux. Il file desktop non dichiara
un protocol handler. Non vengono inventati deep link, flag o metodi D-Bus.

Ricontrollato il 10 novembre 2026 sulla
[release v0.9.0](https://github.com/AprilNEA/OpenLogi/releases/tag/v0.9.0),
identificata anche localmente da `openlogi --version` e RPM
`openlogi-0.9.0-1.x86_64`. Il
[vocabolario `DeeplinkCommand`](https://github.com/AprilNEA/OpenLogi/blob/v0.9.0/crates/openlogi-core/src/brand.rs)
contiene ancora solo `show`, `open-settings`, `open-about`, `check-for-updates`
e `quit`; il parser ignora path/query dei comandi riconosciuti. Non si può usare
`show?device=…` per selezionare una periferica. Il
[bootstrap GUI](https://github.com/AprilNEA/OpenLogi/blob/v0.9.0/crates/openlogi-desktop/src/main.rs)
esce se esiste già un’istanza, senza inoltro della richiesta. Il
[launcher Linux della release](https://github.com/AprilNEA/OpenLogi/blob/v0.9.0/packaging/linux/desktop/openlogi.desktop)
e quello installato conservano `Exec=openlogi-desktop`, senza `%u`, MIME handler
o azioni per dispositivo. La
[richiesta equivalente #1375](https://github.com/AprilNEA/OpenLogi/issues/1375)
risulta ancora aperta. Il limite resta confermato per questa release; nessuna
prova di avvio reale della GUI è stata aggiunta.

Il 10 novembre 2026 l’autore ha chiesto di disattivare il click sulle righe,
perché l’apertura generale è fuorviante e ridondante rispetto all’azione dedicata.
Le righe sono ora di sola consultazione, senza attivazione, focus o hover della
riga; le puntine restano attive e raggiungibili da tastiera. I nomi accessibili
descrivono soltanto dispositivo e stato, senza inviti alla selezione nell’app.
L’azione **Mostra la finestra di OpenLogi** chiama il launcher `openlogi.desktop`
e attiva una finestra esistente con `Main.activateWindow`, oppure ne avvia una
con `Shell.App.activate()`. Apre sempre la **finestra generale**. Il pulsante a
puntina modifica soltanto la visualizzazione del pannello.

**Promemoria concordato:** alle prossime release ricontrollare un’API pubblica
per aprire la pagina del dispositivo e lo stato della
[issue #1375](https://github.com/AprilNEA/OpenLogi/issues/1375), già esistente.
Se il limite persiste, preparare un contributo alla richiesta esistente; creare
una nuova issue solo se manca una richiesta pertinente. Riattivare il click
solo dopo verifica dell’apertura contestuale su Linux, con GUI chiusa, aperta e
minimizzata e gestione esplicita degli ID assenti/ambigui. Nessun messaggio
upstream viene inviato in questa modifica.

Evidenza storica del 30 ottobre 2026, precedente alla disattivazione del click:
nella sessione reale con due dispositivi
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
provare l’azione **Mostra la finestra di OpenLogi** con app chiusa/aperta/minimizzata.
Verificare che apra la finestra generale e richieda ancora la selezione manuale;
il click sulle righe deve restare senza effetto, con puntine funzionanti. Provare
riavvio della sola estensione con richieste pendenti, senza fermare l’agent.
Non usare `openlogi list` per aggirare l’assenza dell’inventario.

## OL-005: blocchi per una eventuale submission EGO

Ricognizione del 30 ottobre 2026 sulle
[review guidelines](https://gjs.guide/extensions/review-guidelines/review-guidelines.html).
Lavori preparatori eseguiti; release e submission EGO restano rimandate alle
verifiche di OL-002 e OL-003. Il repository pubblico è stato creato dall’autore
il 10 novembre 2026, con sincronizzazione dei sorgenti autorizzata.

- **Avviso AI negli header.** Risolto il 30 ottobre 2026: gli header dei file
  contengono solo `SPDX-License-Identifier: GPL-3.0-or-later`. La provenienza AI
  resta documentata in `README.md`, `AI_REVIEW_GUIDELINES.md` e `docs/`. Resta a
  carico dell’autore poter spiegare e mantenere il codice: le linee guida
  respingono comunque le submission non giustificabili.
- **`metadata.json`.** Sistemato: `version` rimosso, `url` aggiunto
  (`https://github.com/giaffa86/openlogi-companion`) e `description` estesa con
  requisiti, sola lettura, apertura generale e indipendenza. Il repository
  pubblico esiste ed è accessibile dal 10 novembre 2026; l’URL è verificato.
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

Le tacche e le puntine multiple aggiunte il 10 novembre 2026 sono verificate
soltanto con backend sintetico. Restano da osservare con dispositivi reali,
insieme alla leggibilità delle tacche a DPI frazionari e su monitor diversi.
I valori restano disponibili nei nomi accessibili, ma ciò non sostituisce la
prova con lettore di schermo.

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

Si possono fissare più dispositivi indipendenti nella stessa sessione. La perdita
di un ID valido rimuove soltanto la puntina interessata; errore, scansione o
disabilitazione azzerano tutte le scelte. Né le puntine né i relativi ID vengono
salvati in GSettings: la nuova chiave `battery-bar` riguarda soltanto la resa UI.

L’API inventario della release include luci ma non webcam. Non implementati
sottoscrizione eventi, notifiche batteria, controlli hardware o modifica profili.
Il profilo corrente della CLI deve coincidere con quello dell’agent; il companion
non legge o cambia configurazioni private per forzarne la corrispondenza.
