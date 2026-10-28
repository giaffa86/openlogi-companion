#!/bin/bash
# Generated with AI for personal use. GPL-3.0-or-later.
set -euo pipefail
gnome-shell --headless --virtual-monitor 1280x720 --debug-control > "$SANDBOX/shell.log" 2>&1 &
SHELL_PID=$!
trap 'kill "$SHELL_PID" 2>/dev/null || :; wait "$SHELL_PID" 2>/dev/null || :' EXIT
python3 "$SOURCE/tests/nested-check.py" | tee "$SANDBOX/results.txt"
