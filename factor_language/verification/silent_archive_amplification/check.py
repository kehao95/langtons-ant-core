#!/usr/bin/env python3
"""Verify the affine family, then independent finite implementation controls.

Default checks never overwrite the witness or frozen report. --write explicitly
creates a new deterministic report. Only this isolated theorem module is run.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
from affine import require, verify, word_trace

HERE = Path(__file__).resolve().parent
STANDARD = ('RRLLLLRLRRRRLRRRRLLLLRLRRRRLRLLRRLLLLRRLLRRRRLLRRLRL'
            'LRLLRLRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRR')


def field(profile: dict, n: int) -> set[tuple[int, int]]:
    require(type(n) is int and n >= 1, 'n must be a positive integer')
    return ({tuple(q) for q in profile['low']}
            | {(x, y + 4*j) for x, y in profile['bulk'] for j in range(n)}
            | {(x, y + 4*n) for x, y in profile['high']})


def inverse_past(black, p=(-1, 0), d=(-1, 0)):
    black = set(black)
    past, reads = [], []
    for _ in range(9):
        p = (p[0] - d[0], p[1] - d[1])
        reads.append(p)
        black.symmetric_difference_update((p,))
        old = p in black
        past.append('L' if old else 'R')
        d = (d[1], -d[0]) if old else (-d[1], d[0])
    return ''.join(reversed(past)), reads


def word_checks(c):
    w, a, b, p = (c['words'][k] for k in ('W', 'A', 'B', 'P'))
    require(w == STANDARD, 'standard word changed')
    legal = {(w*2)[i:i+10] for i in range(104)}
    cover = b+a+a+b+a+a
    require(all(cover[i:i+10] in legal for i in range(len(cover)-9)), 'illegal grammar junction')
    require(a[-9:] == b[-9:], 'return history depends on n')
    past, reads = inverse_past({tuple(q) for q in c['source']['low']})
    require(all(y < 8 for _, y in reads), 'inverse guard does not exclude the bulk/high field')
    require(past == c['true_past9'], 'wrong true intrinsic history')
    stream = b[-9:] + p + p
    first = [i for i in range(20) if stream[i:i+10] not in legal]
    steady = [i for i in range(20) if stream[20+i:30+i] not in legal]
    require(first == [1,2,3,4,5,19], 'wrong first-pulse defects')
    require(steady == [0,1,2,3,4,5,6,7,19], 'wrong stationary-pulse defects')
    visits, displacement, heading = word_trace(p)
    require(displacement == (0,4) and heading == 0, 'pulse geometry')
    require(all(0 <= y < 4 for _, y, _, _ in visits), 'pulse reads a later band')
    first_reads = {}
    for x, y, turn, _ in visits:
        first_reads.setdefault((x,y), turn)
    fuel = sorted(q for q, turn in first_reads.items() if turn == 'L')
    require(fuel == [(0,3),(1,0)], 'wrong distinct external fuel sites')
    require(p[:2] == 'RL' and p[2] == 'R' and c['blocks'][-1]['word'] == 'RLL', 'wrong next-pulse failure')
    claims = c['claims']
    for key, expected in {
        'return_time':[56,167], 'first_J10_time':[56,168], 'first_J10_pose':[1,4,1],
        'max_y_before_first_J10':[4,13], 'pulse_count':[1,1],
        'pulse_J10_count':[len(steady),len(first)], 'first_failure_of_P_from_return':[20,22]
    }.items():
        require(claims[key] == expected, 'wrong derived claim: '+key)
    return {'ten_factor_count':len(legal), 'grammar_windows_checked':len(cover)-9,
            'first_pulse_bad_indices':first, 'steady_pulse_bad_indices':steady,
            'distinct_preexisting_fuel_per_P':len(fuel), 'inverse_reads_guarded':len(reads)}


def literal(c, n):
    black = field(c['source'], n)
    source_count = len(black)
    born = {q:-1 for q in black}
    p, d = (-1,0), (-1,0)
    past, _ = inverse_past(black)
    require(past == c['true_past9'], 'literal inverse mismatch')
    legal = {(STANDARD*2)[i:i+10] for i in range(104)}
    t = dead = fuel_checks = bad_count = 0
    first = None
    max_y = 0
    for block, spec in enumerate(c['blocks']):
        for j in range(spec['count'][0]*n + spec['count'][1]):
            for i, requested in enumerate(spec['word']):
                is_black = p in black
                turn = 'L' if is_black else 'R'
                require(turn == requested, f'literal word mismatch at n={n},t={t}')
                window = past + turn
                bad = window not in legal
                if bad and first is None:
                    first = t
                    require(p == (1,4) and d == (1,0), 'literal first defect pose')
                if block < 4:
                    require(not bad, 'literal defect in legal prelude')
                    max_y = max(max_y, p[1])
                if block == 4:
                    bad_count += bad
                    if i in (1,19):
                        expected = 44+28*j if i == 1 else 56*n+146-28*j
                        require(is_black and born[p] == expected, 'literal birth mismatch')
                        if i == 1:
                            require(bad, 'selected left lifetime is not a defect')
                        fuel_checks += 1
                if is_black:
                    dead += born.pop(p) == -1
                    black.remove(p)
                    d = (-d[1], d[0])
                else:
                    born[p] = t
                    black.add(p)
                    d = (d[1], -d[0])
                p = (p[0]+d[0], p[1]+d[1])
                past = window[1:]
                t += 1
        if block >= 3:
            target = ('return','pulse_end','final')[block-3]
            require(black == field(c[target],n), 'literal COMPLETE checkpoint mismatch')
            if block == 3:
                require(dead == source_count, 'initial lifetimes not all consumed')
    require(p == (0,4*n+9) and d == (-1,0), 'literal final pose')
    row = [n,t,first,bad_count,fuel_checks,len(black),max_y]
    require(row == [n,76*n+190,56*n+168,9*n+6,2*(n+1),22*n+61,4*n+13], 'literal statistics')
    return row


def native(c, cases):
    def emit_field(pts):
        return [str(len(pts))]+[f'{x} {y}' for x,y in sorted(pts)]
    lines = [str(len(cases))]
    for n in cases:
        lines += [str(n)] + emit_field(field(c['source'],n))
        lines += [STANDARD,c['true_past9'],str(len(c['blocks']))]
        lines += [f"{b['word']} {b['count'][0]*n+b['count'][1]}" for b in c['blocks']]
        for stage in ('return','pulse_end','final'):
            lines += emit_field(field(c[stage],n))
    with tempfile.TemporaryDirectory(prefix='silent-archive-') as tmp:
        exe = Path(tmp)/'independent'
        subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Werror',
                        str(HERE/'independent.cpp'),'-o',str(exe)],check=True,
                       capture_output=True,text=True,timeout=30)
        run = subprocess.run([str(exe)],input='\n'.join(lines)+'\n',capture_output=True,
                             text=True,timeout=30,check=True)
    rows = [[int(v) for v in line.split()] for line in run.stdout.splitlines()]
    require(len(rows) == len(cases), 'missing native rows')
    return rows


def negative_controls(c):
    rejected = []
    changes = {
        'missing_input_bulk_cell':lambda d:d['source']['bulk'].pop(),
        'missing_return_cell':lambda d:d['return']['low'].pop(),
        'incorrect_final_cell':lambda d:d['final']['high'].append([17,8]),
        'wrong_birth_time':lambda d:d['claims']['left_birth_n_j_const'].__setitem__(2,45),
        'wrong_death_time':lambda d:d['claims']['right_death_n_j_const'].__setitem__(2,187),
        'wrong_intrinsic_past':lambda d:d.__setitem__('true_past9','L'*9),
        'false_endpoint_time':lambda d:d['claims'].__setitem__('first_J10_time',[56,167]),
        'false_defect_count':lambda d:d['claims'].__setitem__('pulse_J10_count',[8,6]),
    }
    for name, change in changes.items():
        damaged = copy.deepcopy(c)
        change(damaged)
        try:
            word_checks(damaged)
            verify(damaged)
        except (ValueError, KeyError):
            rejected.append(name)
        else:
            raise ValueError('damaged witness accepted: '+name)
    return rejected


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--compare',type=Path)
    parser.add_argument('--write',type=Path)
    args=parser.parse_args()
    c=json.loads((HERE/'witness.json').read_text())
    wc=word_checks(c)
    algebra=verify(c)
    cases=list(range(1,97))+[127,128,255,512,1000]
    pyrows=[literal(c,n) for n in cases]
    crows=native(c,cases)
    require(pyrows == crows, 'Python/C++ controls disagree')
    rejected=negative_controls(c)
    report={'schema':'langtons-ant-silent-archive-report-v1',
            'status':'all-parameter affine checks plus independent FINITE literal controls',
            'word_checks':wc,'affine_certificate':algebra,
            'literal_controls':{'parameters':cases,'cases':len(cases),
                'updates_per_implementation':sum(r[1] for r in pyrows),
                'complete_checkpoint_comparisons_per_implementation':3*len(cases),
                'selected_lifetimes_per_implementation':sum(r[4] for r in pyrows),
                'rows_sha256':hashlib.sha256(json.dumps(pyrows,separators=(',',':')).encode()).hexdigest()},
            'damaged_witnesses_rejected':rejected,
            'source_sha256':{name:hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                for name in ('affine.py','check.py','independent.cpp','witness.json')},
            'not_established':['HC','a finite HC counterexample','infinite autonomous renewal',
                               'a global event budget','post-prefix convergence of this whole family',
                               'Lean formalization','external review','priority']}
    if args.compare:
        require(report == json.loads(args.compare.read_text()), 'frozen report does not match')
    text=json.dumps(report,indent=2)+'\n'
    if args.write:
        args.write.write_text(text)
    print(text,end='')

if __name__ == '__main__':
    main()
