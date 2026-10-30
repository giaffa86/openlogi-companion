// SPDX-License-Identifier: GPL-3.0-or-later

import Clutter from 'gi://Clutter';
import GObject from 'gi://GObject';
import Pango from 'gi://Pango';
import St from 'gi://St';
import * as PopupMenu from 'resource:///org/gnome/shell/ui/popupMenu.js';
import {gettext as _} from 'resource:///org/gnome/shell/extensions/extension.js';
import {batteryText} from './contract.js';

export const KIND_ICONS = {mouse: 'input-mouse-symbolic', trackball: 'input-mouse-symbolic',
    keyboard: 'input-keyboard-symbolic', numpad: 'input-dialpad-symbolic', touchpad: 'input-touchpad-symbolic',
    light: 'display-brightness-symbolic', headset: 'audio-headphones-symbolic', gamepad: 'input-gaming-symbolic'};

export function kindIcon(kind) {
    return KIND_ICONS[kind] ?? 'input-keyboard-symbolic';
}

export const DeviceRow = GObject.registerClass(class DeviceRow extends PopupMenu.PopupBaseMenuItem {
    _init(device, openApp, select) {
        super._init({style_class: 'openlogi-companion-device'});
        this._icon = new St.Icon({style_class: 'popup-menu-icon'});
        this.add_child(this._icon);
        const column = new St.BoxLayout({orientation: Clutter.Orientation.VERTICAL, x_expand: true});
        this._name = new St.Label({x_expand: true});
        this._name.clutter_text.ellipsize = Pango.EllipsizeMode.END;
        this._detail = new St.Label({style_class: 'openlogi-companion-detail', x_expand: true});
        this._detail.clutter_text.ellipsize = Pango.EllipsizeMode.END;
        column.add_child(this._name);
        column.add_child(this._detail);
        this.add_child(column);
        this._pin = new St.Button({style_class: 'button openlogi-companion-pin', can_focus: true,
            accessible_name: _('Show this device in the panel'),
            child: new St.Icon({icon_name: 'view-pin-symbolic', style_class: 'popup-menu-icon'})});
        this._pin.connect('clicked', () => select(this.device));
        this.add_child(this._pin);
        this.connect('activate', openApp);
        this.update(device, false, false);
    }

    update(device, pinnable, selected) {
        this.device = device;
        this._icon.icon_name = kindIcon(device.kind);
        this._name.text = device.name || _('Unnamed device');
        this._detail.text = `${device.online ? _('Connected') : _('Disconnected')} · ${batteryText(device, _)}`;
        this.accessible_name = `${this._name.text}. ${this._detail.text}. ${_('Select the device in the OpenLogi app')}`;
        this._pin.reactive = pinnable;
        this._pin.can_focus = pinnable;
        this._pin.visible = pinnable;
        this._pin.accessible_name = selected ? _('Remove this device from the panel') : _('Show this device in the panel');
        if (selected)
            this._pin.add_style_pseudo_class('checked');
        else
            this._pin.remove_style_pseudo_class('checked');
    }
});
