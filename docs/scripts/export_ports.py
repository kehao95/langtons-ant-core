#!/usr/bin/env python3
"""Export exact browser witnesses from the publication-owned port checkers.

All fields are complete finite states. The browser replays literal ant updates;
all-future and all-parameter claims remain owned by the linked proofs/checkers.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import sys

ROOT = Path(__file__).resolve().parents[2]

def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()

def snapshot(state):
    return {'black': sorted(state.B), 'position': state.p, 'heading': state.h}

def endpoint(state):
    return {'position': state.p, 'heading': state.h, 'mass': len(state.B),
            'fieldSha256': g.digest(state.B)}

def replay(state, steps):
    result, words, _ = g.independent_replay(state, steps)
    return result, ''.join(words)

if __name__ == '__main__':
    gpath = 'four_cell_port/verification/guarded_scattering/check.py'
    rpath = 'four_cell_port/verification/return_scattering/check.py'
    bpath = 'four_cell_port/verification/check.py'
    g = load('browser_guarded_export', gpath)
    r = load('browser_return_export', rpath)
    b = load('browser_port_export', bpath)
    rules = []
    for row in g.TABLE:
        orientation, phase, guard, updates, output_phase, x, y, h = row
        seed = g.kernel(row)
        final, turns = replay(seed, updates)
        assert final.p == (x, y) and final.h == h
        word = (g.WORD * 2)[output_phase:output_phase + 104]
        assert g.tail_breakpoints(final, word) and g.tail_classes(final, word)
        _, _, end, _ = g.plan(word, final.p, final.h)
        out = 0 if g.sub(end, final.p) == (2, 2) else 1
        rules.append({'id': f'{orientation}-{phase}', 'orientation': orientation,
                      'phase': phase, 'guard': guard, 'updates': updates,
                      'outputPhase': output_phase, 'outputOrientation': out,
                      'seed': snapshot(seed), 'endpoint': endpoint(final), 'turns': turns})
    basic = []
    for name, cells, updates in [('gate', b.GATE, 182), ('sharp', b.SHARP, 918)]:
        seed = g.State(set(cells))
        final, turns = replay(seed, updates)
        if name == 'sharp':
            assert b.first_exit(cells)[0] == 918
        else:
            assert final.p == (5, 1) and final.h == 1
        basic.append({'id': name, 'seed': snapshot(seed), 'updates': updates,
                      'endpoint': endpoint(final), 'turns': turns})
    trains = []
    for spec in [[(29,100),(15,100)], [(13,100),(13,100)], [(29,120),(89,120)]]:
        seed, events, updates, point, orientation, phase = g.construct(spec)
        final, turns = replay(seed, updates)
        assert final.p == point
        word = (g.WORD*2)[phase:phase+104]
        assert g.tail_breakpoints(final, word) and g.tail_classes(final, word)
        trains.append({'spec': spec, 'seed': snapshot(seed), 'updates': updates,
                       'events': [{'time': t, 'point': p, 'guard': p[0]+row[2]}
                                  for t, p, row in events], 'endpoint': endpoint(final)})
    returns = []
    for n in [100, 120, 160]:
        seed, rows, updates = r.make_train([100], [n])
        row = rows[0]
        final, turns = replay(seed, updates)
        assert g.tail_breakpoints(final, r.phase(94)) and g.tail_classes(final, r.phase(94))
        primary = row['primary']
        old_point = g.add(primary, r.HIT)
        birth = row['time'] - 1736
        old_read = row['time'] + 208*n + 51948
        control = seed.copy()
        last_birth = None
        for t in range(old_read+1):
            if control.p == old_point:
                if t == old_read:
                    assert control.p in control.B and last_birth == birth
                elif control.p not in control.B:
                    last_birth = t
            control.step()
        returns.append({'n': n, 'seed': snapshot(seed), 'updates': updates,
                        'primaryTime': row['time'], 'birthTime': birth,
                        'oldReadTime': old_read, 'oldPoint': old_point,
                        'lifetime': old_read-birth, 'endpoint': endpoint(final)})
    data = {'schema': 1, 'sources': {p: sha(p) for p in [gpath, rpath, bpath]},
            'word': g.WORD, 'phasePositions': g.P, 'phaseHeadings': g.H,
            'base': sorted(g.BASE), 'rules': rules, 'basic': basic,
            'trains': trains, 'returns': returns,
            'compatiblePairs': sum(a['outputOrientation'] == z['orientation']
                                   for a in rules for z in rules)}
    assert data['compatiblePairs'] == 448
    target = ROOT / 'docs/data/ports.json'
    output = json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '\n'
    if '--check' in sys.argv:
        assert target.read_text() == output, 'ports.json differs; rerun exporter'
        print('Port browser export: source hashes, 30 kernels, 448 pairs, 3 trains, 3 return witnesses PASS')
    else:
        target.write_text(output)
        print(f'Wrote {target.relative_to(ROOT)} ({len(output):,} bytes)')
