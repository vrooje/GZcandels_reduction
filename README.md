GZcandels_reduction
===================

Galaxy Zoo-CANDELS data reduction

Step 1: Download database dump in csv format.
Step 1a: At the moment, edit header line of csv file to remove weird formatting in first column.
Step 2: Currently I extract only the CANDELS db_ids using a simple awk script, but this may not be strictly necessary.
Step 3: run collate_candels.py
Step 4: run combine_duplicates.py

