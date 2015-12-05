# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 17:13:47 2015

@author: Miller
"""


import pandas

from ggplot import *


def lineplot_compare(hr_by_team_year_sf_la_csv):
    # Write a function, lineplot_compare, that will read a csv file
    # called hr_by_team_year_sf_la.csv and plot it using pandas and ggplot.
    #
    # This csv file has three columns: yearID, HR, and teamID. The data in the
    # file gives the total number of home runs hit each year by the SF Giants 
    # (teamID == 'SFN') and the LA Dodgers (teamID == "LAN"). Produce a 
    # visualization comparing the total home runs by year of the two teams. 
    # 
    # You can see the data in hr_by_team_year_sf_la_csv
    # at the link below:
    # https://www.dropbox.com/s/wn43cngo2wdle2b/hr_by_team_year_sf_la.csv
    #
    # Note that to differentiate between multiple categories on the 
    # same plot in ggplot, we can pass color in with the other arguments
    # to aes, rather than in our geometry functions. For example, 
    # ggplot(data, aes(xvar, yvar, color=category_var)). This should help you 
    # in this exercise.
    csv1 = pandas.read_csv(hr_by_team_year_sf_la_csv)
    gg = ggplot(csv1,aes('yearID','HR',color = 'teamID')) + geom_point() + geom_line() + ggtitle('HomeRuns by Giants and Dodgers Over Time')
    return gg

print lineplot_compare('/Users/Miller/GitHub/GhNanoDegree/Class_Intro_to_DataScience/Lesson4_DataViz/hr_by_team_year_sf_la.csv')