# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 08:09:37 2015

@author: Miller
"""

import numpy as np

def compute_r_squared(data, predictions):
    # Write a function that, given two input numpy arrays, 'data', and 'predictions,'
    # returns the coefficient of determination, R^2, for the model that produced 
    # predictions.
    # 
    # Numpy has a couple of functions -- np.mean() and np.sum() --
    # that you might find useful, but you don't have to use them.
    # Andys first trY:
    #sum1 = (np.sum((data - predictions)**2))
    #sum2 = (np.sum((predictions-np.mean(predictions))**2))
    #r_squared = sum1 / sum2
    sum1 = (np.sum((data - predictions)**2))
    sum2 = (np.sum((data-np.mean(data))**2))
    r_squared = 1 - (sum1 / sum2)
    return r_squared