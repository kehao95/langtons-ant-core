"""Reproduce only the finite detour experiment, not an HC classification."""
from __future__ import annotations
from hashlib import sha256
from pathlib import Path
import json, re, subprocess, sys, tempfile
import wake

HERE=Path(__file__).resolve().parent
if sys.flags.optimize: raise SystemExit('Run without Python -O')

# Independent Python depth-first state, using a dictionary instead of the C++
# reverse chronological scan. This checks the complete smaller domain only.
def reference(limit):
    loops=tests=hits=0
    last={}
    def visit(p,h,s):
        nonlocal loops,tests,hits
        if s and p==(0,0) and h==0:
            loops+=1
            for i in range(104):
                tests+=1
                hits+=wake.periodic_data(wake.STANDARD[:i]+s+wake.STANDARD[i:]) is not None
        if len(s)==limit: return
        old=last.get(p)
        for c in ('R','L'):
            if c==old: continue
            g=(h+(1 if c=='R' else -1))%4
            d=wake.MOVES[g];q=(p[0]+d[0],p[1]+d[1])
            if abs(q[0])+abs(q[1])>limit-len(s)-1:continue
            last[p]=c;visit(q,g,s+c)
            if old is None:del last[p]
            else:last[p]=old
    visit((0,0),0,'')
    return {'loops':loops,'tests':tests,'hits':hits}

with tempfile.TemporaryDirectory(prefix='langton-detours-') as tmp:
    exe=Path(tmp)/'search'
    subprocess.run(['g++','-O3','-std=c++17',str(HERE/'detour_search.cpp'),'-o',str(exe)],check=True)
    result={}
    for length in (20,28):
        run=subprocess.run([str(exe),str(length),wake.STANDARD],capture_output=True,text=True,check=True)
        assert not run.stdout.strip(), 'Unexpected positive witness: retain and inspect it'
        m=re.fullmatch(r'loops=(\d+) tests=(\d+) hits=(\d+)\s*',run.stderr)
        assert m
        result[str(length)]=dict(zip(('loops','tests','hits'),map(int,m.groups())))
    assert result['20']=={'loops':490,'tests':50960,'hits':0}
    assert result['28']=={'loops':14386,'tests':1496144,'hits':0}
    control=reference(20)
    assert control==result['20']

report={'schema':'langtons-ant-detour-search-v1','status':'completed',
        'domain':'closed-pose, internally alternating inserted fragments at all 104 standard boundaries',
        'C++_runs':result,'independent_python_max_length':20,'independent_python':control,
        'counts_are_pairs_not_distinct_result_words':True,'all_period_exclusion':False,
        'longer_attempt':{'max_length':36,'completed':False,'claimed_counts':None},
        'sha256':{p.name:sha256(p.read_bytes()).hexdigest() for p in (HERE/'detour_search.cpp',HERE/'search_replay.py',HERE/'wake.py')}}
(HERE/'detour_results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
