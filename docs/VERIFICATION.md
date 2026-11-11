# Local verification

Entries record the state at the time of each check. Earlier results and
publication decisions are historical; later entries and `OPEN_ITEMS.md` describe
the current limitations.

## GitHub synchronization authorization, November 10, 2026

Note updated with AI assistance. After creating the public repository
`https://github.com/giaffa86/openlogi-companion.git`, the author explicitly
requested synchronization with the local project. The GitHub connector confirmed
repository access, push permissions and no branches before the first push.
The request authorizes source commits and pushes, superseding the postponement
recorded in historical sections.

README, `AGENTS.md` and `OPEN_ITEMS.md` were updated to distinguish source
publication from releases and EGO submission, which still depend on remaining
checks. The extension's verification remains that of the latest change:
64 GJS checks, 14 session-script checks, 94 isolated Shell checks and clean
Shexli output. Synchronization adds no hardware coverage and does not install or
reload the host session. ZIPs, generated files, private notes and local
configuration remain excluded through `.gitignore`; the runtime bundle retains
its explicit manifest.

## Read-only device rows, November 10, 2026

Change made with AI assistance at the author's request: disable device clicks,
which are misleading until contextual opening is available.

- `DeviceRow` no longer receives an opening callback or connects `activate`.
  Rows use `reactive: false` and `can_focus: false`; the GNOME component also
  disables the click gesture and hover. Pins retain reactivity and focus without
  disabling child controls.
- Row accessible text describes the device and state. Each pin also announces
  its device name and battery, preserving context when focus goes directly to
  the button.
- General opening remains available through **Show OpenLogi window**. The menu
  message, metadata, README and Italian catalogue were updated (40 messages).
- Persistent reminder in `AGENTS.md` and OL-001 of `OPEN_ITEMS.md`: recheck future
  releases and upstream issue #1375; consider contributing to that request
  before opening another one. No upstream GitHub message was sent.

Checks performed:

- `SHEXLI=/tmp/shexli-venv/bin/shexli ./scripts/verify.sh`: 64 GJS checks,
  14 session-script checks, ZIP matching the manifest, Italian catalogue and
  template aligned on 40 messages; Shexli reported no findings, errors or warnings.
- `./tests/nested.sh`: **94 Shell checks** passed with a synthetic backend.
  Covered non-reactive rows, disabled row focus/hover and click gestures, pin
  accessible names and button focus in all four light/dark theme and text-scale
  1/1.5 combinations. Multiple pins, battery bars and synthetic GUI launch and
  activation checks also remained passing.
- Evidence in `/tmp/openlogi-nested-5tPXlH`; no JavaScript or theme parsing errors
  in the Shell log. The previous run's light menu at text scale 1.5 was visually
  inspected (`/tmp/openlogi-nested-YYR5Gi`): no row highlight, informative text
  and a visible pin focus indicator. The final run adds only device context to
  button accessible names.
- Updated package at
  `dist/openlogi-companion@giaffa86.shell-extension.zip`, containing only runtime
  resources from the manifest. No tests, local documentation or compiled schema.

No installation or reload in the host session, and no publication during this
change. Real hardware, screen reader and DPI checks remain open in `OPEN_ITEMS.md`.

## Contextual opening, OpenLogi 0.9.0 review, November 10, 2026

Review updated with AI assistance at the author's request. The local version
is `openlogi 0.9.0`, RPM `openlogi-0.9.0-1.x86_64`. Official source was read at
tag v0.9.0 rather than inferred from the development branch:

- [Release v0.9.0](https://github.com/AprilNEA/OpenLogi/releases/tag/v0.9.0),
  published November 3, 2026, listed commit `a5b507e`.
- [`brand.rs`](https://github.com/AprilNEA/OpenLogi/blob/v0.9.0/crates/openlogi-core/src/brand.rs):
  `DeeplinkCommand` offers only Show, OpenSettings, OpenAbout, CheckForUpdates
  and Quit. It contains no device identifier or selection command. `parse_url`
  ignores paths and queries, so `show?device=…` is still a plain Show.
- [`main.rs`](https://github.com/AprilNEA/OpenLogi/blob/v0.9.0/crates/openlogi-desktop/src/main.rs):
  single-instance guard exits if the GUI is already running, without URL
  forwarding; no argument parsing for opening a device.
- [`openlogi.desktop`](https://github.com/AprilNEA/OpenLogi/blob/v0.9.0/packaging/linux/desktop/openlogi.desktop):
  `Exec=openlogi-desktop`, without `%u`, a MIME handler or a per-device action.
  Also confirmed by reading the installed launcher in `/usr/share/applications`.
- [CLI documentation](https://github.com/AprilNEA/OpenLogi/blob/v0.9.0/docs/USAGE.md):
  no documented GUI navigation by device. Hardware API selectors do not provide
  a navigation action.
- [Issue #1375](https://github.com/AprilNEA/OpenLogi/issues/1375): an equivalent
  request already exists; its state and comment were read through the GitHub
  connector. No issue, PR or reply was sent.

Result: v0.9.0 does not add the requested contextual opening. The companion
continues to open the general window. OL-001 and checklist item 3 in
`OPEN_ITEMS.md` were updated. The existing upstream request must be considered
before proposing an API.

Only documentation review and local version, RPM and desktop-file reads were
performed. No hardware diagnostics, OpenLogi changes or GUI activation. Remaining
real-world checks in OL-002 stay open. No companion runtime or existing ZIP
changes; runtime tests did not need repeating for this documentation update.

## Battery bars and multiple pins, November 10, 2026

Change made with AI assistance for personal use, at the author's request with
a visual reference showing a keyboard and mouse side by side in the panel.

- Pins become independent selections in an in-memory `Set`, in selection order.
  Each device has its own icon and reading; no averaging or ID persistence.
  Removing one pin leaves the others unchanged.
- The Boolean UI key `battery-bar`, default `false`, switches percentages to
  proportional vertical bars. Existing `show-percentage` and `hide-logo`
  preferences are preserved. Text and Italian catalogue updated for multiple
  devices (41 messages).
- Bars are green above 20%, amber at 20% or below, red at 10% or below. `0%`
  shows an empty track; a missing reading produces no bar. Qualitative levels
  and charging status remain in details and accessible names without invented
  percentages. A charging device without a reading keeps its icon.
- Panel actors are reused during refresh and mode changes, destroyed when
  removed and released on teardown. Disappearance, disconnection, an ambiguous
  ID or loss of battery support removes only that device's pin; errors,
  scanning or disabling clear all selections.
- The runner suppresses the welcome dialog only in its temporary GSettings
  profile so it does not obscure captures.

Checks performed:

- `SHEXLI=/tmp/shexli-venv/bin/shexli ./scripts/verify.sh`: 64 GJS checks,
  14 session-script checks, ZIP from the explicit manifest, translations and
  template aligned. Shexli 0.2.1 with tree-sitter 0.25.2/0.25.0 reported no
  findings, errors or warnings. Scanner installed only in a temporary `/tmp` venv.
- `./tests/nested.sh`: **92 Shell checks** passed with a synthetic backend.
  Covered three simultaneous pins, independent removal, order, actor reuse,
  live numeric/bar switching, zero and missing readings, full and proportional
  fill, color thresholds, restoration after hiding, selective removal of
  absent/offline/ambiguous devices and cleanup with two active pins. Bars also
  visible with light/dark themes at text scales 1 and 1.5.
- Final evidence in `/tmp/openlogi-nested-PJR4Q7`; the keyboard/mouse panel and
  preferences were visually inspected. No JavaScript or theme parsing errors
  in the Shell log; previously observed AT-SPI/PipeWire/Adw environment warnings
  remain. The sandbox initially prevented creating a D-Bus socket; the runner
  succeeded with authorized execution while keeping its bus and profile
  separate from the host session.

No installation or reload in the host session, or remote publication during
this change. The new mode and multiple pins have not been tested with real
devices. `OPEN_ITEMS.md` limitations remain, including real GUI launch/restore,
screen reader, fractional DPI and multiple monitors.

## Preference to hide the panel mark, October 31, 2026

Change made with AI assistance for personal use, at the author's request to
hide the extension logo in the top bar while a device is pinned.

- Added Boolean GSettings key `hide-logo`, default `false`, independent of
  `show-percentage`; no device data is saved.
- `prefs.js` adds a second `Adw.SwitchRow`, bound with
  `Gio.SettingsBindFlags.DEFAULT`, without manually managed GTK signal cleanup.
- `shell/indicator.js` retains a reference to the mark icon (`this._logo`),
  cleared in `destroy()`. The mark is hidden only while the pinned device is
  **actually shown**; otherwise the button would be empty. The button retains
  an accessible name containing the device name and percentage.
- The preferences signal changes from `changed::show-percentage` to `changed`,
  letting both keys update the panel and timer through a single handler.
- Italian translation expanded to 39 messages; template regenerated.

Checks performed:

- `SHEXLI=/tmp/shexli-venv/bin/shexli ./scripts/verify.sh` passed: syntax,
  line limits, 64 GJS checks, 14 session-script checks, ZIP from the manifest,
  Italian catalogue loading and template aligned on 39 messages. Shexli 0.2.1
  with tree-sitter 0.25.2/0.25.0 reported no findings, errors or warnings; the
  `/tmp` venv was recreated with pinned versions.
- `./tests/nested.sh`: **63 Shell checks**, previously 56. New coverage: mark
  hidden with a pinned, visible device; accessible name preserved; logo restored
  when the preference is off; live application without manual refresh; logo
  always present for ambiguous IDs, offline devices or `show-percentage` off.
- Evidence in `/tmp/openlogi-nested-0k0qDv`: `pinned-percentage.png` shows mark,
  keyboard icon and `0%`; `pinned-no-logo.png` shows keyboard and `100%` without
  the mark. Panel crops were inspected.
- No installation or reload in the host session.

At this checkpoint, the unchanged `OPEN_ITEMS.md` list still included numeric
GUI battery comparison, closed/minimized app clicks, window grouping, screen
reader accessibility and DPI/multiple monitors. The new preference was not
tested with real connected devices.

## Session-script review fixes, October 30, 2026

Changes made with AI assistance after reviewing local commits:

- Centralized state reading with `LC_ALL=C LANGUAGE=C`, comparing
  `ACTIVE`/`INACTIVE` rather than `ENABLED`.
- Unreadable JSON, unsuccessful envelopes, incompatible schema or inventory
  without a device array produce `FAIL`, without a `?` count.
- Teardown checks both the `disable` result and the `INACTIVE` state before
  looking for processes, then attempts restoration and verifies `ACTIVE`.
  Re-enabling errors also produce `FAIL`.

`tests/test-session-check.sh`, included in `scripts/verify.sh`, covers 14 cases
with mocked commands, without contacting the host Shell or real CLI. The session
script is sourced only for its functions. These checks do not close the hardware
and real-session limitations in `OPEN_ITEMS.md`.

Checks performed: `SHEXLI=/tmp/shexli-venv/bin/shexli ./scripts/verify.sh` passed
(64 GJS checks, 14 script checks, ZIP and translations; Shexli without findings,
errors or warnings). `./tests/nested.sh`: 56 Shell checks passed with a synthetic
backend; evidence in `/tmp/openlogi-nested-nas5FZ`, with previously known
AT-SPI/PipeWire/Adw environment warnings. No installation or reload in the host
session.

## Session script and installation state, October 30, 2026

Added `scripts/session-check.sh` for manual checks, deliberately separate from
`verify.sh` and `tests/nested.sh` because it installs files and disables/re-enables
the extension in the author's session:

- Without arguments, it compares each file in `scripts/runtime-files.txt` with
  the installed copy, then reports state, CLI version, device count (without
  IDs) and relevant log lines.
- `--install` rebuilds the `.mo` and synchronizes runtime files.
- `--teardown` disables the extension after `DELAY` seconds with the menu open,
  checks for remaining `openlogi api devices` processes and re-enables it.
- `--all` runs the steps in sequence; `-h` shows usage.

First real-session run: every installed file differed from the repository,
showing that the installed copy predated that day's fixes. This explains why
live refresh was not visible and pinning still followed the old percentage
rule. Reported state: `Enabled: No`, `State: INACTIVE`, with no system-wide
installation. The extension was disabled when checked.

The same run reported `openlogi --version` as `openlogi 0.8.19`, not 0.8.18, and
a readable real inventory of 2 devices with schema 1. The contract remains
verified against tag v0.8.18; no additional 0.8.19 hardware coverage was claimed.

## Panel pin and kind icon, October 30, 2026

Author-reported defect: the mouse pin had disappeared from its row. Cause:
`pinnable` required `battery.percentage !== null`, so a charging device without
a reading (`Battery unavailable · Charging`) lost its pin even though the
selection remained valid.

Fix:

- Pin availability now depends only on selection eligibility: a unique ID,
  an online device and battery support (`battery !== null`). Missing readings
  do not hide it. The kind icon is always shown; the percentage only when present.
- After the extension icon, the panel shows the pinned device's kind icon
  (mouse, keyboard, etc.) and percentage when available. The button's accessible
  name includes the device name and value.
- Kind icon mapping is centralized in `shell/deviceRow.js` (`kindIcon`), used
  by both rows and the panel.
- Updated strings: “Show the pinned device in the panel” (preference), “Remove
  this device from the panel” (pin), “Select a device in OpenLogi. Pin a device
  in the panel for this session.” (menu header), and the GSettings description.
  Italian translation expanded to 37 messages.
- Synthetic fixture extended with `charging-no-reading`, a charging mouse
  without a percentage, to cover the regression.

Checks:

- `SHEXLI=/tmp/shexli-venv/bin/shexli ./scripts/verify.sh`: 64 GJS checks,
  previously 61; ZIP, Italian catalogue, template and Shexli all passed.
- `./tests/nested.sh`: **56 Shell checks**, previously 48. New coverage: visible,
  reactive pin without a reading; pin surviving refresh; no pin without battery
  support; correct kind icon with and without a percentage; panel accessible name.
- Evidence: `/tmp/openlogi-nested-i6QndI/pinned-kind-icon.png` shows a mouse icon
  without a percentage; `pinned-percentage.png` shows a keyboard with `0%`.
  Panel crops were inspected.

## Symbolic panel icon, October 30, 2026

Author-reported defect: a white dot appeared instead of the panel mark.
Reproduced by enlarging the real-session screenshot.

Cause: the SVG used two paths with `stroke` and `fill="none"`. Shell/GTK symbolic
recoloring forces `fill` on every path, filling the circle arc into a solid disc
that covered the mouse.

Fix in `icons/openlogi-companion-symbolic.svg`:

- Circle represented by a closed ring (two arcs, `fill-rule="evenodd"`), no stroke.
- Mouse represented by a capsule with a wheel cutout in the same path using evenodd.
- One color, `#2e3436`, replaced by the theme. The file name and path stay the
  same, so the runtime manifest is unchanged.

Checks:

- Raster rendering at 16, 22 and 32 px inspected: distinct ring and mouse, no merging.
- `./tests/nested.sh`: 48 checks passed, screenshots in
  `/tmp/openlogi-nested-LViwg2`. Panel crops inspected with light and dark themes
  at text scale 1; the icon is recognizable in both, unlike the previous disc.
- `tests/check-package.py` now rejects `-symbolic.svg` icons with `stroke` or
  `fill="none"` to prevent regression.
- `SHEXLI=/tmp/shexli-venv/bin/shexli ./scripts/verify.sh` passed.

The square EGO listing icon is a PNG and is unaffected by this defect.

## EGO icon and branding, October 30, 2026

Change made with AI assistance for personal use.

- `scripts/make-ego-icon.py` generates `assets/ego/icon-256.png` and `icon-128.png`
  from the existing logo: rounded dark background (22% radius) with a light
  emblem at 66% of the side, readable on light and dark EGO listings. The logo
  and symbolic Shell SVG were not changed.
- `assets/ego/README.md` documents regeneration and use. `assets/` is outside
  the runtime manifest, so the listing icon is not included in the ZIP.
- README now has a “Trademarks and independence” section: no affiliation,
  original mark, no third-party media in the repository or bundle, and device
  trade names supplied only at runtime.
- Both sizes visually checked: centered emblem, regular margins, no resizing
  artifacts.

`verify.sh` is unaffected: no runtime or test files changed. `nested.sh` was
not rerun for this change.

## Review cleanup, October 30, 2026

Change made with AI assistance for personal use at the author's explicit
request, overriding the previous rule to retain AI notices in generated files.

- Removed `Generated with AI for personal use` and
  `Do NOT upload to extensions.gnome.org` comments from runtime, test, script
  and CSS headers. EGO reviews list them as indicators of AI output. Only
  `SPDX-License-Identifier: GPL-3.0-or-later` remains.
- AI provenance retained in documentation: `README.md`,
  `AI_REVIEW_GUIDELINES.md`, `AGENTS.md`, `assets/branding/README.md` and this
  file. Project rules updated accordingly.
- `metadata.json`: removed deprecated `version`, assigned by EGO; added `url`
  for the planned repository and expanded requirements, read-only behavior,
  click behavior and independence in the description.
- `tests/check-package.py` now rejects a bundle with `version` or without an
  `https://` URL.

Known limitation at this checkpoint: `url` pointed to
`https://github.com/giaffa86/openlogi-companion`, which did not yet exist.
The repository had to be created before any EGO upload.

Checks: `SHEXLI=/tmp/shexli-venv/bin/shexli ./scripts/verify.sh` passed (syntax,
61 GJS checks, ZIP from the manifest, Italian catalogue, template and Shexli
without findings). `./tests/nested.sh` was not rerun because `shell/`, UI and
polling were unchanged.

## Real session and menu refresh, October 30, 2026

Change made with AI assistance for personal use, based on the author's
observations in a GNOME Shell 50 session with real devices connected.

### Real-session observations

- Real inventory arrived and the menu listed two devices with battery and
  charging state; evidence in `assets/screenshots/menu-devices.png`.
- Row clicks and the opening action lead to OpenLogi's **general window**,
  still requiring manual device selection. This was the expected OL-001 behavior,
  not a companion defect.
- Names differ from the GUI home, which uses short trade names (`MX Master`,
  `MX Keys`), while the CLI reports full model names.
- The GUI home does not show charge percentages, so the numeric comparison
  with OpenLogi remained unperformed at this checkpoint; evidence in
  `assets/screenshots/openlogi-gui-home.png`.

### Labels

`Open OpenLogi` repeated the verb in the application name. The menu action
became `Show OpenLogi window` / `Mostra la finestra di OpenLogi`, matching
`Main.activateWindow` and general-window opening. The row accessible name became
`Select the device in the OpenLogi app`. Old strings were removed from
`po/it.po` and the template. No bus filters or notification interception added.

### Live refresh while the menu is open

Observed defect: data did not update with the panel menu open because the
polling timer existed only with `show-percentage` enabled, at a minimum interval
of 60 seconds. Polling now depends on menu visibility:

- Menu open: 5 seconds, with error backoff `10 → 20 → 40 → 60` seconds, capped at 60.
- Menu closed: no timer unless `show-percentage` is enabled, retaining slow
  polling of `60 → 900` seconds.
- One pending request, 5-second timeout, cancellation and reaping unchanged.
- Rows reused for an unchanged inventory, preserving focus and scroll on refresh.

### Translations

English source strings (`msgid`); Italian in `po/it.po`, compiled to
`locale/it/LC_MESSAGES/openlogi-companion.mo`, also the path GNOME Shell expects
for `gettext-domain: openlogi-companion` in `metadata.json`. Other languages
fall back to English. The ZIP contains only the compiled catalogue; EGO rules
list `.po` and `.pot` as unnecessary submission files.

Checks added to `scripts/verify.sh`:

- Compiled catalogue exists at the declared domain path.
- `msgfmt --statistics` on `po/it.po` reports no untranslated or fuzzy entries.
- Catalogue loads and returns `Mostra la finestra di OpenLogi` for
  `Show OpenLogi window`. Checked with Python's `gettext` module because the
  `Gettext` typelib is not installed on this machine.
- `po/openlogi-companion.pot` matches source strings (37 messages).

Updated in this change: the preference subtitle
(`Aggiorna ogni 60 secondi mentre è mostrata nel pannello, con attesa maggiore
dopo errori.`) and the GSettings description, both consistent with 5-second
polling while the menu is open. Only the panel's `OpenLogi Companion` brand
strings remain untranslated English.

### Checks on the changed source

- `SHEXLI=/tmp/shexli-venv/bin/shexli ./scripts/verify.sh`: syntax, line limits,
  61 GJS checks, ZIP from the explicit manifest and `msgcmp` passed on 37
  translated messages. Shexli 0.2.1 with tree-sitter 0.25.2 and
  tree-sitter-javascript 0.25.0 reported no findings, errors or warnings.
- `./tests/nested.sh`: **48 Shell checks** passed with a synthetic backend,
  previously 42. Includes live refresh while the menu is open after changing
  the fake CLI inventory, return to slow polling on close, and opening the
  preferences window with its new subtitle. Evidence and screenshots in
  `/tmp/openlogi-nested-swZqwi`. Dark menu at text scale 1 inspected, with
  `Show OpenLogi window` visible and unchanged AT-SPI/PipeWire environment warnings.
- No installation or reload in the host session during these checks.

At this checkpoint, `OPEN_ITEMS.md` still listed numeric GUI battery comparison,
closed/minimized app clicks, window grouping, screen reader accessibility and
DPI/multiple monitors as open.

## Menu screenshot with devices, October 29, 2026

Note added with AI assistance for personal use. The author reported the
extension working in a real GNOME Shell 50 session, with a functioning menu
and visible devices, and supplied the captured screenshot.
`assets/screenshots/menu-devices.png` is 972×612, SHA-256 `db98d8d5…5e7b`;
provenance and intended use are in its README. It shows two connected devices,
battery and charging state, without IDs or sensitive data. This is visual
evidence supplied by the author, not an automated recapture. It does not replace
`tests/nested.sh` or add hardware coverage beyond `OPEN_ITEMS.md`. The asset is
outside the runtime manifest and therefore the ZIP.

## Logo and icon, October 29, 2026

Change made with AI assistance for personal use. PNG logo generated with
image_gen, with verified alpha channel, in `assets/branding/`; prompt and
provenance in its README. Symbolic SVG adaptation on a 16×16 grid in `icons/`,
loaded by `St.Icon` through `Gio.FileIcon`. The Shell theme determines its color.
The runtime manifest includes only the SVG, without PNG, prompts or documentation.

Checks on the changed source:

- `SHEXLI=/tmp/shexli-venv/bin/shexli ./scripts/verify.sh`: 61 GJS checks,
  ZIP and translations passed; Shexli without findings, errors or warnings.
- `./tests/nested.sh`: 42 Shell checks passed with a synthetic backend. D-Bus
  binding, initially blocked in the sandbox, succeeded with authorized execution
  outside it. Evidence in `/tmp/openlogi-nested-IgFqBv`. Dark screenshot at text
  scale 1 inspected; no icon loading errors in the log. Previously known
  AT-SPI/PipeWire/Adw environment warnings remain.

No installation or reload in the host session. No new hardware or real OpenLogi
GUI tests; all `OPEN_ITEMS.md` limitations remain.

## Verification of October 28, 2026

## Preparing source for GitHub

Note updated with AI assistance for personal use. Local preparation completed;
no remote repository had been created and no push performed at this checkpoint.

Creation of the repository and first commit was subsequently authorized only
locally. Remote publication was still deferred until real connected devices
were checked, as recorded in `OPEN_ITEMS.md`. The synthetic tests below did not
satisfy that condition.

- README updated for the experimental project, with repository-root commands,
  build/verification dependencies and explicit hardware/API limitations.
- Personal paths and references to local projects removed from documentation
  intended for sharing. AI notices, license, historical results, remaining
  checks and the upstream plan retained.
- `.gitignore` excludes ZIPs, compiled catalogues, `gschemas.compiled`, Python
  environments, caches, local agent configuration and temporary files.
- Packaging and sync scripts create the catalogue directory before compiling,
  so they work without an existing `locale/` directory.
- Exclusion rules checked with Git in a separate temporary copy: 31 source and
  documentation files selected, without excluded artifacts. Using only those
  files, without `locale/` or `dist/`, `./scripts/package.sh` rebuilt the ZIP and
  passed manifest, content and import comparisons.

Checks repeated after these changes:

```text
SHEXLI=/tmp/shexli-venv/bin/shexli ./scripts/verify.sh
  61 GJS checks passed; ZIP and translations verified
  Shexli: 0 findings, 0 errors, 0 warnings
./tests/nested.sh
  42 isolated Shell checks passed; synthetic backend
```

The scanner was initially absent. A venv under `/tmp` was prepared with the
pinned versions documented below. The sandbox blocked downloads and test D-Bus
binding; downloads and Shell tests succeeded with authorized execution outside
the sandbox while keeping the bus and test data separate from the host. This
run also produced the AT-SPI/PipeWire/Adw environment warnings described below,
without companion JavaScript errors in the isolated Shell log. Screenshots were
generated by the runner; no additional visual inspection was performed during
this documentation check. No installation or reload in the host session, and
no new hardware or real OpenLogi GUI tests. No sync to the host session.

## Environment and provenance

Rechecked locally:

```text
rpm -q openlogi gnome-shell gjs
openlogi-0.8.18-1.x86_64
gnome-shell-50.5-1.fc44.x86_64
gjs-1.88.1-2.fc44.x86_64
openlogi --version → openlogi 0.8.18
```

The headless Shell reported Mutter 50.6. No other Shell version is claimed to
be compatible. Scripts do not update packages or services.

Official source downloaded to `/tmp/openlogi-upstream-0818` using:

```bash
git clone --depth 1 --branch v0.8.18 https://github.com/AprilNEA/OpenLogi.git /tmp/openlogi-upstream-0818
git -C /tmp/openlogi-upstream-0818 rev-parse HEAD
```

Annotated tag `v0.8.18`: `9fb08172f1e4ca9f1b83374fe1532cec3580cc69`;
actual commit: `d9fd33aca1639c377af25b8fe89ee89c6120f187`.
The sandbox network initially returned `Could not resolve host: github.com`;
the clone succeeded with authorized execution outside the sandbox. `master`
was not used to infer the installed release's contract.

Source read in the clone, with public references from the same release:

- [USAGE.md, automation API](https://github.com/AprilNEA/OpenLogi/blob/v0.8.18/docs/USAGE.md)
- [JSON projection and error codes](https://github.com/AprilNEA/OpenLogi/blob/v0.8.18/crates/openlogi-cli/src/cmd/api/output.rs)
- [api devices command](https://github.com/AprilNEA/OpenLogi/blob/v0.8.18/crates/openlogi-cli/src/cmd/api.rs)
- [Device and battery types](https://github.com/AprilNEA/OpenLogi/blob/v0.8.18/crates/openlogi-core/src/device.rs)
- [Linux launcher](https://github.com/AprilNEA/OpenLogi/blob/v0.8.18/packaging/linux/desktop/openlogi.desktop)
- [Deep-link vocabulary](https://github.com/AprilNEA/OpenLogi/blob/v0.8.18/crates/openlogi-core/src/brand.rs)
- [GUI bootstrap and single instance](https://github.com/AprilNEA/OpenLogi/blob/v0.8.18/crates/openlogi-desktop/src/main.rs)
- [Agent IPC](https://github.com/AprilNEA/OpenLogi/blob/v0.8.18/crates/openlogi-ipc/src/lib.rs)

Confirmed: schema 1 envelope; success exits 0, runtime error 1 and syntax error
2; `inventory` states scanning/ready/unavailable; nullable fields and opaque,
non-persistent IDs. BatteryLevel values critical/low/good/full/unknown and
BatteryStatus values charging/charging_slow/discharging/full/error/unknown.
No public inventory subscription or supported D-Bus interface was found in API
documentation or its code. The upstream active-window extension is not an
inventory service. Chosen approach: asynchronous CLI, no internal IPC protocol.

The installed desktop file matches the upstream fields consumed:
`openlogi.desktop`, `Exec=openlogi-desktop`,
`StartupWMClass=org.openlogi.openlogi`. WM_CLASS differs from the file name.
The deep-link vocabulary has no device selection; bootstrap `on_open_urls` does
not prove Linux registration. A second GUI process can exit through the
single-instance guard: relaunching the binary alone is insufficient to focus
an existing window.

The [Review Guidelines](https://gjs.guide/extensions/review-guidelines/review-guidelines.html)
and [Best Practices](https://gjs.guide/extensions/review-guidelines/best-practices.html)
were consulted on October 28. The AI notice was retained at that time. Local
review included development references outside the repository; no private
module or document is included in the bundle. Subsequent GitHub source
preparation does not extend test coverage or constitute an EGO submission.

## Real inventory

Inside the sandbox, `openlogi api devices` returned exit 1, schema 1 and
`agent_unavailable`, with IPC error `Operation not permitted (os error 1)`.
This does not demonstrate that the agent was stopped.

The same read-only CLI, authorized outside the sandbox, returned:

```json
{"schema_version":1,"ok":true,"data":{"inventory":"ready","devices":[]}}
```

Exit 0. Output was summarized before printing to avoid exposing IDs or hardware
names. This demonstrates communication with the agent and an empty inventory at
that moment, not peripheral compatibility or incompatibility. No real device
or battery state was observed at this checkpoint. No service, private
configuration, package or udev rule was changed.

## Independent checks and GJS provider

Reproducible command from the project root:

```bash
SHEXLI=/tmp/shexli-venv/bin/shexli ./scripts/verify.sh
```

Verification runs ESM syntax parsing through Node (without Node dependencies),
`bash -n`, JSON validation, a 200-column JS/CSS limit, GJS tests,
`msgfmt --check`, `glib-compile-schemas --strict --dry-run schemas`, ZIP build,
exact manifest/content/relative-import comparisons and Shexli. The Italian
catalogue is also checked with `xgettext` extraction and `msgcmp`: no UI messages
missing. GJS gettext loading with `LC_ALL=it_IT.UTF-8` verified:
`Battery unavailable` becomes `Batteria non disponibile`. Node syntax checking
does not test GJS APIs; those are exercised by provider tests and the isolated
Shell.

`gjs -m tests/test.js`: **61 checks passed** with synthetic data and real Python
CLI child processes. Coverage:

- Eight devices with null/duplicate IDs, matching/long names, 0/100%, qualitative
  level without a percentage, slow charging, a batteryless light and an offline
  device with an earlier reading.
- Scanning/unavailable/empty-ready states and zero/null distinction.
- Empty/malformed JSON, invalid envelopes, unknown schema, invalid types,
  out-of-range percentages and inconsistent exit status.
- Missing CLI, unreachable agent, version mismatch, handshake failure, API
  timeout, unknown error code and incompatible CLI syntax.
- Stdout and stderr above 1 MiB, finite timeout, simultaneous stream draining
  without deadlock. Stderr is not accumulated in memory.
- Overlapping refreshes coalesced into the same Promise, teardown cancellation,
  child termination and reaping (`get_if_signaled`), fresh instance after
  teardown. Timeout and limit release request identity.

## Isolated Shell and preferences

Command: `./tests/nested.sh`. The first sandbox attempt failed before startup:
`Failed to bind socket … Operation not permitted`. Tests then succeeded with
authorized execution outside the sandbox, preserving isolation.

The runner creates a fresh D-Bus session, separate XDG_RUNTIME_DIR/DATA_HOME/CONFIG_HOME,
a keyfile GSettings backend and a virtual 1280×720 monitor, then starts:

```bash
gnome-shell --headless --virtual-monitor 1280x720 --debug-control
```

It does not forward the host bus address. The fake CLI reads only a synthetic
fixture; the OpenLogi launcher is masked, then replaced by a GTK test GUI only
inside the temporary XDG directory. The Eval helper is test-local and absent
from the runtime manifest. The script stops and reaps the Shell PID it created,
without searching for processes by pattern. It does not install or reload
extensions in the host session.

The first completed run passed **37 checks**, covering:

- Eight rows, including duplicates; no offline 84% in the details.
- Menu, row focus, accessible names and bounded width.
- Percentages 0 and 100, rejection of ambiguous/offline IDs, unchanged-refresh
  row reuse and selection reset when a device disappears.
- Actual fake-CLI failure: snapshot and rows cleared; retry after rapid menu
  reopening; no current percentage after an error.
- Disable with a delayed child pending, references and timers removed, three
  enable/disable/enable cycles and restoration of eight rows.
- Live preference changes that create/remove polling.
- 200 devices, prefer-light/prefer-dark themes and text scales 1 and 1.5;
  menu within the screen and scrolling list in all four combinations.
- Opening and closing the extension's real GTK preferences window.

Screenshots of all four combinations were captured through the isolated Shell's
Screenshot D-Bus service. Light at 1.5 and dark at 1 were visually inspected:
truncated text, scrolling, theme contrast and focus indicators visible. The
Fedora welcome window in the background belonged only to the new test session.
Text scaling is not fractional monitor scaling. No screen reader or full
physical navigation test; the AT-SPI bus returned `Permission denied`.

Extended launcher testing initially found that the minimized synthetic window
was not activated. Fix: prefer the `Shell.App` window, then look for the
launcher's declared WM_CLASS when the desktop ID differs. Activate with
`Main.activateWindow`; if no window exists, launch with `Shell.App.activate()`.
The final extended run passed **42 checks**, including missing application,
cold launch, an already-open window without duplicates and restore from
minimized, all using only the synthetic GUI. Evidence and screenshots were
kept in the temporary directory printed by the runner (`results.txt`,
`shell.log` and PNGs), without companion JavaScript errors in `shell.log`.
These local artifacts are not distributed with source and may no longer exist.
This does not test the real OpenLogi GUI.

Observed environment warnings: AT-SPI unavailable, PipeWire disconnected, empty
geolocation permission store, unavailable authentication agent and GI warnings
for Adw.PreferencesWindow. These are not extension errors. Full logs stay under
`/tmp`; they are not copied into the project or package.

## Package, license and review

`scripts/runtime-files.txt` contains the exact runtime file list. The ZIP
preserves `shell/`, schema XML, `.mo` catalogue and GPLv3 LICENSE. All bytes
were compared with source and relative imports resolved. Excluded:
`gschemas.compiled`, scripts, tests, prompts, documentation, agent directories
and other local data.

Shexli **0.2.1**, tree-sitter **0.25.2**, tree-sitter-javascript **0.25.0**:
**zero findings, zero errors, zero warnings**. No crash with this combination;
the scanner was not modified. Tree-sitter 0.26.0, reported as problematic in
local references, was not used.

No `manual_review` findings for subprocesses. Explicit assessment: the provider
executes only the official CLI with fixed arguments and user privileges,
shared budget, timeout, cancellation, termination and non-cancellable wait.
It does not execute hardware input or device names. Parameterized constructors
serve the synthetic test backend and are not exposed in preferences.

This is not EGO certification or an OpenLogi RPM audit. Maintainability review
remains the author's responsibility before any publication.

## Remaining checks and user commands

See [OPEN_ITEMS.md](OPEN_ITEMS.md) for the **unmet** device-page selection
requirement, the untested real OpenLogi GUI paths and hardware checks.
To reproduce verification in a terminal without sandbox restrictions:

```bash
# From the repository root:
SHEXLI=/tmp/shexli-venv/bin/shexli ./scripts/verify.sh
./tests/nested.sh
openlogi --version
openlogi api devices
```

If the venv does not exist, prepare it explicitly without changing the scanner:

```bash
python3 -m venv /tmp/shexli-venv
/tmp/shexli-venv/bin/pip install shexli==0.2.1 tree-sitter==0.25.2 tree-sitter-javascript==0.25.0
```

For meaningful interactive tests: `dbus-run-session -- gnome-shell --devkit`
with `mutter-devkit` available, runtime copied into the isolated XDG tree and
a synthetic backend as in the runner. Do not expose the host bus to the devkit.

## Localization — 2026-11-11

English, Italian, Spanish, German and French are available. The 40 UI messages
have complete it/es/de/fr catalogues, compiled during packaging and sync.
Catalogue coverage, placeholders, compiled bytes, isolated language loading,
and the existing verification/nested checks passed. The cross-project native
language matrix, evidence and remaining limits are in [LOCALIZATION.md](LOCALIZATION.md).
Previously recorded hardware and host-session limitations remain open.
