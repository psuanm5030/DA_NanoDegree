# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 11:15:26 2015

@author: Miller
"""

import numpy
import pandas
import statsmodels.api as sm
import matplotlib.pyplot as plt

def custom_heuristic(file_path):
    '''
    You are given a list of Titantic passengers and their associated
    information. More information about the data can be seen at the link below:
    http://www.kaggle.com/c/titanic-gettingStarted/data

    For this exercise, you need to write a custom heuristic that will take
    in some combination of the passenger's attributes and predict if the passenger
    survived the Titanic diaster.

    Can your custom heuristic beat 80% accuracy?
    
    The available attributes are:
    Pclass          Passenger Class
                    (1 = 1st; 2 = 2nd; 3 = 3rd)
    Name            Name
    Sex             Sex
    Age             Age
    SibSp           Number of Siblings/Spouses Aboard
    Parch           Number of Parents/Children Aboard
    Ticket          Ticket Number
    Fare            Passenger Fare
    Cabin           Cabin
    Embarked        Port of Embarkation
                    (C = Cherbourg; Q = Queenstown; S = Southampton)
                    
    SPECIAL NOTES:
    Pclass is a proxy for socioeconomic status (SES)
    1st ~ Upper; 2nd ~ Middle; 3rd ~ Lower

    Age is in years; fractional if age less than one
    If the age is estimated, it is in the form xx.5

    With respect to the family relation variables (i.e. SibSp and Parch)
    some relations were ignored. The following are the definitions used
    for SibSp and Parch.

    Sibling:  brother, sister, stepbrother, or stepsister of passenger aboard Titanic
    Spouse:   husband or wife of passenger aboard Titanic (mistresses and fiancees ignored)
    Parent:   mother or father of passenger aboard Titanic
    Child:    son, daughter, stepson, or stepdaughter of passenger aboard Titanic
    
    Write your prediction back into the "predictions" dictionary. The
    key of the dictionary should be the passenger's id (which can be accessed
    via passenger["PassengerId"]) and the associating value should be 1 if the
    passenger survvied or 0 otherwise. 

    For example, if a passenger is predicted to have survived:
    passenger_id = passenger['PassengerId']
    predictions[passenger_id] = 1

    And if a passenger is predicted to have perished in the disaster:
    passenger_id = passenger['PassengerId']
    predictions[passenger_id] = 0
    
    You can also look at the Titantic data that you will be working with
    at the link below:
    https://www.dropbox.com/s/r5f9aos8p9ri9sa/titanic_data.csv
    '''
    predictions = {}
    points_index = {}
    df = pandas.read_csv(file_path)
    for passenger_index, passenger in df.iterrows():
        passenger_id = passenger['PassengerId']
        pnts = points(passenger) #PASS a Series into the points function.
        points_index[passenger_id] = pnts
    meanpts = heuristic_percentage(points_index) # Get the mean points
    predictions = determine_survival(points_index,meanpts) # Get the survival rating.
    return predictions, meanpts
    
def heuristic_percentage(dict1):
    '''
    This takes in a dictionary and returns the average of its keys
    '''
    lst1 = []
    for k,v in dict1.iteritems():
        lst1.append(v)
        
    heur_ave = numpy.mean(lst1)
    
    return heur_ave
    
def determine_survival(points_dict,mean1):
    '''
    Take in the dictionary of points per passenger ID and the mean points. 
    Give people scoring OVER the mean, a 1 (Survived), else give 0.
    '''
    return_dict = {}
    for k,v in points_dict.iteritems():
        if v >= 4: 
            return_dict[k] = 1
        else: 
            return_dict[k] = 0
    return return_dict

def points(series_passed):
    '''
    Assign points based upon the variable
    '''
    points = 0  
    # The below assignments gets me a accuracy of 80.02%!!
    for item in series_passed.iteritems():
        if item[0] == 'Sex':
            if item[1] == 'female':
                points += 7
        elif item[0] == 'Pclass':
            if item[1] == 1:
                points += 2
            elif item[1] == 2:
                points += 1
        elif item[0] == 'Age':
            if item[1] <= 15:
                points += 5
        elif item[0] == 'SibSp':
            if item[1] <= 2:
                points += 1
        elif item[0] == 'Parch':
            if item[1] <= 2:
                points += 1
        elif item[0] == 'Fare':
            if item[1] >= 25:
                points += 1
        elif item[0] == 'Embarked':
            if item[1] == 'C':
                points += 2
    return points

    
(dict123, mpts) = custom_heuristic("/Users/Miller/GitHub/NanoDegree/Class_Intro_to_DataScience/Lesson1/PS1 - Titanic/titanic_data.csv")
print mpts

