// SPDX-License-Identifier: GPL-3.0-or-later
// Generated with AI for personal use.
// Do NOT upload to extensions.gnome.org (EGO) unless you understand JavaScript
// and can maintain this code.

import Gio from 'gi://Gio';
import GLib from 'gi://GLib';
import {DataError, parseInventory} from './contract.js';

// Each read allocates at most 8192 bytes. Both pipes share one budget.
async function readPipe(stream, request, retain) {
    const chunks = [];
    let length = 0;
    while (true) {
        const bytes = await new Promise((resolve, reject) => {
            stream.read_bytes_async(8192, GLib.PRIORITY_DEFAULT, request.cancel, (source, result) => {
                try {
                    resolve(source.read_bytes_finish(result));
                } catch (error) {
                    reject(error);
                }
            });
        });
        const size = bytes.get_size();
        if (!size)
            break;
        request.bytes += size;
        if (request.bytes > request.limit)
            throw new DataError('output-limit');
        if (retain) {
            chunks.push(bytes.toArray());
            length += size;
        }
    }
    const output = new Uint8Array(length);
    let offset = 0;
    for (const chunk of chunks) {
        output.set(chunk, offset);
        offset += chunk.length;
    }
    return new TextDecoder('utf-8', {fatal: true}).decode(output);
}

export class Provider {
    constructor({argv = ['openlogi', 'api', 'devices'], timeout = 5000, limit = 1024 * 1024} = {}) {
        this._argv = argv;
        this._timeout = timeout;
        this._limit = limit;
        this._request = null;
    }

    refresh() {
        if (this._request)
            return this._request.promise;
        const request = {cancel: new Gio.Cancellable(), process: null, timer: 0, bytes: 0, limit: this._limit, reason: null};
        this._request = request;
        request.promise = this._run(request).finally(() => {
            if (this._request === request)
                this._request = null;
        });
        return request.promise;
    }

    destroy() {
        const request = this._request;
        this._request = null;
        this._argv = null;
        if (request)
            this._stop(request, 'cancelled');
    }

    _stop(request, reason) {
        request.reason ??= reason;
        if (request.timer) {
            GLib.Source.remove(request.timer);
            request.timer = 0;
        }
        request.cancel.cancel();
        if (request.process)
            request.process.force_exit();
    }

    async _run(request) {
        try {
            request.process = Gio.Subprocess.new(this._argv,
                Gio.SubprocessFlags.STDOUT_PIPE | Gio.SubprocessFlags.STDERR_PIPE);
        } catch (error) {
            if (error.matches(GLib.spawn_error_quark(), GLib.SpawnError.NOENT))
                throw new DataError('cli-missing');
            throw new DataError('unavailable');
        }
        const process = request.process;
        request.timer = GLib.timeout_add(GLib.PRIORITY_DEFAULT, this._timeout, () => {
            request.timer = 0;
            this._stop(request, 'timeout');
            return GLib.SOURCE_REMOVE;
        });
        // wait_async is intentionally not cancellable: every owned child is reaped.
        const waited = new Promise((resolve, reject) => process.wait_async(null, (source, result) => {
            try {
                source.wait_finish(result);
                resolve();
            } catch (error) {
                reject(error);
            }
        }));
        const stdout = process.get_stdout_pipe();
        const stderr = process.get_stderr_pipe();
        const guardedRead = (stream, retain) => readPipe(stream, request, retain).catch(error => {
            this._stop(request, error instanceof DataError ? error.code : 'invalid');
            throw error;
        });
        try {
            const results = await Promise.allSettled([guardedRead(stdout, true), guardedRead(stderr, false), waited]);
            if (request.reason)
                throw new DataError(request.reason);
            if (results.some(result => result.status === 'rejected'))
                throw new DataError('unavailable');
            if (!process.get_if_exited())
                throw new DataError('unavailable');
            return parseInventory(results[0].value, process.get_exit_status());
        } finally {
            if (request.timer) {
                GLib.Source.remove(request.timer);
                request.timer = 0;
            }
            stdout.close(null);
            stderr.close(null);
            request.process = null;
        }
    }
}
