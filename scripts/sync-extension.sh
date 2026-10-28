#!/bin/bash
# Generated with AI for personal use. GPL-3.0-or-later.
set -euo pipefail
SOURCE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
TARGET="${HOME}/.local/share/gnome-shell/extensions/openlogi-companion@giaffa86"
cd "$SOURCE"
mkdir -p locale/it/LC_MESSAGES
msgfmt --check po/it.po -o locale/it/LC_MESSAGES/openlogi-companion.mo
while IFS= read -r file; do
    mkdir -p -- "$TARGET/$(dirname -- "$file")"
    cp -- "$file" "$TARGET/$file"
done < scripts/runtime-files.txt
glib-compile-schemas --strict "$TARGET/schemas"
printf '%s
' "Installed in $TARGET. Enable manually; first install on Wayland may require logout/login."
