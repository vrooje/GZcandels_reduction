import sys
import fileinput
import pyfits
import numpy as np
import matplotlib.pyplot as plt
from pyfits import Column

# This is the fits file that maps all the IDs to one another:
#
subjinfo_file = '../classifications/CANDELS_ZooID_dbID_location_match.fits'
print 'Reading', subjinfo_file, '...'
q = pyfits.open(subjinfo_file, memmap=True)
subjinfo = q[1].data
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
print 'Creating columns for vote fractions...'

intcolumn = map(int, subjinfo.magnitude - subjinfo.magnitude)
floatcolumn = subjinfo.magnitude - subjinfo.magnitude

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
c32 = Column(name='t07_galaxy_symmetrical_a1_no_frac', format='D', array=floatcolumn)
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


classifications = pyfits.new_table([c01,c02,c03,c04,c05,c06,c07,c08,c09,c10,c11,c12,c13,c14,c15,c16,c17,c18,c19,c20, c21,c22,c23,c24,c25,c26,c27,c28,c29,c30,c31,c32,c33,c34,c35,c36,c37,c38,c39,c40, c41,c42,c43,c44,c45,c46,c47,c48,c49,c50,c51,c52,c53,c54,c55,c56,c57,c58,c59,c60, c61,c62,c63,c64,c65,c66,c67,c68])
#print classifications.data

qq = q[1].columns + classifications.columns
subjDB = pyfits.new_table(qq)

print 'Reading classifications file...'

# 5 + 18 + 12 + 12 + 19 = 66
# Now open the classifications csv and fill an object with it
with open('2013-10-27_galaxy_zoo_classifications_CANDELSonly.csv') as f:
    subjClass = np.loadtxt(f, delimiter=",", dtype={'names':('classification_id','subject_id','user_id','created_at','lang', 'candels_0','candels_1','candels_2','candels_3','candels_4','candels_5','candels_6','candels_7','candels_8','candels_9','candels_10', 'candels_11','candels_12','candels_13','candels_14','candels_15','candels_16','candels_17', 'sloan_0','sloan_1','sloan_2','sloan_3','sloan_4','sloan_5','sloan_6','sloan_7','sloan_8','sloan_9','sloan_10','sloan_11', 'ukidss_0','ukidss_1','ukidss_2','ukidss_3','ukidss_4','ukidss_5','ukidss_6','ukidss_7','ukidss_8','ukidss_9','ukidss_10','ukidss_11', 'ferengi_0','ferengi_1','ferengi_2','ferengi_3','ferengi_4','ferengi_5','ferengi_6','ferengi_7','ferengi_8','ferengi_9','ferengi_10', 'ferengi_11','ferengi_12','ferengi_13','ferengi_14','ferengi_15','ferengi_16','ferengi_17','ferengi_18'), 'formats':('S24','S24','S24','S19','S3', 'S4','S4','S4','S4','S4','S4','S4','S4','S4','S4','S4', 'S4','S4','S4','S4','S4','S4','S4', 'S4','S4','S4','S4','S4','S4','S4','S4','S4','S4','S4','S4', 'S4','S4','S4','S4','S4','S4','S4','S4','S4','S4','S4','S4', 'S4','S4','S4','S4','S4','S4','S4','S4','S4','S4','S4', 'S4','S4','S4','S4','S4','S4','S4','S4' )},skiprows=1)

print '...done.'
# Note: the full headers are:
#id,subject_id,user_id,created_at,lang,candels-0,candels-1,candels-2,candels-3,candels-4,candels-5,candels-6,candels-7,candels-8,candels-9,candels-10,candels-11,candels-12,candels-13,candels-14,candels-15,candels-16,candels-17,sloan-0,sloan-1,sloan-2,sloan-3,sloan-4,sloan-5,sloan-6,sloan-7,sloan-8,sloan-9,sloan-10,sloan-11,ukidss-0,ukidss-1,ukidss-2,ukidss-3,ukidss-4,ukidss-5,ukidss-6,ukidss-7,ukidss-8,ukidss-9,ukidss-10,ukidss-11,ferengi-0,ferengi-1,ferengi-2,ferengi-3,ferengi-4,ferengi-5,ferengi-6,ferengi-7,ferengi-8,ferengi-9,ferengi-10,ferengi-11,ferengi-12,ferengi-13,ferengi-14,ferengi-15,ferengi-16,ferengi-17,ferengi-18
#or
# 1  classification_id
# 2  subject_id
# 3  user_id
# 4  created_at
# 5  lang
# 6  candels_0
# 7  candels_1
# 8  candels_2
# 9  candels_3
# 10 candels_4
# 11 candels_5
# 12 candels_6
# 13 candels_7
# 14 candels_8
# 15 candels_9
# 16 candels_10
# 17 candels_11
# 18 candels_12
# 19 candels_13
# 20 candels_14
# 21 candels_15
# 22 candels_16
# 23 candels_17
# 24 sloan_0
# 25 sloan_1
# 26 sloan_2
# 27 sloan_3
# 28 sloan_4
# 29 sloan_5
# 30 sloan_6
# 31 sloan_7
# 32 sloan_8
# 33 sloan_9
# 34 sloan_10
# 35 sloan_11
# 36 ukidss_0
# 37 ukidss_1
# 38 ukidss_2
# 39 ukidss_3
# 40 ukidss_4
# 41 ukidss_5
# 42 ukidss_6
# 43 ukidss_7
# 44 ukidss_8
# 45 ukidss_9
# 46 ukidss_10
# 47 ukidss_11
# 48 ferengi_0
# 49 ferengi_1
# 50 ferengi_2
# 51 ferengi_3
# 52 ferengi_4
# 53 ferengi_5
# 54 ferengi_6
# 55 ferengi_7
# 56 ferengi_8
# 57 ferengi_9
# 58 ferengi_10
# 59 ferengi_11
# 60 ferengi_12
# 61 ferengi_13
# 62 ferengi_14
# 63 ferengi_15
# 64 ferengi_16
# 65 ferengi_17
# 66 ferengi_18
#
# But we are only concerned (for now) with the classification_id and the various candels_ids.
#

# There has to be a better way to do this, but for now let's do the brute force way: for each subject, find the matches to it in the classification file and add them up.

#print subjDB.data.field('db_id')
print 'Counting classifications...'

for index, s in enumerate(subjDB.data.field('db_id')) :
    # find each classification for this subject
    this_subj = (subjClass['subject_id'] == s)

    # now add them up - just count, no fractions yet (we don't know the total per question yet)
    for c in subjClass[this_subj] :
        subjDB.data.field('num_classifications')[index] += 1
        
        # t00_smooth_and_rounded:
        #    a0_smooth
        #    a1_features
        #    a2_artifact
        #    count

        if c['candels_0'] == 'a-0' :
            subjDB.data.field('t00_smooth_and_rounded_a0_smooth_frac')[index] += 1.0
            subjDB.data.field('t00_smooth_and_rounded_count')[index] += 1

        if c['candels_0'] == 'a-1' :
            subjDB.data.field('t00_smooth_and_rounded_a1_features_frac')[index] += 1.0
            subjDB.data.field('t00_smooth_and_rounded_count')[index] += 1

        if c['candels_0'] == 'a-2' :
            subjDB.data.field('t00_smooth_and_rounded_a2_artifact_frac')[index] += 1.0
            subjDB.data.field('t00_smooth_and_rounded_count')[index] += 1


        # t01_how_rounded:
        #    a0_completely
        #    a1_inbetween
        #    a2_cigarshaped
        #    count
        if c['candels_1'] == 'a-0' :
            subjDB.data.field('t01_how_rounded_a0_completely_frac')[index] += 1.0
            subjDB.data.field('t01_how_rounded_count')[index] += 1

        if c['candels_1'] == 'a-1' :
            subjDB.data.field('t01_how_rounded_a1_inbetween_frac')[index] += 1.0
            subjDB.data.field('t01_how_rounded_count')[index] += 1

        if c['candels_1'] == 'a-2' :
            subjDB.data.field('t01_how_rounded_a2_cigarshaped_frac')[index] += 1.0
            subjDB.data.field('t01_how_rounded_count')[index] += 1



        # t02_clumpy_appearance:
        #    a0_yes
        #    a1_no
        #    count
        if c['candels_2'] == 'a-0' :
            subjDB.data.field('t02_clumpy_appearance_a0_yes_frac')[index] += 1.0
            subjDB.data.field('t02_clumpy_appearance_count')[index] += 1

        if c['candels_2'] == 'a-1' :
            subjDB.data.field('t02_clumpy_appearance_a1_no_frac')[index] += 1.0
            subjDB.data.field('t02_clumpy_appearance_count')[index] += 1



        # t03_how_many_clumps:
        #    a0_1
        #    a1_2
        #    a2_3
        #    a3_4
        #    a4_5_plus
        #    a5_cant_tell
        #    count
        if c['candels_3'] == 'a-0' :
            subjDB.data.field('t03_how_many_clumps_a0_1_frac')[index] += 1.0
            subjDB.data.field('t03_how_many_clumps_count')[index] += 1

        if c['candels_3'] == 'a-1' :
            subjDB.data.field('t03_how_many_clumps_a1_2_frac')[index] += 1.0
            subjDB.data.field('t03_how_many_clumps_count')[index] += 1

        if c['candels_3'] == 'a-2' :
            subjDB.data.field('t03_how_many_clumps_a2_3_frac')[index] += 1.0
            subjDB.data.field('t03_how_many_clumps_count')[index] += 1

        if c['candels_3'] == 'a-3' :
            subjDB.data.field('t03_how_many_clumps_a3_4_frac')[index] += 1.0
            subjDB.data.field('t03_how_many_clumps_count')[index] += 1

        if c['candels_3'] == 'a-4' :
            subjDB.data.field('t03_how_many_clumps_a4_5_plus_frac')[index] += 1.0
            subjDB.data.field('t03_how_many_clumps_count')[index] += 1

        if c['candels_3'] == 'a-5' :
            subjDB.data.field('t03_how_many_clumps_a5_cant_tell_frac')[index] += 1.0
            subjDB.data.field('t03_how_many_clumps_count')[index] += 1


        # t04_clump_configuration:
        #    a0_straight_line
        #    a1_chain
        #    a2_cluster_or_irregular
        #    a3_spiral
        #    count
        if c['candels_4'] == 'a-0' :
            subjDB.data.field('t04_clump_configuration_a0_straight_line_frac')[index] += 1.0
            subjDB.data.field('t04_clump_configuration_count')[index] += 1

        if c['candels_4'] == 'a-1' :
            subjDB.data.field('t04_clump_configuration_a1_chain_frac')[index] += 1.0
            subjDB.data.field('t04_clump_configuration_count')[index] += 1

        if c['candels_4'] == 'a-2' :
            subjDB.data.field('t04_clump_configuration_a2_cluster_or_irregular_frac')[index] += 1.0
            subjDB.data.field('t04_clump_configuration_count')[index] += 1

        if c['candels_4'] == 'a-3' :
            subjDB.data.field('t04_clump_configuration_a3_spiral_frac')[index] += 1.0
            subjDB.data.field('t04_clump_configuration_count')[index] += 1


        # t05_is_one_clump_brightest:
        #    a0_yes
        #    a1_no
        #    count
        if c['candels_5'] == 'a-0' :
            subjDB.data.field('t05_is_one_clump_brightest_a0_yes_frac')[index] += 1.0
            subjDB.data.field('t05_is_one_clump_brightest_count')[index] += 1

        if c['candels_5'] == 'a-1' :
            subjDB.data.field('t05_is_one_clump_brightest_a1_no_frac')[index] += 1.0
            subjDB.data.field('t05_is_one_clump_brightest_count')[index] += 1



        # t06_brightest_clump_central:
        #    a0_yes
        #    a1_no
        #    count
        if c['candels_6'] == 'a-0' :
            subjDB.data.field('t06_brightest_clump_central_a0_yes_frac')[index] += 1.0
            subjDB.data.field('t06_brightest_clump_central_count')[index] += 1

        if c['candels_6'] == 'a-1' :
            subjDB.data.field('t06_brightest_clump_central_a1_no_frac')[index] += 1.0
            subjDB.data.field('t06_brightest_clump_central_count')[index] += 1



        # t07_galaxy_symmetrical:
        #    a0_yes
        #    a1_no
        #    count
        if c['candels_7'] == 'a-0' :
            subjDB.data.field('t07_galaxy_symmetrical_a0_yes_frac')[index] += 1.0
            subjDB.data.field('t07_galaxy_symmetrical_count')[index] += 1
        
        if c['candels_7'] == 'a-1' :
            subjDB.data.field('t07_galaxy_symmetrical_a1_no_frac')[index] += 1.0
            subjDB.data.field('t07_galaxy_symmetrical_count')[index] += 1
        


        # t08_clumps_embedded_larger_object:
        #    a0_yes
        #    a1_no
        #    count
        if c['candels_8'] == 'a-0' :
            subjDB.data.field('t08_clumps_embedded_larger_object_a0_yes_frac')[index] += 1.0
            subjDB.data.field('t08_clumps_embedded_larger_object_count')[index] += 1
        
        if c['candels_8'] == 'a-1' :
            subjDB.data.field('t08_clumps_embedded_larger_object_a1_no_frac')[index] += 1.0
            subjDB.data.field('t08_clumps_embedded_larger_object_count')[index] += 1
        
        
        
        # t09_disk_edge_on:
        #    a0_yes
        #    a1_no
        #    count
        if c['candels_9'] == 'a-0' :
            subjDB.data.field('t09_disk_edge_on_a0_yes_frac')[index] += 1.0
            subjDB.data.field('t09_disk_edge_on_count')[index] += 1
        
        if c['candels_9'] == 'a-1' :
            subjDB.data.field('t09_disk_edge_on_a1_no_frac')[index] += 1.0
            subjDB.data.field('t09_disk_edge_on_count')[index] += 1
        


        # t10_edge_on_bulge:
        #    a0_yes
        #    a1_no
        #    count
        if c['candels_10'] == 'a-0' :
            subjDB.data.field('t10_edge_on_bulge_a0_yes_frac')[index] += 1.0
            subjDB.data.field('t10_edge_on_bulge_count')[index] += 1
        
        if c['candels_10'] == 'a-1' :
            subjDB.data.field('t10_edge_on_bulge_a1_no_frac')[index] += 1.0
            subjDB.data.field('t10_edge_on_bulge_count')[index] += 1
        


        # t11_bar_feature:
        #    a0_yes
        #    a1_no
        #    count
        if c['candels_11'] == 'a-0' :
            subjDB.data.field('t11_bar_feature_a0_yes_frac')[index] += 1.0
            subjDB.data.field('t11_bar_feature_count')[index] += 1
        
        if c['candels_11'] == 'a-1' :
            subjDB.data.field('t11_bar_feature_a1_no_frac')[index] += 1.0
            subjDB.data.field('t11_bar_feature_count')[index] += 1
        


        # t12_spiral_pattern:
        #    a0_yes
        #    a1_no
        #    count
        if c['candels_12'] == 'a-0' :
            subjDB.data.field('t12_spiral_pattern_a0_yes_frac')[index] += 1.0
            subjDB.data.field('t12_spiral_pattern_count')[index] += 1
        
        if c['candels_12'] == 'a-1' :
            subjDB.data.field('t12_spiral_pattern_a1_no_frac')[index] += 1.0
            subjDB.data.field('t12_spiral_pattern_count')[index] += 1
        

        # t13_spiral_arm_winding:
        #    a0_tight
        #    a1_medium
        #    a2_loose
        #    count
        if c['candels_13'] == 'a-0' :
            subjDB.data.field('t13_spiral_arm_winding_a0_tight_frac')[index] += 1.0
            subjDB.data.field('t13_spiral_arm_winding_count')[index] += 1
        
        if c['candels_13'] == 'a-1' :
            subjDB.data.field('t13_spiral_arm_winding_a1_medium_frac')[index] += 1.0
            subjDB.data.field('t13_spiral_arm_winding_count')[index] += 1
        
        if c['candels_13'] == 'a-2' :
            subjDB.data.field('t13_spiral_arm_winding_a2_loose_frac')[index] += 1.0
            subjDB.data.field('t13_spiral_arm_winding_count')[index] += 1
        


        # t14_spiral_arm_count:
        #    a0_1
        #    a1_2
        #    a2_3
        #    a3_4
        #    a4_5
        #    a5_cant_tell
        #    count
        if c['candels_14'] == 'a-0' :
            subjDB.data.field('t14_spiral_arm_count_a0_1_frac')[index] += 1.0
            subjDB.data.field('t14_spiral_arm_count_count')[index] += 1
        
        if c['candels_14'] == 'a-1' :
            subjDB.data.field('t14_spiral_arm_count_a1_2_frac')[index] += 1.0
            subjDB.data.field('t14_spiral_arm_count_count')[index] += 1
        
        if c['candels_14'] == 'a-2' :
            subjDB.data.field('t14_spiral_arm_count_a2_3_frac')[index] += 1.0
            subjDB.data.field('t14_spiral_arm_count_count')[index] += 1
        
        if c['candels_14'] == 'a-3' :
            subjDB.data.field('t14_spiral_arm_count_a3_4_frac')[index] += 1.0
            subjDB.data.field('t14_spiral_arm_count_count')[index] += 1
        
        if c['candels_14'] == 'a-4' :
            subjDB.data.field('t14_spiral_arm_count_a4_5_plus_frac')[index] += 1.0
            subjDB.data.field('t14_spiral_arm_count_count')[index] += 1
        
        if c['candels_14'] == 'a-5' :
            subjDB.data.field('t14_spiral_arm_count_a5_cant_tell_frac')[index] += 1.0
            subjDB.data.field('t14_spiral_arm_count_count')[index] += 1
        


        # t15_bulge_prominence:
        #    a0_no_bulge
        #    a1_obvious
        #    a2_dominant
        #    count
        if c['candels_15'] == 'a-0' :
            subjDB.data.field('t15_bulge_prominence_a0_no_bulge_frac')[index] += 1.0
            subjDB.data.field('t15_bulge_prominence_count')[index] += 1
        
        if c['candels_15'] == 'a-1' :
            subjDB.data.field('t15_bulge_prominence_a1_obvious_frac')[index] += 1.0
            subjDB.data.field('t15_bulge_prominence_count')[index] += 1
        
        if c['candels_15'] == 'a-2' :
            subjDB.data.field('t15_bulge_prominence_a2_dominant_frac')[index] += 1.0
            subjDB.data.field('t15_bulge_prominence_count')[index] += 1
        


        # t16_merging_tidal_debris:
        #    a0_merging
        #    a1_tidal_debris
        #    a2_both
        #    a3_neither
        #    count
        if c['candels_16'] == 'a-0' :
            subjDB.data.field('t16_merging_tidal_debris_a0_merging_frac')[index] += 1.0
            subjDB.data.field('t16_merging_tidal_debris_count')[index] += 1
        
        if c['candels_16'] == 'a-1' :
            subjDB.data.field('t16_merging_tidal_debris_a1_tidal_debris_frac')[index] += 1.0
            subjDB.data.field('t16_merging_tidal_debris_count')[index] += 1
        
        if c['candels_16'] == 'a-2' :
            subjDB.data.field('t16_merging_tidal_debris_a2_both_frac')[index] += 1.0
            subjDB.data.field('t16_merging_tidal_debris_count')[index] += 1
        
        if c['candels_16'] == 'a-3' :
            subjDB.data.field('t16_merging_tidal_debris_a3_neither_frac')[index] += 1.0
            subjDB.data.field('t16_merging_tidal_debris_count')[index] += 1
        
        
    #print '...done.'


    #Now that we've counted all the classifications for this subject, do the fractions
    #There is probably a better way to do this than manually but WHATEVER
    #print 'Calculating fractions...'
    if index % 1000 == 0 :
        print 'Done ', index, '...'
    
    if subjDB.data.field('t00_smooth_and_rounded_count')[index] > 0 :
        subjDB.data.field('t00_smooth_and_rounded_a0_smooth_frac')[index]   /= subjDB.data.field('t00_smooth_and_rounded_count')[index]
        subjDB.data.field('t00_smooth_and_rounded_a1_features_frac')[index] /= subjDB.data.field('t00_smooth_and_rounded_count')[index]
        subjDB.data.field('t00_smooth_and_rounded_a2_artifact_frac')[index] /= subjDB.data.field('t00_smooth_and_rounded_count')[index]
    else :
        subjDB.data.field('t00_smooth_and_rounded_a0_smooth_frac')[index]   = 0.0
        subjDB.data.field('t00_smooth_and_rounded_a1_features_frac')[index] = 0.0
        subjDB.data.field('t00_smooth_and_rounded_a2_artifact_frac')[index] = 0.0
    
    
    if subjDB.data.field('t01_how_rounded_count')[index] > 0 :
        subjDB.data.field('t01_how_rounded_a0_completely_frac')[index]  /= subjDB.data.field('t01_how_rounded_count')[index]
        subjDB.data.field('t01_how_rounded_a1_inbetween_frac')[index]   /= subjDB.data.field('t01_how_rounded_count')[index]
        subjDB.data.field('t01_how_rounded_a2_cigarshaped_frac')[index] /= subjDB.data.field('t01_how_rounded_count')[index]
    else :
        subjDB.data.field('t01_how_rounded_a0_completely_frac')[index]  = 0.0
        subjDB.data.field('t01_how_rounded_a1_inbetween_frac')[index]   = 0.0
        subjDB.data.field('t01_how_rounded_a2_cigarshaped_frac')[index] = 0.0
    
    
    
    if subjDB.data.field('t02_clumpy_appearance_count')[index] > 0 :
        subjDB.data.field('t02_clumpy_appearance_a0_yes_frac')[index] /= subjDB.data.field('t02_clumpy_appearance_count')[index]
        subjDB.data.field('t02_clumpy_appearance_a1_no_frac')[index]  /= subjDB.data.field('t02_clumpy_appearance_count')[index]
    else :
        subjDB.data.field('t02_clumpy_appearance_a0_yes_frac')[index] = 0.0
        subjDB.data.field('t02_clumpy_appearance_a1_no_frac')[index]  = 0.0
        
        
        
    if subjDB.data.field('t03_how_many_clumps_count')[index] > 0 :
        subjDB.data.field('t03_how_many_clumps_a0_1_frac')[index]         /= subjDB.data.field('t03_how_many_clumps_count')[index]
        subjDB.data.field('t03_how_many_clumps_a1_2_frac')[index]         /= subjDB.data.field('t03_how_many_clumps_count')[index]
        subjDB.data.field('t03_how_many_clumps_a2_3_frac')[index]         /= subjDB.data.field('t03_how_many_clumps_count')[index]
        subjDB.data.field('t03_how_many_clumps_a3_4_frac')[index]         /= subjDB.data.field('t03_how_many_clumps_count')[index]
        subjDB.data.field('t03_how_many_clumps_a4_5_plus_frac')[index]    /= subjDB.data.field('t03_how_many_clumps_count')[index]
        subjDB.data.field('t03_how_many_clumps_a5_cant_tell_frac')[index] /= subjDB.data.field('t03_how_many_clumps_count')[index]
    else :
        subjDB.data.field('t03_how_many_clumps_a0_1_frac')[index]         = 0.0
        subjDB.data.field('t03_how_many_clumps_a1_2_frac')[index]         = 0.0
        subjDB.data.field('t03_how_many_clumps_a2_3_frac')[index]         = 0.0
        subjDB.data.field('t03_how_many_clumps_a3_4_frac')[index]         = 0.0
        subjDB.data.field('t03_how_many_clumps_a4_5_plus_frac')[index]    = 0.0
        subjDB.data.field('t03_how_many_clumps_a5_cant_tell_frac')[index] = 0.0
        
        
        
    if subjDB.data.field('t04_clump_configuration_count')[index] > 0 :
        subjDB.data.field('t04_clump_configuration_a0_straight_line_frac')[index]        /= subjDB.data.field('t04_clump_configuration_count')[index]
        subjDB.data.field('t04_clump_configuration_a1_chain_frac')[index]                /= subjDB.data.field('t04_clump_configuration_count')[index]
        subjDB.data.field('t04_clump_configuration_a2_cluster_or_irregular_frac')[index] /= subjDB.data.field('t04_clump_configuration_count')[index]
        subjDB.data.field('t04_clump_configuration_a3_spiral_frac')[index]               /= subjDB.data.field('t04_clump_configuration_count')[index]
    else :
        subjDB.data.field('t04_clump_configuration_a0_straight_line_frac')[index]        = 0.0
        subjDB.data.field('t04_clump_configuration_a1_chain_frac')[index]                = 0.0
        subjDB.data.field('t04_clump_configuration_a2_cluster_or_irregular_frac')[index] = 0.0
        subjDB.data.field('t04_clump_configuration_a3_spiral_frac')[index]               = 0.0
        
        
        
    if subjDB.data.field('t05_is_one_clump_brightest_count')[index] > 0 :
        subjDB.data.field('t05_is_one_clump_brightest_a0_yes_frac')[index] /= subjDB.data.field('t05_is_one_clump_brightest_count')[index]
        subjDB.data.field('t05_is_one_clump_brightest_a1_no_frac')[index]  /= subjDB.data.field('t05_is_one_clump_brightest_count')[index]
    else :
        subjDB.data.field('t05_is_one_clump_brightest_a0_yes_frac')[index] = 0.0
        subjDB.data.field('t05_is_one_clump_brightest_a1_no_frac')[index]  = 0.0
        
        
        
    if subjDB.data.field('t06_brightest_clump_central_count')[index] > 0 :
        subjDB.data.field('t06_brightest_clump_central_a0_yes_frac')[index] /= subjDB.data.field('t06_brightest_clump_central_count')[index]
        subjDB.data.field('t06_brightest_clump_central_a1_no_frac')[index]  /= subjDB.data.field('t06_brightest_clump_central_count')[index]
    else :
        subjDB.data.field('t06_brightest_clump_central_a0_yes_frac')[index] = 0.0
        subjDB.data.field('t06_brightest_clump_central_a1_no_frac')[index]  = 0.0
        
        
        
    if subjDB.data.field('t07_galaxy_symmetrical_count')[index] > 0 :
        subjDB.data.field('t07_galaxy_symmetrical_a0_yes_frac')[index] /= subjDB.data.field('t07_galaxy_symmetrical_count')[index]
        subjDB.data.field('t07_galaxy_symmetrical_a1_no_frac')[index]  /= subjDB.data.field('t07_galaxy_symmetrical_count')[index]
    else :
        subjDB.data.field('t07_galaxy_symmetrical_a0_yes_frac')[index] = 0.0
        subjDB.data.field('t07_galaxy_symmetrical_a1_no_frac')[index]  = 0.0



    if subjDB.data.field('t08_clumps_embedded_larger_object_count')[index] > 0 :        
        subjDB.data.field('t08_clumps_embedded_larger_object_a0_yes_frac')[index] /= subjDB.data.field('t08_clumps_embedded_larger_object_count')[index]
        subjDB.data.field('t08_clumps_embedded_larger_object_a1_no_frac')[index]  /= subjDB.data.field('t08_clumps_embedded_larger_object_count')[index]
    else :
        subjDB.data.field('t08_clumps_embedded_larger_object_a0_yes_frac')[index] = 0.0
        subjDB.data.field('t08_clumps_embedded_larger_object_a1_no_frac')[index]  = 0.0
       
       
        
    if subjDB.data.field('t09_disk_edge_on_count')[index] > 0 :
        subjDB.data.field('t09_disk_edge_on_a0_yes_frac')[index] /= subjDB.data.field('t09_disk_edge_on_count')[index]
        subjDB.data.field('t09_disk_edge_on_a1_no_frac')[index]  /= subjDB.data.field('t09_disk_edge_on_count')[index]
    else :
        subjDB.data.field('t09_disk_edge_on_a0_yes_frac')[index] = 0.0
        subjDB.data.field('t09_disk_edge_on_a1_no_frac')[index]  = 0.0
        
        
        
    if subjDB.data.field('t10_edge_on_bulge_count')[index] > 0 :
        subjDB.data.field('t10_edge_on_bulge_a0_yes_frac')[index] /= subjDB.data.field('t10_edge_on_bulge_count')[index]
        subjDB.data.field('t10_edge_on_bulge_a1_no_frac')[index]  /= subjDB.data.field('t10_edge_on_bulge_count')[index]
    else :
        subjDB.data.field('t10_edge_on_bulge_a0_yes_frac')[index] = 0.0
        subjDB.data.field('t10_edge_on_bulge_a1_no_frac')[index]  = 0.0
        
        
        
    if subjDB.data.field('t11_bar_feature_count')[index] > 0 :
        subjDB.data.field('t11_bar_feature_a0_yes_frac')[index] /= subjDB.data.field('t11_bar_feature_count')[index]
        subjDB.data.field('t11_bar_feature_a1_no_frac')[index]  /= subjDB.data.field('t11_bar_feature_count')[index]
    else :
        subjDB.data.field('t11_bar_feature_a0_yes_frac')[index] = 0.0
        subjDB.data.field('t11_bar_feature_a1_no_frac')[index]  = 0.0
        
        
        
    if subjDB.data.field('t12_spiral_pattern_count')[index] > 0 :
        subjDB.data.field('t12_spiral_pattern_a0_yes_frac')[index] /= subjDB.data.field('t12_spiral_pattern_count')[index]
        subjDB.data.field('t12_spiral_pattern_a1_no_frac')[index]  /= subjDB.data.field('t12_spiral_pattern_count')[index]
    else :
        subjDB.data.field('t12_spiral_pattern_a0_yes_frac')[index] = 0.0
        subjDB.data.field('t12_spiral_pattern_a1_no_frac')[index]  = 0.0
        
        
        
    if subjDB.data.field('t13_spiral_arm_winding_count')[index] > 0 :
        subjDB.data.field('t13_spiral_arm_winding_a0_tight_frac')[index]  /= subjDB.data.field('t13_spiral_arm_winding_count')[index]
        subjDB.data.field('t13_spiral_arm_winding_a1_medium_frac')[index] /= subjDB.data.field('t13_spiral_arm_winding_count')[index]
        subjDB.data.field('t13_spiral_arm_winding_a2_loose_frac')[index]  /= subjDB.data.field('t13_spiral_arm_winding_count')[index]
    else :
        subjDB.data.field('t13_spiral_arm_winding_a0_tight_frac')[index]  = 0.0
        subjDB.data.field('t13_spiral_arm_winding_a1_medium_frac')[index] = 0.0
        subjDB.data.field('t13_spiral_arm_winding_a2_loose_frac')[index]  = 0.0
        
        
        
    if subjDB.data.field('t14_spiral_arm_count_count')[index] > 0 :
        subjDB.data.field('t14_spiral_arm_count_a0_1_frac')[index]         /= subjDB.data.field('t14_spiral_arm_count_count')[index]
        subjDB.data.field('t14_spiral_arm_count_a1_2_frac')[index]         /= subjDB.data.field('t14_spiral_arm_count_count')[index]
        subjDB.data.field('t14_spiral_arm_count_a2_3_frac')[index]         /= subjDB.data.field('t14_spiral_arm_count_count')[index]
        subjDB.data.field('t14_spiral_arm_count_a3_4_frac')[index]         /= subjDB.data.field('t14_spiral_arm_count_count')[index]
        subjDB.data.field('t14_spiral_arm_count_a4_5_plus_frac')[index]    /= subjDB.data.field('t14_spiral_arm_count_count')[index]
        subjDB.data.field('t14_spiral_arm_count_a5_cant_tell_frac')[index] /= subjDB.data.field('t14_spiral_arm_count_count')[index]
    else :
        subjDB.data.field('t14_spiral_arm_count_a0_1_frac')[index]         = 0.0
        subjDB.data.field('t14_spiral_arm_count_a1_2_frac')[index]         = 0.0
        subjDB.data.field('t14_spiral_arm_count_a2_3_frac')[index]         = 0.0
        subjDB.data.field('t14_spiral_arm_count_a3_4_frac')[index]         = 0.0
        subjDB.data.field('t14_spiral_arm_count_a4_5_plus_frac')[index]    = 0.0
        subjDB.data.field('t14_spiral_arm_count_a5_cant_tell_frac')[index] = 0.0
        
        
        
    if subjDB.data.field('t15_bulge_prominence_count')[index] > 0 :
        subjDB.data.field('t15_bulge_prominence_a0_no_bulge_frac')[index] /= subjDB.data.field('t15_bulge_prominence_count')[index]
        subjDB.data.field('t15_bulge_prominence_a1_obvious_frac')[index]  /= subjDB.data.field('t15_bulge_prominence_count')[index]
        subjDB.data.field('t15_bulge_prominence_a2_dominant_frac')[index] /= subjDB.data.field('t15_bulge_prominence_count')[index]
    else :
        subjDB.data.field('t15_bulge_prominence_a0_no_bulge_frac')[index] = 0.0
        subjDB.data.field('t15_bulge_prominence_a1_obvious_frac')[index]  = 0.0
        subjDB.data.field('t15_bulge_prominence_a2_dominant_frac')[index] = 0.0
        
        
        
    if subjDB.data.field('t16_merging_tidal_debris_count')[index] > 0 :
        subjDB.data.field('t16_merging_tidal_debris_a0_merging_frac')[index]      /= subjDB.data.field('t16_merging_tidal_debris_count')[index]
        subjDB.data.field('t16_merging_tidal_debris_a1_tidal_debris_frac')[index] /= subjDB.data.field('t16_merging_tidal_debris_count')[index]
        subjDB.data.field('t16_merging_tidal_debris_a2_both_frac')[index]         /= subjDB.data.field('t16_merging_tidal_debris_count')[index]
        subjDB.data.field('t16_merging_tidal_debris_a3_neither_frac')[index]      /= subjDB.data.field('t16_merging_tidal_debris_count')[index]
    else :
        subjDB.data.field('t16_merging_tidal_debris_a0_merging_frac')[index]      = 0.0
        subjDB.data.field('t16_merging_tidal_debris_a1_tidal_debris_frac')[index] = 0.0
        subjDB.data.field('t16_merging_tidal_debris_a2_both_frac')[index]         = 0.0
        subjDB.data.field('t16_merging_tidal_debris_a3_neither_frac')[index]      = 0.0


print '...Done.'


subjDB.writeto('../classifications/candels_classifications_collated.fits')





