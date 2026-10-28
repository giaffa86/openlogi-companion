// SPDX-License-Identifier: GPL-3.0-or-later
// Generated with AI for personal use.
// Do NOT upload to extensions.gnome.org (EGO) unless you understand JavaScript
// and can maintain this code.

export class DataError extends Error {
    constructor(code) {
        super(code);
        this.code = code;
    }
}

function object(value) {
    return value !== null && typeof value === 'object' && !Array.isArray(value);
}

function nullableString(value) {
    return value === null || value === undefined || typeof value === 'string';
}

export function parseInventory(text, exitStatus) {
    let envelope;
    try {
        envelope = JSON.parse(text);
    } catch (_error) {
        throw new DataError(exitStatus === 2 ? 'incompatible' : 'invalid');
    }
    if (!object(envelope) || !Number.isInteger(envelope.schema_version))
        throw new DataError('invalid');
    if (envelope.schema_version !== 1)
        throw new DataError('incompatible');
    if (typeof envelope.ok !== 'boolean')
        throw new DataError('invalid');
    if (!envelope.ok) {
        if (!object(envelope.error) || typeof envelope.error.code !== 'string' || typeof envelope.error.message !== 'string')
            throw new DataError('invalid');
        if (exitStatus !== 1)
            throw new DataError('invalid');
        const code = envelope.error.code;
        if (['version_mismatch', 'handshake_failed'].includes(code))
            throw new DataError('incompatible');
        if (['agent_unavailable', 'disconnected'].includes(code))
            throw new DataError('agent-unavailable');
        throw new DataError(code === 'timeout' ? 'timeout' : 'unavailable');
    }
    if (exitStatus !== 0)
        throw new DataError('invalid');
    const data = envelope.data;
    if (!object(data) || !['scanning', 'ready', 'unavailable'].includes(data.inventory) || !Array.isArray(data.devices))
        throw new DataError('invalid');
    const devices = data.devices.map(device => {
        if (!object(device) || !nullableString(device.id) || !nullableString(device.name) ||
            typeof device.kind !== 'string' || typeof device.online !== 'boolean')
            throw new DataError('invalid');
        const battery = device.battery ?? null;
        if (battery !== null) {
            if (!object(battery) || !nullableString(battery.level) || !nullableString(battery.status))
                throw new DataError('invalid');
            const percentage = battery.percentage;
            if (percentage !== null && percentage !== undefined &&
                (!Number.isInteger(percentage) || percentage < 0 || percentage > 100))
                throw new DataError('invalid');
        }
        return {id: device.id ?? null, name: device.name ?? '', kind: device.kind, online: device.online,
            battery: battery && {percentage: battery.percentage ?? null, level: battery.level ?? null, status: battery.status ?? null}};
    });
    const collator = new Intl.Collator(undefined, {numeric: true, sensitivity: 'base'});
    devices.sort((a, b) => Number(b.online) - Number(a.online) || collator.compare(a.name, b.name));
    return {inventory: data.inventory, devices};
}

export function panelDevice(devices, id) {
    const matches = devices.filter(device => device.id !== null && device.id === id);
    return matches.length === 1 && matches[0].online ? matches[0] : null;
}

export function batteryText(device, _) {
    if (!device.online)
        return _('Offline; battery reading is not current');
    const battery = device.battery;
    if (!battery)
        return _('Battery unavailable');
    const levels = {critical: _('Critical'), low: _('Low'), good: _('Good'), full: _('Full')};
    const status = {charging: _('Charging'), charging_slow: _('Charging slowly'), full: _('Charged'),
        discharging: _('On battery'), error: _('Charging error')};
    const charge = battery.percentage !== null
        ? new Intl.NumberFormat(undefined, {style: 'percent'}).format(battery.percentage / 100)
        : levels[battery.level] ?? _('Battery unavailable');
    return status[battery.status] ? `${charge} · ${status[battery.status]}` : charge;
}
