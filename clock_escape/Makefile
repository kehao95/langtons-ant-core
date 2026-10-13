.PHONY: all check
all:
	mkdir -p build
	pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
	pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
check:
	python3 reproduce.py
