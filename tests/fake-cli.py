#!/usr/bin/python3
# Generated with AI for personal use. GPL-3.0-or-later.
import json
from pathlib import Path
import sys
import time
mode = sys.argv[1] if len(sys.argv) > 1 else 'valid'
fixture = json.loads(Path(__file__).with_name('inventory.json').read_text())
if mode == 'slow':
    time.sleep(5)
elif mode == 'large':
    sys.stdout.write('x' * (1024 * 1024 + 8192))
    sys.stdout.flush()
elif mode == 'stderr':
    sys.stderr.write('x' * (1024 * 1024 + 8192))
    sys.stderr.flush()
elif mode == 'both':
    for i in range(64):
        sys.stderr.write('x' * 4096)
        sys.stderr.flush()
    print(json.dumps(fixture))
elif mode == 'empty':
    pass
elif mode == 'invalid':
    print('{')
elif mode == 'syntax':
    sys.exit(2)
elif mode in ('agent_unavailable', 'version_mismatch', 'handshake_failed', 'timeout', 'unknown_error'):
    print(json.dumps({'schema_version': 1, 'ok': False, 'error': {'code': mode, 'message': 'Synthetic failure'}}))
    sys.exit(1)
else:
    print(json.dumps(fixture))
