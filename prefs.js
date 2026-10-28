// SPDX-License-Identifier: GPL-3.0-or-later
// Generated with AI for personal use.
// Do NOT upload to extensions.gnome.org (EGO) unless you understand JavaScript
// and can maintain this code.

import Adw from 'gi://Adw';
import Gio from 'gi://Gio';
import {ExtensionPreferences, gettext as _} from 'resource:///org/gnome/Shell/Extensions/js/extensions/prefs.js';

export default class Preferences extends ExtensionPreferences {
    fillPreferencesWindow(window) {
        const settings = this.getSettings();
        const page = new Adw.PreferencesPage({title: 'OpenLogi Companion', icon_name: 'input-keyboard-symbolic'});
        const group = new Adw.PreferencesGroup({title: _('Panel'),
            description: _('Pin a device from the menu. The choice lasts only for this session.')});
        const row = new Adw.SwitchRow({title: _('Allow panel percentage'),
            subtitle: _('Refresh every 60 seconds, with a longer delay after errors.')});
        settings.bind('show-percentage', row, 'active', Gio.SettingsBindFlags.DEFAULT);
        group.add(row);
        page.add(group);
        window.add(page);
        // GSettings.bind owns its binding; no manually connected preferences signals.
    }
}
