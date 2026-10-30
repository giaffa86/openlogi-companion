// SPDX-License-Identifier: GPL-3.0-or-later

import Clutter from 'gi://Clutter';
import Gio from 'gi://Gio';
import GLib from 'gi://GLib';
import Shell from 'gi://Shell';
import Pango from 'gi://Pango';
import St from 'gi://St';
import * as Main from 'resource:///org/gnome/shell/ui/main.js';
import * as PanelMenu from 'resource:///org/gnome/shell/ui/panelMenu.js';
import * as PopupMenu from 'resource:///org/gnome/shell/ui/popupMenu.js';
import {gettext as _} from 'resource:///org/gnome/shell/extensions/extension.js';
import {Provider} from './provider.js';
import {DeviceRow, kindIcon} from './deviceRow.js';
import {DataError, panelDevice} from './contract.js';

// Polling while the menu is open keeps battery and connection state live without
// any preference; the panel-only poll stays slower because it runs unattended.
const MENU_REFRESH_SECONDS = 5;
const PANEL_REFRESH_SECONDS = 60;
const MENU_REFRESH_MAX_SECONDS = 60;
const PANEL_REFRESH_MAX_SECONDS = 900;

export class Indicator {
    constructor(extension) {
        this._extension = extension;
        this._settings = extension.getSettings();
        this._provider = new Provider();
        this._generation = 0;
        this._pending = null;
        this._timer = 0;
        this._delay = 0;
        this._menuOpen = false;
        this._failures = 0;
        this._selected = null;
        this._snapshot = null;
        this._rows = [];
        this._button = new PanelMenu.Button(0.0, 'OpenLogi Companion');
        const box = new St.BoxLayout({style_class: 'panel-status-menu-box'});
        box.add_child(new St.Icon({
            gicon: new Gio.FileIcon({file: extension.dir.get_child('icons').get_child('openlogi-companion-symbolic.svg')}),
            style_class: 'system-status-icon',
        }));
        this._deviceIcon = new St.Icon({style_class: 'system-status-icon', visible: false});
        this._percentage = new St.Label({y_align: Clutter.ActorAlign.CENTER, visible: false});
        box.add_child(this._deviceIcon);
        box.add_child(this._percentage);
        this._button.add_child(box);
        this._status = new PopupMenu.PopupMenuItem(_('Loading…'), {reactive: false, can_focus: false});
        this._status.label.clutter_text.ellipsize = Pango.EllipsizeMode.END;
        this._status.label.clutter_text.line_wrap = true;
        this._status.label.clutter_text.single_line_mode = false;
        this._button.menu.addMenuItem(this._status);
        this._section = new PopupMenu.PopupMenuSection();
        this._scroll = new St.ScrollView({style_class: 'openlogi-companion-scroll',
            hscrollbar_policy: St.PolicyType.NEVER, vscrollbar_policy: St.PolicyType.AUTOMATIC});
        this._scroll.set_child(this._section.actor);
        this._button.menu.box.add_child(this._scroll);
        this._button.menu.addMenuItem(new PopupMenu.PopupSeparatorMenuItem());
        this._button.menu.addAction(_('Show OpenLogi window'), () => this._openApp());
        this._button.menu.addAction(_('Refresh'), () => this._refresh());
        this._button.menu.addAction(_('Extension preferences'), () => extension.openPreferences());
        this._menuSignal = this._button.menu.connect('open-state-changed', (_menu, open) => {
            this._menuOpen = open;
            if (open) {
                const monitor = Main.layoutManager.primaryMonitor;
                const scale = St.ThemeContext.get_for_stage(global.stage).scale_factor;
                const width = Math.max(100, Math.min(416, (monitor.width - 48) / scale));
                this._button.menu.box.set_style(`max-width: ${width}px;`);
                this._scroll.set_style(`width: ${width}px; max-height: ${Math.max(80, (monitor.height - 250) / scale)}px;`);
                this._refresh();
            } else {
                this._schedule();
            }
        });
        this._settingsSignal = this._settings.connect('changed::show-percentage', () => {
            this._updatePanel();
            this._schedule();
        });
        Main.panel.addToStatusArea(extension.uuid, this._button);
        this._refresh();
    }

    destroy() {
        this._generation++;
        if (this._timer) {
            GLib.Source.remove(this._timer);
            this._timer = 0;
        }
        this._delay = 0;
        this._menuOpen = false;
        this._settings.disconnect(this._settingsSignal);
        this._button.menu.disconnect(this._menuSignal);
        this._provider.destroy();
        this._pending = null;
        this._rows = [];
        this._snapshot = null;
        this._selected = null;
        this._button.destroy();
        this._button = null;
        this._section = null;
        this._scroll = null;
        this._status = null;
        this._percentage = null;
        this._deviceIcon = null;
        this._settings = null;
        this._extension = null;
        this._provider = null;
    }

    async _refresh() {
        if (this._pending)
            return;
        if (this._timer) {
            GLib.Source.remove(this._timer);
            this._timer = 0;
        }
        const request = {};
        const generation = this._generation;
        this._pending = request;
        try {
            const snapshot = await this._provider.refresh();
            if (generation !== this._generation)
                return;
            this._failures = 0;
            this._snapshot = snapshot;
            if (snapshot.inventory !== 'ready') {
                this._clear();
                this._status.label.text = snapshot.inventory === 'scanning' ? _('Scanning devices…') : _('Inventory unavailable');
            } else {
                this._render(snapshot.devices);
                this._status.label.text = snapshot.devices.length
                    ? _('Select a device in OpenLogi. Pin a device in the panel for this session.')
                    : _('No devices');
            }
            this._updatePanel();
        } catch (error) {
            if (generation !== this._generation)
                return;
            if (!(error instanceof DataError))
                console.error('[openlogi-companion] Unexpected refresh failure', error);
            this._failures++;
            this._snapshot = null;
            this._clear();
            const messages = {
                'cli-missing': _('OpenLogi CLI is not installed'),
                'agent-unavailable': _('Cannot reach the OpenLogi agent'),
                incompatible: _('Incompatible CLI, agent or API schema'),
                invalid: _('Invalid inventory data'),
                timeout: _('OpenLogi request timed out'),
                'output-limit': _('OpenLogi output exceeds the limit'),
                unavailable: _('Inventory unavailable'),
            };
            this._status.label.text = messages[error.code] ?? _('Inventory unavailable');
            this._updatePanel();
        } finally {
            if (this._pending === request) {
                this._pending = null;
                this._schedule();
            }
        }
    }

    _clear() {
        this._section.removeAll();
        this._rows = [];
        this._selected = null;
    }

    _render(devices) {
        // Reuse rows in display order when the inventory is unchanged, preserving focus.
        // Duplicate/null routes are never merged and cannot be pinned.
        const same = this._rows.length === devices.length && this._rows.every((row, i) =>
            row.device.id === devices[i].id && row.device.name === devices[i].name && row.device.kind === devices[i].kind);
        if (!same) {
            this._section.removeAll();
            this._rows = devices.map(device => {
                const row = new DeviceRow(device, () => this._openApp(), selected => {
                    this._selected = this._selected === selected.id ? null : selected.id;
                    this._render(this._snapshot.devices);
                    this._updatePanel();
                });
                this._section.addMenuItem(row);
                return row;
            });
        }
        if (!panelDevice(devices, this._selected))
            this._selected = null;
        const counts = new Map();
        for (const device of devices)
            counts.set(device.id, (counts.get(device.id) ?? 0) + 1);
        this._rows.forEach((row, i) => {
            const device = devices[i];
            // The pin is a session selection: it must survive a battery reading that
            // is temporarily missing (for example a mouse charging without a value).
            const pinnable = device.id !== null && device.online && device.battery !== null &&
                counts.get(device.id) === 1;
            row.update(device, pinnable, device.id !== null && device.id === this._selected);
        });
    }

    _updatePanel() {
        const device = this._snapshot?.inventory === 'ready' ? panelDevice(this._snapshot.devices, this._selected) : null;
        const show = device !== null && this._settings.get_boolean('show-percentage');
        const percentage = show ? device.battery?.percentage ?? null : null;
        const text = percentage === null ? '' : new Intl.NumberFormat(undefined, {style: 'percent'}).format(percentage / 100);
        // The kind icon identifies the pinned device even when no percentage exists,
        // so the panel never falls back to an unexplained empty label.
        this._deviceIcon.visible = show;
        if (show)
            this._deviceIcon.icon_name = kindIcon(device.kind);
        this._percentage.visible = show && text !== '';
        this._percentage.text = text;
        const details = show ? ` ${device.name}${text ? ` ${text}` : ''}` : '';
        this._button.accessible_name = `OpenLogi Companion${details}`;
    }

    _schedule() {
        if (this._timer) {
            GLib.Source.remove(this._timer);
            this._timer = 0;
        }
        // Only a visible menu or the panel percentage needs unattended polling.
        if (!this._menuOpen && !this._settings.get_boolean('show-percentage')) {
            this._delay = 0;
            return;
        }
        const base = this._menuOpen ? MENU_REFRESH_SECONDS : PANEL_REFRESH_SECONDS;
        const max = this._menuOpen ? MENU_REFRESH_MAX_SECONDS : PANEL_REFRESH_MAX_SECONDS;
        const seconds = Math.min(base * 2 ** Math.min(this._failures, 4), max);
        this._delay = seconds;
        this._timer = GLib.timeout_add_seconds(GLib.PRIORITY_DEFAULT, seconds, () => {
            this._timer = 0;
            this._refresh();
            return GLib.SOURCE_REMOVE;
        });
    }

    _openApp() {
        const app = Shell.AppSystem.get_default().lookup_app('openlogi.desktop');
        if (!app) {
            this._status.label.text = _('OpenLogi desktop application is not installed');
            return;
        }
        try {
            let window = app.get_windows()[0] ?? null;
            // GPUI's app_id can differ from the desktop filename. Use the
            // launcher's verified StartupWMClass when Shell has not grouped it.
            if (!window) {
                const wmClass = app.get_app_info().get_startup_wm_class();
                if (wmClass)
                    window = global.get_window_actors().map(actor => actor.meta_window)
                        .find(candidate => candidate.get_wm_class() === wmClass) ?? null;
            }
            if (window)
                Main.activateWindow(window);
            else
                app.activate();
            this._button.menu.close();
        } catch (_error) {
            this._status.label.text = _('Could not open OpenLogi');
        }
    }
}
