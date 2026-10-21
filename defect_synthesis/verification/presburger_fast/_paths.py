"""Load only the hash-pinned, unchanged sibling schema syntax and ISL wrapper."""
from pathlib import Path
import hashlib
import sys
BASE = Path(__file__).resolve().parent.parent / 'presburger_defects'
PINNED = {
    'compiler.py': '7fde492d4f3dac7396893448f40da10f02a670f3',
    'isl_exact.py': '241ba421dd190905e7fe00d1a2049cc866cbe744',
}
for name, expected in PINNED.items():
    data = (BASE / name).read_bytes()
    digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    if digest != expected:
        raise ValueError('The baseline changed; audit this explicit dependency: ' + name)
loaded = sys.modules.get('compiler')
if loaded is not None and Path(loaded.__file__).resolve() != (BASE / 'compiler.py').resolve():
    raise ImportError('A different compiler module is already loaded; use an isolated process')
sys.path.insert(0, str(BASE))
