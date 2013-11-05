import sys
import fileinput
import pyfits
import numpy as np
import matplotlib.pyplot as plt
from pyfits import Column
#
# This is a file where I can test random stuff on pieces of the DB, or test parts of 
# algorithms, or just experiment to familiarize myself with Python.
#
# This is the fits file that maps all the IDs to one another:
#
q = pyfits.open('../classifications/CANDELS_ZooID_dbID_location_match.fits', memmap=True)
subjDB = q[1].data

print subjDB.field('zooniverse_id')
print q[1].columns
#
# Columns:
#   hubble_id_base
#   hubble_id_img
#       The hubble id, e.g. 'GDS_12345', is the jpg filename and the internal CANDELS ID.
#       Some of the sources have two instances, e.g. 'GDS_12345_2', so there is a base name
#       and then a name of the image. For now we'll mostly use base below, but it's important
#       to keep the ability to separate them if needed later.
#
#   magnitude
#       The H-band magnitude of the CANDELS image. Not really needed here.
#
#   db_id
#       The database id, which is the only id in both this and the classifications file.
#
#   zooniverse_id
#       The overall Zooniverse id, e.g. AGZ1234567.
#
#   location_standard
#   location_thumbnail
#   location_inverted
#       The URLs to different versions of the subject images.
#

# Now set up the collated classification columns. For each question there is a number of classifications
# as well as vote fractions for each possible answer.
# Each question has a question number T (T00 to T16)
# Each of those questions has a number of answers A.
# In previous iterations the answer numbers were themselves unique but in CANDELS
# they appear to start at A01 for each question number, so they're not.
#

intcolumn = map(int, subjDB.magnitude - subjDB.magnitude)
floatcolumn = subjDB.magnitude - subjDB.magnitude

c01 = Column(name='num_classifications', format='J', array=intcolumn)
                       
c02 = Column(name='t00_smooth_and_rounded_a0_smooth_frac', format='D', array=floatcolumn)
c03 = Column(name='t00_smooth_and_rounded_a1_features_frac', format='D', array=floatcolumn)
c04 = Column(name='t00_smooth_and_rounded_a2_artifact_frac', format='D', array=floatcolumn)
c05 = Column(name='t00_smooth_and_rounded_count', format='J', array=intcolumn)

c06 = Column(name='t01_how_rounded_a0_completely_frac', format='D', array=floatcolumn)
c07 = Column(name='t01_how_rounded_a1_inbetween_frac', format='D', array=floatcolumn)
c08 = Column(name='t01_how_rounded_a2_cigarshaped_frac', format='D', array=floatcolumn)
c09 = Column(name='t01_how_rounded_count', format='J', array=intcolumn)

c10 = Column(name='t02_clumpy_appearance_a0_yes_frac', format='D', array=floatcolumn)
c11 = Column(name='t02_clumpy_appearance_a1_no_frac', format='D', array=floatcolumn)
c12 = Column(name='t02_clumpy_appearance_count', format='J', array=intcolumn)

c13 = Column(name='t03_how_many_clumps_a0_1_frac', format='D', array=floatcolumn)
c14 = Column(name='t03_how_many_clumps_a1_2_frac', format='D', array=floatcolumn)
c15 = Column(name='t03_how_many_clumps_a2_3_frac', format='D', array=floatcolumn)
c16 = Column(name='t03_how_many_clumps_a3_4_frac', format='D', array=floatcolumn)
c17 = Column(name='t03_how_many_clumps_a4_5_plus_frac', format='D', array=floatcolumn)
c18 = Column(name='t03_how_many_clumps_a5_cant_tell_frac', format='D', array=floatcolumn)
c19 = Column(name='t03_how_many_clumps_count', format='J', array=intcolumn)

c20 = Column(name='t04_clump_configuration_a0_straight_line_frac', format='D', array=floatcolumn)
c21 = Column(name='t04_clump_configuration_a1_chain_frac', format='D', array=floatcolumn)
c22 = Column(name='t04_clump_configuration_a2_cluster_or_irregular_frac', format='D', array=floatcolumn)
c23 = Column(name='t04_clump_configuration_a3_spiral_frac', format='D', array=floatcolumn)
c24 = Column(name='t04_clump_configuration_count', format='J', array=intcolumn)

c25 = Column(name='t05_is_one_clump_brightest_a0_yes_frac', format='D', array=floatcolumn)
c26 = Column(name='t05_is_one_clump_brightest_a1_no_frac', format='D', array=floatcolumn)
c27 = Column(name='t05_is_one_clump_brightest_count', format='J', array=intcolumn)

c28 = Column(name='t06_brightest_clump_central_a0_yes_frac', format='D', array=floatcolumn)
c29 = Column(name='t06_brightest_clump_central_a1_no_frac', format='D', array=floatcolumn)
c30 = Column(name='t06_brightest_clump_central_count', format='J', array=intcolumn)

c31 = Column(name='t07_galaxy_symmetrical_a0_yes_frac', format='D', array=floatcolumn)
c32 = Column(name='t07_galaxy_symmetrical_a1_no_fracc', format='D', array=floatcolumn)
c33 = Column(name='t07_galaxy_symmetrical_count', format='J', array=intcolumn)

c34 = Column(name='t08_clumps_embedded_larger_object_a0_yes_frac', format='D', array=floatcolumn)
c35 = Column(name='t08_clumps_embedded_larger_object_a1_no_frac', format='D', array=floatcolumn)
c36 = Column(name='t08_clumps_embedded_larger_object_count', format='J', array=intcolumn)

c37 = Column(name='t09_disk_edge_on_a0_yes_frac', format='D', array=floatcolumn)
c38 = Column(name='t09_disk_edge_on_a1_no_frac', format='D', array=floatcolumn)
c39 = Column(name='t09_disk_edge_on_count', format='J', array=intcolumn)

c40 = Column(name='t10_edge_on_bulge_a0_yes_frac', format='D', array=floatcolumn)
c41 = Column(name='t10_edge_on_bulge_a1_no_frac', format='D', array=floatcolumn)
c42 = Column(name='t10_edge_on_bulge_count', format='J', array=intcolumn)

c43 = Column(name='t11_bar_feature_a0_yes_frac', format='D', array=floatcolumn)
c44 = Column(name='t11_bar_feature_a1_no_frac', format='D', array=floatcolumn)
c45 = Column(name='t11_bar_feature_count', format='J', array=intcolumn)

c46 = Column(name='t12_spiral_pattern_a0_yes_frac', format='D', array=floatcolumn)
c47 = Column(name='t12_spiral_pattern_a1_no_frac', format='D', array=floatcolumn)
c48 = Column(name='t12_spiral_pattern_count', format='J', array=intcolumn)

c49 = Column(name='t13_spiral_arm_winding_a0_tight_frac', format='D', array=floatcolumn)
c50 = Column(name='t13_spiral_arm_winding_a1_medium_frac', format='D', array=floatcolumn)
c51 = Column(name='t13_spiral_arm_winding_a2_loose_frac', format='D', array=floatcolumn)
c52 = Column(name='t13_spiral_arm_winding_count', format='J', array=intcolumn)

c53 = Column(name='t14_spiral_arm_count_a0_1_frac', format='D', array=floatcolumn)
c54 = Column(name='t14_spiral_arm_count_a1_2_frac', format='D', array=floatcolumn)
c55 = Column(name='t14_spiral_arm_count_a2_3_frac', format='D', array=floatcolumn)
c56 = Column(name='t14_spiral_arm_count_a3_4_frac', format='D', array=floatcolumn)
c57 = Column(name='t14_spiral_arm_count_a4_5_plus_frac', format='D', array=floatcolumn)
c58 = Column(name='t14_spiral_arm_count_a5_cant_tell_frac', format='D', array=floatcolumn)
c59 = Column(name='t14_spiral_arm_count_count', format='J', array=intcolumn)

c60 = Column(name='t15_bulge_prominence_a0_no_bulge_frac', format='D', array=floatcolumn)
c61 = Column(name='t15_bulge_prominence_a1_obvious_frac', format='D', array=floatcolumn)
c62 = Column(name='t15_bulge_prominence_a2_dominant_frac', format='D', array=floatcolumn)
c63 = Column(name='t15_bulge_prominence_count', format='J', array=intcolumn)

c64 = Column(name='t16_merging_tidal_debris_a0_merging_frac', format='D', array=floatcolumn)
c65 = Column(name='t16_merging_tidal_debris_a1_tidal_debris_frac', format='D', array=floatcolumn)
c66 = Column(name='t16_merging_tidal_debris_a2_both_frac', format='D', array=floatcolumn)
c67 = Column(name='t16_merging_tidal_debris_a3_neither_frac', format='D', array=floatcolumn)
c68 = Column(name='t16_merging_tidal_debris_count', format='J', array=intcolumn)


classifications = pyfits.new_table([c01,c02,c03,c04,c05,c06,c07,c08,c09,c10,c11,c12,c13,c14,c15,c16,c17,c18,c19,c20,c21,c22,c23,c24,c25,c26,c27,c28,c29,c30,c31,c32,c33,c34,c35,c36,c37,c38,c39,c40,c41,c42,c43,c44,c45,c46,c47,c48,c49,c50,c51,c52,c53,c54,c55,c56,c57,c58,c59,c60,c61,c62,c63,c64,c65,c66,c67,c68])
#print classifications.data

qq = q[1].columns + classifications.columns
bigtable = pyfits.new_table(qq)
bigdata = bigtable.data

print bigdata.field('magnitude')
print bigdata.field('db_id')[1]

#print bigdata

for index, s in enumerate(bigdata.field('db_id')) :
    if s == '504e468dc499611ea600cb69' :
        print index, s
    
    
    


#bigtable.writeto('newtable.fits')
