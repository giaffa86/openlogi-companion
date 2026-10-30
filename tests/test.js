// SPDX-License-Identifier: GPL-3.0-or-later

import Gio from 'gi://Gio';
import GLib from 'gi://GLib';
import System from 'system';
import {parseInventory, panelDevice, batteryText} from '../shell/contract.js';
import {Provider} from '../shell/provider.js';

let checks = 0;
function assert(value, message) {
    if (!value)
        throw new Error(message);
    checks++;
}
const root = GLib.path_get_dirname(GLib.filename_from_uri(import.meta.url)[0]);
const [, bytes] = GLib.file_get_contents(`${root}/inventory.json`);
const fixture = new TextDecoder().decode(bytes);
const identity = text => text;
function expectError(action, code) {
    try {
        action();
    } catch (error) {
        assert(error.code === code, `Expected ${code}, got ${error.code}`);
        return;
    }
    throw new Error(`Missing error ${code}`);
}
async function main() {
    const snapshot = parseInventory(fixture, 0);
    assert(snapshot.devices.length === 9, 'No merging duplicate IDs/names or missing IDs');
    assert(snapshot.devices.at(-1).online === false, 'Connected first');
    const zero = snapshot.devices.find(d => d.id === 'synthetic-a');
    assert(batteryText(zero, identity).includes('0%'), 'Zero is valid');
    assert(batteryText(snapshot.devices.find(d => d.id === 'synthetic-b'), identity).includes('100%'), 'Full');
    assert(batteryText(snapshot.devices.find(d => d.id === null), identity).includes('Low'), 'Level without percentage');
    assert(!batteryText(snapshot.devices.at(-1), identity).includes('84'), 'Offline reading never current');
    assert(panelDevice(snapshot.devices, 'duplicate') === null, 'Reject ambiguous selection');
    assert(panelDevice(snapshot.devices, null) === null, 'Reject absent IDs');
    assert(panelDevice(snapshot.devices, 'offline') === null, 'Reject offline selection');
    assert(panelDevice(snapshot.devices, 'synthetic-a') === zero, 'Unique session selection');
    assert(panelDevice([], 'synthetic-a') === null, 'Disappearance clears selection');
    const charging = snapshot.devices.find(d => d.id === 'charging-no-reading');
    assert(charging.battery !== null && charging.battery.percentage === null, 'Battery without reading kept');
    assert(batteryText(charging, identity).includes('Charging'), 'Charging state without percentage');
    assert(panelDevice(snapshot.devices, 'charging-no-reading') === charging, 'Unread battery still selectable');
    const raw = JSON.parse(fixture);
    for (const state of ['scanning', 'unavailable', 'ready']) {
        raw.data.inventory = state;
        raw.data.devices = [];
        assert(parseInventory(JSON.stringify(raw), 0).inventory === state, `Distinct ${state}`);
    }
    raw.schema_version = 2;
    expectError(() => parseInventory(JSON.stringify(raw), 0), 'incompatible');
    for (const text of ['', '{', 'null', '[]', '{}'])
        expectError(() => parseInventory(text, 0), 'invalid');
    for (const patch of [{online: 'yes'}, {name: 4}, {id: []}, {kind: null},
        {battery: []}, {battery: {percentage: -1}}, {battery: {percentage: 101}},
        {battery: {percentage: '0'}}, {battery: {percentage: 1.5}}, {battery: {level: 3}}]) {
        const malformed = JSON.parse(fixture);
        Object.assign(malformed.data.devices[0], patch);
        expectError(() => parseInventory(JSON.stringify(malformed), 0), 'invalid');
    }
    expectError(() => parseInventory(fixture, 1), 'invalid');
    const failure = JSON.stringify({schema_version: 1, ok: false, error: {code: 'agent_unavailable', message: 'synthetic'}});
    expectError(() => parseInventory(failure, 0), 'invalid');
    const make = (mode, options = {}) => new Provider({argv: ['/usr/bin/python3', `${root}/fake-cli.py`, mode], ...options});
    for (const [mode, code] of [['agent_unavailable', 'agent-unavailable'], ['version_mismatch', 'incompatible'],
        ['handshake_failed', 'incompatible'], ['timeout', 'timeout'], ['unknown_error', 'unavailable'],
        ['invalid', 'invalid'], ['empty', 'invalid'], ['syntax', 'incompatible'],
        ['large', 'output-limit'], ['stderr', 'output-limit'], ['slow', 'timeout']]) {
        const provider = make(mode, {timeout: 1000});
        try {
            await provider.refresh();
            throw new Error(`Missing failure ${mode}`);
        } catch (error) {
            assert(error.code === code, `${mode}: ${error.code}`);
        }
        assert(provider._request === null, `${mode}: request released`);
        provider.destroy();
    }
    const missing = new Provider({argv: ['/nonexistent-openlogi-companion-test']});
    try {
        await missing.refresh();
        throw new Error('Missing executable succeeded');
    } catch (error) {
        assert(error.code === 'cli-missing', 'CLI missing');
    }
    missing.destroy();
    const provider = make('both');
    const a = provider.refresh();
    const b = provider.refresh();
    assert(a === b, 'Overlap coalesced into one request');
    assert((await a).devices.length === 9, 'Concurrent stderr drain without deadlock');
    provider.destroy();
    const pending = make('slow');
    const promise = pending.refresh();
    const process = pending._request.process;
    pending.destroy();
    try {
        await promise;
        throw new Error('Cancelled request succeeded');
    } catch (error) {
        assert(error.code === 'cancelled', 'Teardown cancels request');
    }
    assert(process.get_if_signaled(), 'Owned child terminated and reaped');
    assert(pending._request === null, 'No pending ownership');
    const reconnected = make('valid');
    assert((await reconnected.refresh()).devices.length === 9, 'Fresh provider after teardown');
    reconnected.destroy();
    print(`${checks} contract/provider checks passed (GJS, synthetic data)`);
}
const loop = new GLib.MainLoop(null, false);
let status = 0;
main().catch(error => { console.error(error); status = 1; }).finally(() => loop.quit());
loop.run();
System.exit(status);
