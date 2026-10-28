# Piano per apertura dispositivo in OpenLogi

Concordato il 28 ottobre 2026: i passi 1, 2 e 3 si eseguono in sequenza;
i test del passo 3 accompagnano la PR del passo 2.

## 1. Concordare l’interfaccia tramite issue

- [ ] Ricontrollare il ramo upstream corrente e cercare issue/PR equivalenti.
- [ ] Preparare una issue breve: caso d’uso del companion GNOME, apertura della
  pagina dispositivo da app esterne e limite della release verificata 0.8.18.
- [ ] Proporre un’azione pubblica minima, coerente con i meccanismi upstream;
  concordare trasporto, identità del dispositivo ed errori prima dell’implementazione.
- [ ] Pubblicare la issue quando richiesto dall’utente e attendere il confronto
  con il maintainer. Nessuna issue è stata ancora pubblicata.

## 2. Preparare una PR piccola

- [ ] Lavorare in un checkout separato di OpenLogi sul ramo corrente.
- [ ] Implementare soltanto apertura/attivazione GUI e selezione del dispositivo
  secondo l’interfaccia concordata, senza modifiche estranee.
- [ ] Gestire inoltro all’istanza esistente, avvio da chiusa e inventario non pronto.
- [ ] Documentare contratto, limiti e comportamento degli errori.
- [ ] Preparare descrizione e risultati dei test; pubblicare la PR quando richiesto.

## 3. Includere i test nella PR

- [ ] GUI chiusa: avvio, attesa inventario e selezione corretta.
- [ ] GUI aperta: selezione e focus senza finestre o processi duplicati.
- [ ] GUI minimizzata: ripristino, focus e selezione.
- [ ] Identità mancante, ambigua o dispositivo assente/offline: errore esplicito,
  senza selezionare una periferica diversa.
- [ ] Inventario in scansione/indisponibile e richieste ravvicinate.
- [ ] Verifica Linux reale, test automatici pertinenti e controlli upstream.
- [ ] Integrare il companion soltanto dopo verifica dell’API nella release che
  la distribuisce; fino ad allora il click apre la finestra generale.

## Stato

Piano registrato. Nessuna issue o PR inviata. Nessuna modifica upstream eseguita.
La proposta tecnica iniziale e i limiti sono in [OPEN_ITEMS.md](OPEN_ITEMS.md).
