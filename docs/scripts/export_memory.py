#!/usr/bin/env python3
"""Export small, exact memory witnesses from the publication-owned verifiers.

Run from any directory. No numerical approximation, dependency on a research
checkout, or mutation of the original proof certificates is involved.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
OWNER = ROOT / 'memory_feedback/verification'


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    out = importlib.util.module_from_spec(spec)
    sys.modules[name] = out
    spec.loader.exec_module(out)
    return out


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':'), sort_keys=True).encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='compare to the committed export')
    args = parser.parse_args()
    c = module('interactive_memory_circuit', OWNER / 'scalable_feedback_circuit/circuit.py')
    r = module('interactive_memory_renewal', OWNER / 'birth_filtered_feedback/code/renewal.py')

    def literal(seed, length):
        past = seed
        last = {}
        # The predicate at time zero sees the unique actual past of the state.
        for age in range(1, 257):
            past = c.inverse(past)
            last.setdefault(past.pos, -age)
        black, pos, heading = set(seed.black), seed.pos, seed.heading
        born = {p: None for p in black}
        events = []
        rebirth = None
        for t in range(length):
            bit = pos in black
            age = t - last[pos] if pos in last else None
            if bit and (age is None or age > 128):
                events.append({'t': t, 'point': list(pos), 'birth': born[pos]})
            if bit and born[pos] is not None and pos in seed.black and t - born[pos] > 4 and rebirth is None:
                rebirth = {'t': t, 'point': list(pos), 'birth': born[pos]}
            if bit:
                black.remove(pos); born.pop(pos)
            else:
                black.add(pos); born[pos] = t
            last[pos] = t
            heading = (heading + (-1 if bit else 1)) % 4
            pos = c.add(pos, c.DIRS[heading])
        final = {'black': sorted(black), 'position': list(pos), 'heading': heading}
        return {'seed': sorted(seed.black), 'heading': seed.heading, 'length': length,
                'events128': events, 'rebirth': rebirth, 'final': final,
                'final_sha256': digest(final)}

    blank = literal(c.State(frozenset(), heading=0), 800)
    assert next(e for e in blank['events128'] if e['birth'] is not None) == {'t': 197, 'point': [-3, -2], 'birth': 21}
    reborn = literal(c.State(frozenset({(0, 0)}), heading=0), 800)
    assert reborn['rebirth'] is not None
    families = []
    for n in (20, 22, 24, 30, 40):
        row = literal(c.seed(n), c.standard_entry_time(n) + 104)
        ret = c.first_return_time(n)
        event = next(e for e in row['events128'] if e['t'] == ret)
        assert event['point'] == [0, 2] and event['birth'] == 60
        assert sum(60 < e['t'] < ret for e in row['events128']) == 31
        row.update(n=n, birth=60, death=ret, entry=c.standard_entry_time(n), point=[0, 2])
        families.append(row)

    source_seed = {(-7,0),(-7,1),(-6,-3),(-6,-2),(-6,-1),(-6,2),(-5,-2),(-5,0),(-5,1),(-5,2),(-4,-2),(-4,1),(-3,-3),(-3,1),(-2,-3),(-2,-1),(-2,1),(-1,-2),(-1,0)}
    N = 10**60
    huge = r.fresh_feedback(r.State.explicit(source_seed | {(2*N,-2*N)}, heading=1), 128, set(), r.Limits(10000,100,100000))
    assert huge['kind'] == 'FRESH_EXTERNAL'
    assert huge['birth'] == 104*N-102 and huge['death'] == 104*N+46 and huge['age'] == 148
    terms = [{'start': [str(x) for x in s.start], 'stride': [str(x) for x in s.stride], 'length': str(s.length)} for s in huge['post'].field.terms]
    huge_row = {'N': str(N), 'birth': str(huge['birth']), 'death': str(huge['death']), 'age': huge['age'],
                'point': [str(x) for x in huge['point']], 'post_terms': terms,
                'post_pose': [str(x) for x in huge['post'].pos], 'post_heading': huge['post'].heading,
                'total_written_reads': str(sum(w.segment.length for w in huge['reads'])),
                'post_terms_sha256': digest(terms), 'initial_seed': [[str(x) for x in p] for p in sorted(source_seed | {(2*N,-2*N)})]}
    scales = []
    for exponent in (64, 80, 128, 256, 512):
        row = r.growing_scale_floor(20, 100, 3**exponent)
        scales.append({'exponent': exponent, **{k: str(v) for k, v in row.items()}})
    sources = ['scalable_feedback_circuit/circuit.py', 'birth_filtered_feedback/code/renewal.py', 'birth_filtered_feedback/PROOF.md']
    data = {'schema': 'langton-memory-interactive-v1',
            'scope': 'Exact finite witnesses and arithmetic certificates; universal proofs remain with the linked publication.',
            'source_sha256': {str((OWNER / p).relative_to(ROOT)): hashlib.sha256((OWNER / p).read_bytes()).hexdigest() for p in sources},
            'blank': blank, 'reborn': reborn, 'families': families, 'huge': huge_row, 'scales': scales}
    path = ROOT / 'docs/data/memory.json'
    content = json.dumps(data, indent=2, sort_keys=True) + '\n'
    if args.check:
        assert path.read_text() == content, 'memory export differs; run exporter without --check'
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    print(f'memory fixtures: PASS ({len(families)} full family replays, exact 10^60 query, 5 growing-scale checks)')


if __name__ == '__main__':
    main()
