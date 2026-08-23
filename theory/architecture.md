# Research architecture

The project is organized around four separable obligations. Keeping them apart
prevents a large search program from being mistaken for a proof.

| Layer | Question | Admissible output |
| --- | --- | --- |
| Dynamics | What does one update mean? | exact model and orientation tests |
| Orbit recognition | When is a state already on the translating highway? | finite phase data and a sound checker |
| Restricted families | Which initial configurations are known to reach that orbit? | quantified theorem, certificate, and focused verifier |
| Global bridge | Why must every finite initial configuration reach it? | complete descent or complete obstruction argument |

The first layer is present. The other layers are intentionally open rather than
represented by inherited code. This makes the current frontier visible: an
experiment may inform a later layer, but it cannot silently create a result in
another layer.

The first planned restricted family is specified in
[`restricted-families.md`](./restricted-families.md); it has no promoted
certificate yet.

The arbitrary-offset one-black route is reduced into a finite prefix domain and
an entry-state obstacle theorem in [`one-black-reduction.md`](./one-black-reduction.md).

The remaining finite-support ladder is stated without overclaim in
[`global-conjecture.md`](./global-conjecture.md) and operationalized in the
research [`PROGRAM.md`](../research/PROGRAM.md).

## Information flow

```text
exact dynamics
      |
      +--> highway orbit data --> terminal predicate --> local soundness
      |
      +--> experimental families --> restricted certificates
                                           |
complete history model --> global bridge ---+--> finite-support conclusion
```

Every arrow denotes a statement to be written and checked. The diagram is a
dependency map, not a claim that the downstream conclusion has been proved.
