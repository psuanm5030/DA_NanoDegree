# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 08:41:43 2015

@author: Miller
"""

import numpy as np
import pandas
import statsmodels.api as sm
import scipy
import matplotlib.pyplot as plt

"""
In this question, you need to:
1) implement the linear_regression() procedure
2) Select features (in the predictions procedure) and make predictions.

"""
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

def plot_residuals(turnstile_weather, predictions):
    '''
    Using the same methods that we used to plot a histogram of entries
    per hour for our data, why don't you make a histogram of the residuals
    (that is, the difference between the original hourly entry data and the predicted values).
    Try different binwidths for your histogram.

    Based on this residual histogram, do you have any insight into how our model
    performed?  Reading a bit on this webpage might be useful:

    http://www.itl.nist.gov/div898/handbook/pri/section2/pri24.htm
    '''
    
    plt.figure()
    (turnstile_weather['ENTRIESn_hourly'] - predictions).hist(bins=75)
    return plt

def linear_regression(features, values):
    """
    Perform linear regression given a data set with an arbitrary number of features.
    
    This can be the same code as in the lesson #3 exercise.
    """
    
    features = sm.add_constant(features)
    model = sm.OLS(values, features)
    results = model.fit()
    res_summary = results.summary()
    intercept = results.params[0]
    params = results.params[1:]
    
    return [intercept,params,res_summary]

def predictions(dataframe):
    '''
    The NYC turnstile data is stored in a pandas dataframe called weather_turnstile.
    Using the information stored in the dataframe, let's predict the ridership of
    the NYC subway using linear regression with gradient descent.
    
    You can download the complete turnstile weather dataframe here:
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv    
    
    Your prediction should have a R^2 value of 0.40 or better.
    You need to experiment using various input features contained in the dataframe. 
    We recommend that you don't use the EXITSn_hourly feature as an input to the 
    linear model because we cannot use it as a predictor: we cannot use exits 
    counts as a way to predict entry counts. 
    
    Note: Due to the memory and CPU limitation of our Amazon EC2 instance, we will
    give you a random subet (~10%) of the data contained in 
    turnstile_data_master_with_weather.csv. You are encouraged to experiment with 
    this exercise on your own computer, locally. If you do, you may want to complete Exercise
    8 using gradient descent, or limit your number of features to 10 or so, since ordinary
    least squares can be very slow for a large number of features.
    
    If you receive a "server has encountered an error" message, that means you are 
    hitting the 30-second limit that's placed on running your program. Try using a
    smaller number of features.
    '''
    ############## MODIFY THIS SECTION ###########################
    # Select features. You should modify this section to try different features!             #
    # We've selected rain, precipi, Hour, meantempi, and UNIT (as a dummy) to start you off. #
    # See this page for more info about dummy variables:                                     #
    # http://pandas.pydata.org/pandas-docs/stable/generated/pandas.get_dummies.html          #
    #####################################################
    features = dataframe[['rain', 'precipi', 'Hour', 'meantempi']]
    dummy_units = pandas.get_dummies(dataframe['UNIT'], prefix='unit')
    features = features.join(dummy_units)
    
    # Values
    values = dataframe['ENTRIESn_hourly']

    # Perform linear regression
    lst1 = linear_regression(features, values)
    intercept = lst1[0]
    params = lst1[1]
    results = lst1[2]
    predictions = intercept + np.dot(features, params)
    return predictions, results
    
turnstile_weather = pandas.read_csv("/Users/Miller/GitHub/GhNanoDegree/Class_Intro_to_DataScience/Lesson3_DataAnalysis/PS3_AnalyzingSubwayData/turnstile_data_master_with_weather.csv")
preds, results = predictions(turnstile_weather)
print compute_r_squared(turnstile_weather['ENTRIESn_hourly'],preds)
print results
error_plot = plot_residuals(turnstile_weather,preds)