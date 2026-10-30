"""Exact symbolic query for a supplied k; no expansion of its long highway."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from verify import verify_basis, move, scale, field_digest
ROOT=Path(__file__).resolve().parent

def query(k: int, include_field: bool=False):
    if type(k) is not int or k<0:
        raise ValueError('k must be a nonnegative integer')
    c=json.loads((ROOT/'witness.json').read_text());b=verify_basis(c)
    result={'k':str(k),'initial_black_cells':[list(q)for q in sorted(move(b['seed'],scale(k,b['stride'])))],
            'initial_head':[0,0],'initial_heading':0,'first_impact':str(13318+104*k),
            'first_permanent_P104':str(18743+220*k),'certificate_boundary':str(18921+220*k),
            'RLRLR_occurrences':str(259+k),'contained_defects':str(6702+47*k),'intrinsic_defects':str(6706+47*k),
            'endpoint_black_mass':str(1645+24*k),'endpoint_head':list(b['pose'][0]),
            'endpoint_heading':b['pose'][1],'infinite_suffix':b['O'],
            'literal_k_expansion':False,'scope':'this six-cell family, not a global HIGHWAY decider'}
    if include_field:
        result['complete_endpoint_xor']={
            'base_points':[list(q)for q in sorted(b['H'])],
            'segments':([{'start':list(q),'stride':list(b['stride']),'length':str(k)}
                         for q in sorted(b['Q'])] if k else [])}
    else:
        result['base_field_sha256']=field_digest(b['H'])
        result['archive_pattern_sha256']=field_digest(b['Q'])
        result['archive_terms']=140 if k else 0
        result['archive_segment_length']=str(k)
    return result

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('k',type=int);ap.add_argument('--include-field',action='store_true');a=ap.parse_args()
    print(json.dumps(query(a.k,a.include_field),indent=2,sort_keys=True))
