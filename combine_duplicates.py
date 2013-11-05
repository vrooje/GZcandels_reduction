import sys
import fileinput
import pyfits
import numpy as np
#import matplotlib.pyplot as plt
from pyfits import Column

# This is the fits file that maps all the IDs to one another:
#
subjinfo_file = '../classifications/candels_classifications_collated.fits'
print 'Reading', subjinfo_file, '...'
q = pyfits.open(subjinfo_file, memmap=True)
subjDB = q[1]
#subjDB = q[1].data
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
# Note: actual column numbers are these plus the total number of columns described above
#       (not that this is necessarily helpful).
#
# c01 = Column(name='num_classifications', format='J', array=intcolumn)
#                        
# c02 = Column(name='t00_smooth_and_rounded_a0_smooth_frac', format='D', array=floatcolumn)
# c03 = Column(name='t00_smooth_and_rounded_a1_features_frac', format='D', array=floatcolumn)
# c04 = Column(name='t00_smooth_and_rounded_a2_artifact_frac', format='D', array=floatcolumn)
# c05 = Column(name='t00_smooth_and_rounded_count', format='J', array=intcolumn)
# 
# c06 = Column(name='t01_how_rounded_a0_completely_frac', format='D', array=floatcolumn)
# c07 = Column(name='t01_how_rounded_a1_inbetween_frac', format='D', array=floatcolumn)
# c08 = Column(name='t01_how_rounded_a2_cigarshaped_frac', format='D', array=floatcolumn)
# c09 = Column(name='t01_how_rounded_count', format='J', array=intcolumn)
# 
# c10 = Column(name='t02_clumpy_appearance_a0_yes_frac', format='D', array=floatcolumn)
# c11 = Column(name='t02_clumpy_appearance_a1_no_frac', format='D', array=floatcolumn)
# c12 = Column(name='t02_clumpy_appearance_count', format='J', array=intcolumn)
# 
# c13 = Column(name='t03_how_many_clumps_a0_1_frac', format='D', array=floatcolumn)
# c14 = Column(name='t03_how_many_clumps_a1_2_frac', format='D', array=floatcolumn)
# c15 = Column(name='t03_how_many_clumps_a2_3_frac', format='D', array=floatcolumn)
# c16 = Column(name='t03_how_many_clumps_a3_4_frac', format='D', array=floatcolumn)
# c17 = Column(name='t03_how_many_clumps_a4_5_plus_frac', format='D', array=floatcolumn)
# c18 = Column(name='t03_how_many_clumps_a5_cant_tell_frac', format='D', array=floatcolumn)
# c19 = Column(name='t03_how_many_clumps_count', format='J', array=intcolumn)
# 
# c20 = Column(name='t04_clump_configuration_a0_straight_line_frac', format='D', array=floatcolumn)
# c21 = Column(name='t04_clump_configuration_a1_chain_frac', format='D', array=floatcolumn)
# c22 = Column(name='t04_clump_configuration_a2_cluster_or_irregular_frac', format='D', array=floatcolumn)
# c23 = Column(name='t04_clump_configuration_a3_spiral_frac', format='D', array=floatcolumn)
# c24 = Column(name='t04_clump_configuration_count', format='J', array=intcolumn)
# 
# c25 = Column(name='t05_is_one_clump_brightest_a0_yes_frac', format='D', array=floatcolumn)
# c26 = Column(name='t05_is_one_clump_brightest_a1_no_frac', format='D', array=floatcolumn)
# c27 = Column(name='t05_is_one_clump_brightest_count', format='J', array=intcolumn)
# 
# c28 = Column(name='t06_brightest_clump_central_a0_yes_frac', format='D', array=floatcolumn)
# c29 = Column(name='t06_brightest_clump_central_a1_no_frac', format='D', array=floatcolumn)
# c30 = Column(name='t06_brightest_clump_central_count', format='J', array=intcolumn)
# 
# c31 = Column(name='t07_galaxy_symmetrical_a0_yes_frac', format='D', array=floatcolumn)
# c32 = Column(name='t07_galaxy_symmetrical_a1_no_frac', format='D', array=floatcolumn)
# c33 = Column(name='t07_galaxy_symmetrical_count', format='J', array=intcolumn)
# 
# c34 = Column(name='t08_clumps_embedded_larger_object_a0_yes_frac', format='D', array=floatcolumn)
# c35 = Column(name='t08_clumps_embedded_larger_object_a1_no_frac', format='D', array=floatcolumn)
# c36 = Column(name='t08_clumps_embedded_larger_object_count', format='J', array=intcolumn)
# 
# c37 = Column(name='t09_disk_edge_on_a0_yes_frac', format='D', array=floatcolumn)
# c38 = Column(name='t09_disk_edge_on_a1_no_frac', format='D', array=floatcolumn)
# c39 = Column(name='t09_disk_edge_on_count', format='J', array=intcolumn)
# 
# c40 = Column(name='t10_edge_on_bulge_a0_yes_frac', format='D', array=floatcolumn)
# c41 = Column(name='t10_edge_on_bulge_a1_no_frac', format='D', array=floatcolumn)
# c42 = Column(name='t10_edge_on_bulge_count', format='J', array=intcolumn)
# 
# c43 = Column(name='t11_bar_feature_a0_yes_frac', format='D', array=floatcolumn)
# c44 = Column(name='t11_bar_feature_a1_no_frac', format='D', array=floatcolumn)
# c45 = Column(name='t11_bar_feature_count', format='J', array=intcolumn)
# 
# c46 = Column(name='t12_spiral_pattern_a0_yes_frac', format='D', array=floatcolumn)
# c47 = Column(name='t12_spiral_pattern_a1_no_frac', format='D', array=floatcolumn)
# c48 = Column(name='t12_spiral_pattern_count', format='J', array=intcolumn)
# 
# c49 = Column(name='t13_spiral_arm_winding_a0_tight_frac', format='D', array=floatcolumn)
# c50 = Column(name='t13_spiral_arm_winding_a1_medium_frac', format='D', array=floatcolumn)
# c51 = Column(name='t13_spiral_arm_winding_a2_loose_frac', format='D', array=floatcolumn)
# c52 = Column(name='t13_spiral_arm_winding_count', format='J', array=intcolumn)
# 
# c53 = Column(name='t14_spiral_arm_count_a0_1_frac', format='D', array=floatcolumn)
# c54 = Column(name='t14_spiral_arm_count_a1_2_frac', format='D', array=floatcolumn)
# c55 = Column(name='t14_spiral_arm_count_a2_3_frac', format='D', array=floatcolumn)
# c56 = Column(name='t14_spiral_arm_count_a3_4_frac', format='D', array=floatcolumn)
# c57 = Column(name='t14_spiral_arm_count_a4_5_plus_frac', format='D', array=floatcolumn)
# c58 = Column(name='t14_spiral_arm_count_a5_cant_tell_frac', format='D', array=floatcolumn)
# c59 = Column(name='t14_spiral_arm_count_count', format='J', array=intcolumn)
# 
# c60 = Column(name='t15_bulge_prominence_a0_no_bulge_frac', format='D', array=floatcolumn)
# c61 = Column(name='t15_bulge_prominence_a1_obvious_frac', format='D', array=floatcolumn)
# c62 = Column(name='t15_bulge_prominence_a2_dominant_frac', format='D', array=floatcolumn)
# c63 = Column(name='t15_bulge_prominence_count', format='J', array=intcolumn)
# 
# c64 = Column(name='t16_merging_tidal_debris_a0_merging_frac', format='D', array=floatcolumn)
# c65 = Column(name='t16_merging_tidal_debris_a1_tidal_debris_frac', format='D', array=floatcolumn)
# c66 = Column(name='t16_merging_tidal_debris_a2_both_frac', format='D', array=floatcolumn)
# c67 = Column(name='t16_merging_tidal_debris_a3_neither_frac', format='D', array=floatcolumn)
# c68 = Column(name='t16_merging_tidal_debris_count', format='J', array=intcolumn)


# normal IDs are survey and number, e.g. 'GDS_12345'. 
# examples where a second image of the same galaxy was inserted are e.g. 'GDS_12345_2'.
# So as a shortcut, anything with two underscore characters is a duplicate.
# Beware breaking this in later versions of the database.
second_set    = (subjDB.data.field('hubble_id_img').count('_') > 1)
no_duplicates = (subjDB.data.field('hubble_id_img').count('_') == 1)

print 'Cleaning up', sum(second_set), 'duplicates ...'

for k, dup_set in enumerate(subjDB.data[second_set]) :
    
    idstr = dup_set.field('hubble_id_base')
    # the original is where the base ID from the duplicate is the same as the img ID. (i.e., no _2 in hubble_id_img)
    #index = subjDB.data.field('hubble_id_img') == idstr
    #idstr = subjDB.data.field('hubble_id_base')[index]
    dupstr = idstr + "_2"
    
    for ii, subj_temp in enumerate(subjDB.data) :
        if subj_temp.field('hubble_id_img') == dupstr :
            index = ii
        if subj_temp.field('hubble_id_img') == idstr :
            index_orig = ii
            
    #print idstr, dupstr, index_orig, index
        
            
    subjDB.data.field('num_classifications')[index_orig] = subjDB.data.field('num_classifications')[index_orig] + subjDB.data.field('num_classifications')[index]
    
    # t00_smooth_and_rounded:
    #    a0_smooth
    #    a1_features
    #    a2_artifact
    #    count
    if subjDB.data.field('t00_smooth_and_rounded_count')[index] > 0 :
        count_dup  = subjDB.data.field('t00_smooth_and_rounded_count')[index]
        count_orig = subjDB.data.field('t00_smooth_and_rounded_count')[index_orig]
        count_tot  = count_dup + count_orig
        subjDB.data.field('t00_smooth_and_rounded_a0_smooth_frac')[index_orig]   = ((count_orig * subjDB.data.field('t00_smooth_and_rounded_a0_smooth_frac')[index_orig]) + (count_dup * subjDB.data.field('t00_smooth_and_rounded_a0_smooth_frac')[index]))/float(count_tot)
        subjDB.data.field('t00_smooth_and_rounded_a1_features_frac')[index_orig] = ((count_orig * subjDB.data.field('t00_smooth_and_rounded_a1_features_frac')[index_orig]) + (count_dup * subjDB.data.field('t00_smooth_and_rounded_a1_features_frac')[index]))/float(count_tot)
        subjDB.data.field('t00_smooth_and_rounded_a2_artifact_frac')[index_orig] = ((count_orig * subjDB.data.field('t00_smooth_and_rounded_a2_artifact_frac')[index_orig]) + (count_dup * subjDB.data.field('t00_smooth_and_rounded_a2_artifact_frac')[index]))/float(count_tot)
        subjDB.data.field('t00_smooth_and_rounded_count')[index_orig] = count_tot
    
    
    
    # t01_how_rounded:
    #    a0_completely
    #    a1_inbetween
    #    a2_cigarshaped
    #    count
    if subjDB.data.field('t01_how_rounded_count')[index] > 0 :
        count_dup  = subjDB.data.field('t01_how_rounded_count')[index]
        count_orig = subjDB.data.field('t01_how_rounded_count')[index_orig]
        count_tot  = count_dup + count_orig
        subjDB.data.field('t01_how_rounded_a0_completely_frac')[index_orig]   = ((count_orig * subjDB.data.field('t01_how_rounded_a0_completely_frac')[index_orig]) + (count_dup * subjDB.data.field('t01_how_rounded_a0_completely_frac')[index]))/float(count_tot)
        subjDB.data.field('t01_how_rounded_a1_inbetween_frac')[index_orig]   = ((count_orig * subjDB.data.field('t01_how_rounded_a1_inbetween_frac')[index_orig]) + (count_dup * subjDB.data.field('t01_how_rounded_a1_inbetween_frac')[index]))/float(count_tot)
        subjDB.data.field('t01_how_rounded_a2_cigarshaped_frac')[index_orig]   = ((count_orig * subjDB.data.field('t01_how_rounded_a2_cigarshaped_frac')[index_orig]) + (count_dup * subjDB.data.field('t01_how_rounded_a2_cigarshaped_frac')[index]))/float(count_tot)
        subjDB.data.field('t01_how_rounded_count')[index_orig] = count_tot
    
    
    
    # t02_clumpy_appearance:
    #    a0_yes
    #    a1_no
    #    count
    if subjDB.data.field('t02_clumpy_appearance_count')[index] > 0 :
        count_dup  = subjDB.data.field('t02_clumpy_appearance_count')[index]
        count_orig = subjDB.data.field('t02_clumpy_appearance_count')[index_orig]
        count_tot  = count_dup + count_orig
        subjDB.data.field('t02_clumpy_appearance_a0_yes_frac')[index_orig]   = ((count_orig * subjDB.data.field('t02_clumpy_appearance_a0_yes_frac')[index_orig]) + (count_dup * subjDB.data.field('t02_clumpy_appearance_a0_yes_frac')[index]))/float(count_tot)
        subjDB.data.field('t02_clumpy_appearance_a1_no_frac')[index_orig]   = ((count_orig * subjDB.data.field('t02_clumpy_appearance_a1_no_frac')[index_orig]) + (count_dup * subjDB.data.field('t02_clumpy_appearance_a1_no_frac')[index]))/float(count_tot)
        subjDB.data.field('t02_clumpy_appearance_count')[index_orig] = count_tot
        
        
        
    # t03_how_many_clumps:
    #    a0_1
    #    a1_2
    #    a2_3
    #    a3_4
    #    a4_5_plus
    #    a5_cant_tell
    #    count
    if subjDB.data.field('t03_how_many_clumps_count')[index] > 0 :
        count_dup  = subjDB.data.field('t03_how_many_clumps_count')[index]
        count_orig = subjDB.data.field('t03_how_many_clumps_count')[index_orig]
        count_tot  = count_dup + count_orig
        subjDB.data.field('t03_how_many_clumps_a0_1_frac')[index_orig]   = ((count_orig * subjDB.data.field('t03_how_many_clumps_a0_1_frac')[index_orig]) + (count_dup * subjDB.data.field('t03_how_many_clumps_a0_1_frac')[index]))/float(count_tot)
        subjDB.data.field('t03_how_many_clumps_a1_2_frac')[index_orig]   = ((count_orig * subjDB.data.field('t03_how_many_clumps_a1_2_frac')[index_orig]) + (count_dup * subjDB.data.field('t03_how_many_clumps_a1_2_frac')[index]))/float(count_tot)
        subjDB.data.field('t03_how_many_clumps_a2_3_frac')[index_orig]   = ((count_orig * subjDB.data.field('t03_how_many_clumps_a2_3_frac')[index_orig]) + (count_dup * subjDB.data.field('t03_how_many_clumps_a2_3_frac')[index]))/float(count_tot)
        subjDB.data.field('t03_how_many_clumps_a3_4_frac')[index_orig]   = ((count_orig * subjDB.data.field('t03_how_many_clumps_a3_4_frac')[index_orig]) + (count_dup * subjDB.data.field('t03_how_many_clumps_a3_4_frac')[index]))/float(count_tot)
        subjDB.data.field('t03_how_many_clumps_a4_5_plus_frac')[index_orig]   = ((count_orig * subjDB.data.field('t03_how_many_clumps_a4_5_plus_frac')[index_orig]) + (count_dup * subjDB.data.field('t03_how_many_clumps_a4_5_plus_frac')[index]))/float(count_tot)
        subjDB.data.field('t03_how_many_clumps_a5_cant_tell_frac')[index_orig]   = ((count_orig * subjDB.data.field('t03_how_many_clumps_a5_cant_tell_frac')[index_orig]) + (count_dup * subjDB.data.field('t03_how_many_clumps_a5_cant_tell_frac')[index]))/float(count_tot)
        subjDB.data.field('t03_how_many_clumps_count')[index_orig] = count_tot
        
        
        
    # t04_clump_configuration:
    #    a0_straight_line
    #    a1_chain
    #    a2_cluster_or_irregular
    #    a3_spiral
    #    count
    if subjDB.data.field('t04_clump_configuration_count')[index] > 0 :
        count_dup  = subjDB.data.field('t04_clump_configuration_count')[index]
        count_orig = subjDB.data.field('t04_clump_configuration_count')[index_orig]
        count_tot  = count_dup + count_orig
        subjDB.data.field('t04_clump_configuration_a0_straight_line_frac')[index_orig]   = ((count_orig * subjDB.data.field('t04_clump_configuration_a0_straight_line_frac')[index_orig]) + (count_dup * subjDB.data.field('t04_clump_configuration_a0_straight_line_frac')[index]))/float(count_tot)
        subjDB.data.field('t04_clump_configuration_a1_chain_frac')[index_orig]   = ((count_orig * subjDB.data.field('t04_clump_configuration_a1_chain_frac')[index_orig]) + (count_dup * subjDB.data.field('t04_clump_configuration_a1_chain_frac')[index]))/float(count_tot)
        subjDB.data.field('t04_clump_configuration_a2_cluster_or_irregular_frac')[index_orig]   = ((count_orig * subjDB.data.field('t04_clump_configuration_a2_cluster_or_irregular_frac')[index_orig]) + (count_dup * subjDB.data.field('t04_clump_configuration_a2_cluster_or_irregular_frac')[index]))/float(count_tot)
        subjDB.data.field('t04_clump_configuration_a3_spiral_frac')[index_orig]   = ((count_orig * subjDB.data.field('t04_clump_configuration_a3_spiral_frac')[index_orig]) + (count_dup * subjDB.data.field('t04_clump_configuration_a3_spiral_frac')[index]))/float(count_tot)
        subjDB.data.field('t04_clump_configuration_count')[index_orig] = count_tot
        
        
        
    # t05_is_one_clump_brightest:
    #    a0_yes
    #    a1_no
    #    count
    if subjDB.data.field('t05_is_one_clump_brightest_count')[index] > 0 :
        count_dup  = subjDB.data.field('t05_is_one_clump_brightest_count')[index]
        count_orig = subjDB.data.field('t05_is_one_clump_brightest_count')[index_orig]
        count_tot  = count_dup + count_orig
        subjDB.data.field('t05_is_one_clump_brightest_a0_yes_frac')[index_orig]   = ((count_orig * subjDB.data.field('t05_is_one_clump_brightest_a0_yes_frac')[index_orig]) + (count_dup * subjDB.data.field('t05_is_one_clump_brightest_a0_yes_frac')[index]))/float(count_tot)
        subjDB.data.field('t05_is_one_clump_brightest_a1_no_frac')[index_orig]   = ((count_orig * subjDB.data.field('t05_is_one_clump_brightest_a1_no_frac')[index_orig]) + (count_dup * subjDB.data.field('t05_is_one_clump_brightest_a1_no_frac')[index]))/float(count_tot)
        subjDB.data.field('t05_is_one_clump_brightest_count')[index_orig] = count_tot

        
        
    # t06_brightest_clump_central:
    #    a0_yes
    #    a1_no
    #    count
    if subjDB.data.field('t06_brightest_clump_central_count')[index] > 0 :
        count_dup  = subjDB.data.field('t06_brightest_clump_central_count')[index]
        count_orig = subjDB.data.field('t06_brightest_clump_central_count')[index_orig]
        count_tot  = count_dup + count_orig
        subjDB.data.field('t06_brightest_clump_central_a0_yes_frac')[index_orig]   = ((count_orig * subjDB.data.field('t06_brightest_clump_central_a0_yes_frac')[index_orig]) + (count_dup * subjDB.data.field('t06_brightest_clump_central_a0_yes_frac')[index]))/float(count_tot)
        subjDB.data.field('t06_brightest_clump_central_a1_no_frac')[index_orig]   = ((count_orig * subjDB.data.field('t06_brightest_clump_central_a1_no_frac')[index_orig]) + (count_dup * subjDB.data.field('t06_brightest_clump_central_a1_no_frac')[index]))/float(count_tot)
        subjDB.data.field('t06_brightest_clump_central_count')[index_orig] = count_tot
        
        
        
    # t07_galaxy_symmetrical:
    #    a0_yes
    #    a1_no
    #    count
    if subjDB.data.field('t07_galaxy_symmetrical_count')[index] > 0 :
        count_dup  = subjDB.data.field('t07_galaxy_symmetrical_count')[index]
        count_orig = subjDB.data.field('t07_galaxy_symmetrical_count')[index_orig]
        count_tot  = count_dup + count_orig
        subjDB.data.field('t07_galaxy_symmetrical_a0_yes_frac')[index_orig]   = ((count_orig * subjDB.data.field('t07_galaxy_symmetrical_a0_yes_frac')[index_orig]) + (count_dup * subjDB.data.field('t07_galaxy_symmetrical_a0_yes_frac')[index]))/float(count_tot)
        subjDB.data.field('t07_galaxy_symmetrical_a1_no_frac')[index_orig]   = ((count_orig * subjDB.data.field('t07_galaxy_symmetrical_a1_no_frac')[index_orig]) + (count_dup * subjDB.data.field('t07_galaxy_symmetrical_a1_no_frac')[index]))/float(count_tot)
        subjDB.data.field('t07_galaxy_symmetrical_count')[index_orig] = count_tot



    # t08_clumps_embedded_larger_object:
    #    a0_yes
    #    a1_no
    #    count
    if subjDB.data.field('t08_clumps_embedded_larger_object_count')[index] > 0 :        
        count_dup  = subjDB.data.field('t08_clumps_embedded_larger_object_count')[index]
        count_orig = subjDB.data.field('t08_clumps_embedded_larger_object_count')[index_orig]
        count_tot  = count_dup + count_orig
        subjDB.data.field('t08_clumps_embedded_larger_object_a0_yes_frac')[index_orig]   = ((count_orig * subjDB.data.field('t08_clumps_embedded_larger_object_a0_yes_frac')[index_orig]) + (count_dup * subjDB.data.field('t08_clumps_embedded_larger_object_a0_yes_frac')[index]))/float(count_tot)
        subjDB.data.field('t08_clumps_embedded_larger_object_a1_no_frac')[index_orig]   = ((count_orig * subjDB.data.field('t08_clumps_embedded_larger_object_a1_no_frac')[index_orig]) + (count_dup * subjDB.data.field('t08_clumps_embedded_larger_object_a1_no_frac')[index]))/float(count_tot)
        subjDB.data.field('t08_clumps_embedded_larger_object_count')[index_orig] = count_tot

       
        
    # t09_disk_edge_on:
    #    a0_yes
    #    a1_no
    #    count
    if subjDB.data.field('t09_disk_edge_on_count')[index] > 0 :
        count_dup  = subjDB.data.field('t09_disk_edge_on_count')[index]
        count_orig = subjDB.data.field('t09_disk_edge_on_count')[index_orig]
        count_tot  = count_dup + count_orig
        subjDB.data.field('t09_disk_edge_on_a0_yes_frac')[index_orig]   = ((count_orig * subjDB.data.field('t09_disk_edge_on_a0_yes_frac')[index_orig]) + (count_dup * subjDB.data.field('t09_disk_edge_on_a0_yes_frac')[index]))/float(count_tot)
        subjDB.data.field('t09_disk_edge_on_a1_no_frac')[index_orig]   = ((count_orig * subjDB.data.field('t09_disk_edge_on_a1_no_frac')[index_orig]) + (count_dup * subjDB.data.field('t09_disk_edge_on_a1_no_frac')[index]))/float(count_tot)
        subjDB.data.field('t09_disk_edge_on_count')[index_orig] = count_tot

        
        
    # t10_edge_on_bulge:
    #    a0_yes
    #    a1_no
    #    count
    if subjDB.data.field('t10_edge_on_bulge_count')[index] > 0 :
        count_dup  = subjDB.data.field('t10_edge_on_bulge_count')[index]
        count_orig = subjDB.data.field('t10_edge_on_bulge_count')[index_orig]
        count_tot  = count_dup + count_orig
        subjDB.data.field('t10_edge_on_bulge_a0_yes_frac')[index_orig]   = ((count_orig * subjDB.data.field('t10_edge_on_bulge_a0_yes_frac')[index_orig]) + (count_dup * subjDB.data.field('t10_edge_on_bulge_a0_yes_frac')[index]))/float(count_tot)
        subjDB.data.field('t10_edge_on_bulge_a1_no_frac')[index_orig]   = ((count_orig * subjDB.data.field('t10_edge_on_bulge_a1_no_frac')[index_orig]) + (count_dup * subjDB.data.field('t10_edge_on_bulge_a1_no_frac')[index]))/float(count_tot)
        subjDB.data.field('t10_edge_on_bulge_count')[index_orig] = count_tot

        
        
    # t11_bar_feature:
    #    a0_yes
    #    a1_no
    #    count    
    if subjDB.data.field('t11_bar_feature_count')[index] > 0 :
        count_dup  = subjDB.data.field('t11_bar_feature_count')[index]
        count_orig = subjDB.data.field('t11_bar_feature_count')[index_orig]
        count_tot  = count_dup + count_orig
        subjDB.data.field('t11_bar_feature_a0_yes_frac')[index_orig]   = ((count_orig * subjDB.data.field('t11_bar_feature_a0_yes_frac')[index_orig]) + (count_dup * subjDB.data.field('t11_bar_feature_a0_yes_frac')[index]))/float(count_tot)
        subjDB.data.field('t11_bar_feature_a1_no_frac')[index_orig]   = ((count_orig * subjDB.data.field('t11_bar_feature_a1_no_frac')[index_orig]) + (count_dup * subjDB.data.field('t11_bar_feature_a1_no_frac')[index]))/float(count_tot)
        subjDB.data.field('t11_bar_feature_count')[index_orig] = count_tot

        
        
    # t12_spiral_pattern:
    #    a0_yes
    #    a1_no
    #    count
    if subjDB.data.field('t12_spiral_pattern_count')[index] > 0 :
        count_dup  = subjDB.data.field('t12_spiral_pattern_count')[index]
        count_orig = subjDB.data.field('t12_spiral_pattern_count')[index_orig]
        count_tot  = count_dup + count_orig
        subjDB.data.field('t12_spiral_pattern_a0_yes_frac')[index_orig]   = ((count_orig * subjDB.data.field('t12_spiral_pattern_a0_yes_frac')[index_orig]) + (count_dup * subjDB.data.field('t12_spiral_pattern_a0_yes_frac')[index]))/float(count_tot)
        subjDB.data.field('t12_spiral_pattern_a1_no_frac')[index_orig]   = ((count_orig * subjDB.data.field('t12_spiral_pattern_a1_no_frac')[index_orig]) + (count_dup * subjDB.data.field('t12_spiral_pattern_a1_no_frac')[index]))/float(count_tot)
        subjDB.data.field('t12_spiral_pattern_count')[index_orig] = count_tot

        
        
    # t13_spiral_arm_winding:
    #    a0_tight
    #    a1_medium
    #    a2_loose
    #    count
    if subjDB.data.field('t13_spiral_arm_winding_count')[index] > 0 :
        count_dup  = subjDB.data.field('t13_spiral_arm_winding_count')[index]
        count_orig = subjDB.data.field('t13_spiral_arm_winding_count')[index_orig]
        count_tot  = count_dup + count_orig
        subjDB.data.field('t13_spiral_arm_winding_a0_tight_frac')[index_orig]   = ((count_orig * subjDB.data.field('t13_spiral_arm_winding_a0_tight_frac')[index_orig]) + (count_dup * subjDB.data.field('t13_spiral_arm_winding_a0_tight_frac')[index]))/float(count_tot)
        subjDB.data.field('t13_spiral_arm_winding_a1_medium_frac')[index_orig]   = ((count_orig * subjDB.data.field('t13_spiral_arm_winding_a1_medium_frac')[index_orig]) + (count_dup * subjDB.data.field('t13_spiral_arm_winding_a1_medium_frac')[index]))/float(count_tot)
        subjDB.data.field('t13_spiral_arm_winding_a2_loose_frac')[index_orig]   = ((count_orig * subjDB.data.field('t13_spiral_arm_winding_a2_loose_frac')[index_orig]) + (count_dup * subjDB.data.field('t13_spiral_arm_winding_a2_loose_frac')[index]))/float(count_tot)
        subjDB.data.field('t13_spiral_arm_winding_count')[index_orig] = count_tot

        
        
    # t14_spiral_arm_count:
    #    a0_1
    #    a1_2
    #    a2_3
    #    a3_4
    #    a4_5
    #    a5_cant_tell
    #    count
    if subjDB.data.field('t14_spiral_arm_count_count')[index] > 0 :
        count_dup  = subjDB.data.field('t14_spiral_arm_count_count')[index]
        count_orig = subjDB.data.field('t14_spiral_arm_count_count')[index_orig]
        count_tot  = count_dup + count_orig
        subjDB.data.field('t14_spiral_arm_count_a0_1_frac')[index_orig]   = ((count_orig * subjDB.data.field('t14_spiral_arm_count_a0_1_frac')[index_orig]) + (count_dup * subjDB.data.field('t14_spiral_arm_count_a0_1_frac')[index]))/float(count_tot)
        subjDB.data.field('t14_spiral_arm_count_a1_2_frac')[index_orig]   = ((count_orig * subjDB.data.field('t14_spiral_arm_count_a1_2_frac')[index_orig]) + (count_dup * subjDB.data.field('t14_spiral_arm_count_a1_2_frac')[index]))/float(count_tot)
        subjDB.data.field('t14_spiral_arm_count_a2_3_frac')[index_orig]   = ((count_orig * subjDB.data.field('t14_spiral_arm_count_a2_3_frac')[index_orig]) + (count_dup * subjDB.data.field('t14_spiral_arm_count_a2_3_frac')[index]))/float(count_tot)
        subjDB.data.field('t14_spiral_arm_count_a3_4_frac')[index_orig]   = ((count_orig * subjDB.data.field('t14_spiral_arm_count_a3_4_frac')[index_orig]) + (count_dup * subjDB.data.field('t14_spiral_arm_count_a3_4_frac')[index]))/float(count_tot)
        subjDB.data.field('t14_spiral_arm_count_a4_5_plus_frac')[index_orig]   = ((count_orig * subjDB.data.field('t14_spiral_arm_count_a4_5_plus_frac')[index_orig]) + (count_dup * subjDB.data.field('t14_spiral_arm_count_a4_5_plus_frac')[index]))/float(count_tot)
        subjDB.data.field('t14_spiral_arm_count_a5_cant_tell_frac')[index_orig]   = ((count_orig * subjDB.data.field('t14_spiral_arm_count_a5_cant_tell_frac')[index_orig]) + (count_dup * subjDB.data.field('t14_spiral_arm_count_a5_cant_tell_frac')[index]))/float(count_tot)
        subjDB.data.field('t14_spiral_arm_count_count')[index_orig] = count_tot

        
        
    # t15_bulge_prominence:
    #    a0_no_bulge
    #    a1_obvious
    #    a2_dominant
    #    count
    if subjDB.data.field('t15_bulge_prominence_count')[index] > 0 :
        count_dup  = subjDB.data.field('t15_bulge_prominence_count')[index]
        count_orig = subjDB.data.field('t15_bulge_prominence_count')[index_orig]
        count_tot  = count_dup + count_orig
        subjDB.data.field('t15_bulge_prominence_a0_no_bulge_frac')[index_orig]   = ((count_orig * subjDB.data.field('t15_bulge_prominence_a0_no_bulge_frac')[index_orig]) + (count_dup * subjDB.data.field('t15_bulge_prominence_a0_no_bulge_frac')[index]))/float(count_tot)
        subjDB.data.field('t15_bulge_prominence_a1_obvious_frac')[index_orig]   = ((count_orig * subjDB.data.field('t15_bulge_prominence_a1_obvious_frac')[index_orig]) + (count_dup * subjDB.data.field('t15_bulge_prominence_a1_obvious_frac')[index]))/float(count_tot)
        subjDB.data.field('t15_bulge_prominence_a2_dominant_frac')[index_orig]   = ((count_orig * subjDB.data.field('t15_bulge_prominence_a2_dominant_frac')[index_orig]) + (count_dup * subjDB.data.field('t15_bulge_prominence_a2_dominant_frac')[index]))/float(count_tot)
        subjDB.data.field('t15_bulge_prominence_count')[index_orig] = count_tot



    # t16_merging_tidal_debris:
    #    a0_merging
    #    a1_tidal_debris
    #    a2_both
    #    a3_neither
    #    count
    if subjDB.data.field('t16_merging_tidal_debris_count')[index] > 0 :
        count_dup  = subjDB.data.field('t16_merging_tidal_debris_count')[index]
        count_orig = subjDB.data.field('t16_merging_tidal_debris_count')[index_orig]
        count_tot  = count_dup + count_orig
        subjDB.data.field('t16_merging_tidal_debris_a0_merging_frac')[index_orig]   = ((count_orig * subjDB.data.field('t16_merging_tidal_debris_a0_merging_frac')[index_orig]) + (count_dup * subjDB.data.field('t16_merging_tidal_debris_a0_merging_frac')[index]))/float(count_tot)
        subjDB.data.field('t16_merging_tidal_debris_a1_tidal_debris_frac')[index_orig]   = ((count_orig * subjDB.data.field('t16_merging_tidal_debris_a1_tidal_debris_frac')[index_orig]) + (count_dup * subjDB.data.field('t16_merging_tidal_debris_a1_tidal_debris_frac')[index]))/float(count_tot)
        subjDB.data.field('t16_merging_tidal_debris_a2_both_frac')[index_orig]   = ((count_orig * subjDB.data.field('t16_merging_tidal_debris_a2_both_frac')[index_orig]) + (count_dup * subjDB.data.field('t16_merging_tidal_debris_a2_both_frac')[index]))/float(count_tot)
        subjDB.data.field('t16_merging_tidal_debris_a3_neither_frac')[index_orig]   = ((count_orig * subjDB.data.field('t16_merging_tidal_debris_a3_neither_frac')[index_orig]) + (count_dup * subjDB.data.field('t16_merging_tidal_debris_a3_neither_frac')[index]))/float(count_tot)
        subjDB.data.field('t16_merging_tidal_debris_count')[index_orig] = count_tot


    if (k % 50 == 0) :
        print 'Done', k, '...'
        print idstr, dupstr, index_orig, index, subjDB.data.field('num_classifications')[index_orig], subjDB.data.field('num_classifications')[index]
   

        



print '...Done.'

qq = subjDB.data[no_duplicates]
subjDB_nodup = pyfits.BinTableHDU(qq)
subjDB_nodup.writeto('../classifications/candels_classifications_collated_noduplicates.fits')





