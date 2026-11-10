#!/bin/bash
# SPDX-License-Identifier: GPL-3.0-or-later.
# Isolated synthetic session. Never bridges the host D-Bus address.
set -euo pipefail
SOURCE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
SANDBOX=$(mktemp -d /tmp/openlogi-nested-XXXXXX)
printf '%s\n' "Evidence directory: $SANDBOX"
mkdir -p "$SANDBOX"/{data/gnome-shell/extensions,config,runtime,bin}
chmod 700 "$SANDBOX/runtime"
UUID=openlogi-companion@giaffa86
TARGET="$SANDBOX/data/gnome-shell/extensions/$UUID"
mkdir -p "$TARGET" "$SANDBOX/data/applications"
cat > "$SANDBOX/data/applications/openlogi.desktop" <<'EOF'
[Desktop Entry]
Type=Application
Name=Masked OpenLogi for isolated tests
Hidden=true
EOF
while IFS= read -r file; do
    mkdir -p "$TARGET/$(dirname -- "$file")"
    cp "$SOURCE/$file" "$TARGET/$file"
done < "$SOURCE/scripts/runtime-files.txt"
glib-compile-schemas --strict "$TARGET/schemas"
mkdir -p "$SANDBOX/data/gnome-shell/extensions/openlogi-test@local"
cat > "$SANDBOX/data/gnome-shell/extensions/openlogi-test@local/metadata.json" <<'EOF'
{"uuid":"openlogi-test@local","name":"Isolated test control","description":"Test only","shell-version":["50"]}
EOF
cat > "$SANDBOX/data/gnome-shell/extensions/openlogi-test@local/extension.js" <<'EOF'
import {Extension} from 'resource:///org/gnome/shell/extensions/extension.js';
export default class Test extends Extension {
    enable() { global.context.unsafe_mode = true; }
    disable() { global.context.unsafe_mode = false; }
}
EOF
cp "$SOURCE/tests/fake-cli.py" "$SOURCE/tests/inventory.json" "$SANDBOX/bin/"
ln -s "$SANDBOX/bin/fake-cli.py" "$SANDBOX/bin/openlogi"
chmod +x "$SANDBOX/bin/fake-cli.py"
export XDG_DATA_HOME="$SANDBOX/data" XDG_CONFIG_HOME="$SANDBOX/config" XDG_RUNTIME_DIR="$SANDBOX/runtime"
export GSETTINGS_BACKEND=keyfile
export LANG=C.UTF-8 LANGUAGE=C
export PATH="$SANDBOX/bin:$PATH"
export SOURCE SANDBOX
# keyfile backend settings are confined to XDG_CONFIG_HOME.
gsettings set org.gnome.shell enabled-extensions "['openlogi-test@local', '$UUID']"
# Suppress the first-run modal only in this private profile so captures show UI.
NESTED_SHELL_VERSION=$(gnome-shell --version)
gsettings set org.gnome.shell welcome-dialog-last-shown-version "${NESTED_SHELL_VERSION##* }"
timeout 90 dbus-run-session -- bash "$SOURCE/tests/nested-inner.sh"
