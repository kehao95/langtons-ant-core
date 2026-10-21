#!/usr/bin/env python3
"""Rebuild the complete nine-factor certificate and exact eight-factor counterfamily."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
from mass_bound import independent_enumeration,graph_certificate
from eight_witness import verify as verify_eight

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[2]

def main():
    if not __debug__:raise RuntimeError('Do not use -O')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--compare',type=Path)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    native=REPO/'research/nine_factor/enumerate.cpp'
    with tempfile.TemporaryDirectory(prefix='nine-mass-') as td:
        work=Path(td);binary=work/'enumerate';words=work/'nine150.txt'
        subprocess.run(['g++','-std=c++17','-O2',str(native),'-o',str(binary)],check=True)
        run=subprocess.run([str(binary),'9','150','10000000',str(words)],capture_output=True,text=True,check=True)
        finite=json.loads(run.stdout);assert finite['complete'] and finite['words']==164283
        raw=words.read_bytes();sha=hashlib.sha256(raw).hexdigest()
        independent=independent_enumeration()
        assert independent['nodes']==finite['nodes'] and independent['words']==finite['words']
        assert independent['words_sha256']==sha=='61e8ac60994d9dfcdcbf9a0366378215cc0969ec636d1f69d21e4a02f5c1a1a9'
        patterns=json.loads((ROOT/'forbidden_factors.json').read_text())['words']
        result=graph_certificate(raw.decode().splitlines(),patterns)
        assert result['max_all_path_cost']==1004 and independent['max_short_deficit']==322
        eight=verify_eight()
        sources={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
                 for name in ('mass_bound.py','eight_witness.py','check.py','forbidden_factors.json')}
        sources['research/nine_factor/enumerate.cpp']=hashlib.sha256(native.read_bytes()).hexdigest()
        report={'schema':'langtons-ant-nine-mass-and-sharp-window-v1',
          'scope':'Analytic coverage plus exact finite certificate. No nine-factor attraction, finite HC negative or global HC proof.',
          'native_enumeration':finite,'independent_enumeration':independent,
          'nine_factor':result,'eight_factor':eight,'sources_sha256':sources}
        # JSON is the certificate contract: tuple coordinates serialize as lists.
        # Normalize the freshly built report before comparing with parsed JSON.
        report=json.loads(json.dumps(report,ensure_ascii=False))
        if args.compare:
            old=json.loads(args.compare.read_text())
            if report!=old:raise RuntimeError('deterministic nine-mass report mismatch')
        if args.output:args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
        print('PASS: complete nine-factor bound 1004; eight-factor finite-prefix counterfamily; not HC closure.',flush=True)
        print(json.dumps({'finite_words':finite['words'],'product_edges_checked':result['complex_component']['product_edges'],
                          'nine_bound':1004,'short_prefix_bound':322,'eight_period':22,'eight_deficit_per_period':66}))

if __name__=='__main__':main()
