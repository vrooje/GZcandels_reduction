GZcandels_reduction
===================

Galaxy Zoo-CANDELS data reduction: in progress.

Note: this repository is public, but the database of classifications is not. Currently the raw database *and* the classifications files that results from running the code here is stored in a separate directory (../classifications/) which is not synced here.

## To run

- Step 1: Download database dump in csv format.

- Step 1a: Run fix_raw_classifications.sh to edit header line of csv file to remove weird formatting in first column.

- Step 2: Select only the CANDELS galaxies using extract_candels_ids.sh

- Step 3: run collate_candels.py to collate votes

- Step 4: run combine_duplicates.py to remove duplicates from intended 2- and 6-orbit depths

