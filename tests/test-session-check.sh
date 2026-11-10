#!/bin/bash
# SPDX-License-Identifier: GPL-3.0-or-later
# Session commands are mocked; this test never contacts the host Shell or CLI.
set -euo pipefail
SOURCE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
source "$SOURCE/scripts/session-check.sh"

require_session() { :; }
sleep() { :; }
pgrep() { return 1; }

gnome-extensions() {
    case "$1" in
        info)
            [ "${INFO_FAIL:-0}" -eq 0 ] || return 1
            if [ "${LC_ALL:-}" != C ] || [ "${LANGUAGE:-}" != C ]; then
                printf '  Stato: %s\n' "$MOCK_STATE"
            else
                printf '  State: %s\n' "$MOCK_STATE"
            fi ;;
        disable)
            [ "${DISABLE_FAIL:-0}" -eq 0 ] || return 1
            MOCK_STATE=${AFTER_DISABLE:-INACTIVE} ;;
        enable)
            [ "${ENABLE_FAIL:-0}" -eq 0 ] || return 1
            MOCK_STATE=${AFTER_ENABLE:-ACTIVE} ;;
        *) return 1 ;;
    esac
}

openlogi() {
    if [ "$1" = --version ]; then
        printf 'openlogi test\n'
    else
        [ "$*" = 'api devices' ] || return 1
        printf '%s\n' "$INVENTORY"
    fi
}

checks=0
run_case() {
    local name=$1 expected=$2 action=$3 output
    shift 3
    output=$(
        STATUS=0
        MOCK_STATE=ACTIVE
        export LC_ALL=C LANGUAGE=it
        for assignment in "$@"; do
            export "$assignment"
        done
        "$action"
        [ "$STATUS" -eq "$expected" ]
    ) || { printf 'FAIL %s\n%s\n' "$name" "$output"; exit 1; }
    if [ "$action" = teardown_test ] && [ "$expected" -ne 0 ]; then
        if [[ "$output" == *'test --teardown interrotto'* ]] &&
            [[ "$output" != *'estensione riabilitata'* ]]; then
            printf 'FAIL %s: ripristino non verificato\n%s\n' "$name" "$output"
            exit 1
        fi
        if [[ "$output" == *'nessun processo CLI orfano'* ]] &&
            [[ "$output" != *'riabilitazione non riuscita'* ]]; then
            printf 'FAIL %s: teardown falsamente riuscito\n%s\n' "$name" "$output"
            exit 1
        fi
    fi
    checks=$((checks + 1))
}

run_case 'ACTIVE with Italian locale' 0 check_state
run_case 'INACTIVE rejected' 1 check_state MOCK_STATE=INACTIVE
run_case 'Info command failure' 1 check_state INFO_FAIL=1
run_case 'Valid inventory' 0 check_cli \
    'INVENTORY={"schema_version":1,"ok":true,"data":{"inventory":"ready","devices":[]}}'
run_case 'Malformed JSON' 1 check_cli INVENTORY=invalid-json
run_case 'Missing data' 1 check_cli 'INVENTORY={}'
run_case 'Devices must be an array' 1 check_cli \
    'INVENTORY={"schema_version":1,"ok":true,"data":{"inventory":"ready","devices":{}}}'
run_case 'API error envelope' 1 check_cli \
    'INVENTORY={"schema_version":1,"ok":false,"data":{"inventory":"ready","devices":[]}}'
run_case 'Unsupported schema' 1 check_cli \
    'INVENTORY={"schema_version":2,"ok":true,"data":{"inventory":"ready","devices":[]}}'
run_case 'Successful teardown and restore' 0 teardown_test
run_case 'Disable command failure' 1 teardown_test DISABLE_FAIL=1
run_case 'Disable did not deactivate' 1 teardown_test AFTER_DISABLE=ACTIVE
run_case 'Enable command failure' 1 teardown_test ENABLE_FAIL=1
run_case 'Enable did not activate' 1 teardown_test AFTER_ENABLE=ERROR
printf '%s session-check checks passed (mock commands)\n' "$checks"
