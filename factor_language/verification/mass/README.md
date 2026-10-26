# Mass growth versus standard-language violations

For ANY finite-support classical Langton-ant trajectory segment,

    3(t-s)-26(|B_t|-|B_s|) <= 351*N10(s,t)+322.

N10 counts bad ten-letter standard-factor windows wholly contained in the segment. The stronger base lemma D<=322 holds for every physically feasible ten-legal finite word, with an explicit sharp 90-step witness. No infinite-future legality promise is imposed on the global inequality.

Read [the complete proof](PROOF.md). Run `python reproduce.py` for a disposable exact Python/C++17 replay. The immutable `witness.json` fixes counts, hashes, the 90-letter word and all 28 initial black cells. Large enumeration files are regenerated in the temporary directory, compared between implementations and tested by integer edge inequalities; they are not repository dependencies.

A sublinear-mass infinite trajectory must have lower ten-factor violation density at least 1/117. This is NOT an HC proof or a global upper bound on violation count.
