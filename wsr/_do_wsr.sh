#!/bin/bash

# Simple script to do the WSR. Takes the .rst file as argument, prepares it to .docx,
# then prepares the email in mutt.

WP="$(./_convert_to_word.sh "$1")"
msword "$WP"
echo Enter to continue...
read


#SEND_TO="cpavlin1@binghamton.edu"
SEND_TO="wcpta@binghamton.edu"

BODY_TMP="$(mktemp)"

BODY_TEXT="Dear WCP TAs,

Attached is our weekly status report for the week of $(date +%Y-%m-%d).

Sincerely,

Chris Pavlina
BS Electrical Engineering, Spring 2015
Binghamton University
cpavlin1@binghamton.edu
"

echo "$BODY_TEXT" > "$BODY_TMP"

mutt3 -s "WCP52 Gain-Phase Weekly Pres $(date +%Y-%m-%d)" "$SEND_TO" -i "$BODY_TMP" -a "$WP" -b "howens1@binghamton.edu" -b "kxu14@binghamton.edu" -b "kzach1@binghamton.edu"

