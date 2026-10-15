# Standard-wake uniqueness and inverse synthesis

The complete twelve-class standard wake and full drift `(2,-2)` determine the
standard period-104 read trace uniquely. An integer period bound reduces the
all-period statement to a complete ordered-event enumeration. The project also
retains the general decision procedure for prescribed finite wakes and non-axis
drift: it computes a period cutoff and constructs a word and finite seed whenever
one exists.

## Paper and proof

Hao Ke, *Uniqueness of the Classical Langton Ant Highway Under Its Standard Wake*.
Version **0.2.0** is published at
[doi:10.5281/zenodo.23405441](https://doi.org/10.5281/zenodo.23405441),
updating the existing Zenodo concept **23402421**.

- [Current manuscript](paper/main.tex), [published PDF](release/v0.2.0/paper.pdf),
  [proof](PROOF.md), and [evidence](evidence/README.md).
- [Published 0.1.0](https://doi.org/10.5281/zenodo.23402422), titled
  *Reading the Wake: Period Bounds and Inverse Synthesis for Langton's Ant*;
  [exact published PDF](release/v0.1.0/paper.pdf).
- [Release records](release/README.md),
  [literature](paper/LITERATURE.md).

The theorem fixes every odd translation class, including its longitudinal
residue, and the full drift. The classification concerns periodic read traces;
complete finite initial fields may also contain unread cells. General period
budgets and inverse synthesis from version 0.1.0 remain in the revised paper.
The integer clock is developed in [the clock companion](../clock_escape/),
and the supplied-word realization criterion is attributed to Jillhewar.

## Reproduce

```sh
python3 wake_synthesis/reproduce.py
python3 wake_synthesis/reproduce.py --baseline
python3 wake_synthesis/reproduce.py --search
make -C wake_synthesis/paper
python3 tools/prepare_preprints.py --project wake_synthesis
```

Python 3.10+ and g++ with C++17 and undefined-behavior sanitizer support are
required. The default command verifies the
algebraic evidence, reconstructs the upper certificate, and completes the
standard-wake uniqueness search. `--baseline` additionally repeats the original
unpruned enumeration; `--search` adds the earlier finite detour experiment.
Checks work in a disposable directory and preserve retained evidence. The source
archive is self-contained. Mathematical coverage is established in the proof;
finite calculations use exact integer arithmetic.

## Open

Independent mathematical peer review and journal preparation.
