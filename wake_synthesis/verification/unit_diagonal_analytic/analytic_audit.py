"""Regressions for the analytic proof; no finite result is a proof premise."""
from collections import Counter
import local_obstruction as local

MOVE={'N':(0,1),'E':(1,0),'S':(0,-1),'W':(-1,0)}

def first_return(word):
    x=y=0
    for j,c in enumerate(word):
        dx,dy=MOVE[c];x+=dx;y+=dy
        if (x,y)==(0,0):return j==len(word)-1
    return False

def verify():
    paths=('NESW','ENWS','ENESWNWS','SENW','NWSE')
    assert all(first_return(w) for w in paths)
    prefix=[];examined=0
    for c in (2,3):
        for bits in local.candidates(-2,c,c):
            examined+=1
            p=[i for i,b in enumerate(bits) if b]
            q=[i for i,b in enumerate(local.departures(-2,bits)) if b]
            if p[0]==q[1]+1:prefix.append((c,''.join(map(str,bits))))
    assert examined==124 and sorted(prefix)==[(3,'00001101'),(3,'000011010')]
    counts=Counter()
    for c in (5,6):
        for bits in local.candidates(-3,c,c):
            counts['third_layer_candidates']+=1
            p=[i for i,b in enumerate(bits) if b]
            q=[i for i,b in enumerate(local.departures(-3,bits)) if b]
            if p[2]==q[1]+1 and p[4]==q[3]+1:
                counts['both_forced_returns']+=1
                assert p[1]==q[1] or p[4]==q[4]
                counts['forbidden_bridge_forced']+=1
    assert counts['third_layer_candidates']==12756
    return dict(status='complete',role='regression, not a mathematical premise',
                first_return_compass_paths=list(paths),second_layer_candidates=examined,
                forced_second_layer_words=prefix,interleaving_checks=dict(counts))

if __name__=='__main__':
    import json
    if not __debug__:raise RuntimeError('Run without Python -O')
    print(json.dumps(verify(),indent=2))
