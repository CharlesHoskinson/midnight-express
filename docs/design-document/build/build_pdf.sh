#!/usr/bin/env bash
# Build the PDF from build/document.md  (run from anywhere)
set -euo pipefail
cd "$(dirname "$0")/.."
SRC=${1:-build/document.md}; OUT=${2:-build/midnight-express.pdf}
pandoc "$SRC" -o "$OUT" \
  --pdf-engine=xelatex \
  --from=markdown+pipe_tables+footnotes+raw_tex+smart+implicit_figures+header_attributes+fenced_divs+yaml_metadata_block \
  --top-level-division=chapter --number-sections --toc --toc-depth=1 \
  --citeproc --bibliography=build/references.json --metadata link-citations=true \
  -V documentclass=book -V classoption=oneside -V fontsize=10.5pt -V papersize=letter \
  -V geometry:"left=1.15in,right=1in,top=1in,bottom=0.95in,headsep=0.3in,headheight=14pt" \
  -V colorlinks=true -V linkcolor=mcLink -V urlcolor=mcLink -V citecolor=mcLink -V toc-title="Contents" \
  --include-in-header=build/header.tex --include-before-body=build/cover.tex \
  -V title-meta="Midnight Express: Private Events for Midnight" -V author-meta="Charles Hoskinson" \
  2> build/pdf.log || { grep -E "^!|Error|error:" -A3 build/pdf.log | head -40; exit 1; }
pdfinfo "$OUT" | grep -E "Pages|File size"
