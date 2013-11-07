GZcandels_reduction
===================

Galaxy Zoo-CANDELS data reduction: in progress.

Note: this repository is public, but the database of classifications is not. Currently the raw database *and* the classifications files that results from running the code here is stored in a separate directory (../classifications/) which is not synced here.

## To run

- Step 0: Download database dump in csv format.

- Step 1: Edit header line to remove weird formatting in first column

- Step 2: Select only the CANDELS galaxies

- Step 3: Collate votes

- Step 4: Remove duplicates from intended 2- and 6-orbit depths

```
    ./fix_raw_classifications.sh 2013-11-03_galaxy_zoo_classifications.csv
    ./extract_candels_ids.sh 2013-11-03_galaxy_zoo_classifications.csv
    python collate_candels.py 2013-11-03_galaxy_zoo_classifications.csv
    python combine_duplicates.py classifications/candels_classifications_collated.fits
```

Required Python packages:

- numpy
- astropy *or* pyfits
