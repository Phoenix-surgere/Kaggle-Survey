# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 01:22:19 2019

@author: black

GUIDE:
1. 'parts' is my main file, with "easy"-to-work with data - Renamed as 'main' to make more sense in context

2. 'mpresponce' is my additional data file, which has been extensively worked to make more sense to work with, especially indexing. 
I ignored text answers. I consider a bit "harder" to work with, thus extensive preprocessing

3.'answers' are the answers of 2. , but clearly depicted for easier merging

Plan: 
EDA parts on its own, then merge selectively with mpresponce with help from answers    

"""

import pandas as pd

questions = pd.read_csv(r'kaggle-survey-2019/questions_only.csv')
schema = pd.read_csv(r'kaggle-survey-2019/survey_schema.csv')
mpresponce = pd.read_csv(r'kaggle-survey-2019/multiple_choice_responses.csv')
txtresponce = pd.read_csv(r'kaggle-survey-2019/other_text_responses.csv')
mporig = mpresponce

SUBSET = list(mpresponce.columns.to_series().str.contains('OTHER_TEXT'))
DF = mpresponce.loc[:,SUBSET]
mpresponce = mpresponce.drop(columns=DF)
rows = mpresponce.iloc[0]

#Can actually do quite some interesting analysis using parts itself as well
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
mpresponce.drop(columns=COLS, inplace=True)  

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
#TO D0: CREATE MAPPING OF QUESTIONS - ANSWERS USING LSC for indexing on  parts - DONE 
inds = []                       
for i,j in enumerate(lsc):
    if j =='Other':
        print(i)
        inds.append(i+1)  #finding cutoffs between categories via Other
question_categories = ['main_job_roles', 'media_sources_DS', 'course_platforms', 
                       'IDE', 'hosted_notebooks', 'language_used', 'visualization_libraries',
                       'specialized_hardware', 'ML_algos_used','ML_tools_used',
                       'CV_methods','NLP_methods','ML_frameworks','cloud_computing_platforms',
                       'cloud_computing_products',  'big_data_tools_used','ML_products',
                       'auto_ML_tools', 'relational_databases'
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

def countplot(df, column, title):
    sns.countplot(x=df[column],data=df)
    plt.xticks(rotation=45)
    plt.title(title)
    plt.grid(True)
    plt.show()
    

countplot(main,'recommended_language', 'Recommended Languages')
countplot(main,'Gender', 'Gender Distribution')
countplot(main, 'Education', 'Education Attained')
countplot(main, 'Job_title', 'Job Title')

top_countries = (main.Country.value_counts(normalize=True)*100)[0:15]
us = main.loc[(main.Country == 'United States of America')]  
ind = main.loc[(main.Country == 'India')]

def barchart(df, column, title, ncols=None):
    df[column].value_counts()[0:ncols].plot(kind='bar')
    plt.title(title)
    plt.grid(True)
    plt.show()

barchart(us, 'Age','Distribution of Ages - USA')
barchart(ind, 'Age','Distribution of Ages - India')

barchart(us, 'Job_title', 'Distribution of Job titles - USA',6 )
barchart(ind, 'Job_title', 'Distribution of Job titles - India', 6)

barchart(us, 'annual_salary', 'Distribution of Salaries - USA',6 )
barchart(ind, 'annual_salary', 'Distribution of Salaries - India',6 )

def stripcols(col, df=mpresponce, keys=answers):
    stripped = df[list(keys[col].dropna().values)[:-2]]
    aggregated = stripped.apply(pd.Series.count).sort_values(ascending=False)
    return aggregated

def plot_categories(aggregated, title=None, xlabel=None, ylabel=None):
    plt.figure(figsize=(10,6))
    aggregated.sort_values(ascending=False).plot.barh()
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.show()
#1st approach is defining the aggregated matrix explictly, 2nd is to just use a functional approach to save writing.
#platforms = stripcols('course_platforms')
#plot_categories(platforms, title= 'Course Platforms by popularity', 
#                ylabel='Participants')

#plot_categories(stripcols('media_sources_DS'), title='Media Data Science Sources')

#Display all plots with a loop in one go
for column in answers.columns:
    plot_categories(stripcols(column), title=column)

