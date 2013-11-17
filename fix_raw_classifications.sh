#!/bin/bash

# Shell script removes the corrupted header line on raw classification data. 
# Deprecated as of 17 Nov 2013; CSV file when downloaded from servers now has correct header.

# Originally written by K. Willett, UMN, 06 Nov 2013

TMP=$(mktemp)
HEADER_FILE='headers.csv'
HEADER_TEMP='headers_temp.csv'
cp $HEADER_FILE $HEADER_TEMP

# Strip first line in place

sed '1d' $1 > $TMP
cat $TMP >> $HEADER_TEMP
mv $HEADER_TEMP $1
rm $TMP

echo "Saved CSV file with fixed header in "$1

#head $1

exit $?
