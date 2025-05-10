manuscript = notes
latexopt   = -halt-on-error -file-line-error

all: all-via-pdf clean

all-via-pdf: $(manuscript).tex
	pdflatex $(latexopt) $<
	pdflatex $(latexopt) $<
	pdflatex $(latexopt) $<
	
clean: 
	rm -f *.dvi *.toc *.aux *.out *.log *.bbl *.blg *.log *.spl *~ *.spl *.zip *.acn *.glo *.ist *.epub *.fdb_latexmk *.fls

