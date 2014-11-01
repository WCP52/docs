#!/bin/bash

# Filename without .rst
FN="${1%.rst}"

rst2odt2 "$1" "$FN.odt"
unoconv -f docx -t _format_template.ott "$FN.odt"
rm "$FN.odt"

# Apply proper file name
PROPER_FN="WCP52 Gain-Phase Weekly $(date +%Y-%m-%d).docx"

mv "$FN.docx" "$PROPER_FN"
echo "$PROPER_FN"
