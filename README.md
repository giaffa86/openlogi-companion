# OpenLogi Companion

Companion indipendente per GNOME Shell 50: un indicatore mostra i dispositivi
restituiti dall’agent [OpenLogi](https://github.com/AprilNEA/OpenLogi) e la loro
batteria. Progetto sperimentale nato per uso personale, indipendente da OpenLogi.
Licenza [GPL-3.0-or-later](LICENSE).

Il marchio è un mouse dentro un cerchio aperto. Il pannello usa una
[icona SVG simbolica](icons/openlogi-companion-symbolic.svg) che segue il tema
GNOME; [logo trasparente e provenienza AI](assets/branding/README.md) sono
conservati separatamente dal pacchetto runtime. L’[icona quadrata per la pagina
EGO](assets/ego/README.md) è generata dallo stesso marchio.

**Stato sperimentale:** i test automatici usano dispositivi sintetici. Sono stati
osservati due dispositivi reali (MX Master e MX Keys) con inventario, batteria e
confronto della percentuale con la pagina dispositivo di OpenLogi. Restano da
provare l’apertura della GUI con app chiusa/minimizzata e le verifiche di
accessibilità. Altri modelli non sono disponibili all’autore e non sono
dichiarati compatibili. È supportata soltanto GNOME Shell 50.

La pubblicazione su extensions.gnome.org è pianificata ma **subordinata** alle
verifiche residue elencate in [OPEN_ITEMS.md](docs/OPEN_ITEMS.md) (OL-002,
OL-003, OL-005); i commit locali e la creazione del repository remoto la
precedono.

Il [repository dei sorgenti](https://github.com/giaffa86/openlogi-companion)
è pubblico su autorizzazione dell’autore del 10 novembre 2026. Questa scelta
non chiude le verifiche residue né anticipa release o submission EGO; vedere
[limiti e punto di ripresa](docs/OPEN_ITEMS.md).

**Le righe dei dispositivi sono di sola consultazione; le puntine restano attive.**
L’azione **Mostra la finestra di OpenLogi** apre/attiva la finestra generale;
la pagina del dispositivo va selezionata nell’app.
Il controllo dei sorgenti è stato aggiornato alla v0.9.0 il 10 novembre 2026:
non è stata individuata un’azione pubblica supportata per questa selezione. Vedi
[limiti e proposta upstream](docs/OPEN_ITEMS.md).

## Marchi e indipendenza

Il progetto è indipendente: nessuna affiliazione, sponsorizzazione o approvazione
da parte di OpenLogi, Logitech o del GNOME Project. “OpenLogi” è usato solo in
senso descrittivo, per indicare l’app di cui l’estensione legge l’inventario, e
compare anche nel nome scelto dall’autore per riconoscibilità.

- Il marchio (mouse in un cerchio aperto) è originale, generato con assistenza
  AI; non riproduce loghi Logitech, OpenLogi o GNOME.
- Nel repository e nel bundle non ci sono loghi, icone, screenshot o altri
  media di terzi. `LICENSE` è il solo testo di terzi distribuito.
- I nomi commerciali dei dispositivi (`MX Master`, `MX Keys`, …) arrivano a
  runtime dalla CLI di OpenLogi e non sono inclusi nel pacchetto.
- La scheda EGO userà la stessa dichiarazione di indipendenza della
  `description` in `metadata.json`.

## Requisiti e comportamento

Fedora, GNOME Shell 50, GJS, OpenLogi RPM con CLI `openlogi api devices`,
agent raggiungibile nello stesso profilo della CLI e launcher `openlogi.desktop`.
Contratto verificato sul tag OpenLogi v0.8.18, schema JSON 1; la CLI reale
osservata il 30 ottobre 2026 è `openlogi 0.8.19`, che ha risposto con schema 1. Nessuna promessa
per tutti i dispositivi visibili nella GUI: l’inventario API include luci senza
batteria, ma non webcam. Osservati due dispositivi reali (MX Master e MX Keys);
G515 e Keys-To-Go 2 non sono stati provati.

L’indicatore parte con la sola icona. In **Preferenze dell’estensione** si può
mostrare nel pannello più dispositivi fissati: ciascuno con icona del tipo (mouse,
tastiera, …​) e batteria propria. La preferenza **Mostra la batteria a tacca**
alterna la percentuale numerica (predefinita) con una barra verticale proporzionale
alla lettura: verde sopra il 20%, ambra fino al 20%, rossa fino al 10%.
Lo 0% mostra la traccia vuota; senza percentuale non compare alcuna tacca e non
si deduce un valore dal livello qualitativo. Il menu e il nome accessibile
mantengono il dettaglio della batteria anche in modalità tacca.
Il pulsante a puntina di ogni riga aggiunge o rimuove quel solo dispositivo,
senza sostituire gli altri; l’ordine nel pannello segue quello delle puntine.
Per fissare un dispositivo serve un ID attualmente univoco su
un dispositivo online con supporto batteria; **non** serve una lettura valida,
quindi un dispositivo in carica senza percentuale resta fissabile e nel pannello
mostra almeno la sua icona. Con la preferenza **Nascondi l’icona dell’estensione
quando ci sono dispositivi fissati** il marchio del companion lascia il posto
ai dispositivi fissati, riconoscibili dalla propria icona di tipo.
Non viene calcolata una media. ID null/duplicati non impediscono la visualizzazione
delle righe, ma impediscono la scelta nel pannello. Le scelte restano in memoria:
scomparsa, disconnessione, ID ambiguo o perdita del supporto batteria rimuovono
solo la puntina interessata; errore, nuova scansione o disabilitazione le rimuovono tutte.
Non è un’identità hardware persistente: non sopravvive a cambi della route.

Aggiornamento all’abilitazione, all’apertura del menu e con **Aggiorna**. Mentre
il menu è aperto il polling è di 5 secondi, così batteria e connessione cambiano
senza chiudere il pannello; dopo errori il ritardo sale a 10, 20, 40 e massimo 60
secondi. A menu chiuso l’unico timer è quello della preferenza: con i dispositivi
consentiti nel pannello, polling ogni 60 secondi anche prima della scelta, con ritardo crescente
120, 240, 480 e massimo 900 secondi dopo errori. Richieste contemporanee vengono
accorpate. Senza menu aperto e senza la preferenza non ci sono timer di polling.

La preferenza **Nascondi l’icona dell’estensione quando ci sono dispositivi
fissati** toglie il marchio solo quando almeno un dispositivo fissato viene
effettivamente mostrato: restano le icone dei tipi e le rispettive batterie.
Se nessun dispositivo fissato è mostrato (puntine assenti, preferenza disattivata,
righe ambigue, dispositivi offline o inventario non pronto) il marchio riappare,
quindi il pannello non può mai diventare un pulsante vuoto.

Le stringhe sono in inglese nel sorgente e tradotte in italiano tramite
`po/it.po`; il bundle include solo il catalogo compilato in
`locale/it/LC_MESSAGES/openlogi-companion.mo`, nel percorso atteso da
`gettext-domain`. Ogni altra lingua usa l’inglese. Il controllo in
`scripts/verify.sh` verifica che il catalogo compilato si carichi davvero e che
template e traduzione restino allineati.

I dispositivi connessi precedono gli altri, poi segue il nome secondo la locale.
Le righe restano distinte anche per nomi o ID uguali. Le righe immutate vengono
riutilizzate per conservare il focus. La lista scorre, i nomi lunghi sono troncati,
lo stile e il focus usano il tema Shell. Stringhe inglesi traducibili e catalogo
italiano incluso; le percentuali seguono la locale.

Gli stati di caricamento, scansione, inventario indisponibile, nessun dispositivo,
CLI assente, agent irraggiungibile, incompatibilità e dati invalidi sono distinti.
Solo `ready` vuoto significa nessun dispositivo. Durante scansione o errore le
righe precedenti vengono rimosse. Una periferica offline non mostra la vecchia
batteria come attuale. Valori mancanti non diventano zero; i livelli qualitativi
non diventano percentuali. Nessuna notifica duplicata di batteria scarica.

## Installazione locale

Scaricare o clonare il repository e aprire un terminale nella sua directory radice
(quella che contiene `metadata.json`). Tutti i comandi seguenti partono da lì.
Per compilare traduzioni/schema servono `msgfmt` e `glib-compile-schemas`
(su Fedora, forniti da `gettext` e `glib2`).

```bash
./scripts/sync-extension.sh
gnome-extensions enable openlogi-companion@giaffa86
```

Lo script copia esclusivamente i file runtime e compila lo schema nel target
`~/.local/share/gnome-shell/extensions/openlogi-companion@giaffa86/`.
Non esegue reload, installazioni di pacchetti o comandi sudo. La prima installazione
può richiedere logout/login; su Wayland la cache dei moduli può richiederlo anche
dopo modifiche. La sessione non viene interrotta automaticamente.

In alternativa, generare e installare il pacchetto locale; per crearlo serve
anche `zip` e, per verificarne il contenuto, Python 3:

```bash
./scripts/package.sh
gnome-extensions install --force dist/openlogi-companion@giaffa86.shell-extension.zip
```

Il bundle conserva `shell/`, schema XML, catalogo italiano e licenza; lo schema
compilato è escluso (compilato dall’installer delle estensioni). Non contiene
prompt, test, script, documentazione di lavoro o dati personali.

Rimozione del solo companion:

```bash
gnome-extensions disable openlogi-companion@giaffa86
gnome-extensions uninstall openlogi-companion@giaffa86
```

Queste operazioni non disinstallano OpenLogi, non fermano l’agent e non cancellano
configurazioni hardware. Per una copia manuale non registrata nell’installer,
rimuovere esclusivamente la directory utente dell’UUID sopra indicato dopo averla
disabilitata.

## Verifica e sviluppo

Eseguire dalla radice del repository. Il controllo completo richiede Node
(solo parsing sintattico), GJS, Python 3, Bash, `zip`, gli strumenti GLib e gettext
(`msgfmt`, `msgcmp`, `xgettext`) e Shexli. La combinazione già verificata per lo
scanner è Shexli 0.2.1 con tree-sitter 0.25.2 e tree-sitter-javascript 0.25.0.
Per predisporre lo scanner in un ambiente Python separato:

```bash
python3 -m venv /tmp/shexli-venv
/tmp/shexli-venv/bin/pip install shexli==0.2.1 tree-sitter==0.25.2 tree-sitter-javascript==0.25.0
```

Quindi:

```bash
# Node è solo un syntax checker, non una toolchain runtime.
SHEXLI=/tmp/shexli-venv/bin/shexli ./scripts/verify.sh
# Ambiente separato, inventario e applicazione GUI sintetici:
./tests/nested.sh
# Rigenera il bundle:
./scripts/package.sh
```

Il test isolato richiede `dbus-run-session`, GNOME Shell con supporto headless,
monitor virtuale, `gdbus`, Python 3 con PyGObject/GTK4 e un renderer disponibile.
Crea bus, impostazioni, launcher finto e copie runtime in `/tmp`; non espone il
bus host e non usa il vero OpenLogi per i test GUI. Le evidenze restano nella
directory stampata all’avvio. Il controllo Eval non sicuro è abilitato da una
piccola estensione presente **solo nella copia di test**, mai nel pacchetto.

Per una prova interattiva usare una sessione di sviluppo separata:
`dbus-run-session -- gnome-shell --devkit` (richiede `mutter-devkit`).
Un bus isolato non vede automaticamente l’agent host: non collegare i due bus
per aggirare l’isolamento. Consultare [VERIFICATION.md](docs/VERIFICATION.md) per
risultati, comandi, versioni, prove non eseguite e limiti del sandbox.

Nella sessione reale, con l’estensione già installata:

```bash
# Sola lettura: confronta i file installati col repository, stato, CLI, log.
./scripts/session-check.sh
# Aggiorna la copia installata (poi logout/login su Wayland).
./scripts/session-check.sh --install
# Test interattivo: disabilita col menu aperto e cerca processi orfani.
DELAY=8 ./scripts/session-check.sh --teardown
```

Questi comandi toccano la sessione dell’utente e non sono usati da `verify.sh`
né da `tests/nested.sh`.

## Flusso dei dati

```text
Agent OpenLogi (profilo corrente)
  → CLI ufficiale: openlogi api devices
  → Provider: due pipe asincrone, timeout, limite condiviso
  → validazione schema 1, ordinamento stabile
  → menu Shell, con icona del tipo e batteria dei dispositivi fissati in memoria

Show OpenLogi window → finestra del launcher openlogi.desktop
  → Main.activateWindow se esiste, Shell.App.activate per avviarla
Preferenze GTK/Adw → GSettings: solo show-percentage, battery-bar e hide-logo
```

Il provider avvia solo la CLI in lettura, con argv fisso; non avvia l’agent,
non apre HID, non legge `config.toml` e non decodifica IPC interno. Timeout di 5 s,
budget stdout+stderr di 1 MiB, letture di massimo 8192 byte (un chunk che supera
il limite provoca l’arresto). Stderr viene drenato senza conservarlo. A timeout,
limite o teardown vengono cancellate le letture, terminato e raccolto il solo
figlio CLI. Nessuno snapshot o ID viene salvato in GSettings, file o log.
La GUI aperta dall’utente è indipendente dal teardown.

Il codice è stato sviluppato con assistenza AI; la provenienza è documentata qui,
in [AI_REVIEW_GUIDELINES.md](AI_REVIEW_GUIDELINES.md) e in `docs/`. I file
sorgente e di runtime non contengono avvisi AI né prompt: portano solo l’SPDX
`GPL-3.0-or-later`, perché le review EGO trattano quei commenti come indicatori
di codice generato. La manutenzione richiede la comprensione del JavaScript;
Shexli non certifica l’accettazione EGO.

Il repository contiene sorgenti, traduzioni, test, script e documentazione.
Il bundle installabile include soltanto i file elencati in
`scripts/runtime-files.txt`; esclude test, script, documentazione e schema compilato.
ZIP, cataloghi compilati e altri artefatti locali non sono versionati: vengono
rigenerati dagli script.

Le verifiche residue e il punto di ripresa sono in [OPEN_ITEMS.md](docs/OPEN_ITEMS.md).
Il [piano upstream](docs/UPSTREAM_PLAN.md) descrive la proposta di selezione diretta;
nessuna issue o PR è stata inviata.
