# Ten-factor attraction and local-event decision

Read [the complete proof](PROOF.md). The theorem assumes that all future
length-ten turn factors belong to the standard P104 language. It proves three
eventual physical modes; finite initial black support excludes the two modes
requiring infinite backgrounds. Standard entrance is at most `12m+212`, with
optimal slope 12. The all-input J10 algorithm decides whether another violation
exists; it does not bound the total event count or prove HC.

## Reproduce

From the repository root:

```sh
python3 factor_language/reproduce.py
```

The runner works in a disposable directory. `restore_certificates.py`
reconstructs `windows10.txt` and `quotient.tsv`, verifies their frozen SHA-256
hashes and refuses to replace a different existing file. The independent checks
re-enumerate all 6,605 words in Python and C++17, verify every quotient edge,
reject damaged certificates and check the complete-field local-event algorithm.
The all-parameter fold exclusion and seed-family arguments are in the proof;
finite simulations do not replace their universal coverage arguments.

Python 3.10+ standard library and a C++17 compiler suffice. Run without `-O`.
The small JSON witnesses and exact reconstruction recipes fix the finite inputs;
[source hashes](../../sources.json) identify the accompanying implementations.
