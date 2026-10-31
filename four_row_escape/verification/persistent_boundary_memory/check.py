"""Reconstruct finite premises and check complete autonomous counter runs.

Default mode compares a frozen report, never silently replaces it.
All infinite-parameter conclusions use the written scan/shift induction.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
from core import (A, B, C, V, K, DIRECTIONS, Catalog, black_field, literal,
                  mirrored, natural, prediction, right, source)

HERE = Path(__file__).resolve().parent
MASK64 = (1 << 64)-1


def digest(data):
    return hashlib.sha256(data).hexdigest()


def check_kernel(record):
    columns, pose = tuple(record['source']), tuple(record['pose'])
    field, end, word, positions = literal(black_field(columns), len(columns), 5,
                                         pose, limit=100)
    assert (end, word, len(word)) == (tuple(record['finish']), record['word'], record['steps'])
    assert field == black_field(record['target'])
    assert positions == [tuple(p) for p in record['read_positions']]
    assert all(0 <= x < len(columns) and 0 <= y < 5 for x, y in positions)
    assert end[0] in (-1, len(columns)) and 0 <= end[1] < 5


def verify_representatives(catalog):
    """Every future branch of every representative, using full set dynamics."""
    count = updates = 0
    for p in (0, 1):
        seen = set()
        def follow(field, width, node):
            nonlocal count, updates
            key = frozenset(field), width, node
            if key in seen:
                return
            seen.add(key)
            for channel, y in enumerate(catalog.ins[p]):
                target, pose, w, _ = literal(field, width, catalog.height,
                                             (0, y, 1), limit=100000)
                count += 1
                updates += len(w)
                ans = catalog.types[p][node][channel]
                if pose[0] == -1 and 0 <= pose[1] < catalog.height:
                    assert ans is not None
                    out, residual = ans
                    assert pose == (-1, catalog.outs[p][out], 3)
                    follow(target, width, residual)
                else:
                    assert ans is None
        for node, columns in enumerate(catalog.witness[p]):
            if columns:
                follow(black_field(columns, catalog.height), len(columns), node)
            else:
                assert node == 0
    return count, updates


def export_catalogs(catalogs, path):
    lines = [str(len(catalogs))]
    for c in catalogs:
        lines.append(f'{c.height} {len(c.types[0])} {len(c.types[1])}')
        for p in (0, 1):
            for i, row in enumerate(c.types[p]):
                cells = [c.rank[p][i]]
                for ans in row:
                    cells.extend((-1, -1) if ans is None else ans)
                lines.append(' '.join(map(str, cells)))
        for p in (0, 1):
            for row in c.products[p]:
                lines.append(' '.join(map(str, row)))
    path.write_text('\n'.join(lines)+'\n')


def expected_checkpoint(l, r, j, stage):
    left = mirrored((5,) + right(j, l-j))
    if stage == 0:
        return left + right(j, r-j), (2*l+5, 3, 1)
    return left + right(j+1, r-j-1), (2*l+4, 2, 3)


def stream_run(l, r):
    columns, pose = source(l, r)
    predicted_t, predicted_pose, predicted_columns, predicted_cross = prediction(l, r)
    field = black_field(columns)
    assert len(field) == 6*r+4*l+23
    width, seam = len(columns), 2*l+5
    x, y, h = pose
    dx, dy = DIRECTIONS[h]
    t = cross = comparisons = 0
    hash_value = 1469598103934665603
    m = min(l, r)
    selected = set(range(m+1)) if m <= 128 else {0, 1, 2, m//2, m-1, m}
    checkpoints = {}
    for j in selected:
        checkpoints[8*j*j+56*j] = j, 0
        if j < r:
            checkpoints[8*j*j+64*j+30] = j, 1
    while 0 <= x < width and 0 <= y < 5:
        assert t <= predicted_t, 'claimed first-exit formula too small'
        if t in checkpoints:
            j, stage = checkpoints[t]
            colors, wanted_pose = expected_checkpoint(l, r, j, stage)
            assert field == black_field(colors)
            assert (x, y, DIRECTIONS.index((dx, dy))) == wanted_pose
            comparisons += 1
        old_x = x
        if (x, y) in field:
            letter = 76
            field.remove((x, y))
            dx, dy = -dy, dx
        else:
            letter = 82
            field.add((x, y))
            dx, dy = dy, -dx
        hash_value = ((hash_value ^ letter)*1099511628211) & MASK64
        x, y = x+dx, y+dy
        t += 1
        cross += (old_x < seam) != (x < seam)
    pose = x, y, DIRECTIONS.index((dx, dy))
    assert (t, pose, cross) == (predicted_t, predicted_pose, predicted_cross)
    assert field == black_field(predicted_columns)
    assert len(field) == 6*r+4*l+23-(2 if l < r else 0)
    return dict(l=l, r=r, steps=t, pose=list(pose), crossings=cross,
                turn_hash=f'{hash_value:016x}', columns=list(predicted_columns)), comparisons+1


def run():
    witness = json.loads((HERE/'witness.json').read_text())
    assert witness['columns'] == dict(A=list(A), B=list(B), C=list(C), V=list(V))
    assert len(witness['kernels']) == 6
    for record in witness['kernels']:
        check_kernel(record)
    assert witness['kernels'][2]['word'] == K
    damaged = copy.deepcopy(witness['kernels'][2])
    damaged['word'] = ('L' if K[0] == 'R' else 'R') + K[1:]
    try:
        check_kernel(damaged)
    except AssertionError:
        pass
    else:
        raise AssertionError('damaged kernel accepted')

    catalogs = [Catalog(h).close() for h in range(1, 5)]
    expected = [(1, 0), (2, 1), (7, 3), (269, 13)]
    catalog_rows = []
    representative_count = representative_updates = 0
    local_checks = 0
    for c, (size, rank) in zip(catalogs, expected):
        assert all(len(c.types[p]) == size and max(c.rank[p]) == rank for p in (0, 1))
        local_checks += c.verify_local()
        count, steps = verify_representatives(c)
        representative_count += count
        representative_updates += steps
        raw = json.dumps([c.types, c.products, c.witness], separators=(',', ':'), sort_keys=True).encode()
        catalog_rows.append(dict(height=c.height, types_each_parity=size,
                                 max_rank=rank, closed_width=c.closed_width,
                                 counts=c.levels, certificate_sha256=digest(raw)))

    # Symbolic sweep recurrence controls, including degenerate budgets.
    recurrence_cases = recurrence_updates = response_cases = response_updates = 0
    for j in range(13):
        for k in range(9):
            a = right(j, k)
            field, pose, w, _ = literal(black_field(a), len(a), 5, (0, 3, 1), limit=10000)
            if k:
                assert pose == (-1, 2, 3) and len(w) == 8*j+30
                assert field == black_field(right(j+1, k-1))
                assert w == 'RLLR'*j + K + 'RLLR'*j
            else:
                assert pose == (len(a), 1, 1) and len(w) == 4*j+16
                assert field == black_field(B*(j+1)+(10, 18))
            recurrence_cases += 1
            recurrence_updates += len(w)
    # Same-width, time-blind distinguishing protocols for all tested candidates.
    for m in (0, 1, 2, 5, 12, 40):
        for remaining in range(m+1):
            a = right(m-remaining, remaining)
            field = black_field(a)
            for j in range(remaining+1):
                field, pose, word, _ = literal(field, len(a), 5, (0, 3, 1), limit=100000)
                response_updates += len(word)
                assert (pose == (-1, 2, 3)) == (j < remaining)
                if j == remaining:
                    assert pose == (len(a), 1, 1)
            response_cases += 1
    # For taller strips the entire distinguishing trace is still in the bottom five rows.
    for height in (6, 9, 20):
        field = black_field(right(2, 5))
        for j in range(6):
            field, pose, w, _ = literal(field, 18, height, (0, 3, 1), limit=100000)
            assert (pose == (-1, 2, 3)) == (j < 5)

    cases = sorted(set([(l, r) for l in range(16) for r in range(16)] +
                       [(k, k) for k in (16, 31, 64, 127, 256, 1000)] +
                       [(0, 1000), (1000, 0), (17, 31), (31, 17), (63, 64), (64, 63)]))
    rows = []
    endpoints = physical_steps = 0
    for l, r in cases:
        row, comparisons = stream_run(l, r)
        rows.append(row)
        physical_steps += row['steps']
        endpoints += comparisons
    with tempfile.TemporaryDirectory(prefix='boundary-memory-') as temp:
        temp = Path(temp)
        table, inputs, executable = temp/'catalog.txt', temp/'cases.txt', temp/'independent'
        export_catalogs(catalogs, table)
        inputs.write_text(''.join(f'{l} {r}\n' for l, r in cases))
        subprocess.run(['g++', '-O2', '-std=c++17', str(HERE/'independent.cpp'), '-o', str(executable)], check=True)
        native = subprocess.run([str(executable), str(table), str(inputs)], capture_output=True, text=True, check=True, timeout=60)
        native_rows = [json.loads(line) for line in native.stdout.splitlines()]
        assert native_rows[0] == dict(catalog_equations=local_checks,
                                      catalog_nodes=sum(len(c.types[p]) for c in catalogs for p in (0, 1)))
        assert native_rows[1:] == rows
        damaged_table = temp/'damaged.txt'
        damaged_table.write_text(table.read_text().replace('4\n1 1 1\n0\n0 -1 -1\n', '4\n1 1 1\n1\n0 -1 -1\n', 1))
        assert damaged_table.read_bytes() != table.read_bytes()
        bad = subprocess.run([str(executable), str(damaged_table), str(inputs)], capture_output=True, text=True, timeout=10)
        assert bad.returncode != 0

    cols, start = source(2, 3)
    remote = {(10**60, -10**60), (-10**60, 10**60)}
    f, p, w, _ = literal(black_field(cols) | remote, len(cols), 5, start, limit=10000)
    t, pose, end, _ = prediction(2, 3)
    assert f == black_field(end) | remote and p == pose and len(w) == t
    try:
        literal(black_field(cols), len(cols), 5, start, limit=1)
    except RuntimeError:
        pass
    else:
        raise AssertionError('execution cap was converted to an answer')
    for bad in (-1, 1.5, True):
        try:
            natural(bad)
        except ValueError:
            pass
        else:
            raise AssertionError('invalid parameter accepted')
    huge = 10**60
    huge_time = 8*huge**2+60*huge+16
    assert huge_time == 8*huge*(huge-1) + 64*huge + 4*huge + 16

    # Only deterministic evidence, never elapsed-time estimates, is frozen.
    return dict(schema='persistent-boundary-memory-v1', status='passed',
                date='2026-10-30', mathematical_base='54d14c7589dc41247157463dd0aa12119a9a56ed',
                kernels=6, catalogs=catalog_rows, local_catalog_equations=local_checks,
                representative_requests=representative_count,
                representative_updates=representative_updates,
                recurrence_controls=recurrence_cases, recurrence_control_updates=recurrence_updates,
                same_width_response_cases=response_cases, same_width_response_updates=response_updates,
                autonomous_inputs=len(rows), literal_updates_per_implementation=physical_steps,
                complete_python_checkpoints=endpoints,
                cpp_complete_endpoint_equalities=len(rows),
                trajectory_report_sha256=digest(json.dumps(rows, sort_keys=True, separators=(',', ':')).encode()),
                maximal_parameter=1000, symmetric_formula=[8, 60, 16],
                negative_controls=dict(damaged_kernel=True, damaged_catalog=True,
                                       resource_cap_is_unknown=True, invalid_parameters=3),
                remote_black_cells_retained=True,
                scope='sharp boundary-response height threshold and autonomous quadratic first-exit family; no HC proof',
                sources_sha256={name:digest((HERE/name).read_bytes()) for name in
                                ('core.py','check.py','independent.cpp','witness.json')})


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('run without -O')
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', type=Path, help='explicit report generation, not comparison')
    args = parser.parse_args()
    report = run()
    if args.write is not None:
        args.write.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True)+'\n')
        print('generated', args.write)
    else:
        frozen = json.loads((HERE/'report.json').read_text())
        if report != frozen:
            raise SystemExit('FAIL: frozen report mismatch; report was not changed')
        print('PASS: all finite certificate clauses and full-field controls agree')
