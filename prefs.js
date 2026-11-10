// SPDX-License-Identifier: GPL-3.0-or-later

import Adw from 'gi://Adw';
import Gio from 'gi://Gio';
import {ExtensionPreferences, gettext as _} from 'resource:///org/gnome/Shell/Extensions/js/extensions/prefs.js';

export default class Preferences extends ExtensionPreferences {
    fillPreferencesWindow(window) {
        const settings = this.getSettings();
        const page = new Adw.PreferencesPage({title: 'OpenLogi Companion', icon_name: 'input-keyboard-symbolic'});
        const group = new Adw.PreferencesGroup({title: _('Panel'),
            description: _('Pin devices from the menu. The choices last only for this session.')});
        const row = new Adw.SwitchRow({title: _('Show pinned devices in the panel'),
            subtitle: _('Each device keeps its own icon and battery; refresh every 60 seconds, with a longer delay after errors.')});
        settings.bind('show-percentage', row, 'active', Gio.SettingsBindFlags.DEFAULT);
        group.add(row);
        const battery = new Adw.SwitchRow({title: _('Show battery as a bar'),
            subtitle: _('Use a vertical bar instead of a numeric percentage for each pinned device.')});
        settings.bind('battery-bar', battery, 'active', Gio.SettingsBindFlags.DEFAULT);
        group.add(battery);
        const logo = new Adw.SwitchRow({title: _('Hide the extension icon when devices are pinned'),
            subtitle: _('Requires at least one pinned device to be shown in the panel.')});
        settings.bind('hide-logo', logo, 'active', Gio.SettingsBindFlags.DEFAULT);
        group.add(logo);
        page.add(group);
        window.add(page);
        // GSettings.bind owns its binding; no manually connected preferences signals.
    }
}
