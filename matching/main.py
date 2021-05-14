from matching.constants import *
from matching.mentor import *
from matching.mentee import *
from matching.stable_match import *
from sklearn.metrics.pairwise import euclidean_distances
from matching.export import *
import numpy as np
import pandas as pd

def matching_algorithm(mentors_array, mentees_array):
    processed_mentors = preprocess_mentors(mentors_array)

    familyToMentors, mentor_tables = cluster_mentors(processed_mentors)

    num_mentors_in_category=dict()
    for category in mentor_tables.keys():
        num_mentors_in_category[category]=mentor_tables[category].shape[0]
    
    processed_mentees = preprocess_mentee_responses(mentees_array)

    mentorEmailToMenteesEmails = defaultdict(list)

    for category in mentor_tables.keys():
        p = 1
        num_match_mentors=int(p * num_mentors_in_category[category])
        if(num_mentors_in_category[category] > 0):
            familyToMentees, menteeClusterData=cluster_mentees(processed_mentees[category], num_match_mentors)
        
            mentorNums = mentor_tables[category][mentorMatchCols].to_numpy()
            mentorNums = mentorNums[:num_match_mentors]
  
            #repMentees is a matrix of representative mentees for each mentee cluster to be KMeansed with mentors
            representativeMentees = []

            for key in range (0, len(menteeClusterData)):
                representative = np.zeros(len(menteeMatchCols))
                for mentee in menteeClusterData[key]:
                    representative = representative + mentee[menteeMatchCols]
                representative /= len(menteeClusterData[key])
                representativeMentees.append(representative)
            representativeMentees = np.array(representativeMentees)

            mentorToPref = dict()
            menteeToPref = dict()

            mentorPrefs = euclidean_distances(mentorNums, representativeMentees)
            menteePrefs = euclidean_distances(representativeMentees, mentorNums)

            # Create the mentor preferences matrix by sorting each row of the pairwise distance matrix
            # Create the mentee preferences matrix in a similar fashion

            for i,mentor in enumerate(mentorPrefs):
                mentorPrefs[i]=sorted(range(mentorPrefs.shape[1]), key=lambda x: mentor[x])
            for i,mentee in enumerate(menteePrefs):
                menteePrefs[i]=sorted(range(menteePrefs.shape[1]), key=lambda x: mentee[x])

            mentorPrefs=np.array(mentorPrefs).astype(int)
            menteePrefs=np.array(menteePrefs).astype(int)

            stableMatchResult = stable_match(num_match_mentors, mentorPrefs, menteePrefs)

            print(stableMatchResult)

            for i in range(0, len(stableMatchResult)):
                menteeEmails = familyToMentees[i]
                mentor = mentor_tables[category].iloc[stableMatchResult[i]]['email']
                mentorEmailToMenteesEmails[mentor] = menteeEmails
    
    return familyToMentors, mentorEmailToMenteesEmails 
