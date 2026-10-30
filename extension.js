// SPDX-License-Identifier: GPL-3.0-or-later

import {Extension} from 'resource:///org/gnome/shell/extensions/extension.js';
import {Indicator} from './shell/indicator.js';

export default class OpenLogiCompanion extends Extension {
    enable() {
        this._indicator = new Indicator(this);
    }

    disable() {
        this._indicator.destroy();
        this._indicator = null;
    }
}
