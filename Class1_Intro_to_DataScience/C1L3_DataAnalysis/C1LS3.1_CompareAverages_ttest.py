# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 08:20:52 2015

@author: Miller
"""

import numpy
import scipy.stats
import pandas

def compare_averages(filename):
    """
    Performs a t-test on two sets of baseball data (left-handed and right-handed hitters).

    You will be given a csv file that has three columns.  A player's
    name, handedness (L for lefthanded or R for righthanded) and their
    career batting average (called 'avg'). You can look at the csv
    file by downloading the baseball_stats file from Downloadables below. 
    
    Write a function that will read that the csv file into a pandas data frame,
    and run Welch's t-test on the two cohorts defined by handedness.
    
    One cohort should be a data frame of right-handed batters. And the other
    cohort should be a data frame of left-handed batters.
    
    We have included the scipy.stats library to help you write
    or implement Welch's t-test:
    http://docs.scipy.org/doc/scipy/reference/stats.html
    
    With a significance level of 95%, if there is no difference
    between the two cohorts, return a tuple consisting of
    True, and then the tuple returned by scipy.stats.ttest.  
    
    If there is a difference, return a tuple consisting of
    False, and then the tuple returned by scipy.stats.ttest.
    
    For example, the tuple that you return may look like:
    (True, (9.93570222, 0.000023))
    """
    # Read data into DF
    df = pandas.read_csv(filename)
    # Separate the data into cohorts defined by handedness (right and left)
    cohort_left = df[df['handedness'] == 'L']
    cohort2_right = df[df['handedness'] == 'R']
    # Perform Welch's T-Test
    result = scipy.stats.ttest_ind(cohort_left['avg'],cohort2_right['avg'],equal_var=False)
    (tstat,pvalue) = result
    # Produce desired result:
    if pvalue > .05:
        return (True,result)
    else: 
        return (False,result)

print compare_averages("/Users/Miller/GitHub/NanoDegree/Class_Intro_to_DataScience/Lesson3_DataAnalysis/BattingAverage.txt")

# Good job! Your calculations are correct.
# Your calculated t-statistic is 9.93570222624
# The correct t-statistic is +/-9.93570222624
# Performing the t-test to determine, with a 95% confidence, whether the avg batting average of the two cohorts are different. In other words, do left handers have a statistically signficant different avg batting avg than right handers. 
