"""Check the frozen source manifest and recompute all three scoped reports."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

root=Path(__file__).resolve().parent
if not __debug__:
    raise SystemExit("Run with assertions enabled; do not use python -O")
manifest=json.loads((root/'manifest.json').read_text())
for name,expected in manifest['sha256'].items():
    got=hashlib.sha256((root/name).read_bytes()).hexdigest()
    if got!=expected:
        raise SystemExit('Source/evidence hash mismatch: '+name)
for source,report in [('check.py','check-report.json'),
                      ('independent.py','independent-report.json'),
                      ('cycle_count.py','cycle-count-report.json')]:
    result=subprocess.run([sys.executable,str(root/source)],cwd=root,
                          text=True,capture_output=True,check=True)
    fresh=json.loads(result.stdout)
    frozen=json.loads((root/report).read_text())
    if fresh!=frozen:
        raise SystemExit('Fresh report differs: '+report)
    print('PASS '+source+' == '+report,flush=True)
print('PASS scoped analytic-identity regression package; not a formal HC proof')
