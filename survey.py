# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 01:22:19 2019

@author: black
"""

import pandas as pd

questions = pd.read_csv(r'kaggle-survey-2019/questions_only.csv')
schema = pd.read_csv(r'kaggle-survey-2019/survey_schema.csv')
mpresponce = pd.read_csv(r'kaggle-survey-2019/multiple_choice_responses.csv')
txtresponce = pd.read_csv(r'kaggle-survey-2019/other_text_responses.csv')

SUBSET = list(mpresponce.columns.to_series().str.contains('OTHER_TEXT'))
DF = mpresponce.loc[:,SUBSET]; mpresponce = mpresponce.drop(columns=DF)

rows = mpresponce.iloc[0]
mpresponce.columns = rows
mpresponce = mpresponce.iloc[1:]; rows = rows.iloc[1:]
mpresponce = mpresponce.iloc[:, 1:]

names = ['Age', 'Gender', 'Country', 'Education', 'Job_title', 'Employer_Size',
         'DS_Employees', 'Employer_uses_ML', ]

for orig, new in zip(list(rows)[0:len(names)], names):
    #print(orig, new)
    mpresponce.rename(columns={orig: new},inplace=True)
    
#print(list(mpresponce.columns.values))

subsets = list(mpresponce.columns.to_series().str.contains('Select all that apply'))
DF = mpresponce.loc[:, subsets]

#Testing whether regex to get rid of extra descriptions
ls = list(DF.columns[0:15])
import re
pattern = r'.+-\s\w+\s\w+\s-\s'  #this keeps the CHOICE, not the Question.
ls0 = ls[0]                          #More conventient to get rid of the last part
print(re.sub(pattern, '', ls0))     #ie keep the reverse of what I keep now

pattern = r':'  #to just get the question
print(re.split(pattern, ls0)[0])