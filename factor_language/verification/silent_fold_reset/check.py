#!/usr/bin/env python3
"""Regenerate the supplied all-parameter silent-fold certificate; not HC."""
from engine import *

def run():
    grammar=json.loads((HERE/'grammar.json').read_text())
    require(grammar['schema']=='langtons-ant-silent-fold-reset-v1','schema')
    blocks=grammar['blocks'];require(len(blocks)==18 and grammar['fold_blocks']==5,'block count')
    recs,bounds=records(blocks);groups=grouped(recs)
    require(bounds[4]=={'x':-1,'ya':0,'yb':0,'h':3,'time':[56,397]},'fold endpoint')
    require(bounds[-1]=={'x':8,'ya':0,'yb':7,'h':1,'time':[152,2735]},'recovery endpoint')
    I,O,sc,pc=masks_and_caps(groups)
    require(len(sc['top'])+len(sc['bottom'])==76,'initial caps')
    require(len(pc['top'])+len(pc['bottom'])==128,'post-event caps')
    require(all(-5<=q[0]<=2 for q in pc['top']+pc['bottom']),'post source width')
    extras=template_endpoints(I,O,sc,pc)
    # All original inverse-history cells are in this fixed square.
    for x in range(-9,10):
        for y in range(-9,10):
            r=y%4;k=(r-y)//4;extras[x,r].update(((0,k),(0,k+1)))
    tail=blocks[-1]['word'][-104:]
    pts,end,hh=geometry(tail,(8,7),1);drift=end[0]-8,end[1]-7
    require(drift==(2,2) and hh==1,'tail geometry')
    xmin=min(q[0] for q in groups);xmax=max(q[0] for q in groups)
    ray_queries=set()
    for x,y in pts:
        k=0
        while x+2*k<=xmax:
            if x+2*k>=xmin:ray_queries.add((x+2*k,y+2*k))
            k+=1
    for x,y in ray_queries:
        r=y%4;k=(r-y)//4;extras[x,r].update(((0,k),(0,k+1)))
    # Include both group sets so no template-only spatial class can be omitted.
    for q in extras:groups.setdefault(q,[])
    N,nfunc,npairs=bound_for_orders(groups,extras)
    pre_records=[r for r in recs if r.block<5]
    require(all(4-4*r.high[0]>=0 and r.r-4*r.high[1]+26>=0 for r in pre_records),'universal minimum-y inequalities')
    require(any(r.high[0]==1 and r.r-4*r.high[1]==-26 for r in pre_records),'attained affine fold depth')
    require(N<2000,'unexpectedly huge finite certificate')
    W=grammar['standard_word']
    port={(0,-1),(1,1),(1,3),(2,2)}
    port_end=literal(port,(0,0),1,182)
    port_period=literal(port_end[0],port_end[1],port_end[2],104)[3]
    require(port_period==W and parity_tail(port_end[0],port_end[1],port_end[2],W)[0],'inherited standard control')
    allowed={ (W*2)[i:i+10] for i in range(104)}
    require(len(W)==104 and len(allowed)==84 and tail in W*2,'standard identity')
    interval_checks=0;tail_checks=0;endpoint_runs=0;literal_updates=0
    refs=[];stable_top=None
    # Fixed-order all-n reduction: below N exhaustive; above N a single order type.
    for n in range(N+1):
        source,post,final,foot,checks=interval_fields(groups,n)
        interval_checks+=checks
        require(source==field_template(n,I,sc),'all-n source template')
        require(post==field_template(n,O,pc),'all-n post template')
        require(len(source)==10*n+76 and len(post)==18*n+128 and len(final)==18*n+301,'affine masses')
        require(inverse_suffix(source,(0,0),0)=='LLLLRLLLL','initial inverse history')
        valid,num=parity_tail(final,(8,7),1,tail);tail_checks+=num
        require(valid and stable_class_tail(final,(8,7),1,tail),'permanent standard future')
        raybits=frozenset(final&ray_queries)
        if n==N:stable_top=raybits
        # Universal first two origin visits: use symbolic event times, no long replay.
        origin=[r for r in groups[0,0] if ev(r.low,n)<=0<=ev(r.high,n) and r.block<5]
        times=[r.time[0]*n+r.time[2] for r in origin]
        require(times==[0,56*n+396] and [r.letter for r in origin]==['R','L'],'origin lifetime')
        # min/max of read-record geometric endpoints prove the asserted excursion.
        pre=[r for r in recs if r.block<5]
        ymin=min(r.r-4*ev(r.high,n) for r in pre)
        require(ymin==-4*n-26,'fold depth')
    require(affine_mass(groups,N,'source')==[10,76],'stable source mass coefficients')
    require(affine_mass(groups,N,'post')==[18,128],'stable post mass coefficients')
    require(affine_mass(groups,N,'final')==[18,301],'stable final mass coefficients')
    # Independent full literal replay. These checks supplement, not replace, the reduction.
    parameters=sorted({0,1,2,3,4,8,16,32,64,N,N+1,2*N+3})
    jtotals=[]
    for n in parameters:
        fold=power_word(blocks[:5],n);full=power_word(blocks,n)
        source,post,final,foot,_=interval_fields(groups,n)
        require(source==minimal_seed(fold),'independent minimal initial field')
        b,p,h,stream,path=literal(source,(0,0),0,len(full))
        require(stream==full and b==final and p==(8,7) and h==1,'independent complete orbit')
        b1,p1,h1,_,_=literal(source,(0,0),0,len(fold)+1)
        require(b1==post and p1==(-1,1) and h1==0,'first J10 complete endpoint')
        suffix=inverse_suffix(source,(0,0),0)
        observed=suffix+stream+tail[:9]
        bad=[t for t in range(len(stream)+9) if observed[t:t+10] not in allowed]
        require(bad[:9]==list(range(9)) and bad[9]==56*n+397,'first next J10')
        require(len(bad)==56*n+926 and bad[-1]==152*n+2534,'event count and last event')
        require(stream[-208:]==tail*2 and stream[-209]!=tail[-1],'exact first standard boundary')
        require(path[9]==(-1,2) and path[len(fold)]==(-1,0),'fixed J10 macro endpoints')
        require(len(full)==152*n+2735,'duration')
        endpoint_runs+=1;literal_updates+=len(full)+len(fold)+1
        jtotals.append([n,len(bad),bad[-1]])
        refs.append({'n':n,'initial_black':len(source),'post_first_J10_black':len(post),
                     'first_J10_from_time9':56*n+388,'exact_first_standard_time':152*n+2527,
                     'intrinsic_J10_total':len(bad),'complete_final_sha256':digest_field(final)})
    # Inserting a period changes only cyclic factor count, since retained repetitions
    # leave at least nine letters on both sides. Enumerate every interface at n=0,1.
    increments=[]
    for bi,b in enumerate(blocks):
        if b['count'][0]:
            u=b['word'];P=len(u);repeats=b['count'][1]
            require(repeats>=2*((9+P-1)//P),'both length-nine splice contexts')
            cyc=sum((u*((P+9)//P+2))[i:i+10] not in allowed for i in range(P))
            increments.append([bi,P,repeats,cyc])
    require(sum(z[3] for z in increments)==56,'all-n factor-count slope')
    require(all(z[3]==0 for z in increments if z[0]<5),'silent fold factors')
    # The last first-event context and standard-onset context lie in fixed literal caps.
    require(len(blocks[4]['word'])>=9 and len(blocks[5]['word'])>=1,'event cap')
    tables=repair_table(I,O)
    require(all(10*max(0,m-3)>=4*m-136 for m in range(1000)),'perpendicular comparison control')
    # Negative controls against silently dropping the future corridor.
    source,post,final,_,_=interval_fields(groups,0)
    blocker=(pts[0][0]+2*10**20,pts[0][1]+2*10**20)
    ok,_=parity_tail(final|{blocker},(8,7),1,tail)
    require(not ok,'far future blocker must reject')
    marker=(xmax+100, min(y for x,y in final)-100)
    if any((k:=multiple((marker[0]-x,marker[1]-y),drift)) is not None and k>=0 for x,y in pts):
        marker=(xmin-100,0)
    ok,_=parity_tail(final|{marker},(8,7),1,tail)
    require(ok and marker not in final,'off-trace debris guard')
    mutated=json.loads(json.dumps(blocks));u=mutated[5]['word'];mutated[5]['word']=('L' if u[0]=='R' else 'R')+u[1:]
    caught=False
    try:interval_fields(grouped(records(mutated)[0]),0)
    except AssertionError:caught=True
    require(caught,'damaged recovery certificate rejection')
    # Initial black perturbation on the very first visited white cell must disagree.
    require(literal(source|{(0,0)},(0,0),0,1)[3]=='L','initial colour control')
    for n in range(100):
        for m in range(100):
            length=max(0,4*m-136)
            delta=10*m+76-(18*n+128)
            require(3*length-26*delta-322==3*length+468*n-260*m+1030,'clean reset mass-defect algebra')
    table_data={'input_mask':[[x,r,v] for (x,r),v in sorted(I.items())],
                'post_mask':[[x,r,v] for (x,r),v in sorted(O.items())],
                'source_caps':sc,'post_caps':pc,'parallel_mismatches':tables}
    (HERE/'derived_masks.json').write_text(json.dumps(table_data,sort_keys=True,separators=(',',':'))+'\n')
    report={'schema':'silent-fold-reset-audit-v1','base_commit':BASE,
       'scope':'one all-parameter complete-input family and its reset obstruction; no HC solution',
       'proof_boundary':'Affine endpoint ordering with slopes 0/1 proves completeness of representatives n=0,1,2. Universal geometric and reset arguments are written analytic proofs, not kernel-checked.',
       'universal_certificate':{'read_records':len(recs),'spatial_residue_groups':len(groups),
          'affine_breakpoint_functions':nfunc,'cross_slope_pairs':npairs,'stable_order_from_n':N,
          'representatives':N+1,'ordered_read_checks':interval_checks,'tail_parity_checks':tail_checks,
          'fixed_tail_ray_queries':len(ray_queries),'endpoint_x_range':[xmin,xmax]},
       'complete_literal_controls':{'inputs':endpoint_runs,'updates':literal_updates,'parameters':refs},
       'formulae':{'fold_length':'56*n+397','origin_black_age':'56*n+396',
          'J10_macro_from_time9':'first event at offset 56*n+388; source (-1,2),W; read (-1,0),W; post (-1,1),N',
          'first_standard':'152*n+2527','intrinsic_J10_count':'56*n+926',
          'repair_lower_bound':'max(0,4*m-136) literal toggles to enable any pose of w_m from Y_n'},
       'cyclic_factor_increments':increments,
       'reset_certificate':{'parallel_minima':[min(z[2] for z in tables[str(r)]) for r in (0,2)],
           'parallel_comparisons':2*25*4*len(I),'clean_reset_algebra_controls':10000,'initial_cap_black':76,'post_cap_black':128,
           'bulk_target_read_cells':len(I),'bulk_target_black':sum(I.values()),'bulk_post_black':sum(O.values())},
       'negative_controls':{'damaged_recovery_rejected':caught,'remote_blocker_rejected':True,'off_trace_marker_retained':True},
       'sha256':{p.name:sha256(p.read_bytes()).hexdigest() for p in (HERE/'grammar.json',HERE/'derived_masks.json',HERE/'engine.py',HERE/'check.py')}}
    return report


def digest_field(b):return sha256(json.dumps(sorted(b),separators=(',',':')).encode()).hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--compare',type=Path)
    parser.add_argument('--output',type=Path,default=HERE/'report.json')
    args=parser.parse_args()
    report=run();data=json.dumps(report,sort_keys=True,indent=2)+'\n'
    if args.compare:
        require(data==args.compare.read_text(),'report differs from retained evidence')
    args.output.write_text(data)
    print(json.dumps({k:v for k,v in report.items() if k not in ('complete_literal_controls','sha256')},indent=2))
    print('complete literal updates:',report['complete_literal_controls']['updates'])
    print('PASS: all-parameter supplied family, not HC')

if __name__=='__main__':main()
