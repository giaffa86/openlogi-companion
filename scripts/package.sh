#!/bin/bash
# SPDX-License-Identifier: GPL-3.0-or-later.
set -euo pipefail
SOURCE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
cd "$SOURCE"
mkdir -p locale/it/LC_MESSAGES
msgfmt --check po/it.po -o locale/it/LC_MESSAGES/openlogi-companion.mo
glib-compile-schemas --strict --dry-run schemas
mkdir -p dist
ARCHIVE="$SOURCE/dist/openlogi-companion@giaffa86.shell-extension.zip"
# Rebuild from scratch so a previous archive cannot retain removed files.
rm -f -- "$ARCHIVE"
zip -q "$ARCHIVE" -@ < scripts/runtime-files.txt
python3 tests/check-package.py "$ARCHIVE"
