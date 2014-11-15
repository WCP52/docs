#!/usr/bin/zsh


OUT_FULL="renders/${1%.yaml}.pdf"
OUT_SIMP="renders/${1%.yaml}-simple.pdf"

OUT_FULL_PNG="renders/${1%.yaml}.png"
OUT_SIMP_PNG="renders/${1%.yaml}-simple.png"

# Render to pdf

TD=$(mktemp -d)
./gantt-to-tex.py "$1" > "$TD/gantt.tex"
pushd "$TD"
pdflatex gantt.tex
popd
mv "$TD/gantt.pdf" "$OUT_FULL"
rm -r "$TD"

TD=$(mktemp -d)
./gantt-to-tex.py "$1" simplified > "$TD/gantt.tex"
pushd "$TD"
pdflatex gantt.tex
popd
mv "$TD/gantt.pdf" "$OUT_SIMP"
rm -r "$TD"

#convert -alpha Off +antialias -trim -density 600 -resize 25% "$OUT_FULL" "$OUT_FULL_PNG"
convert -alpha Off +antialias -trim -density 300 -resize 25% "$OUT_SIMP" "$OUT_SIMP_PNG"
