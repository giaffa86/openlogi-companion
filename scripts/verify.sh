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
SHEXLI=${SHEXLI:-shexli}
"$SHEXLI" dist/openlogi-companion@giaffa86.shell-extension.zip
