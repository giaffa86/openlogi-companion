#!/bin/bash
# SPDX-License-Identifier: GPL-3.0-or-later.
# Manual session checks for the author's own GNOME session. Never used by
# verify.sh or the nested runner: it installs files and toggles the live
# extension, so it must be run on purpose.
set -euo pipefail
SOURCE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
UUID=openlogi-companion@giaffa86
TARGET="${HOME}/.local/share/gnome-shell/extensions/${UUID}"
DELAY=${DELAY:-8}
STATUS=0

usage() {
    cat <<'EOF'
Uso: scripts/session-check.sh [opzione]

  (nessuna)    Confronta i file installati con il repository e mostra lo stato.
  --install    Rigenera il .mo, sincronizza i file runtime e ricompila lo schema.
  --teardown   Test interattivo: disabilita l'estensione col menu aperto e
               controlla che non restino processi CLI orfani.
  --all        --install, poi le verifiche e infine --teardown.
  -h, --help   Questo testo.

DELAY=8 regola i secondi prima della disabilitazione nel test --teardown.
Nessuna opzione tocca la sessione: il controllo file e' in sola lettura.
EOF
}

fail() {
    printf 'FAIL  %s\n' "$1"
    STATUS=1
}

pass() {
    printf 'OK    %s\n' "$1"
}

require_session() {
    if ! command -v gnome-extensions > /dev/null; then
        printf 'gnome-extensions non trovato: serve una sessione GNOME.\n' >&2
        exit 2
    fi
    if [ ! -d "$TARGET" ]; then
        printf '%s non installata in %s: esegui prima --install.\n' "$UUID" "$TARGET" >&2
        exit 2
    fi
}

check_files() {
    local file missing stale=0
    while IFS= read -r file; do
        if [ ! -f "$TARGET/$file" ]; then
            fail "manca $file nella copia installata"
            stale=1
        elif ! cmp -s -- "$SOURCE/$file" "$TARGET/$file"; then
            fail "diverso dal repository: $file"
            stale=1
        fi
    done < "$SOURCE/scripts/runtime-files.txt"
    if [ "$stale" -eq 0 ]; then
        pass "file runtime installati identici al repository"
    else
        printf '      Copia non aggiornata: ./scripts/session-check.sh --install, poi logout/login.\n'
    fi
}

check_state() {
    local info state
    info=$(gnome-extensions info "$UUID" 2>&1) || {
        fail "gnome-extensions info non risponde per $UUID"
        return
    }
    state=$(printf '%s\n' "$info" | sed -n 's/^ *State: *//p' | head -1)
    if [ "$state" = "ENABLED" ]; then
        pass "estensione ENABLED"
    else
        fail "stato estensione: ${state:-sconosciuto}"
        printf '      Abilita con: gnome-extensions enable %s\n' "$UUID"
        printf '      Se hai appena sincronizzato i file, fai logout/login prima di abilitare.\n'
    fi
}

check_cli() {
    if ! command -v openlogi > /dev/null; then
        fail "CLI openlogi non nel PATH"
        return
    fi
    pass "openlogi $(openlogi --version 2>/dev/null | head -1)"
    local inventory devices
    if ! inventory=$(openlogi api devices 2>/dev/null); then
        fail "openlogi api devices non ha risposto"
        return
    fi
    devices=$(printf '%s' "$inventory" | python3 -c 'import json,sys;d=json.load(sys.stdin);print(len(d["data"]["devices"]))' 2>/dev/null || printf '?')
    pass "inventario leggibile, ${devices} dispositivi (ID non stampati)"
}

check_log() {
    if ! journalctl --user -b -o cat /usr/bin/gnome-shell 2>/dev/null | grep -ci 'openlogi-companion' > /dev/null; then
        pass "nessuna riga openlogi-companion nel log della Shell"
        return
    fi
    printf 'INFO  righe openlogi-companion nel log corrente:\n'
    journalctl --user -b -o cat /usr/bin/gnome-shell 2>/dev/null | grep -i 'openlogi-companion' | tail -10 | sed 's/^/      /'
}

install_files() {
    cd "$SOURCE"
    ./scripts/sync-extension.sh
    printf '      Riavvia la sessione (logout/login): su Wayland il codice JS resta in cache.\n'
}

teardown_test() {
    require_session
    local before orphans
    before=$(gnome-extensions info "$UUID" | sed -n 's/^ *State: *//p' | head -1)
    if [ "$before" != "ENABLED" ]; then
        fail "l'estensione non e' ENABLED, test --teardown saltato"
        return
    fi
    printf 'Apri il menu dell'"'"'estensione entro %s secondi e lascialo aperto.\n' "$DELAY"
    printf 'Allo scadere il comando disabilita l'"'"'estensione e chiude il menu.\n'
    (sleep "$DELAY"; gnome-extensions disable "$UUID") &
    local job=$!
    wait "$job" || true
    sleep 1
    orphans=$(pgrep -af 'openlogi api devices' || true)
    if [ -n "$orphans" ]; then
        fail "processi CLI ancora vivi dopo il teardown:"
        printf '%s\n' "$orphans" | sed 's/^/      /'
    else
        pass "nessun processo CLI orfano dopo la disabilitazione"
    fi
    gnome-extensions enable "$UUID"
    sleep 1
    if gnome-extensions info "$UUID" | grep -q 'State: ENABLED'; then
        pass "estensione riabilitata"
    else
        fail "riabilitazione non riuscita: riabilitala a mano"
    fi
}

MAIN=0
for argument in "$@"; do
    case "$argument" in
        --install) install_files ;;
        --teardown) teardown_test ;;
        --all) install_files; require_session; check_files; check_state; check_cli; check_log; teardown_test ;;
        -h|--help) usage; exit 0 ;;
        *) printf 'Opzione sconosciuta: %s\n' "$argument" >&2; usage >&2; exit 2 ;;
    esac
    MAIN=1
done

if [ "$MAIN" -eq 0 ]; then
    require_session
    check_files
    check_state
    check_cli
    check_log
fi

exit "$STATUS"
