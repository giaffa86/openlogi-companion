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

1. [ ] Quando saranno disponibili periferiche collegate, verificare la versione
   di OpenLogi e l’inventario con `openlogi api devices`; confrontare nomi, stato
   online e batteria con la GUI reale (OL-002).
2. [ ] Dopo installazione esplicita del companion, provare riga e azione Apri con
   OpenLogi chiuso, aperto e minimizzato. Il risultato atteso resta la finestra
   generale, con selezione manuale del dispositivo (OL-001 e OL-002).
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

La CLI reale ha risposto `ready` con zero dispositivi fuori dal sandbox. Non
sono stati osservati dispositivi reali né batterie: nessuna compatibilità hardware
è dimostrata, in particolare per G515 e Keys-To-Go 2.

Il percorso Shell di avvio/attivazione è testato con un’app GTK sintetica e il
medesimo desktop ID/StartupWMClass in una sessione separata. Non è una prova di
OpenLogi GPUI: restano da provare GUI reale chiusa, aperta, minimizzata e relativo
raggruppamento finestra. Non sono state avviate GUI reali o installate estensioni
nella sessione host durante la build.

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

## OL-003: accessibilità e layout residui

Testati focus programmatico delle righe, nomi accessibili, troncamento, scrolling,
200 dispositivi, temi chiaro/scuro e scala testo 1 e 1,5 su monitor virtuale
1280×720. Screenshot ispezionati visivamente. Non completata una prova con lettore
di schermo, navigazione fisica Tab/frecce e interazione touch. Il bus AT-SPI nella
sessione isolata ha segnalato `Permission denied`; non è una prova che
l’accessibilità del companion sia incompatibile. Restano DPI monitor frazionari,
monitor molto piccoli e multi-monitor, non equivalenti alla scala del testo.

## OL-004: identità e copertura API

Nessun favorito persistente fino a un’identità pubblica stabile verificata.
ID opachi attuali soltanto in memoria; se mancanti o duplicati non si può fissare
una percentuale. Non si deduplicano le righe. I cambi della route richiedono una
nuova scelta. Non è possibile ricostruire in modo affidabile la stessa periferica
fisica da nomi o ID riutilizzati dall’upstream.

L’API inventario della release include luci ma non webcam. Non implementati
sottoscrizione eventi, notifiche batteria, controlli hardware o modifica profili.
Il profilo corrente della CLI deve coincidere con quello dell’agent; il companion
non legge o cambia configurazioni private per forzarne la corrispondenza.
