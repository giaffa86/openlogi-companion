#!/bin/bash
# SPDX-License-Identifier: GPL-3.0-or-later.
set -euo pipefail
SOURCE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
TARGET="${HOME}/.local/share/gnome-shell/extensions/openlogi-companion@giaffa86"
cd "$SOURCE"
./scripts/i18n.sh compile
while IFS= read -r file; do
    mkdir -p -- "$TARGET/$(dirname -- "$file")"
    cp -- "$file" "$TARGET/$file"
done < scripts/runtime-files.txt
glib-compile-schemas --strict "$TARGET/schemas"
printf '%s
' "Installed in $TARGET. Enable manually; first install on Wayland may require logout/login."
