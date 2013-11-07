import sys
import numpy as np
try:
    from astropy.io import fits as pyfits
except ImportError:
    import pyfits

path_class = 'classifications'

# This is the fits file that maps all the IDs to one another:
#
try:
    sys.argv[1]
except NameError,IndexError:
    subjinfo_file = '%s/candels_classifications_collated.fits' % path_class
else:
    subjinfo_file = sys.argv[1]

print 'Reading %s ...' % subjinfo_file
q = pyfits.open(subjinfo_file, memmap=True)
subjDB = q[1]

# normal IDs are survey and number, e.g. 'GDS_12345'. 
# examples where a second image of the same galaxy was inserted are e.g. 'GDS_12345_2'.
# So as a shortcut, anything with two underscore characters is a duplicate.
# Beware breaking this in later versions of the database.
second_set    = (subjDB.data.field('hubble_id_img').count('_') > 1)
no_duplicates = (subjDB.data.field('hubble_id_img').count('_') == 1)

print 'Cleaning up %5i duplicates ...' % sum(second_set)
print '     %5s %20s %20s %8s %8s %3s %3s ' % ('#', 'idstr', 'dupstr', 'index_orig', 'index_dup', 'N_orig', 'N_dup')

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


    if (k % 100 == 0) :
        print 'Done %5i %20s %20s %8i %8i %3i %3i ' % (k, idstr, dupstr, index_orig, index, subjDB.data.field('num_classifications')[index_orig], subjDB.data.field('num_classifications')[index])
   
print '...Done.'

qq = subjDB.data[no_duplicates]
subjDB_nodup = pyfits.BinTableHDU(qq)
subjDB_nodup.writeto('%s/candels_classifications_collated_noduplicates.fits' % path_class, clobber=True)

