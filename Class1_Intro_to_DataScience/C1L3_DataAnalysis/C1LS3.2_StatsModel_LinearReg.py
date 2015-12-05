# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 07:46:58 2015

@author: Miller
"""

import statsmodels.api as sm

def linear_regression(features, values):
    """
    Performs linear regression given a dataset with an arbitrary number of features.
    'features' is the input data points (or the X's) and 'values' is the output data points
    (or the Y's).
    
    Returns the intercept and the parameters, that is, the optimal values of theta.
    
    This page contains example code that may be helpful:
    http://statsmodels.sourceforge.net/0.5.0/generated/statsmodels.regression.linear_model.OLS.html
    """

    features = sm.add_constant(features)
    model = sm.OLS(values, features)
    results = model.fit()
    intercept = results.params[0]
    params = results.params[1:]
    return intercept, params
    
    return intercept, params
    
Y = [1,3,4,5,2,3,4]
X = range(1,8)
X = sm.add_constant(X)
print linear_regression(X,Y)

# Note that add_constant adds the constant feature as the first feature, so the intercept is at index 0 of the array results.params. The remaining values of results.params, from index 1 to the end, are the parameters, or weights, of the real features.
# Also note that values comes before features when creating the OLS model, just as Y came before X in the example code.