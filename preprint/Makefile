PANDOC ?= pandoc
PDF_ENGINE ?= xelatex

.PHONY: all clean

all: paper.pdf

paper.pdf: paper.md references.bib
	$(PANDOC) paper.md \
		--from=markdown+tex_math_dollars+raw_tex \
		--citeproc \
		--pdf-engine=$(PDF_ENGINE) \
		--output=$@

clean:
	rm -f paper.pdf
