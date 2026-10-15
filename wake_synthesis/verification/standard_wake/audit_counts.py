"""Independent local-string controls, residue induction, and exact count minimum."""
from collections import defaultdict
from itertools import product
from pathlib import Path
import importlib.util
import json

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("standard_counts", HERE / "inputs/counts.py")
counts = importlib.util.module_from_spec(spec)
spec.loader.exec_module(counts)


def verify():
    if not __debug__:
        raise RuntimeError("Run without Python -O")
    groups = defaultdict(set)
    words = 0
    for parity in (0, 1):
        for size in range(11):
            for arrivals in product((0, 1), repeat=size):
                outgoing = sum((arrival ^ (rank % 2)) if parity == 0
                               else 1 - (arrival ^ (rank % 2))
                               for rank, arrival in enumerate(arrivals))
                groups[parity, sum(arrivals), outgoing, size % 2].add(size)
                words += 1
    for margins, sizes in groups.items():
        assert {size for size in counts.counts(*margins) if size <= 10} == sizes

    # Independently propagate the four boundary counts modulo two. The local
    # formula then fixes each class size modulo four, without a period cutoff.
    frontier = (1, 1, 1, 1)
    residues = [(1, 1)]
    for level in range(-9, 0):
        out0, out1, in0, in1 = frontier
        incoming = (out0, out1) if level % 2 else (out1, out0)
        outgoing = (in1, in0) if level % 2 else (in0, in1)
        row = tuple((2 * (incoming[r] + outgoing[r]) + int((level, r) in counts.WAKE)
                     if level % 2 == 0 else
                     2 * (outgoing[r] - incoming[r]) - int((level, r) in counts.WAKE)) % 4
                    for r in (0, 1))
        residues.append(row)
        frontier = tuple((row[r] - side[r]) % 2
                         for side in (outgoing, incoming) for r in (0, 1))
    residues.append((1, 1))
    assert tuple(residues) == counts.RESIDUES
    phase_sums = [sum(residues[t + 10][r] for t in range(-10, 1) for r in (0, 1)
                      if 2 * r + t % 2 == phase) for phase in range(4)]
    assert phase_sums == [10, 6, 10, 10]
    assert all(total % 4 == 2 for total in phase_sums)
    minimum, profiles = counts.optimal_profiles(104, "top")
    reverse_minimum, reverse_profiles = counts.optimal_profiles(104, "bottom")
    assert minimum == reverse_minimum == 104
    assert profiles == reverse_profiles and len(profiles) == 12
    return {"status": "passed", "local_binary_words": words,
            "local_count_cases": len(groups), "class_residues": residues,
            "phase_group_residue_sums": phase_sums, "period_congruence": "8 mod 16",
            "minimum_period": minimum, "minimum_count_profiles": len(profiles),
            "both_count_orientations_agree": True}


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
