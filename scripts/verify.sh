#!/bin/bash
# SPDX-License-Identifier: GPL-3.0-or-later.
set -euo pipefail
SOURCE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
cd "$SOURCE"
while IFS= read -r file; do
    node --input-type=module --check < "$file"
done < <(find shell tests -name '*.js' -type f; printf '%s\n' extension.js prefs.js)
for file in scripts/*.sh tests/*.sh; do bash -n "$file"; done
python3 - <<'PY'
import json
from pathlib import Path
for name in ('metadata.json', 'tests/inventory.json'):
    json.loads(Path(name).read_text())
for path in [*Path('shell').glob('*.js'), *Path('tests').glob('*.js'), Path('extension.js'), Path('prefs.js'), Path('stylesheet.css')]:
    assert all(len(line) <= 200 for line in path.read_text().splitlines()), path
print('Syntax, JSON and JS/CSS line limits passed')
PY
gjs -m tests/test.js
bash tests/test-session-check.sh
./scripts/package.sh
# The compiled catalogue must match po/, load through the packaged domain and
# contain no untranslated or fuzzy entries; the panel falls back to English.
python3 - <<'PY'
import gettext
import json
from pathlib import Path
import subprocess

domain = json.loads(Path('metadata.json').read_text())['gettext-domain']
mo = Path('locale/it/LC_MESSAGES') / f'{domain}.mo'
assert mo.is_file(), f'missing compiled catalogue {mo}'
stats = subprocess.run(['msgfmt', '--statistics', '-o', '/dev/null', 'po/it.po'],
                       capture_output=True, text=True, check=True).stderr
assert 'untranslated' not in stats and 'fuzzy' not in stats, stats
catalogue = gettext.translation(domain, 'locale', languages=['it'])
assert catalogue.gettext('Show OpenLogi window') == 'Mostra la finestra di OpenLogi'
assert catalogue.gettext('Refresh') == 'Aggiorna'
print(f'Italian catalogue loads from {mo.parent} with domain {domain}')
PY
POT=$(mktemp /tmp/openlogi-companion-check-XXXXXX.pot)
trap 'rm -f -- "$POT"' EXIT
xgettext --language=JavaScript --keyword=_ --from-code=UTF-8 -o "$POT" \
    extension.js prefs.js shell/contract.js shell/deviceRow.js shell/indicator.js
msgcmp po/it.po "$POT"
python3 - "$POT" <<'PY'
import sys
from pathlib import Path

def msgids(path):
    """Join wrapped msgid lines so wrapping does not affect the comparison."""
    found = []
    for block in Path(path).read_text().split('\n\n')[1:]:
        ident, mode = [], None
        for line in block.splitlines():
            if line.startswith('#'):
                continue
            if line.startswith('msgid '):
                mode, ident = 'id', [line[6:]]
            elif line.startswith(('msgstr', 'msgctxt')):
                mode = None
            elif mode == 'id' and line.startswith('"'):
                ident.append(line)
        if ident:
            found.append(''.join(ident))
    return sorted(found)

committed = msgids('po/openlogi-companion.pot')
fresh = msgids(sys.argv[1])
assert committed == fresh, 'po/openlogi-companion.pot is stale'
print(f'Template in sync: {len(fresh)} messages')
PY
SHEXLI=${SHEXLI:-shexli}
"$SHEXLI" dist/openlogi-companion@giaffa86.shell-extension.zip
