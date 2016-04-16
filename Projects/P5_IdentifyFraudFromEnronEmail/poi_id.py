#!/usr/bin/python

# P5: Identify Fraud from Enron Email
# Student: Andy Miller
# Udacity's Data Analyst Nanodegree (https://www.udacity.com/course/nd002)


import sys
sys.path.append("/Users/Miller/GitHub/DAnanodegree/Class4_Intro_ML/UD120/ud120-projects/tools")
sys.path.append("/Users/Miller/GitHub/DAnanodegree/Class4_Intro_ML/UD120/ud120-projects/final_project")
sys.path.append("/Users/Miller/GitHub/DAnanodegree/Projects/P5_IdentifyFraudFromEnronEmail")
import os
import operator
from time import time
import pickle
import pprint as pp
from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data, test_classifier
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import statistics as stat


### TASK 1: SELECT THE FEATURES TO USE AND LOAD DATA ###
# Listing of Features:
features_list = ['poi', 'salary', 'deferral_payments', 'total_payments', 'exercised_stock_options',
                 'bonus', 'restricted_stock', 'restricted_stock_deferred', 'total_stock_value',
                 'expenses', 'loan_advances', 'other', 'director_fees', 'deferred_income',
                 'long_term_incentive','Ratio_from_POI','Ratio_to_POI','from_messages','shared_receipt_with_poi','to_messages']

### Load the dictionary containing the dataset
with open("/Users/Miller/GitHub/DAnanodegree/Class4_Intro_ML/UD120/ud120-projects/final_project/final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### TASK 2: REMOVE OUTLIERS ###

# 2.1 - Check NaNs by Observation to determine if any users have alot of NaNs and should be excluded.
def check_nan_row(dict):
    """
    Check NaNs by Observation to determine if any users have alot of NaNs and should be excluded.
    Args:
        dict: data dictionary

    Returns: Dictionary for each person with the count of NaNs and percentage of columns
    """
    final_row = {}
    for k,v in dict.iteritems():
        feat_cnt = len(v.keys())
        cnt = 0
        for val in v.itervalues():
            if val == 'NaN': cnt+=1
        final_row[k] = {
            'Cnt':cnt,
            'Perc':round(float(cnt)/float(feat_cnt),2)
        }
    return final_row

row_check = check_nan_row(data_dict)
print '\nNaN Checks for Each Observation'
pp.pprint(row_check)
"""Results
{'ALLEN PHILLIP K': {'Cnt': 2, 'Perc': 0.1},
 'BADUM JAMES P': {'Cnt': 15, 'Perc': 0.71},
 'BANNANTINE JAMES M': {'Cnt': 5, 'Perc': 0.24},
 'BAXTER JOHN C': {'Cnt': 9, 'Perc': 0.43},
 'BAY FRANKLIN R': {'Cnt': 9, 'Perc': 0.43},
 'BAZELIDES PHILIP J': {'Cnt': 13, 'Perc': 0.62},
 'BECK SALLY W': {'Cnt': 7, 'Perc': 0.33},
 'BELDEN TIMOTHY N': {'Cnt': 4, 'Perc': 0.19},
 'BELFER ROBERT': {'Cnt': 14, 'Perc': 0.67},
 'BERBERIAN DAVID': {'Cnt': 13, 'Perc': 0.62},
 'BERGSIEKER RICHARD P': {'Cnt': 5, 'Perc': 0.24},
 'BHATNAGAR SANJAY': {'Cnt': 8, 'Perc': 0.38},
 'BIBI PHILIPPE A': {'Cnt': 5, 'Perc': 0.24},
 'BLACHMAN JEREMY M': {'Cnt': 5, 'Perc': 0.24},
 'BLAKE JR. NORMAN P': {'Cnt': 16, 'Perc': 0.76},
 'BOWEN JR RAYMOND M': {'Cnt': 5, 'Perc': 0.24},
 'BROWN MICHAEL': {'Cnt': 12, 'Perc': 0.57},
 'BUCHANAN HAROLD G': {'Cnt': 5, 'Perc': 0.24},
 'BUTTS ROBERT H': {'Cnt': 10, 'Perc': 0.48},
 'BUY RICHARD B': {'Cnt': 4, 'Perc': 0.19},
 'CALGER CHRISTOPHER F': {'Cnt': 5, 'Perc': 0.24},
 'CARTER REBECCA C': {'Cnt': 6, 'Perc': 0.29},
 'CAUSEY RICHARD A': {'Cnt': 5, 'Perc': 0.24},
 'CHAN RONNIE': {'Cnt': 16, 'Perc': 0.76},
 'CHRISTODOULOU DIOMEDES': {'Cnt': 16, 'Perc': 0.76},
 'CLINE KENNETH W': {'Cnt': 17, 'Perc': 0.81},
 'COLWELL WESLEY': {'Cnt': 5, 'Perc': 0.24},
 'CORDES WILLIAM R': {'Cnt': 11, 'Perc': 0.52},
 'COX DAVID': {'Cnt': 5, 'Perc': 0.24},
 'CUMBERLAND MICHAEL S': {'Cnt': 12, 'Perc': 0.57},
 'DEFFNER JOSEPH M': {'Cnt': 5, 'Perc': 0.24},
 'DELAINEY DAVID W': {'Cnt': 5, 'Perc': 0.24},
 'DERRICK JR. JAMES V': {'Cnt': 3, 'Perc': 0.14},
 'DETMERING TIMOTHY J': {'Cnt': 7, 'Perc': 0.33},
 'DIETRICH JANET R': {'Cnt': 5, 'Perc': 0.24},
 'DIMICHELE RICHARD G': {'Cnt': 10, 'Perc': 0.48},
 'DODSON KEITH': {'Cnt': 9, 'Perc': 0.43},
 'DONAHUE JR JEFFREY M': {'Cnt': 5, 'Perc': 0.24},
 'DUNCAN JOHN H': {'Cnt': 15, 'Perc': 0.71},
 'DURAN WILLIAM D': {'Cnt': 5, 'Perc': 0.24},
 'ECHOLS JOHN B': {'Cnt': 10, 'Perc': 0.48},
 'ELLIOTT STEVEN': {'Cnt': 10, 'Perc': 0.48},
 'FALLON JAMES B': {'Cnt': 5, 'Perc': 0.24},
 'FASTOW ANDREW S': {'Cnt': 10, 'Perc': 0.48},
 'FITZGERALD JAY L': {'Cnt': 5, 'Perc': 0.24},
 'FOWLER PEGGY': {'Cnt': 11, 'Perc': 0.52},
 'FOY JOE': {'Cnt': 10, 'Perc': 0.48},
 'FREVERT MARK A': {'Cnt': 2, 'Perc': 0.1},
 'FUGH JOHN L': {'Cnt': 16, 'Perc': 0.76},
 'GAHN ROBERT S': {'Cnt': 10, 'Perc': 0.48},
 'GARLAND C KEVIN': {'Cnt': 5, 'Perc': 0.24},
 'GATHMANN WILLIAM D': {'Cnt': 16, 'Perc': 0.76},
 'GIBBS DANA R': {'Cnt': 9, 'Perc': 0.43},
 'GILLIS JOHN': {'Cnt': 17, 'Perc': 0.81},
 'GLISAN JR BEN F': {'Cnt': 5, 'Perc': 0.24},
 'GOLD JOSEPH': {'Cnt': 11, 'Perc': 0.52},
 'GRAMM WENDY L': {'Cnt': 18, 'Perc': 0.86},
 'GRAY RODNEY': {'Cnt': 15, 'Perc': 0.71},
 'HAEDICKE MARK E': {'Cnt': 2, 'Perc': 0.1},
 'HANNON KEVIN P': {'Cnt': 4, 'Perc': 0.19},
 'HAUG DAVID L': {'Cnt': 10, 'Perc': 0.48},
 'HAYES ROBERT E': {'Cnt': 10, 'Perc': 0.48},
 'HAYSLETT RODERICK J': {'Cnt': 12, 'Perc': 0.57},
 'HERMANN ROBERT J': {'Cnt': 9, 'Perc': 0.43},
 'HICKERSON GARY J': {'Cnt': 6, 'Perc': 0.29},
 'HIRKO JOSEPH': {'Cnt': 13, 'Perc': 0.62},
 'HORTON STANLEY C': {'Cnt': 9, 'Perc': 0.43},
 'HUGHES JAMES A': {'Cnt': 11, 'Perc': 0.52},
 'HUMPHREY GENE E': {'Cnt': 8, 'Perc': 0.38},
 'IZZO LAWRENCE L': {'Cnt': 6, 'Perc': 0.29},
 'JACKSON CHARLENE R': {'Cnt': 6, 'Perc': 0.29},
 'JAEDICKE ROBERT': {'Cnt': 13, 'Perc': 0.62},
 'KAMINSKI WINCENTY J': {'Cnt': 5, 'Perc': 0.24},
 'KEAN STEVEN J': {'Cnt': 5, 'Perc': 0.24},
 'KISHKILL JOSEPH G': {'Cnt': 12, 'Perc': 0.57},
 'KITCHEN LOUISE': {'Cnt': 6, 'Perc': 0.29},
 'KOENIG MARK E': {'Cnt': 5, 'Perc': 0.24},
 'KOPPER MICHAEL J': {'Cnt': 11, 'Perc': 0.52},
 'LAVORATO JOHN J': {'Cnt': 5, 'Perc': 0.24},
 'LAY KENNETH L': {'Cnt': 2, 'Perc': 0.1},
 'LEFF DANIEL P': {'Cnt': 7, 'Perc': 0.33},
 'LEMAISTRE CHARLES': {'Cnt': 15, 'Perc': 0.71},
 'LEWIS RICHARD': {'Cnt': 12, 'Perc': 0.57},
 'LINDHOLM TOD A': {'Cnt': 9, 'Perc': 0.43},
 'LOCKHART EUGENE E': {'Cnt': 20, 'Perc': 0.95},
 'LOWRY CHARLES P': {'Cnt': 16, 'Perc': 0.76},
 'MARTIN AMANDA K': {'Cnt': 6, 'Perc': 0.29},
 'MCCARTY DANNY J': {'Cnt': 11, 'Perc': 0.52},
 'MCCLELLAN GEORGE': {'Cnt': 5, 'Perc': 0.24},
 'MCCONNELL MICHAEL S': {'Cnt': 5, 'Perc': 0.24},
 'MCDONALD REBECCA': {'Cnt': 11, 'Perc': 0.52},
 'MCMAHON JEFFREY': {'Cnt': 5, 'Perc': 0.24},
 'MENDELSOHN JOHN': {'Cnt': 16, 'Perc': 0.76},
 'METTS MARK': {'Cnt': 7, 'Perc': 0.33},
 'MEYER JEROME J': {'Cnt': 16, 'Perc': 0.76},
 'MEYER ROCKFORD G': {'Cnt': 9, 'Perc': 0.43},
 'MORAN MICHAEL P': {'Cnt': 11, 'Perc': 0.52},
 'MORDAUNT KRISTINA M': {'Cnt': 12, 'Perc': 0.57},
 'MULLER MARK S': {'Cnt': 4, 'Perc': 0.19},
 'MURRAY JULIA H': {'Cnt': 5, 'Perc': 0.24},
 'NOLES JAMES L': {'Cnt': 15, 'Perc': 0.71},
 'OLSON CINDY K': {'Cnt': 4, 'Perc': 0.19},
 'OVERDYKE JR JERE C': {'Cnt': 11, 'Perc': 0.52},
 'PAI LOU L': {'Cnt': 11, 'Perc': 0.52},
 'PEREIRA PAULO V. FERRAZ': {'Cnt': 16, 'Perc': 0.76},
 'PICKERING MARK R': {'Cnt': 7, 'Perc': 0.33},
 'PIPER GREGORY F': {'Cnt': 3, 'Perc': 0.14},
 'PIRO JIM': {'Cnt': 12, 'Perc': 0.57},
 'POWERS WILLIAM': {'Cnt': 12, 'Perc': 0.57},
 'PRENTICE JAMES': {'Cnt': 14, 'Perc': 0.67},
 'REDMOND BRIAN L': {'Cnt': 8, 'Perc': 0.38},
 'REYNOLDS LAWRENCE': {'Cnt': 8, 'Perc': 0.38},
 'RICE KENNETH D': {'Cnt': 4, 'Perc': 0.19},
 'RIEKER PAULA H': {'Cnt': 4, 'Perc': 0.19},
 'SAVAGE FRANK': {'Cnt': 17, 'Perc': 0.81},
 'SCRIMSHAW MATTHEW': {'Cnt': 17, 'Perc': 0.81},
 'SHANKMAN JEFFREY A': {'Cnt': 5, 'Perc': 0.24},
 'SHAPIRO RICHARD S': {'Cnt': 6, 'Perc': 0.29},
 'SHARP VICTORIA T': {'Cnt': 4, 'Perc': 0.19},
 'SHELBY REX': {'Cnt': 5, 'Perc': 0.24},
 'SHERRICK JEFFREY B': {'Cnt': 11, 'Perc': 0.52},
 'SHERRIFF JOHN R': {'Cnt': 6, 'Perc': 0.29},
 'SKILLING JEFFREY K': {'Cnt': 5, 'Perc': 0.24},
 'STABLER FRANK': {'Cnt': 12, 'Perc': 0.57},
 'SULLIVAN-SHAKLOVITZ COLLEEN': {'Cnt': 12, 'Perc': 0.57},
 'SUNDE MARTIN': {'Cnt': 7, 'Perc': 0.33},
 'TAYLOR MITCHELL S': {'Cnt': 7, 'Perc': 0.33},
 'THE TRAVEL AGENCY IN THE PARK': {'Cnt': 18, 'Perc': 0.86},
 'THORN TERENCE H': {'Cnt': 5, 'Perc': 0.24},
 'TILNEY ELIZABETH A': {'Cnt': 5, 'Perc': 0.24},
 'TOTAL': {'Cnt': 6, 'Perc': 0.29},
 'UMANOFF ADAM S': {'Cnt': 10, 'Perc': 0.48},
 'URQUHART JOHN A': {'Cnt': 16, 'Perc': 0.76},
 'WAKEHAM JOHN': {'Cnt': 17, 'Perc': 0.81},
 'WALLS JR ROBERT H': {'Cnt': 5, 'Perc': 0.24},
 'WALTERS GARETH W': {'Cnt': 15, 'Perc': 0.71},
 'WASAFF GEORGE': {'Cnt': 4, 'Perc': 0.19},
 'WESTFAHL RICHARD K': {'Cnt': 11, 'Perc': 0.52},
 'WHALEY DAVID A': {'Cnt': 18, 'Perc': 0.86},
 'WHALLEY LAWRENCE G': {'Cnt': 5, 'Perc': 0.24},
 'WHITE JR THOMAS E': {'Cnt': 11, 'Perc': 0.52},
 'WINOKUR JR. HERBERT S': {'Cnt': 16, 'Perc': 0.76},
 'WODRASKA JOHN': {'Cnt': 17, 'Perc': 0.81},
 'WROBEL BRUCE': {'Cnt': 18, 'Perc': 0.86},
 'YEAGER F SCOTT': {'Cnt': 12, 'Perc': 0.57},
 'YEAP SOON': {'Cnt': 16, 'Perc': 0.76}}
"""
# Get a look at the user entries that have a high percentage of blanks.
print '\nObservations with over 80% of Features with NaNs'
for k in row_check.iterkeys():
    if row_check[k]['Perc'] > 0.80:
        print k
        print row_check[k]

# 2.2 - Check the % of NaNs for each feature - for general understanding.
def check_nan_features(dict):
    """
    Checks the percentage of NaNs for each feature in the data.
    Args:
        dict: data dictionary

    Returns: dict of all features with the percentage of NaNs
    """
    final = {}
    ftrs_list = dict[dict.keys()[0]].keys()
    cnt = float(len(data_dict))
    for i in ftrs_list:
        n = 0.0
        for k, v in dict.iteritems():
            if v[i] == 'NaN':
                n += 1.0
        final[i] = (n / cnt)
    return final

nans_check = check_nan_features(data_dict)
sorted_nans_check = sorted(nans_check.items(), key=operator.itemgetter(1))
print '\nNaN Checks for Each Feature'
print sorted_nans_check
"""
[('poi', 0.0), ('total_stock_value', 0.136986301369863), ('total_payments', 0.14383561643835616), ('email_address', 0.23972602739726026), ('restricted_stock', 0.2465753424657534), ('exercised_stock_options', 0.3013698630136986), ('salary', 0.3493150684931507), ('expenses', 0.3493150684931507), ('other', 0.363013698630137), ('to_messages', 0.410958904109589), ('shared_receipt_with_poi', 0.410958904109589), ('from_messages', 0.410958904109589), ('from_poi_to_this_person', 0.410958904109589), ('from_this_person_to_poi', 0.410958904109589), ('bonus', 0.4383561643835616), ('long_term_incentive', 0.547945205479452), ('deferred_income', 0.6643835616438356), ('deferral_payments', 0.7328767123287672), ('restricted_stock_deferred', 0.8767123287671232), ('director_fees', 0.8835616438356164), ('loan_advances', 0.9726027397260274)]

We see that there are several features that have NaNs for more than half of the people.  These items will not
be used in our listing of features: long_term_incentive, deferred_income, deferral_payments,
restricted_stock_deferred, director_fees, and loan_advances.
"""

# 2.3 - Remove the outliers
# Outliers noted:
# - "TOTAL" from the data
len(data_dict) # Check before number of keys
data_dict.pop('TOTAL') # Remove from the data.
data_dict.pop('THE TRAVEL AGENCY IN THE PARK') # Remove from the data, as this is not a person.
data_dict.pop('LOCKHART EUGENE E') # Remove from the data, as this person has 95% of features as 'NAN'
len(data_dict) # Check AFTER POP number of keys

### TASK 3: CREATE NEW FEATURES ###

# Created Feature #1 & #2 - Ration of Messages FROM POI and TO POI
def compute_ratio(dict):
    """
    Create a ratio of the messages the person received from a POI from all the messages they received.
    Args:
        dict: data dictionary (excl. outliers) - key by key

    Returns: tuple of ratios iteratively for each dictionary key
    """
    if (dict['from_this_person_to_poi'] == 'NaN') or (dict['to_messages'] == 'NaN' or dict['to_messages'] == 0):
        to_poi = 0.
    else:
        to_poi = float(dict['from_this_person_to_poi']) / float(dict['to_messages'])

    if (dict['from_poi_to_this_person'] == 'NaN') or (dict['from_messages'] == 'NaN' or dict['from_messages'] ==
        0):
        from_poi = 0.
    else:
        from_poi = float(dict['from_poi_to_this_person']) / float(dict['from_messages'])
    return (from_poi,to_poi)

for key in data_dict:
    data_dict[key]['Ratio_from_POI'], data_dict[key]['Ratio_to_POI'] = compute_ratio(data_dict[key])

### Store to my_dataset for easy export below.
my_dataset = data_dict

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

### TASK 4: TRY CLASSIFIERS ###

# Load the various classifiers to test.
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.decomposition import RandomizedPCA, PCA
from sklearn.grid_search import GridSearchCV
from sklearn.feature_selection import SelectKBest, chi2, f_classif
from sklearn.preprocessing import MinMaxScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.cross_validation import StratifiedShuffleSplit

# Prior to configuring my pipelines, I would like to review the features and their importance.
from sklearn.feature_selection import SelectKBest

def find_k_best(data_dict, features_list, k):
    """
    Figure out the effectiveness of each feature in terms of their predictive capacity.
    Args:
        data_dict: data dictionary
        features_list: features
        k: number of features to check scores for

    Returns: dict of features and their respective scores.

    """
    data = featureFormat(data_dict, features_list)
    labels, features = targetFeatureSplit(data)

    k_best = SelectKBest(k=k)
    k_best.fit(features, labels)
    scores = k_best.scores_
    unsort_pairs = zip(features_list[1:], scores)
    sorted_pairs = list(reversed(sorted(unsort_pairs, key=lambda x: x[1])))
    best_feats = dict(sorted_pairs[:k])
    return best_feats

num = 15 # Get the top 15
best_features = find_k_best(my_dataset, features_list, num)
best_features_sort = sorted(best_features.items(), reverse=True, key=lambda tup: tup[1])
print '\nBest Features (per SelectKBest): '
pp.pprint(best_features_sort)

# Build out Pipelines for each Classifier being used:

def build_SVM():
    """
    Setup the pipeline and parameters for the SVM Algo.
    Returns: the correct pipeline and parameters to feed into the grid search function.
    """
    estimators = [('Scale',MinMaxScaler()),  ('SKB', SelectKBest()), ('PCA', RandomizedPCA()), ('SVM', SVC())]
    pipe = Pipeline(estimators)
    pipe

    parameters = {
        'Scale__feature_range': [(0, 1)],
        'SKB__k': [2,3,4,5],
        'SKB__score_func': [f_classif],
        'PCA__n_components': [1,2,3],
        'PCA__whiten': [True],
        'SVM__kernel': ['rbf', 'linear'],
        'SVM__C': [10.0, 100.0, 1000.0, 10000.0],
        'SVM__gamma': [0.01, 0.001, 0.0001]
    }
    return pipe, parameters

def build_NB():
    """
    Setup the pipeline and parameters for the Naive Bayes Algo.
    Returns: the correct pipeline and parameters to feed into the grid search function.
    """
    estimators = [('Scale',MinMaxScaler()), ('SKB', SelectKBest()), ('PCA', RandomizedPCA()), ('NB', GaussianNB())]
    pipe = Pipeline(estimators)
    pipe

    parameters = {
        'SKB__k': [5],
        'SKB__score_func': [f_classif],
        'PCA__n_components': [2],
        'PCA__whiten': [True]
    }
    return pipe, parameters

def build_ADA():
    """
    Setup the pipeline and parameters for the ADA Boost Algo.
    Returns: the correct pipeline and parameters to feed into the grid search function.
    """
    estimators = [('Scale',MinMaxScaler()), ('SKB', SelectKBest()), ('PCA', RandomizedPCA()), ('ADA',
                                                                                               AdaBoostClassifier())]
    pipe = Pipeline(estimators)
    pipe

    parameters = {
        'SKB__k': [2,3,4,5,6],
        'SKB__score_func': [f_classif],
        'PCA__n_components': [2,3],
        'PCA__whiten': [True],
        'ADA__n_estimators':[50,75,100],
        'ADA__learning_rate':[0.1,0.15,0.2,0.3,0.4,0.5,0.9,1],
        'ADA__algorithm':['SAMME.R','SAMME']
    }
    return pipe, parameters

def build_DT():
    """
    Setup the pipeline and parameters for the Decision Tree Algo.
    Returns: the correct pipeline and parameters to feed into the grid search function.
    """
    estimators = [('SKB', SelectKBest()), ('PCA', RandomizedPCA()), ('DT', DecisionTreeClassifier())]
    pipe = Pipeline(estimators)
    pipe

    parameters = {
        'SKB__k': [2,3,4,5],
        'SKB__score_func': [f_classif],
        'PCA__n_components': [1,2,3],
        'PCA__whiten': [True],
        'DT__max_features': [.1, .2, .3, .5]
    }
    return pipe, parameters

def build_LOG():
    """
    Setup the pipeline and parameters for the Logistic Regression Algo.
    Returns: the correct pipeline and parameters to feed into the grid search function.

    """
    estimators = [('SKB', SelectKBest()), ('PCA', RandomizedPCA()), ('LOG', LogisticRegression())]
    pipe = Pipeline(estimators)
    pipe

    parameters = {
        'SKB__k': [2,3,4,5],
        'SKB__score_func': [f_classif],
        'PCA__n_components': [1,2,3],
        'PCA__whiten': [True],
        'LOG__C': [.1,1,10,100],
        'LOG__tol':[0.01,0.001,0.0001],
        'LOG__class_weight':['balanced']
    }
    return pipe, parameters

def build_KNN():
    """
    Setup the pipeline and parameters for the K-Nearest Neighbors Algo.
    Returns: the correct pipeline and parameters to feed into the grid search function.

    """
    estimators = [('Scale',MinMaxScaler()), ('SKB', SelectKBest()), ('PCA', RandomizedPCA()),('KNN', KNeighborsClassifier())]
    pipe = Pipeline(estimators)
    pipe

    parameters = {
        'SKB__k': [2,3,4,5],
        'SKB__score_func': [f_classif],
        'PCA__n_components': [2,3],
        'PCA__whiten': [True],
        'KNN__n_neighbors': [1, 5, 10],
        'KNN__leaf_size': [1, 10, 30, 60],
        'KNN__algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute']
    }
    return pipe, parameters

def build_Cluster():
    """
    Setup the pipeline and parameters for the K-Means Cluster Algo.
    Returns: the correct pipeline and parameters to feed into the grid search function.
    """
    estimators = [('Scale',MinMaxScaler()), ('SKB', SelectKBest()), ('PCA', RandomizedPCA()),('KM', KMeans())]
    pipe = Pipeline(estimators)
    pipe

    parameters = {
        'SKB__k': [3,4,5,6,7],
        'SKB__score_func': [f_classif],
        'PCA__n_components': [2,3],
        'PCA__whiten': [True],
        'KM__n_clusters':[2],
        'KM__tol': [0.001,0.01,0.1]
    }
    return pipe, parameters

def build_RF():
    """
    Setup the pipeline and parameters for the Random Forest Algo.
    Returns: the correct pipeline and parameters to feed into the grid search function.
    """
    estimators = [('Scale',MinMaxScaler()), ('SKB', SelectKBest()), ('PCA', RandomizedPCA()),('RF',
                                                                                               RandomForestClassifier())]
    pipe = Pipeline(estimators)
    pipe

    parameters = {
        'SKB__k': [4],
        'SKB__score_func': [f_classif],
        'PCA__n_components': [3],
        'PCA__whiten': [True],
        'RF__n_estimators': [1000],
        'RF__criterion': ['gini'] # 'entropy'
        # 'RF__max_features': [.2,.4],
        # 'RF__min_samples_split': [1, 2, 3],
        # 'RF__min_samples_leaf': [1, 2, 3]
    }
    return pipe, parameters

# Build out the Pipeline execution, including stratified shuffle split
def main_pipe_review(type, features, labels):
    """
    Consolidated function to test various algorithms and get the best classifier in return.
    Args:
        type (str): What algo is to be used.  Values consist of: SVM, RF, DT, NB, or Cluster
        data (tuple): Both features and labels

    Returns:
        gs.best_estimator_  --- the best estimator from the Grid Search.
        gs.best_estimator_.get_params() --- the best parameters from the Grid Search.
        gs.predict(features) --- the predicted labels based upon the Grid Search.
        features_selected_list --- Listing of the best features based upon the grid search.
    """
    if type == 'SVM':
        pipe, parameters = build_SVM()

    if type == 'NB':
        pipe, parameters = build_NB()

    if type == 'RF':
        pipe, parameters = build_RF()

    if type == 'Cluster':
        pipe, parameters = build_Cluster()

    if type == 'DT':
        pipe, parameters = build_DT()

    if type == 'KNN':
        pipe, parameters = build_KNN()

    if type == 'ADA':
        pipe, parameters = build_ADA()

    if type == 'LOG':
        pipe, parameters = build_LOG()

    # Create a Stratified Shuffle Split iterator for cv
    sss = StratifiedShuffleSplit(
        labels,
        n_iter=1000,
        random_state=42
    )

    gs = GridSearchCV(pipe, parameters, n_jobs=-1, verbose=1, cv=sss)
    print "Performing grid search for %s..." % (type)
    print "pipeline:", [name for name, _ in pipe.steps]
    print "parameters:"
    pp.pprint(parameters)
    t0 = time()
    gs.fit(features, labels)
    print("done in %0.3fs" % (time() - t0))
    print

    print "Best score: %0.3f" % gs.best_score_
    print "Best parameters set:"
    best_parameters = gs.best_estimator_.get_params()
    for param_name in sorted(parameters.keys()):
        print "\t%s: %r" % (param_name, best_parameters[param_name])
    print "Best features set:"
    features_selected_bool = gs.best_estimator_.named_steps['SKB'].get_support()
    features_selected_list = [x for x, y in zip(features_list[1:], features_selected_bool) if y]
    print features_selected_list
    # Return list of items:
    final_items = [gs.best_estimator_, gs.best_estimator_.get_params(), gs.predict(features),features_selected_list]
    return final_items


### TASK 5: TUNE CLASSIFIERS ###
### Tune your classifier to achieve better than .3 precision and recall
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info:
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!
from sklearn.cross_validation import train_test_split
features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)

# Fit the model using the selected Pipeline
# Returns list of the following:
# [gs.best_estimator_, gs.best_estimator_.get_params(), gs.predict(features),features_selected_list]

# algo_type = 'SVM' # Good - Best: Accuracy: 0.86529	Precision: 0.82386	Recall: 0.07250
# algo_type = 'DT' # Good - Best: Accuracy: 0.80569	Precision: 0.35921	Recall: 0.33550
algo_type = 'NB' # Good - Best: Accuracy: 0.87714	Precision: 0.61628	Recall: 0.37100
# algo_type = 'RF' # Good - Best: Accuracy: 0.85129	Precision: 0.43212	Recall: 0.13050
# algo_type = 'Cluster' # Good - Best: Accuracy: 0.72977	Precision: 0.22660	Recall: 0.31350
# algo_type = 'KNN' # Good - Best: Accuracy: 0.84592	Precision: 0.20000	Recall: 0.00050
# algo_type = 'ADA' # Good - Best: Accuracy: 0.84493	Precision: 0.41560	Recall: 0.21050
# algo_type = 'LOG' # Good - Best: Accuracy: 0.76371	Precision: 0.24943	Recall: 0.32550

final = main_pipe_review(algo_type, features, labels)

clf, best_parameters, labels_pred, final_features_list = final[0], final[1], final[2], final[3]

print "\nBest Features produced by Grid Search"
print final_features_list,'\n'

# Update the 'features_list' based upon the output:
# features_list = ['poi', 'salary', 'deferral_payments', 'total_payments', 'exercised_stock_options',
#                  'bonus', 'restricted_stock', 'restricted_stock_deferred', 'total_stock_value',
#                  'expenses', 'loan_advances', 'other', 'director_fees', 'deferred_income',
#                  'long_term_incentive', 'Ratio_from_POI', 'Ratio_to_POI']
final_features_list.insert(0, "poi")

print "\nBest Parameters produced by Grid Search"
print best_parameters,'\n'

print "\nOptimal Model produced by Grid Search"
print clf,'\n'

# Print Results  (will print the Grid Search score)
print "\nGrid Search Classification report:"
print classification_report(labels, labels_pred), '\n'

# Print Results  (will print the tester.py score)
print "tester.py Classification report:\n"
test_classifier(clf, my_dataset, final_features_list)

""" Notes on performance
NB:

Pipeline(steps=[('Scale', MinMaxScaler(copy=True, feature_range=(0, 1))), ('SKB', SelectKBest(k=6, score_func=<function f_classif at 0x10caafc08>)), ('PCA', RandomizedPCA(copy=True, iterated_power=3, n_components=2, random_state=None,
       whiten=True)), ('NB', GaussianNB())])
	Accuracy: 0.86607	Precision: 0.55094	Recall: 0.33800	F1: 0.41896	F2: 0.36632
	Total predictions: 14000	True positives:  676	False positives:  551	False negatives: 1324	True negatives: 11449


Classification Performance Report:
             precision    recall  f1-score   support

        0.0       0.92      0.95      0.94        38
        1.0       0.50      0.40      0.44         5

avg / total       0.87      0.88      0.88        43

['salary', 'exercised_stock_options', 'bonus', 'total_stock_value', 'deferred_income', 'long_term_incentive']

Pipeline(steps=[('Scale', MinMaxScaler(copy=True, feature_range=(0, 1))), ('SKB', SelectKBest(k=6, score_func=<function f_classif at 0x10ca7c320>)), ('PCA', RandomizedPCA(copy=True, iterated_power=3, n_components=3, random_state=None,
       whiten=True)), ('NB', GaussianNB())])
	Accuracy: 0.86900	Precision: 0.55980	Recall: 0.38850	F1: 0.45868	F2: 0.41383
	Total predictions: 14000	True positives:  777	False positives:  611	False negatives: 1223	True negatives: 11389


Classification Performance Report:
             precision    recall  f1-score   support

        0.0       0.92      0.95      0.94        38
        1.0       0.50      0.40      0.44         5

avg / total       0.87      0.88      0.88        43

['salary', 'exercised_stock_options', 'bonus', 'total_stock_value', 'deferred_income']

Pipeline(steps=[('Scale', MinMaxScaler(copy=True, feature_range=(0, 1))), ('SKB', SelectKBest(k=5, score_func=<function f_classif at 0x10ca7c320>)), ('PCA', RandomizedPCA(copy=True, iterated_power=3, n_components=2, random_state=None,
       whiten=True)), ('NB', GaussianNB())])
	Accuracy: 0.87714	Precision: 0.61628	Recall: 0.37100	F1: 0.46317	F2: 0.40309
	Total predictions: 14000	True positives:  742	False positives:  462	False negatives: 1258	True negatives: 11538

Classification Performance Report:
             precision    recall  f1-score   support

        0.0       0.93      0.97      0.95        38
        1.0       0.67      0.40      0.50         5

avg / total       0.89      0.91      0.90        43

SVM:
['salary', 'exercised_stock_options', 'bonus', 'total_stock_value', 'deferred_income']

Pipeline(steps=[('Scale', MinMaxScaler(copy=True, feature_range=(0, 1))), ('SKB', SelectKBest(k=5, score_func=<function f_classif at 0x10d18b320>)), ('PCA', RandomizedPCA(copy=True, iterated_power=3, n_components=1, random_state=None,
       whiten=True)), ('SVM', SVC(C=10.0, cache_size=200, class_weight=None, coef0=0.0,
  decision_function_shape=None, degree=3, gamma=0.01, kernel='rbf',
  max_iter=-1, probability=False, random_state=None, shrinking=True,
  tol=0.001, verbose=False))])
	Accuracy: 0.86529	Precision: 0.82386	Recall: 0.07250	F1: 0.13327	F2: 0.08867
	Total predictions: 14000	True positives:  145	False positives:   31	False negatives: 1855	True negatives: 11969


Classification Performance Report:
             precision    recall  f1-score   support

        0.0       0.88      1.00      0.94        38
        1.0       0.00      0.00      0.00         5

avg / total       0.78      0.88      0.83        43

DT:
['salary', 'exercised_stock_options', 'bonus', 'total_stock_value', 'deferred_income']

Pipeline(steps=[('SKB', SelectKBest(k=5, score_func=<function f_classif at 0x10ca7c320>)), ('PCA', RandomizedPCA(copy=True, iterated_power=3, n_components=3, random_state=None,
       whiten=True)), ('DT', DecisionTreeClassifier(class_weight=None, criterion='gini', max_depth=None,
            max_features=0.1, max_leaf_nodes=None, min_samples_leaf=1,
            min_samples_split=2, min_weight_fraction_leaf=0.0,
            presort=False, random_state=None, splitter='best'))])
	Accuracy: 0.81443	Precision: 0.34113	Recall: 0.32100	F1: 0.33076	F2: 0.32483
	Total predictions: 14000	True positives:  642	False positives: 1240	False negatives: 1358	True negatives: 10760


Classification Performance Report:
             precision    recall  f1-score   support

        0.0       0.95      0.92      0.93        38
        1.0       0.50      0.60      0.55         5

avg / total       0.89      0.88      0.89        43

Pipeline(steps=[('SKB', SelectKBest(k=4, score_func=<function f_classif at 0x10caafc08>)), ('PCA', RandomizedPCA(copy=True, iterated_power=3, n_components=3, random_state=None,
       whiten=True)), ('DT', DecisionTreeClassifier(class_weight=None, criterion='gini', max_depth=None,
            max_features=0.2, max_leaf_nodes=None, min_samples_leaf=1,
            min_samples_split=2, min_weight_fraction_leaf=0.0,
            presort=False, random_state=None, splitter='best'))])
	Accuracy: 0.80569	Precision: 0.35921	Recall: 0.33550	F1: 0.34695	F2: 0.33999
	Total predictions: 13000	True positives:  671	False positives: 1197	False negatives: 1329	True negatives: 9803


Classification Performance Report:
             precision    recall  f1-score   support

        0.0       0.92      0.89      0.91        38
        1.0       0.33      0.40      0.36         5

avg / total       0.85      0.84      0.84        43


RF:
['salary', 'exercised_stock_options', 'bonus', 'total_stock_value']

Pipeline(steps=[('Scale', MinMaxScaler(copy=True, feature_range=(0, 1))), ('SKB', SelectKBest(k=4, score_func=<function f_classif at 0x10d18b320>)), ('PCA', RandomizedPCA(copy=True, iterated_power=3, n_components=3, random_state=None,
       whiten=True)), ('RF', RandomForestClassifier(bootstrap=True, class_...n_jobs=1,
            oob_score=False, random_state=None, verbose=0,
            warm_start=False))])
	Accuracy: 0.82962	Precision: 0.34074	Recall: 0.11500	F1: 0.17196	F2: 0.13256
	Total predictions: 13000	True positives:  230	False positives:  445	False negatives: 1770	True negatives: 10555


Classification Performance Report:
             precision    recall  f1-score   support

        0.0       0.88      0.92      0.90        38
        1.0       0.00      0.00      0.00         5

avg / total       0.77      0.81      0.79        43

Pipeline(steps=[('Scale', MinMaxScaler(copy=True, feature_range=(0, 1))), ('SKB', SelectKBest(k=6, score_func=<function f_classif at 0x10c925a28>)), ('PCA', RandomizedPCA(copy=True, iterated_power=3, n_components=2, random_state=None,
       whiten=True)), ('RF', RandomForestClassifier(bootstrap=True, class_...n_jobs=1,
            oob_score=False, random_state=None, verbose=0,
            warm_start=False))])
	Accuracy: 0.85129	Precision: 0.43212	Recall: 0.13050	F1: 0.20046	F2: 0.15167
	Total predictions: 14000	True positives:  261	False positives:  343	False negatives: 1739	True negatives: 11657


Classification Performance Report:
             precision    recall  f1-score   support

        0.0       0.90      0.97      0.94        39
        1.0       0.50      0.20      0.29         5

avg / total       0.86      0.89      0.86        44

KNN:
['salary', 'exercised_stock_options', 'bonus', 'total_stock_value']

Pipeline(steps=[('Scale', MinMaxScaler(copy=True, feature_range=(0, 1))), ('SKB', SelectKBest(k=4, score_func=<function f_classif at 0x10caafc08>)), ('PCA', RandomizedPCA(copy=True, iterated_power=3, n_components=1, random_state=None,
       whiten=True)), ('KNN', KNeighborsClassifier(algorithm='auto', leaf_size=1, metric='minkowski',
           metric_params=None, n_jobs=1, n_neighbors=10, p=2,
           weights='uniform'))])
	Accuracy: 0.84592	Precision: 0.20000	Recall: 0.00050	F1: 0.00100	F2: 0.00062
	Total predictions: 13000	True positives:    1	False positives:    4	False negatives: 1999	True negatives: 10996


Classification Performance Report:
             precision    recall  f1-score   support

        0.0       0.88      1.00      0.94        38
        1.0       0.00      0.00      0.00         5

avg / total       0.78      0.88      0.83        43

ADA:
['salary', 'exercised_stock_options', 'bonus', 'total_stock_value']

Pipeline(steps=[('Scale', MinMaxScaler(copy=True, feature_range=(0, 1))), ('SKB', SelectKBest(k=4, score_func=<function f_classif at 0x10caafc08>)), ('PCA', RandomizedPCA(copy=True, iterated_power=3, n_components=3, random_state=None,
       whiten=True)), ('ADA', AdaBoostClassifier(algorithm='SAMME.R', base_estimator=None,
          learning_rate=1.0, n_estimators=50, random_state=None))])
	Accuracy: 0.79354	Precision: 0.25983	Recall: 0.18500	F1: 0.21612	F2: 0.19631
	Total predictions: 13000	True positives:  370	False positives: 1054	False negatives: 1630	True negatives: 9946


Classification Performance Report:
             precision    recall  f1-score   support

        0.0       0.87      0.87      0.87        38
        1.0       0.00      0.00      0.00         5

avg / total       0.77      0.77      0.77        43

['salary', 'exercised_stock_options', 'bonus', 'total_stock_value', 'deferred_income']

Pipeline(steps=[('Scale', MinMaxScaler(copy=True, feature_range=(0, 1))), ('SKB', SelectKBest(k=5, score_func=<function f_classif at 0x10caafc08>)), ('PCA', RandomizedPCA(copy=True, iterated_power=3, n_components=3, random_state=None,
       whiten=True)), ('ADA', AdaBoostClassifier(algorithm='SAMME', base_estimator=None, learning_rate=1,
          n_estimators=50, random_state=None))])
	Accuracy: 0.84493	Precision: 0.41560	Recall: 0.21050	F1: 0.27946	F2: 0.23355
	Total predictions: 14000	True positives:  421	False positives:  592	False negatives: 1579	True negatives: 11408


Classification Performance Report:
             precision    recall  f1-score   support

        0.0       0.89      0.84      0.86        38
        1.0       0.14      0.20      0.17         5

avg / total       0.80      0.77      0.78        43

K-Means:
['exercised_stock_options', 'bonus', 'total_stock_value']

Pipeline(steps=[('Scale', MinMaxScaler(copy=True, feature_range=(0, 1))), ('SKB', SelectKBest(k=3, score_func=<function f_classif at 0x10caafc08>)), ('PCA', RandomizedPCA(copy=True, iterated_power=3, n_components=2, random_state=None,
       whiten=True)), ('KM', KMeans(copy_x=True, init='k-means++', max_iter=300, n_clusters=2, n_init=10,
    n_jobs=1, precompute_distances='auto', random_state=None, tol=0.001,
    verbose=0))])
	Accuracy: 0.73246	Precision: 0.22650	Recall: 0.30600	F1: 0.26031	F2: 0.28593
	Total predictions: 13000	True positives:  612	False positives: 2090	False negatives: 1388	True negatives: 8910


Classification Performance Report:
             precision    recall  f1-score   support

        0.0       0.86      0.50      0.63        38
        1.0       0.10      0.40      0.15         5

avg / total       0.77      0.49      0.58        43

LOG:
['salary', 'exercised_stock_options', 'bonus', 'total_stock_value', 'deferred_income']

Pipeline(steps=[('SKB', SelectKBest(k=5, score_func=<function f_classif at 0x10caafc08>)), ('PCA', RandomizedPCA(copy=True, iterated_power=3, n_components=1, random_state=None,
       whiten=True)), ('LOG', LogisticRegression(C=0.1, class_weight='balanced', dual=False,
          fit_intercept=True, intercept_scaling=1, max_iter=100,
          multi_class='ovr', n_jobs=1, penalty='l2', random_state=None,
          solver='liblinear', tol=0.01, verbose=0, warm_start=False))])
	Accuracy: 0.76371	Precision: 0.24943	Recall: 0.32550	F1: 0.28243	F2: 0.30679
	Total predictions: 14000	True positives:  651	False positives: 1959	False negatives: 1349	True negatives: 10041


Classification Performance Report:
             precision    recall  f1-score   support

        0.0       0.94      0.89      0.92        38
        1.0       0.43      0.60      0.50         5

avg / total       0.88      0.86      0.87        43

"""

# Test the model using the test data
clf.fit(features_train,labels_train)
pred = clf.predict(features_test)
print '\n', "Classification Performance Report:"
print classification_report(labels_test, pred)


### TASK 6: DUMP CLASSIFER, DATASET, AND FEATURES_LIST ###
### So anyone can check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, final_features_list)
print 'Project Completed :-)'