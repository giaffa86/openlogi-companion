# OpenLogi Companion

An independent companion for GNOME Shell 50: a panel indicator shows the devices
reported by the [OpenLogi](https://github.com/AprilNEA/OpenLogi) agent and their
battery levels. An experimental project created for personal use, independent
of OpenLogi. Licensed under [GPL-3.0-or-later](LICENSE).

The project mark is a mouse inside an open circle. The panel uses a
[symbolic SVG icon](icons/openlogi-companion-symbolic.svg) that follows the GNOME
theme; the [transparent logo and AI provenance](assets/branding/README.md) are
kept outside the runtime package. The [square EGO listing icon](assets/ego/README.md)
is generated from the same mark.

**Experimental status:** automated tests use synthetic devices. Two real devices
(MX Master and MX Keys) have been observed, including inventory, battery readings
and a percentage comparison with OpenLogi's device page. Launching the GUI when
closed or minimized and accessibility checks remain untested. Other models are
not available to the author and are not claimed to be compatible. Only GNOME
Shell 50 is supported.

Publication on extensions.gnome.org is planned but **depends on** the remaining
checks in [OPEN_ITEMS.md](docs/OPEN_ITEMS.md) (OL-002, OL-003, OL-005). Local
commits and the remote source repository precede that step.

The [source repository](https://github.com/giaffa86/openlogi-companion) is public
with the author's authorization of November 10, 2026. This does not close the
remaining checks or authorize an early release or EGO submission; see the
[limitations and resumption checklist](docs/OPEN_ITEMS.md).

**Device rows display information only; pin buttons remain active.**
**Show OpenLogi window** opens or activates the general window; select the device
page inside the app. The source review was updated to v0.9.0 on November 10,
2026: no supported public action for selecting a device was found. See the
[limitations and upstream proposal](docs/OPEN_ITEMS.md).

## Trademarks and independence

This project is independent, with no affiliation, sponsorship or endorsement
from OpenLogi, Logitech or the GNOME Project. “OpenLogi” is used descriptively to
identify the app whose inventory the extension reads, and appears in the name
chosen by the author to make the companion recognizable.

- The original mark, a mouse inside an open circle, was generated with AI
  assistance. It does not reproduce Logitech, OpenLogi or GNOME logos.
- The runtime bundle contains no third-party logos, icons, screenshots or
  other media. The repository keeps an OpenLogi GUI screenshot only as
  verification evidence, not for promotional use or EGO upload. `LICENSE` is
  the only third-party text distributed.
- Device trade names (`MX Master`, `MX Keys`, etc.) come from the OpenLogi CLI at
  runtime and are not included in the package.
- The EGO listing will use the same independence statement as the `description`
  in `metadata.json`.

## Requirements and behavior

Fedora, GNOME Shell 50, GJS, the OpenLogi RPM with its `openlogi api devices` CLI,
an agent reachable under the same profile as the CLI, and the `openlogi.desktop`
launcher are required. The contract was checked against OpenLogi tag v0.8.18,
JSON schema 1. The real CLI observed on October 30, 2026 was `openlogi 0.8.19`,
which returned schema 1. There is no compatibility promise for every device
visible in the GUI: the API inventory includes lights without batteries, but
not webcams. Two real devices have been observed (MX Master and MX Keys);
G515 and Keys-To-Go 2 have not been tested.

The indicator initially shows only the extension icon. In **Extension
preferences**, you can show multiple pinned devices in the panel, each with its
own kind icon (mouse, keyboard, etc.) and battery reading. **Show battery as a
bar** switches between a numeric percentage (the default) and a proportional
vertical bar: green above 20%, amber at 20% or below, red at 10% or below.
`0%` shows an empty track. A missing percentage produces no bar; qualitative
levels are never converted into a made-up value. The menu and accessible names
retain the battery details in bar mode.

Each row's pin button adds or removes that device independently. Panel order
follows pin selection order. Pinning requires a currently unique ID and an
online device with battery support; it does **not** require a valid reading.
A charging device without a percentage can therefore remain pinned and shows
at least its kind icon. **Hide the extension icon when devices are pinned** lets
the pinned devices replace the companion mark, while their kind icons identify
them.

No average is calculated. Null or duplicate IDs do not hide inventory rows,
but prevent panel selection. Selections stay in memory: disappearance,
disconnection, an ambiguous ID or loss of battery support removes only the
affected pin. An error, a new scan or disabling the extension clears all pins.
These are not persistent hardware identities; selections do not survive route
changes.

Data refreshes when the extension is enabled, when the menu opens and through
**Refresh**. While the menu is open, polling runs every 5 seconds, so battery
and connection changes appear without closing it. After errors, the delay rises
to 10, 20, 40 and at most 60 seconds. With the menu closed, only the panel
preference enables polling: every 60 seconds, even before a device is selected,
with delays of 120, 240, 480 and at most 900 seconds after errors. Concurrent
requests are coalesced. With the menu closed and the preference off, there are
no polling timers.

**Hide the extension icon when devices are pinned** hides the mark only while
at least one pinned device is actually shown. Kind icons and individual battery
readings remain. If no pinned device is shown (no pins, the panel preference is
off, ambiguous rows, offline devices or inventory not ready), the mark returns,
so the panel button is never empty.

The interface supports English, Italian, Spanish, German and French. English
is the source language and fallback; translations follow the session language.
Editable catalogues live in `po/`; only compiled `locale/*/LC_MESSAGES/*.mo`
files enter the runtime bundle. Build tools require gettext and Python 3.
`scripts/i18n.sh update` refreshes the template and catalogues after UI edits;
`scripts/i18n.sh compile` compiles them; `scripts/i18n.sh check` checks source
coverage, completeness, format placeholders and compiled catalogue equality.
Packaging and `scripts/verify.sh` run these checks automatically.

Connected devices appear first, then names are sorted according to the locale.
Rows stay separate even when names or IDs match. Unchanged rows are reused to
preserve focus. The list scrolls, long names are truncated, and styling and
focus indicators follow the Shell theme. Percentages follow the locale.

Loading, scanning, unavailable inventory, no devices, missing CLI, unreachable
agent, incompatibility and invalid data are distinct states. Only an empty
`ready` inventory means no devices. Scanning and errors remove previous rows.
An offline device never presents its old battery reading as current. Missing
values do not become zero; qualitative levels do not become percentages. The
extension does not duplicate low-battery notifications.

## Local installation

Download or clone the repository and open a terminal at its root, containing
`metadata.json`. All commands below run from that directory. Compiling
translations and schemas requires `msgfmt` and `glib-compile-schemas` (provided
by `gettext` and `glib2` on Fedora).

```bash
./scripts/sync-extension.sh
gnome-extensions enable openlogi-companion@giaffa86
```

The script copies only runtime files and compiles the schema in
`~/.local/share/gnome-shell/extensions/openlogi-companion@giaffa86/`.
It does not reload the extension, install packages or run sudo commands. The
first installation may require logout/login; Wayland's module cache may also
require it after changes. The script never interrupts the session automatically.

Alternatively, build and install the local package. Creating it also requires
`zip`, and checking its contents requires Python 3:

```bash
./scripts/package.sh
gnome-extensions install --force dist/openlogi-companion@giaffa86.shell-extension.zip
```

The bundle preserves `shell/`, the schema XML, Italian catalogue and license.
The compiled schema is excluded and is built by the extension installer. The
bundle contains no prompts, tests, scripts, working documentation or personal
data.

To remove only the companion:

```bash
gnome-extensions disable openlogi-companion@giaffa86
gnome-extensions uninstall openlogi-companion@giaffa86
```

These operations do not uninstall OpenLogi, stop its agent or delete hardware
configuration. For a manual copy not registered with the installer, disable it
and remove only the user extension directory for the UUID shown above.

## Verification and development

Run from the repository root. Full verification requires Node (syntax parsing
only), GJS, Python 3, Bash, `zip`, GLib and gettext tools (`msgfmt`, `msgcmp`,
`xgettext`), and Shexli. The tested scanner combination is Shexli 0.2.1 with
tree-sitter 0.25.2 and tree-sitter-javascript 0.25.0. To prepare the scanner in
an isolated Python environment:

```bash
python3 -m venv /tmp/shexli-venv
/tmp/shexli-venv/bin/pip install shexli==0.2.1 tree-sitter==0.25.2 tree-sitter-javascript==0.25.0
```

Then run:

```bash
# Node is only a syntax checker, not a runtime toolchain.
SHEXLI=/tmp/shexli-venv/bin/shexli ./scripts/verify.sh
# Separate environment with synthetic inventory and GUI application:
./tests/nested.sh
# Rebuild the bundle:
./scripts/package.sh
```

The isolated test requires `dbus-run-session`, GNOME Shell with headless and
virtual-monitor support, `gdbus`, Python 3 with PyGObject/GTK4 and an available
renderer. It creates a bus, settings, fake launcher and runtime copies under
`/tmp`. It does not expose the host bus or use the real OpenLogi app for GUI
tests. Evidence remains in the directory printed at startup. Unsafe Eval
control is enabled by a small extension present **only in the test copy**,
never in the package.

For interactive testing, use a separate development session:
`dbus-run-session -- gnome-shell --devkit` (requires `mutter-devkit`). An
isolated bus does not automatically see the host agent; do not connect the two
buses to bypass isolation. See [VERIFICATION.md](docs/VERIFICATION.md) for
results, commands, versions, unperformed checks and sandbox limitations.

In the real session, with the extension already installed:

```bash
# Read only: compare installed files with the repository, state, CLI and logs.
./scripts/session-check.sh
# Update the installed copy, then log out/in on Wayland.
./scripts/session-check.sh --install
# Interactive test: disable with the menu open and check for orphan processes.
DELAY=8 ./scripts/session-check.sh --teardown
```

These commands affect the user's session and are not run by `verify.sh` or
`tests/nested.sh`.

## Data flow

```text
OpenLogi agent (current profile)
  → Official CLI: openlogi api devices
  → Provider: two asynchronous pipes, timeout and shared limit
  → Schema 1 validation and stable sorting
  → Shell menu, with kind icons and batteries for devices pinned in memory

Show OpenLogi window → window from the openlogi.desktop launcher
  → Main.activateWindow if one exists, Shell.App.activate to launch it
GTK/Adw preferences → GSettings: only show-percentage, battery-bar and hide-logo
```

The provider starts only the read-only CLI with fixed arguments. It does not
start the agent, open HID devices, read `config.toml` or decode internal IPC.
The timeout is 5 seconds, with a shared stdout+stderr budget of 1 MiB and reads
of at most 8192 bytes; a chunk that exceeds the limit stops the request. Stderr
is drained without being retained. On timeout, limit breach or teardown, reads
are cancelled and only the owned CLI child is terminated and reaped. No
snapshot or ID is stored in GSettings, files or logs. A GUI opened by the user
is independent of extension teardown.

The code was developed with AI assistance. Provenance is documented here, in
[AI_REVIEW_GUIDELINES.md](AI_REVIEW_GUIDELINES.md) and in `docs/`. Source and
runtime files contain no AI notices or prompts; they carry only the SPDX
`GPL-3.0-or-later` identifier, because EGO reviews treat such comments as
indicators of generated code. Maintenance requires understanding the JavaScript;
Shexli does not certify EGO acceptance.

The repository contains source, translations, tests, scripts and documentation.
The installable bundle includes only files listed in `scripts/runtime-files.txt`;
it excludes tests, scripts, documentation and the compiled schema. ZIPs, compiled
catalogues and other local artifacts are not versioned; scripts regenerate them.

Remaining checks and the resumption checklist are in
[OPEN_ITEMS.md](docs/OPEN_ITEMS.md). The [upstream plan](docs/UPSTREAM_PLAN.md)
describes the proposed direct device selection; no issue or PR has been sent
by this project.

Language verification: [docs/LOCALIZATION.md](docs/LOCALIZATION.md).
