"""Regenerate all necessary 11-layer masks and exact port count relaxation."""
import subprocess,sys,json,hashlib,tempfile
from pathlib import Path
from masks import raw_masks,canonical,sha
ROOT=Path(__file__).parent
with tempfile.TemporaryDirectory(prefix='hc-moment-masks-') as td:
    binary=Path(td)/'count_screen'
    subprocess.run(['g++','-std=c++17','-O2',str(ROOT/'count_screen.cpp'),'-o',str(binary)],check=True)
    raw=raw_masks()
    r=subprocess.run([str(binary)],input=''.join(' '.join(map(str,x))+'\n' for x in raw),text=True,capture_output=True,check=True,timeout=180)
    accepted=[tuple(map(int,s.split()))for s in r.stdout.splitlines()]
    rep=canonical(accepted,set(raw))
    obj={'schema':'width10-wake-mask-v1','raw_count':len(raw),'count_feasible':len(accepted),'lane_swap_identifications':len(accepted)-len(rep),'representatives':len(rep),'representatives_leq168':sum(x[3]<=168 for x in rep),'raw_sha256':sha(raw),'count_pass_sha256':sha(accepted),'representative_sha256':sha(rep),'rows':rep}
    target=ROOT/'masks.json'
    if '--write' in sys.argv:
        target.write_text(json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n')
        print('WROTE',target,flush=True)
    else:
        expected=json.loads(target.read_text())
        if json.loads(json.dumps(obj))!=expected:raise AssertionError('frozen count candidates mismatch')
        print('PASS all normalized masks and count relaxation',len(rep),flush=True)
