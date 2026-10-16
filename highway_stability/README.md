# One Bit Off the Highway: Uniform Recovery for Langton's Ant

An independent manuscript about one toggle at arbitrary age and site on the
complete growing canonical highway. This input family differs from a complete
one-black initial state, so it does not replace or rename the one-black paper.

[Manuscript](paper/main.tex) · [Review PDF](paper/review.pdf) ·
[Proof source](proof/canonical-highway-one-bit-stability.md) · [Evidence map](PROOF.md)

The analytic reduction, all-age coupling, exact first-impact query and complete
endpoint formula are written up. The numerical recovery theorem is explicitly
conditional on the specified finite certificate in this review draft. It is
**not in the release-ready candidate packager**.

## Available verification

```sh
python3 highway_stability/reproduce.py --analytic-controls
make -C highway_stability/paper
```

These controls check the 104-letter canonical word, complete deposition identity,
all future canonical phase rays, and the 104 thresholds' 739-case index count.
They do not replay the perturbed cases or certify the bounds 64,584 / 78 / 33,595.
The default reproduction command fails clearly while those data are absent.

## Open

Restore `langtons-ant-uniform-one-bit-recovery-2026-10-15.zip`, SHA256
`be64e9793d8da98c1e418a4c20c6b6c9119fdce7c7561a6bfd92dc07a161d972`.
The [original manifest](evidence/original-package-manifest.json) identifies every
checker and certificate hash. Then replay all 739 cases and 104 infinite-age
and inverse-history guards, compare Python/C++ complete endpoints, and replace
the certificate implication by the verified numerical theorem. Publication
preparation follows that replay and author review.
