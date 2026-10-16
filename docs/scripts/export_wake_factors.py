#!/usr/bin/env python3
"""Export browser-sized witnesses from canonical proof certificates (no network)."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
SOURCES = []
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--check", action="store_true", help="compare deterministic exports without writing")
ARGS = parser.parse_args()
def read(path):
    SOURCES.append(path)
    return json.loads((ROOT / path).read_text())
def module(path):
    SOURCES.append(path)
    spec = importlib.util.spec_from_file_location('export_proof', ROOT / path)
    obj = importlib.util.module_from_spec(spec); spec.loader.exec_module(obj)
    return obj
def output(name, data, sources):
    data['provenance'] = [{'path': p, 'sha256': hashlib.sha256((ROOT/p).read_bytes()).hexdigest()} for p in sources]
    destination = ROOT/'docs/data'/f'{name}.json'
    content = json.dumps(data, indent=2)+'\n'
    if ARGS.check:
        if not destination.exists() or destination.read_text() != content:
            raise SystemExit(f'Stale export: {destination.relative_to(ROOT)}')
    else:
        destination.write_text(content)
v = module('wake_synthesis/verification/profile_classification/verify_word.py')
seed, wake, drift = v.synthesize(v.STANDARD)
assert v.forever(seed, v.STANDARD)
parity = read('wake_synthesis/verification/mixed_wake_parity/check_results_full.json')
cases = read('wake_synthesis/verification/thin_wake/evidence/cases.json')
screen = module('wake_synthesis/verification/mixed_wake_parity/mixed_wake.py')
for example in parity['example'].values():
    assert screen.parity_screen(example['wake']) == example['test']
maxlayer = max(t for t,r in wake)
# Translation (0,-maxlayer) normalizes the top and changes checkerboard sigma.
sigma = -1 * (-1 if maxlayer%2 else 1)
output('wake', {'word':v.STANDARD, 'heading':1, 'seed':sorted(seed), 'drift':drift,
 'oddClasses':sorted((t-maxlayer,r) for t,r in wake), 'sigma':sigma,
 'examples':parity['example'], 'cases':[{'hole':c['hole'],'mask':c['mask'],'cap':c['upper'],'jobs':len(c['jobs'])} for c in cases['cases']],
 'proof':{'cases':76,'jobs':83,'integerEdges':90158,'prefixVisits':391065872}}, SOURCES[:])
SOURCES.clear()
mass = read('factor_language/verification/mass/witness.json')
ten = read('factor_language/verification/ten/certificates/witness.json')
silent = read('factor_language/verification/silent_archive_amplification/witness.json')
W=mass['standard_word']; allowed=sorted({(W+W)[i:i+10] for i in range(len(W))})
assert len(allowed)==84
output('factors', {'word':W,'allowed10':allowed,
 'mass':{k:mass[k] for k in ('short_seed','short_witness','global_constant','defect_penalty','vertices','edges')},
 'sharpFamily':ten['sharp_family'],'silent':{k:silent[k] for k in ('pose','true_past9','source','claims')}}, SOURCES[:])
print(('Checked' if ARGS.check else 'Exported') + ' exact wake and factor witnesses with source SHA-256 provenance.')
