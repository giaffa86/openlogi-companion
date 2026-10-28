#!/bin/bash
# Generated with AI for personal use. GPL-3.0-or-later.
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
./scripts/package.sh
POT=$(mktemp /tmp/openlogi-companion-check-XXXXXX.pot)
trap 'rm -f -- "$POT"' EXIT
xgettext --language=JavaScript --keyword=_ --from-code=UTF-8 -o "$POT" \
    extension.js prefs.js shell/contract.js shell/deviceRow.js shell/indicator.js
msgcmp po/it.po "$POT"
SHEXLI=${SHEXLI:-shexli}
"$SHEXLI" dist/openlogi-companion@giaffa86.shell-extension.zip
