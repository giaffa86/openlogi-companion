# Screenshots for publication

Project assets for the extensions.gnome.org listing. They are outside the
runtime bundle: `scripts/runtime-files.txt` does not list them and
`scripts/package.sh` does not include them in the ZIP.

## `menu-devices.png`

- Captured by the author on October 29, 2026 in a GNOME Shell 50 session with
  the extension installed and the real OpenLogi inventory populated.
- Content: panel menu with two connected devices, battery percentages, charging
  state and menu actions.
- Dimensions: 972×612 px, RGBA PNG. No opaque IDs or sensitive data are visible.
- SHA-256: `db98d8d58f21fe2919e74651443081e8abfda58eaa9302b8b10d34dfecea5e7b`

Intended use: upload to the screenshot field on the extension's
extensions.gnome.org listing. For better results when the listing scales the
image, recapture at a wider size (roughly at least 1200 px wide) with text scale
1, rather than enlarging this file.

## `openlogi-gui-home.png`

- Captured by the author on October 30, 2026 from the OpenLogi window as a
  comparison for OL-002. It is not promotional material and must not be uploaded
  to extensions.gnome.org: it shows a third-party project's interface.
- Content: the Devices screen with two device cards.
- Dimensions: 1867×1171 px, RGBA PNG. No opaque IDs or sensitive data are visible.
- SHA-256: `47b9a840b5a6d6c8a12a5b281e2fa39d50fc1d4c81ca4a499dda1ec4f7d1f32e`

Related observations: the GUI uses short trade names (`MX Master`, `MX Keys`),
while the CLI inventory reports full model names (`Wireless Mouse MX Master`,
`MX Keys Wireless Keyboard`). The home screen does not expose a charge
percentage, so this screenshot alone does not complete the numeric battery
comparison. See OL-002 in `docs/OPEN_ITEMS.md` for the later device-page check.
