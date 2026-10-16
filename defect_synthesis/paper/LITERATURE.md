# Attribution and literature check

The manuscript combines the two project implementations of fixed-budget synthesis
as one theorem. Factor rigidity, bounded-fold physical exclusion and the finite
cover are inputs owned by the companion factor paper. First-read consistency and
same-cell alternation follow the symbolic-ant tradition of Gajardo (2003),
DOI 10.46298/dmtcs.2312.

The generic tools are attributed to Presburger arithmetic and flat-system
verification, including Decker–Pirogov (2019), Haase et al. (ICALP 2024), and
Demri–Dhar–Sangnier, *Taming past LTL and flat counter systems*, Information and
Computation 242 (2015), 306–339, DOI 10.1016/j.ic.2015.03.007.
Primary author copy: https://www.irif.fr/~sangnier/publis/DDS-IC15.pdf.

The explicit integer small-solution bound was checked against Bottesch–Haslbeck–
Reynaud–Thiemann, NFM 2020, pp. 233–250, DOI 10.1007/978-3-030-55754-6_14.
Page 235 explicitly gives `(n+1)! a^n`, independent of the number of inequalities.
Primary open chapter: https://link.springer.com/content/pdf/10.1007/978-3-030-55754-6_14.pdf.
This formalization is an external arithmetic input; it does not formalize the ant
interval verifier or chamber coefficient bounds.

The ant-specific contributions are complete mutable-field synthesis, the explicit
resource spectra and sharp three-parameter classification, and the specialized
small-witness chamber construction. A full publication-priority review and journal
selection remain subsequent scholarly work; this targeted check is not a novelty
certification. The original optional small-witness implementation is absent and
is not represented as a reproduced experiment in the new manuscript.
