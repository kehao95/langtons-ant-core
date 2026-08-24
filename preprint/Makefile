PANDOC ?= pandoc
PDF_ENGINE ?= xelatex
SCATTERING_PANELS := $(wildcard figures/scattering/*.png)
EXCEPTIONAL_PANELS := $(wildcard figures/exceptional/*.png)
STAGE_PANELS := $(wildcard figures/stages/*.png)
PDF := Every-One-Black-Cell-Langton-Ant-Reaches-the-Period-104-Highway-A-Lean-Checked-Proof.pdf

.PHONY: all clean

all: $(PDF)

$(PDF): paper.md references.bib $(SCATTERING_PANELS) $(EXCEPTIONAL_PANELS) $(STAGE_PANELS)
	$(PANDOC) paper.md \
		--from=markdown+tex_math_dollars+raw_tex \
		--citeproc \
		--pdf-engine=$(PDF_ENGINE) \
		--output=$@

clean:
	rm -f $(PDF)
