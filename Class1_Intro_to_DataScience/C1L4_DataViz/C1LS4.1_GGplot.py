# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 14:52:48 2015

@author: Miller
"""

from pandas import *
from ggplot import *

import pandas

def lineplot(hr_year_csv):
    # A csv file will be passed in as an argument which
    # contains two columns -- 'HR' (the number of homerun hits)
    # and 'yearID' (the year in which the homeruns were hit).
    #
    # Fill out the body of this function, lineplot, to use the
    # passed-in csv file, hr_year.csv, and create a
    # chart with points connected by lines, both colored 'red',
    # showing the number of HR by year.
    #
    # You will want to first load the csv file into a pandas dataframe
    # and use the pandas dataframe along with ggplot to create your visualization
    #
    # You can check out the data in the csv file at the link below:
    # https://www.dropbox.com/s/awgdal71hc1u06d/hr_year.csv
    #
    # You can read more about ggplot at the following link:
    # https://github.com/yhat/ggplot/
    
    
    gg = ggplot(hr_year_csv,aes('yearID','HR')) + \
    geom_point(color='red') + \
    geom_line(color='red') + \
    xlab('Year') + ylab('Home Runs') + ggtitle('Total HRs by Year')
    
    return gg

hr_year_csv = pandas.read_csv('/Users/Miller/GitHub/GhNanoDegree/Class_Intro_to_DataScience/Lesson4_DataViz/hr_year.csv')
print lineplot(hr_year_csv)