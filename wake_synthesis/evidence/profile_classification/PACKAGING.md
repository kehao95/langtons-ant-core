# Delivery and fresh replay

This commit delivers the previously prepared layer-profile theorem. The proof,
five verification modules and historical evidence retain their original bytes.
Six larger reports are stored losslessly as `NAME.gz`. Decompress them before
checking `manifest.json` against raw evidence bytes:

```sh
python3 - <<'PY'
from pathlib import Path
import gzip, hashlib, json
p = Path('wake_synthesis/evidence/profile_classification')
m = json.loads((p/'manifest.json').read_text())
for name, expected in m['evidence_sha256'].items():
    q = p/name
    data = q.read_bytes() if q.exists() else gzip.decompress((p/(name+'.gz')).read_bytes())
    assert hashlib.sha256(data).hexdigest() == expected, name
print('All historical evidence hashes verified')
PY
```

The historical manifest describes the earlier local snapshot, including its
`remote_modified=false` field; this is not the status of the current delivery.
The current project README is updated navigation and is intentionally different
from that snapshot. Mathematical proof and all five module source hashes are
unchanged. The statement at the end of the proof about no remote action likewise
records the earlier patch's provenance, not this commit.

Before this delivery, another full replay completed with 40 exact cap-168 runs,
40 sanitized cap-104 baseline/refined comparisons and all infinite-tail controls.
Its summary, modular audits, count relaxations, differential report, accepted
words and upper certificate are byte-identical to the retained originals.
Every deterministic search field agrees; elapsed seconds are excluded.
All 215,709,876 prefixes and both accepted masks (92,163) were reproduced.
No published release or paper is changed, and no new publication is authorized.
