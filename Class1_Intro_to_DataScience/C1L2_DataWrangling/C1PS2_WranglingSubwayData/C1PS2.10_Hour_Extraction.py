# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 07:06:50 2015

@author: Miller
"""

import pandas
import datetime

def time_to_hour(time):
    '''
    Given an input variable time that represents time in the format of:
    "00:00:00" (hour:minutes:seconds)
    
    Write a function to extract the hour part from the input variable time
    and return it as an integer. For example:
        1) if hour is 00, your code should return 0
        2) if hour is 01, your code should return 1
        3) if hour is 21, your code should return 21
        
    Please return hour as an integer.
    '''
    # First example is if given a date field.
    # hour = int(dt.date.strftime(time,"%H"))
    # Udacity solution:
    hour = int(time[0:2]) # for string extraction
    return hour
    
birth = dt.datetime(2015,01,29,8,1,59)

print time_to_hour(birth)