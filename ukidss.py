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

def collate_classifications(ukidss_filename):

    # This is the fits file that maps all the IDs to one another:
    #
    print ''
    print 'Reading %s ...' % ukidss_filename
    data = ascii.read(ukidss_filename, 'b')
    
    subjects = set(data['subject_id'])
    
    # Now set up the collated classification columns. 
    # Each question has a question number from ukidss-0 to ukidss-11
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

    c02 = Column(name='t00_smooth_or_features_a0_smooth_frac', format='D', array=floatcolumn)
    c03 = Column(name='t00_smooth_or_features_a1_features_frac', format='D', array=floatcolumn)
    c04 = Column(name='t00_smooth_or_features_a2_artifact_frac', format='D', array=floatcolumn)
    c05 = Column(name='t00_smooth_or_features_count', format='J', array=intcolumn)

    c06 = Column(name='t01_disk_edge_on_a0_yes_frac', format='D', array=floatcolumn)
    c07 = Column(name='t01_disk_edge_on_a1_no_frac', format='D', array=floatcolumn)
    c08 = Column(name='t01_disk_edge_on_count', format='J', array=intcolumn)

    c09 = Column(name='t02_bar_a0_bar_frac', format='D', array=floatcolumn)
    c10 = Column(name='t02_bar_a1_no_bar_frac', format='D', array=floatcolumn)
    c11 = Column(name='t02_bar_count', format='J', array=intcolumn)

    c12 = Column(name='t03_spiral_a0_spiral_frac', format='D', array=floatcolumn)
    c13 = Column(name='t03_spiral_a1_no_spiral_frac', format='D', array=floatcolumn)
    c14 = Column(name='t03_spiral_count', format='J', array=intcolumn)

    c15 = Column(name='t04_bulge_prominence_a0_no_bulge_frac', format='D', array=floatcolumn)
    c16 = Column(name='t04_bulge_prominence_a1_just_noticeable_frac', format='D', array=floatcolumn)
    c17 = Column(name='t04_bulge_prominence_a2_obvious_frac', format='D', array=floatcolumn)
    c18 = Column(name='t04_bulge_prominence_a3_dominant_frac', format='D', array=floatcolumn)
    c19 = Column(name='t04_bulge_prominence_count', format='J', array=intcolumn)

    c20 = Column(name='t05_odd_a0_yes_frac', format='D', array=floatcolumn)
    c21 = Column(name='t05_odd_a1_no_frac', format='D', array=floatcolumn)
    c22 = Column(name='t05_odd_count', format='J', array=intcolumn)

    c23 = Column(name='t06_odd_feature_x0_ring_frac', format='D', array=floatcolumn)
    c24 = Column(name='t06_odd_feature_x1_lens_frac', format='D', array=floatcolumn)
    c25 = Column(name='t06_odd_feature_x2_disturbed_frac', format='D', array=floatcolumn)
    c26 = Column(name='t06_odd_feature_x3_irregular_frac', format='D', array=floatcolumn)
    c27 = Column(name='t06_odd_feature_x4_other_frac', format='D', array=floatcolumn)
    c28 = Column(name='t06_odd_feature_x5_merger_frac', format='D', array=floatcolumn)
    c29 = Column(name='t06_odd_feature_x6_dustlane_frac', format='D', array=floatcolumn)
    c30 = Column(name='t06_odd_feature_a0_discuss_frac', format='D', array=floatcolumn)
    c31 = Column(name='t06_odd_feature_count', format='J', array=intcolumn)

    c32 = Column(name='t07_rounded_a0_completely_round_frac', format='D', array=floatcolumn)
    c33 = Column(name='t07_rounded_a1_in_between_frac', format='D', array=floatcolumn)
    c34 = Column(name='t07_rounded_a2_cigar_shaped_frac', format='D', array=floatcolumn)
    c35 = Column(name='t07_rounded_count', format='J', array=intcolumn)

    c36 = Column(name='t08_bulge_shape_a0_rounded_frac', format='D', array=floatcolumn)
    c37 = Column(name='t08_bulge_shape_a1_boxy_frac', format='D', array=floatcolumn)
    c38 = Column(name='t08_bulge_shape_a2_no_bulge_frac', format='D', array=floatcolumn)
    c39 = Column(name='t08_bulge_shape_count', format='J', array=intcolumn)

    c40 = Column(name='t09_arms_winding_a0_tight_frac', format='D', array=floatcolumn)
    c41 = Column(name='t09_arms_winding_a1_medium_frac', format='D', array=floatcolumn)
    c42 = Column(name='t09_arms_winding_a2_loose_frac', format='D', array=floatcolumn)
    c43 = Column(name='t09_arms_winding_count', format='J', array=intcolumn)

    c44 = Column(name='t10_arms_number_a0_1_frac', format='D', array=floatcolumn)
    c45 = Column(name='t10_arms_number_a1_2_frac', format='D', array=floatcolumn)
    c46 = Column(name='t10_arms_number_a2_3_frac', format='D', array=floatcolumn)
    c47 = Column(name='t10_arms_number_a3_4_frac', format='D', array=floatcolumn)
    c48 = Column(name='t10_arms_number_a4_more_than_4_frac', format='D', array=floatcolumn)
    c49 = Column(name='t10_arms_number_a5_cant_tell_frac', format='D', array=floatcolumn)
    c50 = Column(name='t10_arms_number_count', format='J', array=intcolumn)

    c51 = Column(name='t11_discuss_a0_yes_frac', format='D', array=floatcolumn)
    c52 = Column(name='t11_discuss_a1_no_frac', format='D', array=floatcolumn)
    c53 = Column(name='t11_discuss_count', format='J', array=intcolumn)
    
    frac_dict = {
        'ukidss-0':{
            'a-0':'t00_smooth_or_features_a0_smooth_frac',
            'a-1':'t00_smooth_or_features_a1_features_frac',
            'a-2':'t00_smooth_or_features_a2_artifact_frac',
            'count':'t00_smooth_or_features_count'
         }
        ,
        'ukidss-1':{
            'a-0':'t01_disk_edge_on_a0_yes_frac',
            'a-1':'t01_disk_edge_on_a1_no_frac',
            'count':'t01_disk_edge_on_count'
        }
        ,
        'ukidss-2':{
            'a-0':'t02_bar_a0_bar_frac',
            'a-1':'t02_bar_a1_no_bar_frac',
            'count':'t02_bar_count'
        }
        ,
        'ukidss-3':{
            'a-0':'t03_spiral_a0_spiral_frac',
            'a-1':'t03_spiral_a1_no_spiral_frac',
            'count':'t03_spiral_count'
        }
        ,
        'ukidss-4':{
            'a-0':'t04_bulge_prominence_a0_no_bulge_frac',
            'a-1':'t04_bulge_prominence_a1_just_noticeable_frac',
            'a-2':'t04_bulge_prominence_a2_obvious_frac',
            'a-3':'t04_bulge_prominence_a3_dominant_frac',
            'count':'t04_bulge_prominence_count'
        }
        ,
        'ukidss-5':{
            'a-0':'t05_odd_a0_yes_frac',
            'a-1':'t05_odd_a1_no_frac',
            'count':'t05_odd_count'
        }
        ,
        'ukidss-6':{
            'x-0':'t06_odd_feature_x0_ring_frac',
            'x-1':'t06_odd_feature_x1_lens_frac',
            'x-2':'t06_odd_feature_x2_disturbed_frac',
            'x-3':'t06_odd_feature_x3_irregular_frac',
            'x-4':'t06_odd_feature_x4_other_frac',
            'x-5':'t06_odd_feature_x5_merger_frac',
            'x-6':'t06_odd_feature_x6_dustlane_frac',
            'x-0':'t06_odd_feature_a0_discuss_frac',
            'count':'t06_odd_feature_count'
        }
        ,
        'ukidss-7':{
            'a-0':'t07_rounded_a0_completely_round_frac',
            'a-1':'t07_rounded_a1_in_between_frac',
            'a-2':'t07_rounded_a2_cigar_shaped_frac',
            'count':'t07_rounded_count'
        }
        ,
        'ukidss-8':{
            'a-0':'t08_bulge_shape_a0_rounded_frac',
            'a-1':'t08_bulge_shape_a1_boxy_frac',
            'a-2':'t08_bulge_shape_a2_no_bulge_frac',
            'count':'t08_bulge_shape_count'
        }
        ,
        'ukidss-9':{
            'a-0':'t09_arms_winding_a0_tight_frac',
            'a-1':'t09_arms_winding_a1_medium_frac',
            'a-2':'t09_arms_winding_a2_loose_frac',
            'count':'t09_arms_winding_count'
        }
        ,
        'ukidss-10':{
            'a-0':'t10_arms_number_a0_1_frac',
            'a-1':'t10_arms_number_a1_2_frac',
            'a-2':'t10_arms_number_a2_3_frac',
            'a-3':'t10_arms_number_a3_4_frac',
            'a-4':'t10_arms_number_a4_more_than_4_frac',
            'a-5':'t10_arms_number_a5_cant_tell_frac',
            'count':'t10_arms_number_count'
        }
        ,
        'ukidss-11':{
            'a-0':'t11_discuss_a0_yes_frac',
            'a-1':'t11_discuss_a1_no_frac',
            'count':'t11_discuss_count'
        }
    }
    
    classifications = pyfits.new_table([c01,c02,c03,c04,c05,c06,c07,c08,c09,c10,c11,c12,c13,c14,c15,c16,c17,c18,c19,c20,c21,c22,c23,c24,c25,c26,c27,c28,c29,c30,c31,c32,c33,c34,c35,c36,c37,c38,c39,c40,c41,c42,c43,c44,c45,c46,c47,c48,c49,c50,c51,c52,c53])

    subjDB = pyfits.new_table(classifications.columns)
    questions = ['ukidss-%i' % j for j in np.arange(len(frac_dict))]
    questions.remove('ukidss-6')
    
    print 'Counting classifications...'
    print 'new'

    for idx,s in enumerate(subjects):

        if idx % 1000 == 0:
            print idx, datetime.datetime.now().strftime('%H:%M:%S.%f')

        # Find each classification for this subject
        this_subj = (data['subject_id'] == s)

        subjDB.data.field('subject_id')[idx] = s
    
        # Loop over each question in the tree and record count, vote fractions
        for q in questions:
            ctr = Counter(data[this_subj][q])
            N_total = np.sum(ctr.values())
            subjDB.data.field(frac_dict[q]['count'])[idx] = N_total
            for key in ctr.keys():
                try:
                    subjDB.data.field(frac_dict[q][key])[idx] = ctr[key]/float(N_total) if N_total > 0 else 0.
                except KeyError:
                    pass

        # Question 6 (odd features) is treated differently, since more than one answer can be selected

        ctr6 = Counter(data[this_subj]['ukidss-6'])
        N_total = np.sum(ctr6.values())
        subjDB.data.field(frac_dict['ukidss-6']['count'])[idx] = N_total
        for key in ctr6.keys():
            strkey = str(key)
            splitkey = strkey.split(';')
            if len(splitkey) > 1:
                for sk in splitkey:
                    try:
                        subjDB.data.field(frac_dict['ukidss-6'][sk])[idx] += ctr6[sk]/float(N_total) if N_total > 0 else 0.
                    except KeyError:
                        pass
            else:
                try:
                    subjDB.data.field(frac_dict['ukidss-6'][key])[idx] = ctr6[key]/float(N_total) if N_total > 0 else 0.
                except KeyError:
                    pass

    print 'Finished looping over classifications'
    
    # Write final data to FITS file
    subjDB.writeto('%s/ukidss_classifications_collated.fits' % path_class, clobber=True)

def get_subject_ids():

    # Connect to Mongo client
    client = MongoClient('localhost', 27017)
    db = client['ouroboros'] 
    
    subjects = db['galaxy_zoo_subjects'] 		# subjects = images
    
    # Retrieve RGZ data, convert into data frames
    batch_subject = subjects.find({"metadata.survey": "ukidss"})
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
    dfs2.to_csv('%s/ukidss_subjectids_sdssids.csv' % path_class)
    
    return None

if __name__ == '__main__':

    collate_ukidss(sys.argv[1])

