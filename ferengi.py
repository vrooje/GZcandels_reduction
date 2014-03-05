import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime

from collections import Counter
from pymongo import MongoClient

try:
    from astropy.io import fits as pyfits
    from astropy.io.fits import Column
    from astropy.io import ascii
except ImportError:
    import pyfits
    from pyfits import Column

path_class = './'

def collate_classifications(ferengi_filename):

    # This is the fits file that maps all the IDs to one another:
    #
    print ''
    print 'Reading %s ...' % ferengi_filename
    #data = ascii.read(ferengi_filename, 'b')
    
    #subjects = set(data['subject_id'])
    
    # using pandas is faster
    this_data = pd.read_csv(ferengi_filename,low_memory=False)
    subjects = this_data.subject_id.unique()

    
    # Now set up the collated classification columns. 
    # Each question has a question number from ferengi-0 to ferengi-18
    # Each of those questions has some number of possible answers a-0, a-1, etc. 
    #   One question = odd features (07) has click boxes where multiple answers can be selected.
    #   This question alone needs to be treated differently than the others.
    # In GZ2/GZH the answer numbers were themselves unique but in Ouroboros they start at a-0 for each question number.
    #
    print 'Creating columns for vote fractions...'
    
    # Create column of integer zeros and float zeros
    intcolumn = np.zeros(len(subjects),dtype=int)
    floatcolumn = np.zeros(len(subjects),dtype=float)
    strcolumn = np.array(['                        ']*len(subjects),dtype='S24')
    
    #c01 = Column(name='num_classifications', format='J', array=intcolumn)          # c05 = c01, by definition



    c01 = Column(name='subject_id', format='A24', array=strcolumn)          # c05 = c01, by definition

    c02 = Column(name='t01_smooth_or_features_a01_smooth_frac', format='D', array=floatcolumn)
    c03 = Column(name='t01_smooth_or_features_a02_features_frac', format='D', array=floatcolumn)
    c04 = Column(name='t01_smooth_or_features_a03_artifact_frac', format='D', array=floatcolumn)
    c05 = Column(name='t01_smooth_or_features_count', format='J', array=intcolumn)

    c06 = Column(name='t02_disk_edge_on_a04_yes_frac', format='D', array=floatcolumn)
    c07 = Column(name='t02_disk_edge_on_a05_no_frac', format='D', array=floatcolumn)
    c08 = Column(name='t02_disk_edge_on_count', format='J', array=intcolumn)

    c09 = Column(name='t03_bar_a06_bar_frac', format='D', array=floatcolumn)
    c10 = Column(name='t03_bar_a07_no_bar_frac', format='D', array=floatcolumn)
    c11 = Column(name='t03_bar_count', format='J', array=intcolumn)

    c12 = Column(name='t04_spiral_a08_spiral_frac', format='D', array=floatcolumn)
    c13 = Column(name='t04_spiral_a09_no_spiral_frac', format='D', array=floatcolumn)
    c14 = Column(name='t04_spiral_count', format='J', array=intcolumn)

    c15 = Column(name='t05_bulge_prominence_a10_no_bulge_frac', format='D', array=floatcolumn)
    c16 = Column(name='t05_bulge_prominence_a11_just_noticeable_frac', format='D', array=floatcolumn)
    c17 = Column(name='t05_bulge_prominence_a12_obvious_frac', format='D', array=floatcolumn)
    c18 = Column(name='t05_bulge_prominence_a13_dominant_frac', format='D', array=floatcolumn)
    c19 = Column(name='t05_bulge_prominence_count', format='J', array=intcolumn)

    c20 = Column(name='t06_odd_a14_yes_frac', format='D', array=floatcolumn)
    c21 = Column(name='t06_odd_a15_no_frac', format='D', array=floatcolumn)
    c22 = Column(name='t06_odd_count', format='J', array=intcolumn)

    c23 = Column(name='t07_rounded_a16_completely_round_frac', format='D', array=floatcolumn)
    c24 = Column(name='t07_rounded_a17_in_between_frac', format='D', array=floatcolumn)
    c25 = Column(name='t07_rounded_a18_cigar_shaped_frac', format='D', array=floatcolumn)
    c26 = Column(name='t07_rounded_count', format='J', array=intcolumn)

    c27 = Column(name='t08_odd_feature_a19_ring_frac', format='D', array=floatcolumn)
    c28 = Column(name='t08_odd_feature_a20_lens_frac', format='D', array=floatcolumn)
    c29 = Column(name='t08_odd_feature_a21_disturbed_frac', format='D', array=floatcolumn)
    c30 = Column(name='t08_odd_feature_a22_irregular_frac', format='D', array=floatcolumn)
    c31 = Column(name='t08_odd_feature_a23_other_frac', format='D', array=floatcolumn)
    c32 = Column(name='t08_odd_feature_a24_merger_frac', format='D', array=floatcolumn)
    c33 = Column(name='t08_odd_feature_a38_dustlane_frac', format='D', array=floatcolumn)
    c34 = Column(name='t08_odd_feature_count', format='J', array=intcolumn)

    c35 = Column(name='t09_bulge_shape_a25_rounded_frac', format='D', array=floatcolumn)
    c36 = Column(name='t09_bulge_shape_a26_boxy_frac', format='D', array=floatcolumn)
    c37 = Column(name='t09_bulge_shape_a27_no_bulge_frac', format='D', array=floatcolumn)
    c38 = Column(name='t09_bulge_shape_count', format='J', array=intcolumn)

    c39 = Column(name='t10_arms_winding_a28_tight_frac', format='D', array=floatcolumn)
    c40 = Column(name='t10_arms_winding_a29_medium_frac', format='D', array=floatcolumn)
    c41 = Column(name='t10_arms_winding_a30_loose_frac', format='D', array=floatcolumn)
    c42 = Column(name='t10_arms_winding_count', format='J', array=intcolumn)

    c43 = Column(name='t11_arms_number_a31_1_frac', format='D', array=floatcolumn)
    c44 = Column(name='t11_arms_number_a32_2_frac', format='D', array=floatcolumn)
    c45 = Column(name='t11_arms_number_a33_3_frac', format='D', array=floatcolumn)
    c46 = Column(name='t11_arms_number_a34_4_frac', format='D', array=floatcolumn)
    c47 = Column(name='t11_arms_number_a36_more_than_4_frac', format='D', array=floatcolumn)
    c48 = Column(name='t11_arms_number_a37_cant_tell_frac', format='D', array=floatcolumn)
    c49 = Column(name='t11_arms_number_count', format='J', array=intcolumn)

    c50 = Column(name='t14_clumpy_a39_yes_frac', format='D', array=floatcolumn)
    c51 = Column(name='t14_clumpy_a40_no_frac', format='D', array=floatcolumn)
    c52 = Column(name='t14_clumpy_count', format='J', array=floatcolumn)
    
    c53 = Column(name='t16_bright_clump_a43_yes_frac', format='D', array=floatcolumn)
    c54 = Column(name='t16_bright_clump_a44_no_frac', format='D', array=floatcolumn)
    c55 = Column(name='t16_bright_clump_count', format='J', array=floatcolumn)

    c56 = Column(name='t17_bright_clump_central_a45_yes_frac', format='D', array=floatcolumn)
    c57 = Column(name='t17_bright_clump_central_a46_no_frac', format='D', array=floatcolumn)
    c58 = Column(name='t17_bright_clump_central_count', format='J', array=floatcolumn)

    c59 = Column(name='t18_clumps_arrangement_a47_line_frac', format='D', array=floatcolumn)
    c60 = Column(name='t18_clumps_arrangement_a48_chain_frac', format='D', array=floatcolumn)
    c61 = Column(name='t18_clumps_arrangement_a49_cluster_frac', format='D', array=floatcolumn)
    c62 = Column(name='t18_clumps_arrangement_a59_spiral_frac', format='D', array=floatcolumn)
    c63 = Column(name='t18_clumps_arrangement_count', format='J', array=floatcolumn)

    c64 = Column(name='t19_clumps_count_a50_2_frac', format='D', array=floatcolumn)
    c65 = Column(name='t19_clumps_count_a51_3_frac', format='D', array=floatcolumn)
    c66 = Column(name='t19_clumps_count_a52_4_frac', format='D', array=floatcolumn)
    c67 = Column(name='t19_clumps_count_a53_more_than_4_frac', format='D', array=floatcolumn)
    c68 = Column(name='t19_clumps_count_a54_cant_tell_frac', format='D', array=floatcolumn)
    c69 = Column(name='t19_clumps_count_a60_1_frac', format='D', array=floatcolumn)
    c70 = Column(name='t19_clumps_count_count', format='J', array=floatcolumn)

    c71 = Column(name='t20_clumps_symmetrical_a55_yes_frac', format='D', array=floatcolumn)
    c72 = Column(name='t20_clumps_symmetrical_a56_no_frac', format='D', array=floatcolumn)
    c73 = Column(name='t20_clumps_symmetrical_count', format='J', array=floatcolumn)

    c74 = Column(name='t21_clumps_embedded_a57_yes_frac', format='D', array=floatcolumn)
    c75 = Column(name='t21_clumps_embedded_a58_no_frac', format='D', array=floatcolumn)
    c76 = Column(name='t21_clumps_embedded_count', format='J', array=floatcolumn)
    
    c77 = Column(name='t22_discuss_a61_yes_frac', format='D', array=floatcolumn)
    c78 = Column(name='t22_discuss_a62_no_frac', format='D', array=floatcolumn)
    c79 = Column(name='t22_discuss_count', format='J', array=intcolumn)


    # Note the answer order in the csv is not the same as the task numbers in hubble zoo
    # it's based on https://github.com/zooniverse/Galaxy-Zoo/blob/master/app/lib/ferengi_tree.coffee
    frac_dict = {
        'ferengi-0':{
            'a-0':'t01_smooth_or_features_a01_smooth_frac',
            'a-1':'t01_smooth_or_features_a02_features_frac',
            'a-2':'t01_smooth_or_features_a03_artifact_frac',
            'count':'t01_smooth_or_features_count'
         }
        ,
        'ferengi-9':{
            'a-0':'t02_disk_edge_on_a04_yes_frac',
            'a-1':'t02_disk_edge_on_a05_no_frac',
            'count':'t02_disk_edge_on_count'
        }
        ,
        'ferengi-11':{
            'a-0':'t03_bar_a06_bar_frac',
            'a-1':'t03_bar_a07_no_bar_frac',
            'count':'t03_bar_count'
        }
        ,
        'ferengi-12':{
            'a-0':'t04_spiral_a08_spiral_frac',
            'a-1':'t04_spiral_a09_no_spiral_frac',
            'count':'t04_spiral_count'
        }
        ,
        'ferengi-15':{
            'a-0':'t05_bulge_prominence_a10_no_bulge_frac',
            'a-1':'t05_bulge_prominence_a11_just_noticeable_frac',
            'a-2':'t05_bulge_prominence_a12_obvious_frac',
            'a-3':'t05_bulge_prominence_a13_dominant_frac',
            'count':'t05_bulge_prominence_count'
        }
        ,
        'ferengi-17':{
            'a-0':'t06_odd_a14_yes_frac',
            'a-1':'t06_odd_a15_no_frac',
            'count':'t06_odd_count'
        }
        ,
        'ferengi-1':{
            'a-0':'t07_rounded_a16_completely_round_frac',
            'a-1':'t07_rounded_a17_in_between_frac',
            'a-2':'t07_rounded_a18_cigar_shaped_frac',
            'count':'t07_rounded_count'
        }
        ,
        'ferengi-18':{
            'x-0':'t08_odd_feature_a19_ring_frac',
            'x-1':'t08_odd_feature_a20_lens_frac',
            'x-2':'t08_odd_feature_a21_disturbed_frac',
            'x-3':'t08_odd_feature_a22_irregular_frac',
            'x-4':'t08_odd_feature_a23_other_frac',
            'x-5':'t08_odd_feature_a24_merger_frac',
            'x-6':'t08_odd_feature_a38_dustlane_frac',
            'x-0':'t08_odd_feature_a99_discuss_frac',
            'count':'t08_odd_feature_count'
        }
        ,
        'ferengi-10':{
            'a-0':'t09_bulge_shape_a25_rounded_frac',
            'a-1':'t09_bulge_shape_a26_boxy_frac',
            'a-2':'t09_bulge_shape_a27_no_bulge_frac',
            'count':'t09_bulge_shape_count'
        }
        ,
        'ferengi-13':{
            'a-0':'t10_arms_winding_a28_tight_frac',
            'a-1':'t10_arms_winding_a29_medium_frac',
            'a-2':'t10_arms_winding_a30_loose_frac',
            'count':'t10_arms_winding_count'
        }
        ,
        'ferengi-14':{
            'a-0':'t11_arms_number_a31_1_frac',
            'a-1':'t11_arms_number_a32_2_frac',
            'a-2':'t11_arms_number_a33_3_frac',
            'a-3':'t11_arms_number_a34_4_frac',
            'a-4':'t11_arms_number_a36_more_than_4_frac',
            'a-5':'t11_arms_number_a37_cant_tell_frac',
            'count':'t11_arms_number_count'
        }
        ,
        'ferengi-2':{
            'a-0':'t14_clumpy_a39_yes_frac',
            'a-1':'t14_clumpy_a40_no_frac',
            'count':'t14_clumpy_count'
        }
        ,
        'ferengi-5':{
            'a-0':'t16_bright_clump_a43_yes_frac',
            'a-1':'t16_bright_clump_a44_no_frac',
            'count':'t16_bright_clump_count'
        }
        ,
        'ferengi-6':{
            'a-0':'t17_bright_clump_central_a45_yes_frac',
            'a-1':'t17_bright_clump_central_a46_no_frac',
            'count':'t17_bright_clump_central_count'
        }
        ,
        'ferengi-4':{
            'a-0':'t18_clumps_arrangement_a47_line_frac',
            'a-1':'t18_clumps_arrangement_a48_chain_frac',
            'a-2':'t18_clumps_arrangement_a49_cluster_frac',
            'a-3':'t18_clumps_arrangement_a59_spiral_frac',
            'count':'t18_clumps_arrangement_count'
        }
        ,
        'ferengi-3':{
            'a-0':'t19_clumps_count_a50_2_frac',
            'a-1':'t19_clumps_count_a51_3_frac',
            'a-2':'t19_clumps_count_a52_4_frac',
            'a-3':'t19_clumps_count_a53_more_than_4_frac',
            'a-4':'t19_clumps_count_a54_cant_tell_frac',
            'a-5':'t19_clumps_count_a60_1_frac',
            'count':'t19_clumps_count_count'
        }
        ,
        'ferengi-16':{
            'a-0':'t22_discuss_a61_yes_frac',
            'a-1':'t22_discuss_a62_no_frac',
            'count':'t22_discuss_count'
        }
        ,
        'ferengi-7':{
            'a-0':'t20_clumps_symmetrical_a55_yes_frac',
            'a-1':'t20_clumps_symmetrical_a56_no_frac',
            'count':'t20_clumps_symmetrical_count'
        }
        ,
        'ferengi-8':{
            'a-0':'t21_clumps_embedded_a57_yes_frac',
            'a-1':'t21_clumps_embedded_a58_no_frac',
            'count':'t21_clumps_embedded_count'
        }
        
    }


    #print len(frac_dict['ferengi-3'])




    
    classifications = pyfits.new_table([c01,c02,c03,c04,c05,c06,c07,c08,c09,c10,c11,c12,c13,c14,c15,c16,c17,c18,c19,c20,c21,c22,c23,c24,c25,c26,c27,c28,c29,c30,c31,c32,c33,c34,c35,c36,c37,c38,c39,c40,c41,c42,c43,c44,c45,c46,c47,c48,c49,c50,c51,c52,c53,c54,c55,c56,c57,c58,c59,c60,c61,c62,c63,c64,c65,c66,c67,c68,c69,c70,c71,c72,c73,c74,c75,c76,c77,c78,c79])

    subjDB = pyfits.new_table(classifications.columns)
    questions = ['ferengi-%i' % j for j in np.arange(len(frac_dict))]
    questions.remove('ferengi-18')
    
    print 'Counting classifications...'
    print 'new'
    
    
    
    for q in questions:
    
        print q, datetime.datetime.now().strftime('%H:%M:%S.%f')
    
        # groups all answers to question q by subject id and counts instances of each non-blank answer separately
        # ON ONE LINE = WIN
        this_question = this_data[q].groupby(this_data.subject_id).apply(lambda x:x.value_counts())
        # all of these comments below are because I'm not yet too familiar with pandas
        # example output of this_question.head(10) for ferengi-1:
        # In [59]: this_question.head(10)
        # Out[59]: 
        # subject_id                   
        # 5249ce0c3ae74072a30033c1  a-1    12
        #                           a-0     3
        # 5249ce0c3ae74072a30033c2  a-1    20
        #                           a-0     5
        # 5249ce0c3ae74072a30033c3  a-1    17
        # 5249ce0c3ae74072a30033c4  a-1    14
        #                           a-0     4
        #                           a-2     1
        # 5249ce0c3ae74072a30033c5  a-1    15
        #                           a-0     1
        # dtype: int64
        
        
        # counts total answers to all non-blank for this question (per subject id)
        N_answer_total = this_question.sum(level=0)
        # example output of this_question.head(10).sum(level=0):
        #In [60]: this_question.head(10).sum(level=0)
        #Out[60]: 
        #subject_id
        #5249ce0c3ae74072a30033c1    15
        #5249ce0c3ae74072a30033c2    25
        #5249ce0c3ae74072a30033c3    17
        #5249ce0c3ae74072a30033c4    19
        #5249ce0c3ae74072a30033c5    16
        #dtype: int64
        
        #also note: 
        #In [67]: this_question['5249ce0c3ae74072a30033c1']
        #Out[67]: 
        #a-1    12
        #a-0     3
        #dtype: int64
        #
        #In [68]: this_question['5249ce0c3ae74072a30033c1']['a-1']
        #Out[68]: 12
        #
        #In [77]: this_question.head(10).sum(level=0)['5249ce0c3ae74072a30033c1']
        #Out[77]: 15
    
        errors=0
        for idx, s in enumerate(subjects):
        
            if q == 'ferengi-0':
                subjDB.data.field('subject_id')[idx] = s
                
            
            try:
                subjDB.data.field(frac_dict[q]['count'])[idx] = N_answer_total[s]
            except KeyError:
                errors+=1
                pass
            
            answers = ['a-%i' % j for j in np.arange(len(frac_dict[q]))]
            
            for a in answers:
                try:
                    subjDB.data.field(frac_dict[q][a])[idx] = this_question[s][a]/float(N_answer_total[s]) if N_answer_total[s] > 0 else 0.
                except KeyError:
                    pass
                


#    for idx,s in enumerate(subjects):

        # Question 18 (odd features) is treated differently, since more than one answer can be selected

#         ctr6 = Counter(data[this_subj]['ferengi-18'])
#         N_total = np.sum(ctr6.values())
#         subjDB.data.field(frac_dict['ferengi-18']['count'])[idx] = N_total
#         for key in ctr6.keys():
#             strkey = str(key)
#             splitkey = strkey.split(';')
#             if len(splitkey) > 1:
#                 for sk in splitkey:
#                     try:
#                         subjDB.data.field(frac_dict['ferengi-18'][sk])[idx] += ctr6[sk]/float(N_total) if N_total > 0 else 0.
#                     except KeyError:
#                         pass
#             else:
#                 try:
#                     subjDB.data.field(frac_dict['ferengi-18'][key])[idx] = ctr6[key]/float(N_total) if N_total > 0 else 0.
#                 except KeyError:
#                     pass

    print 'Finished looping over classifications', datetime.datetime.now().strftime('%H:%M:%S.%f')
    
    # Write final data to FITS file
    subjDB.writeto('%s/ferengi_classifications_collated.fits' % path_class, clobber=True)
    
    
    

def get_subject_ids():

    # Connect to Mongo client
    client = MongoClient('localhost', 27017)
    db = client['ouroboros'] 
    
    subjects = db['galaxy_zoo_subjects'] 		# subjects = images
    
    # Retrieve RGZ data, convert into data frames
    batch_subject = subjects.find({"metadata.survey": "ferengi"})
    dfs = pd.DataFrame( list(batch_subject) )

    # Retrieve desired data from the frame
    metadata = dfs['metadata']
    location = dfs['location']
    subject_id = [s for s in dfs['_id']]
    dr7objid = [m['sdss_dr7_id'] for m in metadata]
    dr8objid = [m['sdss_dr8_id'] for m in metadata]
    url_standard = [l['standard'] for l in location]

    # Create a new dataframe with only the columns we want
    dfs2 = pd.DataFrame({'subject_id':subject_id,'dr7objid':dr7objid,'dr8objid':dr8objid,'url_standard':url_standard})

    # Write to CSV file to be matched in TOPCAT
    dfs2.to_csv('%s/ferengi_subjectids_sdssids.csv' % path_class)
    
    return None

if __name__ == '__main__':

    collate_classifications(sys.argv[1])

