GZcandels_reduction
===================

Galaxy Zoo-CANDELS data reduction: in progress.

Note: this repository is public, but the database of classifications is not. Currently the raw database *and* the classifications files that results from running the code here is stored in a separate directory (../classifications/) which is not synced here.

## To run

Step 1: Download database dump in csv format.

Step 1a: At the moment, edit header line of csv file to remove weird formatting in first column.

Step 2: Currently I extract only the CANDELS db_ids using a simple awk script, but this may not be strictly necessary.

Step 3: run collate_candels.py

Step 4: run combine_duplicates.py

