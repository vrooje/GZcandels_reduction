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

import get_question_answer_mapping

def collate_classifications(classifications_filename, which_survey, output_consensus_filename):

    # output_consensus_filename can be either .fits or .csv -- it will write both but just input one.
    # also you can just omit the suffix and it will still do both.
    
    if output_consensus_filename.endswith('.csv') or output_consensus_filename.endswith('.fits'):
        if output_consensus_filename.endswith('.csv'):
            output_consensus_csv = output_consensus_filename
            output_consensus_fits = output.consensus_filename.replace('.csv','.fits')
        else:
            output_consensus_fits = output_consensus_filename
            output_consensus_csv = output.consensus_filename.replace('.fits','.csv')
    else:
        output_consensus_csv = output_consensus_filename+'.csv'
        output_consensus_fits = output_consensus_filename+'.fits'
        
        

    # This is the fits file that maps all the IDs to one another:
    #
    print ''
    print 'Reading %s ...' % classifications_filename
    #data = ascii.read(ferengi_filename, 'b')  
    #subjects = set(data['subject_id'])
    
    # using pandas is faster even without low-memory shortcut
    classifications_in = pd.read_csv(classifications_filename,low_memory=False)
    classifications = classifications_in.set_index('id')
    subjects = classifications.subject_id.unique()

    
    # Now set up the collated classification columns. 
    # Each question has a question number from e.g. ferengi-0 to ferengi-18
    # Each of those questions has some number of possible answers a-0, a-1, etc. 
    #   Depending on the survey:
    #   One question = odd features (18) may have click boxes where multiple answers can be selected.
    #   This question alone needs to be treated differently than the others.
    # In GZ2/GZH the answer numbers were themselves unique but in Ouroboros they start at a-0 for each question number.
    #
    
    q_a_map = get_question_answer_mapping(which_survey)
    weird_question = get_weird_question(which_survey)

    
    print 'Creating columns for vote fractions...'
    
    # Create column of integer zeros and float zeros
    intcolumn = np.zeros(len(subjects),dtype=int)
    floatcolumn = np.zeros(len(subjects),dtype=float)
    strcolumn = np.array(['                        ']*len(subjects),dtype='S24')
    


    # I'm just going to leave this for the moment -- there has to be a way to generalize this for pyfits.
    # Note I'd also like to save it as a csv, so in a dataframe.

    c01 = Column(name='num_classifications', format='J', array=intcolumn)
                           
    c02 = Column(name='t00_smooth_or_featured_a0_smooth_frac', format='D', array=floatcolumn)
    c03 = Column(name='t00_smooth_or_featured_a1_features_frac', format='D', array=floatcolumn)
    c04 = Column(name='t00_smooth_or_featured_a2_artifact_frac', format='D', array=floatcolumn)
    c05 = Column(name='t00_smooth_or_featured_count', format='J', array=intcolumn)
    
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

    subjDB = pyfits.new_table(classifications.columns)
    questions = [which_survey+'-%i' % j for j in np.arange(len(q_a_map))]
    if (len(weird_question) > 0):
        questions.remove(weird_question)
    
    print 'Counting classifications...'
    print 'new'
    
    
    
    for q in questions:
    
        print q, datetime.datetime.now().strftime('%H:%M:%S.%f')
        
        # groups all answers to question q by subject id and counts instances of each non-blank answer separately
        # ON ONE LINE and 12x speed of previous method = WIN
        # alas it only works if all the weights are 1. #fail #mostlymyfailingpythonskillz
        #this_question = classifications[q].groupby(classifications.subject_id).apply(lambda x:x.value_counts())

        # the double-indexing thing is not working for me so I'm shortcutting it by making a new index column
        # that is the combination of the subject id and each answer choice.
        classifications['subject_ans'] = classifications['subject_id']+'___'+q
        # then we can sort on that and do a sum.
        this_question = classifications['weight'].groupby(classifications.subject_ans).apply(lambda x:sum(x))
        
        # now we need to assign values
                
        # counts total answers to all non-blank for this question (per subject id)
        N_answer_total = this_question.sum(level=0)
    
        # for some reason about 1/4 of the objects weren't actually classified
        # and those will give a key error, so ignore them (but count them)
        errors=0
        for idx, s in enumerate(subjects):
        
            # assign subject id
            if q == which_survey+'-0':
                subjDB.data.field('subject_id')[idx] = s

            #one_subj=ww.index.map(lambda x:x.startswith('504e340fc499611ea6000001'))
            # get just the answers for this subject - the index is subjectid___answer as a string
            this_q_this_subject = this_question.index.map(lambda x:x.startswith(s))
            
            # total weighted number of all answers given for this question
            N_answer_total = sum(this_q_this_subject)
        
                
            # assign total number count for this question
            try:
                subjDB.data.field(q_a_map[q]['count'])[idx] = N_answer_total
            except KeyError:
                errors+=1
                pass
            
            answers = ['a-%i' % j for j in np.arange(len(q_a_map[q]))]
            
            # assign vote fractions
            for a in answers:
                this_q_a_this_subject = this_question.index.map(lambda x:x.startswith(s) and x.endswith(a))
                try:
                    subjDB.data.field(q_a_map[q][a])[idx] = float(this_q_a_this_subject)/float(N_answer_total) if N_answer_total > 0 else 0.
                except KeyError:
                    pass
                
                
                
                
    # now do the weird question(s), if they exist -- NOTE this does not do the weighting correctly at the moment
    if len(weird_question) > 0:
        print weird_question, datetime.datetime.now().strftime('%H:%M:%S.%f')
        
        this_question = classifications[weird_question].groupby(classifications.subject_id).apply(lambda x:x.value_counts())
        
        # here's why this question is weird: users can click on more than one option, 
        # and answers are stored as unique combinations of answer choices. e.g.:
        #In [219]: this_question
        #Out[219]: 
        #subject_id                                               
        #5249ce0c3ae74072a30033c1  a-0;x-3                            2
        #5249ce0c3ae74072a30033c2  a-0;x-0                            1
        #                          a-0                                1
        #                          a-0;x-0;x-1;x-2;x-3;x-4;x-5;x-6    1
        #5249ce0c3ae74072a30033c3  a-0                                3
        #                          a-0;x-2;x-4;x-6                    1
        #                          a-0;x-3                            1
        #                          a-0;x-4                            1
        #
        # So we have to parse each answer combination for each subject separately.
    
        for idx, s in enumerate(subjects):
            try:
                n_answers = this_question.sum(level=0)[s]
    
                answer_combos = this_question[s].index
                # e.g. second subject above:
                #In [230]: this_question['5249ce0c3ae74072a30033c2'].index
                #Out[230]: Index([u'a-0;x-0', u'a-0', u'a-0;x-0;x-1;x-2;x-3;x-4;x-5;x-6'], dtype='object')
                #
                # Now loop through these answers
                n_combos = answer_combos.size
                
                for i_combo in range(0, n_combos):
                    #unpack separate answers for this index
                    these_answers = answer_combos[i_combo].split(';')
                    for this_ans in these_answers:
                        #need to add the number of votes for the answer within this combination to the total
                        #count, not frac (yet)
                        
                        # note there is an a-0, which is clicking the "next" button, and sometimes people do
                        # get to "odd" and then not click anything but "next", but as you *must* click next
                        # to advance, the fraction of people answering a-0 should always be 1.0, so we're skipping a-0
                        # (it's not included in subjDB so it will throw an error when looping through keys).
                        try:
                            subjDB.data.field(q_a_map[q][this_ans])[idx] += this_question[s][answer_combos[i_combo]]
                        except KeyError:
                            pass
                        
                answers = ['x-%i' % j for j in np.arange(len(q_a_map[q]))]
                #answers == np.append(aa, 'a-0')
                
                #now loop through answers and calculate fractions (which need not add to 1)
                for a in answers:
                    try:
                        subjDB.data.field(q_a_map[q][a])[idx] = subjDB.data.field(q_a_map[q][a])[idx]/float(n_answers) if n_answers > 0 else 0.
                    except KeyError:
                        pass
                    
            except KeyError:
                pass
    

    print 'Finished looping over classifications', datetime.datetime.now().strftime('%H:%M:%S.%f')
    
    
    
    # Write final data to FITS file
    subjDB.writeto(output_consensus_fits % path_class, clobber=True)
    # and write to CSV file
    consensus_df.to_csv(output_consensus_csv)
    
    
    

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

    collate_classifications(sys.argv[1], sys.argv[2], sys.argv[3])

