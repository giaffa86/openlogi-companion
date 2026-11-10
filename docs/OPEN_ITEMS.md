# Limitations and open checks

## Source publication authorized, November 10, 2026

The author created the public
[giaffa86/openlogi-companion](https://github.com/giaffa86/openlogi-companion)
repository and explicitly requested synchronization with the local project.
This authorizes source commits and pushes, superseding the earlier postponement
of remote publication. The hardware and GUI checks below remain open: releases
and EGO submission still depend on OL-002, OL-003 and OL-005. No additional
compatibility is claimed.

## Agreed resumption point, October 28, 2026 (historical)

Note updated with AI assistance for personal use.

No connected devices were available at this checkpoint. Hardware checks were
pending; the observed empty inventory did not demonstrate incompatibility.
Use the following checklist when resuming.

**October 28 decision, superseded for pushes by the authorization above:** source
and a local Git commit could be prepared. Creating the GitHub repository,
pushing and releasing were deferred until the extension had been checked with
real connected devices, including inventory/battery and GUI opening in items
1 and 2. Results were to be recorded here and in `VERIFICATION.md` before
resuming remote publication. Local preparation did not authorize early
publication. The October 30, 2026 checkpoint recorded items 1 and 2 as partly tested,
with the numeric GUI battery comparison and closed/minimized OpenLogi checks
still listed as pending. The updated checklist below records subsequent results.

1. [x] Real inventory observed on October 30, 2026: two devices with battery
   readings in the menu, with the OpenLogi GUI open on those same devices.
   Numeric comparison against the GUI's device page was consistent.
   **Non-blocking note:** the CLI reports full model names
   (`Wireless Mouse MX Master`, `MX Keys Wireless Keyboard`), while the GUI home uses short names
   (`MX Master`, `MX Keys`). This is not a defect.
2. [x] Before device row clicks were disabled, row clicks and the Open action
   were tested in the real session: **both opened the general window**, as
   expected under OL-001. **Partial:** the dedicated action still needs testing
   with OpenLogi closed or minimized, along with window grouping (OL-002).
3. [x] Review updated on November 10, 2026 against v0.9.0, now installed:
   release source, CLI documentation and the Linux launcher do not offer direct
   device-page opening. The equivalent [upstream issue #1375](https://github.com/AprilNEA/OpenLogi/issues/1375)
   already exists and remains open. This was a source and installed-package
   review, without a GUI launch test.
4. [ ] If the limitation persists, prepare a concrete upstream request for a
   stable public identity and an action to open a device page, including an
   already-running GUI and explicit errors. No proposal has been sent; this
   note does not authorize sending it. Coordinate with the existing equivalent
   issue #1375 first.
5. [ ] Integrate direct selection only after verifying the public interface.
   Until then, keep general-window opening and session-only in-memory pins
   (OL-001 and OL-004).

## OL-001: direct device-page opening, requirement not met

OpenLogi v0.8.18 provides no verified public action for selecting a device in
the GUI. `brand.rs` defines generic `show` and `open-settings` commands, without
device selection. `main.rs` registers `on_open_urls`, but that does not prove
Linux registration. The desktop file declares no protocol handler. No deep
links, flags or D-Bus methods are invented.

Rechecked on November 10, 2026 against
[release v0.9.0](https://github.com/AprilNEA/OpenLogi/releases/tag/v0.9.0), also
identified locally through `openlogi --version` and RPM
`openlogi-0.9.0-1.x86_64`. The
[`DeeplinkCommand` vocabulary](https://github.com/AprilNEA/OpenLogi/blob/v0.9.0/crates/openlogi-core/src/brand.rs)
still contains only `show`, `open-settings`, `open-about`, `check-for-updates`
and `quit`. Its parser ignores paths and queries for recognized commands;
`show?device=…` cannot select a peripheral. The
[GUI bootstrap](https://github.com/AprilNEA/OpenLogi/blob/v0.9.0/crates/openlogi-desktop/src/main.rs)
exits when another instance exists, without forwarding the request. The
[release's Linux launcher](https://github.com/AprilNEA/OpenLogi/blob/v0.9.0/packaging/linux/desktop/openlogi.desktop)
and the installed launcher retain `Exec=openlogi-desktop`, without `%u`, a MIME
handler or device actions. The [equivalent request #1375](https://github.com/AprilNEA/OpenLogi/issues/1375)
remains open. The limitation is confirmed for this release; no new real GUI
launch test was added.

On November 10, 2026, the author requested disabling row clicks because general
opening is misleading and redundant with the dedicated action. Rows now display
information only, without row activation, focus or hover. Pin buttons remain
active and keyboard-focusable. Row accessible names describe only the device
and its state, without instructions to select it in the app.
**Show OpenLogi window** calls the `openlogi.desktop` launcher and activates an
existing window with `Main.activateWindow`, or starts one with
`Shell.App.activate()`. It always opens the **general window**. Pin buttons
change only what is displayed in the panel.

**Agreed reminder:** with future releases, recheck a public device-page opening
API and the status of the existing [issue #1375](https://github.com/AprilNEA/OpenLogi/issues/1375).
If the limitation persists, prepare a contribution to that request; create a
new issue only if no relevant request exists. Re-enable row clicks only after
verifying contextual opening on Linux with the GUI closed, open and minimized,
and explicit handling of missing or ambiguous IDs. No upstream message is sent
as part of this change.

Historical evidence from October 30, 2026, before row clicks were disabled:
with two real connected devices, both the row click and the opening action
showed the general window, not the device page.

Separate, unsent upstream proposal: introduce a public, versioned Linux
`OpenDevice` action through a desktop action, D-Bus or registered deep link,
with a stable public device identity and a way to resolve its current route.
A null or duplicate ID must produce an error, never select the first match.
GUI closed: launch and apply selection after inventory becomes ready. GUI
open/minimized: forward to the existing instance, select and focus. The client
must distinguish success, absent/offline device, ambiguous identity and
inventory not ready. Avoid serial numbers in public URLs/logs. Direct selection
remains unimplemented until this interface is verified.

## OL-002: real peripherals and OpenLogi GUI integration

First real-device observation on October 30, 2026: a `ready` inventory with two
connected devices (mouse and keyboard), battery and charging state displayed
correctly in the menu, and no errors in the Shell log. Evidence is in
`assets/screenshots/`.

Closed on October 30, 2026: the **numeric battery comparison** with OpenLogi's
device page matched the menu row; the GUI home does not expose the percentage.
The real case `Battery unavailable · Charging`, without a reading, was also
observed. Before the fix the pin disappeared; the device now remains pinnable
and the panel shows its kind icon.

Remaining limitations:

- Names: the CLI exposes the full model name; the GUI home uses the short trade
  name. The companion neither renames devices nor infers aliases.
- GUI launch: tested only with OpenLogi already open. Closed, minimized and
  window grouping remain to be checked (real GPUI, `StartupWMClass`).
- Other models, such as G515 and Keys-To-Go 2, are not available to the author.
  They belong to others, so compatibility is not claimed and testing them is
  not a publication requirement.
- Builds did not launch real GUIs or install extensions in the host session.
  The real-device test was performed by the author.

The Shell launch/activation path is tested using a synthetic GTK app with the
same desktop ID/StartupWMClass in a separate session. This does not test OpenLogi
GPUI.

To close this item, after explicitly installing the companion:

```bash
openlogi --version
openlogi api devices
gnome-extensions info openlogi-companion@giaffa86
journalctl --user -b -o cat /usr/bin/gnome-shell
```

Do not share inventory output without redacting IDs. With real devices
connected, compare names, connection state and battery with OpenLogi, then test
**Show OpenLogi window** with the app closed, open and minimized. Check that it
opens the general window and still requires manual device selection. Row clicks
must have no effect while pins keep working. Restart only the extension with
requests pending, without stopping the agent. Do not use `openlogi list` to
bypass missing inventory.

## OL-005: blockers for a possible EGO submission

Review of the [review guidelines](https://gjs.guide/extensions/review-guidelines/review-guidelines.html)
on October 30, 2026. Preparation is complete; releases and EGO submission remain
deferred pending OL-002 and OL-003. The author created the public repository on
November 10, 2026 and authorized source synchronization.

- **AI notices in headers.** Resolved on October 30, 2026: file headers contain
  only `SPDX-License-Identifier: GPL-3.0-or-later`. AI provenance remains in
  `README.md`, `AI_REVIEW_GUIDELINES.md` and `docs/`. The author must still be
  able to explain and maintain the code; the guidelines also reject submissions
  that cannot be justified.
- **`metadata.json`.** Fixed: `version` removed, `url` added
  (`https://github.com/giaffa86/openlogi-companion`), and `description` expanded
  with requirements, read-only behavior, general opening and independence.
  The public repository has existed and been accessible since November 10,
  2026; its URL is verified. `tests/check-package.py` rejects a bundle with
  `version` or without an HTTPS `url`.
- **Subprocess requirement.** Cannot be removed under the current constraints:
  the only documented public interface used is `openlogi api devices`. Project
  rules exclude internal IPC, direct HID, `openlogi list`, additional daemons
  and reading `config.toml`. The submission rationale is in `README.md` and here:
  official read-only CLI, fixed arguments, no shell, timeout, limits,
  cancellation and reaping.
- **Branding.** Clarified on October 30, 2026: independence statement in the
  `metadata.json` description, the README's “Trademarks and independence” section
  and the private note `private/ego-subprocess.md`. The mark is original; the
  bundle contains no third-party media. **Open:** the name remains the author's
  choice. EGO guidelines list trademarked names among protected content without
  permission, so `OpenLogi Companion` may be challenged during review.
  Alternatives are ready if requested: a neutral name such as “Wireless
  Peripheral Battery”, mentioning OpenLogi only in the description.
- **EGO listing icon.** Ready: `assets/ego/icon-256.png` and `icon-128.png`,
  a light emblem on a rounded dark background, readable on light and dark
  listings. Regenerate with `scripts/make-ego-icon.py`. Upload through the web
  form, separately from the ZIP. Appearance on the actual listing still needs
  evaluation after upload.
- **Screenshots.** `assets/screenshots/menu-devices.png` is ready; recapturing
  at a width of at least 1200 px is preferable. Do not upload
  `openlogi-gui-home.png`.
- **Unnecessary files.** EGO rules list `.po`, `.pot`, build scripts and unused
  media. The current ZIP contains only runtime files, the icon, schema, compiled
  catalogue and `LICENSE`, meeting this requirement.
- **Language.** English source strings, compiled Italian catalogue; other
  languages fall back to English. A future EGO translation portal would work
  on repository source, not the ZIP.
- **Accessibility.** Screen reader and fractional-DPI checks in OL-003 remain open.

## OL-003: remaining accessibility and layout checks

Automated coverage in the isolated Shell includes programmatic row focus,
accessible names, truncation, scrolling, 200 devices, light/dark themes, text
scales 1 and 1.5 on a virtual 1280×720 monitor, and preserved focus/scroll during
live menu refresh. With read-only rows, focus is now tested on pin buttons.

Battery bars and multiple pins added on November 10, 2026 have been tested only
with a synthetic backend. They still need observation with real devices,
including bar readability at fractional DPI and on different monitors. Values
remain available in accessible names, which does not replace a screen reader
test.

**Not covered, manual tests deferred by the author:** the local, unversioned
`private/accessibility-tests.md` checklist covers a screen reader (Orca),
physical Tab/arrow navigation, touch, fractional DPI, multiple monitors and
very small displays. AT-SPI reported `Permission denied` in the isolated
session. This does not demonstrate incompatibility, but screen reader coverage
is still absent and must not be claimed.

## OL-004: identity and API coverage

No persistent favorites until a stable public identity is verified. Current
opaque IDs stay in memory only. Missing or duplicate IDs prevent panel pinning.
A pin does not require a valid battery reading: an online device with battery
support remains pinnable without a percentage, and the panel shows at least
its kind icon. Rows are not deduplicated. Route changes require a new selection.
The same physical device cannot reliably be reconstructed from names or IDs
reused by upstream.

Multiple devices can be pinned independently in the same session. Loss of a
valid ID removes only the affected pin; errors, scanning or disabling clear
all selections. Neither pins nor their IDs are stored in GSettings. The new
`battery-bar` key controls UI rendering only.

The release's inventory API includes lights but not webcams. Event
subscriptions, battery notifications, hardware controls and profile changes
are not implemented. The CLI's current profile must match the agent's; the
companion does not read or change private configuration to force a match.
