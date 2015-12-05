# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 15:14:01 2015

@author: Miller
"""

from pandas import *
import numpy

def imputation(filename):
    # Pandas dataframes have a method called 'fillna(value)', such that you can
    # pass in a single value to replace any NAs in a dataframe or series. You
    # can call it like this: 
    #     dataframe['column'] = dataframe['column'].fillna(value)
    #
    # Using the numpy.mean function, which calculates the mean of a numpy
    # array, impute any missing values in our Lahman baseball
    # data sets 'weight' column by setting them equal to the average weight.
    # 
    # You can access the 'weight' colum in the baseball data frame by
    # calling baseball['weight']

    baseball = pandas.read_csv(filename)
    baseball['weight'] = baseball['weight'].fillna(numpy.mean(baseball['weight']))
    return baseball
    
    
df = imputation("/Users/Miller/GitHub/NanoDegree/Class_Intro_to_DataScience/Lesson2_DataWrangling/lahman_baseball/Master.csv")