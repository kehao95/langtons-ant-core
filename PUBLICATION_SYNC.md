# Public preprint integration — 2026-10-13

Both published preprints are available in this repository, with self-contained
source and verification entry points:

| Paper | Public source | Published version |
|---|---|---|
| One-black highway theorem | [`preprint/`](preprint/README.md), [`one_black/`](one_black/README.md) | [0.2.0](https://doi.org/10.5281/zenodo.23341609) |
| Rational clocks and square escape | [`clock_escape/`](clock_escape/README.md) | [0.2.0](https://doi.org/10.5281/zenodo.23341604) |

## Provenance

The one-black publication pins source commit
`897e6f11a70054faed1f8a86b4d4e1e2b0071445` in this repository. Its
[published source manifest](preprint/published-source-manifest.json) retains
all source and figure hashes. The newer record 23341609 belongs to the same
Zenodo version chain as original 22086968 (concept 22086967).

The clock publication pins research-source commit
`8cb3fa4e91f658af4ca72dd66a97a9f080be4611`. Its public source was imported from
the published archive after verifying the archive and PDF against the retained
publication receipt. All 28 archived source files matched their SHA256 manifest
at import. Navigation and release documents were then adapted to this public
repository; manuscript, Lean proofs, checkers and certificates are unchanged.
The [original manifest](clock_escape/published-source-manifest.json) preserves
the archived snapshot. Both papers retain their original publication receipts.

## Checks run for this integration

- Clock reproduction ran in a temporary standalone directory with bundled
  dependencies. All four numerical reports and the Lean axiom output match the
  retained published evidence exactly.
- This includes 9,720 independent local cases, all 4,213,000 square states for
  side lengths 1 through 4 (exit maxima 1, 6, 17, 46), the baseline checks,
  complete-state algorithms and integer certificates.
- The clock PDF rebuilt successfully without overfull boxes or undefined
  references. Its extracted text matches the published PDF exactly.
- All 85 one-black scientific source and figure files checked against
  the published source manifest match. All 43 Lean source files also match the
  retained clean-build report. This integration reuses that clean-build evidence;
  it does not claim a new one-black Lean build.
- Repository whitespace and local navigation checks pass.

The machine-readable integration report is
[`clock_escape/evidence/public-integration.json`](clock_escape/evidence/public-integration.json).
The clock's full escape theorem remains analytically proved, with local algebra
and telescoping formalized in Lean; the one-black standard-trace theorem has
its complete Lean proof and recorded three native computation leaves.

Future manuscript work belongs in these public source directories. Historical
research preparation remains in its originating repository. This integration
updates GitHub; the published Zenodo artifacts retain their versioned contents.
