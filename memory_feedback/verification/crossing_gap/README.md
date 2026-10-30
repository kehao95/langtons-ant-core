# Crossing information and spatial width

Run `python3 memory_feedback/reproduce.py --crossing-only` from the repository
root. Python 3.10+ and a C++17 compiler are required. The replay compares frozen
`report.json` in a disposable directory.

`core.py` implements full-field dynamics, permanent crossing certificates,
alternating-parity signature capacity, packing work, and finite profile deadlines.
The rational-normal classifier returns TRANSLATOR, WIDTH_EXCEEDED, or UNKNOWN
at an optional caller cap. Without that cap the analytic finite deadline gives
termination. TRANSLATOR permits any nonzero drift; it does not assert P104.
Normals use min(|alpha|,|beta|)=1, and width covers the entire head prefix.

The report checks 100 complete inputs against an independent C++ implementation,
113152 updates per implementation, crossing parity and capacity, exact packing,
corner inequalities, cyclic-rule balance and remote-cell guards. The all-prefix
and all-time statements follow from the article's analytic proofs. Generalized
cyclic rules have an analytic balance extension, not an implemented full classifier.
