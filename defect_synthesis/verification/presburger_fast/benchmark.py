"""Recorded one-shot decisions and factor-construction costs, not universal speed claims.

Common Schema construction and the old ISL context/source setup are outside
the timers; new totals include fresh solver setup. Exact timer locations below
define the comparison.
The legacy path computes explicit domains/fields before asking nonemptiness;
the new path keeps a succinct circuit. This output-representation difference is
intentional and documented. Three repeats, median; no extrapolated runtimes.
"""
from __future__ import annotations
import _paths  # Pin and load the unchanged sibling schema syntax.
import argparse
import gc
import json
import resource
import statistics
import time
from pathlib import Path
from compiler import Schema,Power,var,W,T,A,factor_cases,compile_schema
from isl_exact import Context
from stream_qf import Circuit,Encoder,point_source,Segment,atom
from factor_dag import count_circuit
from solver import Session,version
from check_fast import STANDARD,source_isl


def factors():
    out=[]
    for n in (4,8,12,16):
        ps=tuple(f'kk{i}' for i in range(n));parts=[]
        for i,p in enumerate(ps):
            u=(W,T,A)[i%3];shift=(i*7)%len(u);u=u[shift:]+u[:shift]
            parts.extend([Power(u,var(p)),'LR' if i%2 else 'RLL'])
        s=Schema(ps,parts)
        oldtimes=[];newtimes=[]
        for _ in range(3):
            start=time.perf_counter();cases=factor_cases(s);oldtimes.append(time.perf_counter()-start)
            count=len(cases);del cases;gc.collect()
            start=time.perf_counter();c=Circuit(ps);result,_=count_circuit(s,c);newtimes.append(time.perf_counter()-start)
        if count!=2**n:raise AssertionError('wrong baseline branch count')
        row=dict(powers=n,old_cases=count,new_circuit_nodes=c.nodes,new_bytes=len(c.text().encode()),
                 old_seconds=oldtimes,new_seconds=newtimes,
                 median_ratio=statistics.median(oldtimes)/statistics.median(newtimes))
        out.append(row);print('factor',row,flush=True)
    for n in (32,64,128):
        ps=tuple(f'kk{i}' for i in range(n));parts=[]
        for i,p in enumerate(ps):
            u=(W,T,A)[i%3];shift=(i*7)%len(u);u=u[shift:]+u[:shift]
            parts.extend([Power(u,var(p)),'LR' if i%2 else 'RLL'])
        s=Schema(ps,parts);start=time.perf_counter();c=Circuit(ps);count_circuit(s,c);elapsed=time.perf_counter()-start
        row=dict(powers=n,old_cases_formula=str(2**n),old_executed=False,
                 new_circuit_nodes=c.nodes,new_bytes=len(c.text().encode()),new_seconds=elapsed)
        out.append(row);print('wide',row,flush=True)
    return out


def decisions():
    n=var('nn');m=var('mm')
    workloads=[('standard',Schema(('nn','mm'),[Power(W,n)]),point_source(STANDARD)),
               ('interrupted_pair',Schema(('nn','mm'),[Power(W,n),'LR',Power(W,m)]),point_source(STANDARD)),
               ('changed_final_turn',Schema(('nn','mm'),[Power(W,n),'L']),point_source(STANDARD)),
               ('finite_rail',Schema(('nn','mm'),[Power('LRRL',m)],heading=1),
                (Segment((0,0),(2,0),n),Segment((1,0),(2,0),n)))]
    out=[]
    for name,s,source in workloads:
        oldtime=[];newtime=[];gen=[];sat=[]
        for _ in range(3):
            ctx=Context(30000000);bs=source_isl(s,ctx,source);start=time.perf_counter()
            old=compile_schema(s,ctx,bs);oldans=not old.feasible.is_empty();oldtime.append(time.perf_counter()-start)
            start=time.perf_counter();e=Encoder(s,source);middle=time.perf_counter()
            with Session(30000) as z:
                z.run(e.smt());answer=z.check()
            end=time.perf_counter()
            if answer not in ('sat','unsat') or (answer=='sat')!=oldans:raise AssertionError('different decisions')
            newtime.append(end-start);gen.append(middle-start);sat.append(end-middle)
        row=dict(name=name,answer=answer,legacy_seconds=oldtime,new_total_seconds=newtime,
                 new_build_seconds=gen,new_solver_seconds=sat,encoding=e.stats(),
                 median_ratio=statistics.median(oldtime)/statistics.median(newtime))
        out.append(row);print('decision',row,flush=True)
    return out


def main():
    p=argparse.ArgumentParser();p.add_argument('--part',choices=['factors','decisions'],required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    report={'scope':'wall-clock local comparison; no full budget cover; source fields unchanged',
            'solver':version(),'repeats':3,a.part:globals()[a.part](),
            'process_peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
