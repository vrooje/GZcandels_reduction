#!/bin/bash

# Extract the CANDELS Zooniverse IDs from larger data dump

# K. Willett, UMN, 06 Nov 2013

OLDFILE=$1
NEWFILE=${OLDFILE%.*}"_CANDELSonly.csv"

# Delete lines with no responses for CANDELS question 0

sed '/[en|zh|es],a-/!d' $1 > $NEWFILE

read lines_old words_old chars_old filename_old <<< $(wc $OLDFILE)
read lines_new words_new chars_new filename_new <<< $(wc $NEWFILE)
echo ""
echo "Extracted "$lines_new" CANDELS classifications from "$lines_old" total in GZ."
echo ""

# Check the header fields to make sure SLOAN, UKIDSS, FERENGI are unpopulated
# cat $NEWFILE | awk -F, '{print "CANDELS-0: "$6", SLOAN-0: "$24", UKIDSS-0: "$36", FERENGI-0: "$48}'
# echo ""

exit $?
