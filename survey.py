# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 01:22:19 2019

@author: black

GUIDE:
1. parts is my main file, with easy-to-work with data
2. mpresponce is my additional data file, which has been extensively worked 
to make more sense to work with, especially indexing. I ignored text answers
3.answers are the answers of 2. , but clearly depicted for easier merging

Plan: 
EDA parts on its own, then merge selectively with mpresponce with help from answers    

"""

import pandas as pd

questions = pd.read_csv(r'kaggle-survey-2019/questions_only.csv')
schema = pd.read_csv(r'kaggle-survey-2019/survey_schema.csv')
mpresponce = pd.read_csv(r'kaggle-survey-2019/multiple_choice_responses.csv')
txtresponce = pd.read_csv(r'kaggle-survey-2019/other_text_responses.csv')
mporig = mpresponce
#QS = mporig.columns

SUBSET = list(mpresponce.columns.to_series().str.contains('OTHER_TEXT'))
DF = mpresponce.loc[:,SUBSET]
mpresponce = mpresponce.drop(columns=DF)
rows = mpresponce.iloc[0]

#Can actually do quite some analysis using parts itself as well
qs = mpresponce.columns[1:]
qs = list(mporig.columns.to_series().str.contains('_Part_'))
parts = mporig.loc[:, list(~pd.Series(qs))]
parts.drop(list(parts.filter(regex = 'OTHER_TEXT')), axis = 1, inplace = True)
COLS = parts.iloc[0,:]; COLS = COLS[1:]
mpresponce.columns = rows
mpresponce = mpresponce.iloc[1:]; rows = rows.iloc[1:]
mpresponce = mpresponce.iloc[:, 1:]

names = ['Age', 'Gender', 'Country', 'Education', 'Job_title', 'Employer_Size',
         'DS_Employees', 'Employer_uses_ML', 
         'annual_salary', 'money_spent_ML', 'tools_ML', 'yrs_experience_coding',
         'recommended_language', 'used_TPU', 'yrs_using_ML']
parts.columns = parts.iloc[0,:]
parts = parts.iloc[1:,:]
parts = parts.iloc[:, 1:]
parts.columns = names
mpresponce.drop(columns=COLS, inplace=True)  #can do analysis from that line on

colnums = list(range(32,37)) #found via manual search
mpresponce.drop(mpresponce.columns[colnums], axis=1, inplace=True)
import re 
pattern = r'Choice\s-\s'
lsc =[]
mpresponce_cols = mpresponce.columns
for col in mpresponce_cols:
    lsc.append(re.split(pattern, col)[1])  #lsc=>Answers
lsc = [word.strip() for word in lsc]
mpresponce.columns = lsc    
#TO D0: CREATE MAPPING OF QUESTIONS - ANSWERS USING LSC for indexing on  parts
inds = []                       
for i,j in enumerate(lsc):
    if j =='Other':
        print(i)
        inds.append(i+1)  #finding cutoffs between categories via Other
question_categories = ['main_job_roles', 
                       'media_sources_DS',
                       'course_platforms', 
                       'IDE',
                       'hosted_notebooks', 
                       'language_used',
                       'visualization_libraries',
                       'specialized_hardware',
                       'ML_algos_used',
                       'ML_tools_used',
                       'CV_methods',
                       'NLP_methods',
                       'ML_frameworks',
                       'cloud_computing_platforms',
                       'cloud_computing_products',                                              
                       'big_data_tools_used',
                       'ML_products',
                       'auto_ML_tools',
                       'relational_databases'
                       ]  
answers = []
for i in range(1,len(inds)):
    if i ==1:
        print(lsc[0:inds[i-1]])
        print('*'*10)
        answers.append(lsc[0:inds[i-1]])
    print(lsc[inds[i-1]:inds[i]])   #have answers here, just need to group by qs
    print('*'*10)
    answers.append(lsc[inds[i-1]:inds[i]])
answers = pd.DataFrame.from_records(answers).T #ANSWERS!! Added the columns for clarity
answers.columns = question_categories

#EDA: Easy columns
import matplotlib.pyplot as plt
import seaborn


