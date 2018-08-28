#!/bin/bash

pandoc -s test.md --filter isolate_citations.py --bibliography Untitled.bib -M link-citations -t docx -o test.docx
pandoc -s test.md --filter isolate_citations.py --bibliography Untitled.bib -M link-citations -o test.pdf

pandoc -s test.docx -o out.md --wrap=none --atx-headers --reference-location=section --filter undo_citations.py 

