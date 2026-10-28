# OpenLogi Companion

Companion indipendente per GNOME Shell 50: un indicatore mostra i dispositivi
restituiti dall’agent [OpenLogi](https://github.com/AprilNEA/OpenLogi) e la loro
batteria. Progetto sperimentale nato per uso personale, indipendente da OpenLogi.
Licenza [GPL-3.0-or-later](LICENSE).

**Stato sperimentale:** i test automatici usano dispositivi sintetici. Non sono
ancora state verificate periferiche reali né la GUI OpenLogi reale; in particolare
G515 e Keys-To-Go 2 restano da provare. È supportata soltanto GNOME Shell 50.
La condivisione dei sorgenti su GitHub non costituisce una certificazione EGO;
non è prevista una pubblicazione su extensions.gnome.org.

La pubblicazione remota è rimandata alla verifica con dispositivi reali collegati.
Preparazione dei sorgenti e commit locali precedono questo passaggio; vedere il
[punto di ripresa](docs/OPEN_ITEMS.md).

**Il click su un dispositivo apre/attiva la finestra generale di OpenLogi.
La pagina del dispositivo non viene selezionata:** bisogna sceglierlo nell’app.
Nella release verificata v0.8.18 non è stata individuata un’azione pubblica
supportata per questa selezione. Vedi
[limiti e proposta upstream](docs/OPEN_ITEMS.md).

## Requisiti e comportamento

Fedora, GNOME Shell 50, GJS, OpenLogi RPM con CLI `openlogi api devices`,
agent raggiungibile nello stesso profilo della CLI e launcher `openlogi.desktop`.
Contratto verificato sul tag OpenLogi v0.8.18, schema JSON 1. Nessuna promessa
per tutti i dispositivi visibili nella GUI: l’inventario API include luci senza
batteria, ma non webcam. G515 e Keys-To-Go 2 non sono stati verificati.

L’indicatore parte con la sola icona. In **Preferenze dell’estensione** si può
consentire la percentuale; il pulsante a puntina di una riga sceglie il dispositivo
per la sessione. Serve un ID attualmente univoco e una percentuale disponibile.
Non viene calcolata una media. ID null/duplicati non impediscono la visualizzazione
delle righe, ma impediscono la scelta nel pannello. La scelta resta in memoria e
si perde dopo scomparsa, disconnessione, errore, nuova scansione o disabilitazione.
Non è un’identità hardware persistente: non sopravvive a cambi della route.

Aggiornamento all’abilitazione, all’apertura del menu e con **Aggiorna**. Con la
percentuale consentita, polling ogni 60 secondi anche prima della scelta;
dopo errori il ritardo sale a 120, 240, 480 e massimo 900 secondi.
Aprire il menu consente un tentativo immediato; richieste contemporanee vengono
accorpate. Senza tale preferenza non ci sono timer di polling.

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

## Flusso dei dati

```text
Agent OpenLogi (profilo corrente)
  → CLI ufficiale: openlogi api devices
  → Provider: due pipe asincrone, timeout, limite condiviso
  → validazione schema 1, ordinamento stabile
  → menu Shell e percentuale di un solo dispositivo in memoria

Click riga / Apri OpenLogi → finestra del launcher openlogi.desktop
  → Main.activateWindow se esiste, Shell.App.activate per avviarla
Preferenze GTK/Adw → GSettings: solo show-percentage
```

Il provider avvia solo la CLI in lettura, con argv fisso; non avvia l’agent,
non apre HID, non legge `config.toml` e non decodifica IPC interno. Timeout di 5 s,
budget stdout+stderr di 1 MiB, letture di massimo 8192 byte (un chunk che supera
il limite provoca l’arresto). Stderr viene drenato senza conservarlo. A timeout,
limite o teardown vengono cancellate le letture, terminato e raccolto il solo
figlio CLI. Nessuno snapshot o ID viene salvato in GSettings, file o log.
La GUI aperta dall’utente è indipendente dal teardown.

Il codice è generato con assistenza AI e conserva l’avviso di uso personale:
la manutenzione richiede la comprensione del JavaScript. Vedere
[le linee guida di revisione](AI_REVIEW_GUIDELINES.md). Shexli non certifica
l’accettazione EGO.

Il repository contiene sorgenti, traduzioni, test, script e documentazione.
Il bundle installabile include soltanto i file elencati in
`scripts/runtime-files.txt`; esclude test, script, documentazione e schema compilato.
ZIP, cataloghi compilati e altri artefatti locali non sono versionati: vengono
rigenerati dagli script.

Le verifiche residue e il punto di ripresa sono in [OPEN_ITEMS.md](docs/OPEN_ITEMS.md).
Il [piano upstream](docs/UPSTREAM_PLAN.md) descrive la proposta di selezione diretta;
nessuna issue o PR è stata inviata.
