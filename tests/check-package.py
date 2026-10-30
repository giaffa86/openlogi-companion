# SPDX-License-Identifier: GPL-3.0-or-later.
import json
from pathlib import Path
import sys
import zipfile
root = Path(__file__).resolve().parent.parent
expected = (root / 'scripts/runtime-files.txt').read_text().splitlines()
with zipfile.ZipFile(sys.argv[1]) as archive:
    assert sorted(archive.namelist()) == sorted(expected)
    metadata = json.loads(archive.read('metadata.json'))
    assert metadata['uuid'] == 'openlogi-companion@giaffa86'
    assert metadata['shell-version'] == ['50']
    # EGO sets the version itself and expects a repository URL.
    assert 'version' not in metadata, 'deprecated version key in the bundle'
    assert metadata['url'].startswith('https://'), metadata.get('url')
    for filename in expected:
        assert archive.read(filename) == (root / filename).read_bytes(), filename
        if filename.endswith('-symbolic.svg'):
            # Symbolic recolouring overrides the fill of every path, so a stroked
            # shape or fill="none" would be painted as a solid blob in the panel.
            icon = archive.read(filename).decode()
            assert 'stroke' not in icon, f'{filename}: symbolic icons must use fills only'
            assert 'fill="none"' not in icon, f'{filename}: fill="none" is ignored'
        if filename.endswith('.js'):
            import re
            for relative in re.findall(r"from ['\"](\.[^'\"]+)['\"]", archive.read(filename).decode()):
                import posixpath
                target = posixpath.normpath(posixpath.join(posixpath.dirname(filename), relative))
                assert target in expected, target
print('ZIP: explicit manifest, source equality and relative imports verified')
