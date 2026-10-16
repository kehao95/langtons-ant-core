#!/usr/bin/env python3
"""Check available analytic inputs; full numerical replay requires the original archive."""
import argparse,hashlib,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def analytic_controls():
    proof=(ROOT/'proof/canonical-highway-one-bit-stability.md').read_text()
    word=re.search(r'    W=([LR]+)\.',proof).group(1)
    thresholds=[int(x.strip().rstrip('.')) for x in re.search(r'threshold sequence, in phase order, is\n\n(.*?)\n\nThus',proof,re.S).group(1).replace('\n','').split(',') if x.strip().rstrip('.')]
    P={(0,-2),(0,-1),(0,0),(1,-1),(2,-1),(2,1),(3,-2),(3,1),(4,-2),(4,0),(5,-1),(5,0),(6,0)}
    D={(0,-3),(0,0),(1,-4),(1,-3),(1,-2),(2,-1),(2,0),(3,0),(6,-1),(7,-1),(7,0),(8,-1)}
    dirs=((0,1),(1,0),(0,-1),(-1,0));field=set(P);x=y=0;h=2;positions=[]
    for letter in word:
        positions.append((x,y))
        assert letter==('L' if (x,y) in field else 'R')
        field.symmetric_difference_update({(x,y)})
        h=(h+(-1 if letter=='L' else 1))%4
        dx,dy=dirs[h];x+=dx;y+=dy
    assert len(word)==104 and (x,y,h)==(2,-2,2)
    shifted={(x+2,y-2) for x,y in P}
    assert not shifted&D and field==shifted|D
    def multiple(q):
        x,y=q
        return x//2 if x%2==0 and y==-x else None
    assert len({(x+y,x%2) for x,y in D})==12
    for a in D:
        for b in P:
            k=multiple((a[0]-b[0],a[1]-b[1]))
            assert k is None or k<1
    # Complete phase-ray proof from P: old black hits and all self-write thresholds.
    for i,(x,y) in enumerate(positions):
        hits={k for bx,by in P if (k:=multiple((bx-x,by-y))) is not None and k>=0}
        flips=[]
        for j,(jx,jy) in enumerate(positions):
            k=multiple((jx-x,jy-y))
            if k is not None and (k>0 or (k==0 and j<i)):flips.append(k)
        boundaries={0,*hits,*[k+1 for k in hits],*flips}
        boundaries.add(max(boundaries)+1)
        for k in boundaries:
            assert ((k in hits) ^ (sum(z<=k for z in flips)%2==1))==(word[i]=='L')
    assert len(thresholds)==104 and max(thresholds)==25 and sum(n+1 for n in thresholds)==739
    return {'canonical_word_length':104,'period_drift':[2,-2], 'complete_deposition_identity':True,
            'permanent_canonical_tail':True,'thresholds':104,'required_records':739,
            'numerical_recovery_certificate_replayed':False}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--analytic-controls',action='store_true')
    ap.add_argument('--output-report',type=Path)
    args=ap.parse_args()
    if not __debug__:ap.error('Run without Python -O')
    if not args.analytic_controls:
        manifest=json.loads((ROOT/'evidence/original-package-manifest.json').read_text())
        raise SystemExit('Full recovery replay unavailable: restore '+manifest['artifact_name']+' (SHA256 '+manifest['artifact_sha256']+'). Use --analytic-controls for the available source identities only.')
    report=analytic_controls()
    report['status']='partial-controls-passed'
    report['checker_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    if args.output_report:args.output_report.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
