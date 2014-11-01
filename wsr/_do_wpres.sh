#!/bin/bash

# Simple script to do the weekly presentation. No formatting, just preps
# the email. Renames the file to comply with naming standard.

#SEND_TO="cpavlin1@binghamton.edu"
SEND_TO="wcpta@binghamton.edu"

BODY_TMP="$(mktemp)"

BODY_TEXT="Dear WCP TAs,

Attached is my team's weekly status presentation.

Sincerely,

Chris Pavlina
BS Electrical Engineering, Spring 2015
Binghamton University
cpavlin1@binghamton.edu
"

echo "$BODY_TEXT" > "$BODY_TMP"

WP="WCP52 Gain-Phase Weekly Pres $(date +%Y-%m-%d).pptx"

cp "$1" "$WP"

mutt3 -s "WCP52 Gain-Phase Weekly Pres $(date +%Y-%m-%d)" "$SEND_TO" -i "$BODY_TMP" -a "$WP" -b "howens1@binghamton.edu" -b "kxu14@binghamton.edu" -b "kzach1@binghamton.edu"

rm "$WP"

