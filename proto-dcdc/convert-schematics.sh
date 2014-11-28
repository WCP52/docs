#!/usr/bin/zsh

for i in *.eps; do
    convert -alpha Off +antialias -density 320 -resize 25% "$i" "renders/${i%.eps}.png"
    epspdf "$i" "renders/${i%.eps}.pdf"
done
