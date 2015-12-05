# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 13:26:50 2015

@author: Miller
"""

import pandas

def add_full_name(path_to_csv, path_to_new_csv):
    #Assume you will be reading in a csv file with the same columns that the
    #Lahman baseball data set has -- most importantly, there are columns
    #called 'nameFirst' and 'nameLast'.
    #1) Write a function that reads a csv
    #located at "path_to_csv" into a pandas dataframe and adds a new column
    #called 'nameFull' with a player's full name.
    #
    #For example:
    #   for Hank Aaron, nameFull would be 'Hank Aaron', 
	#
	#2) Write the data in the pandas dataFrame to a new csv file located at
	#path_to_new_csv

    df = pandas.read_csv(path_to_csv)
    df['nameFull'] = df['nameFirst']+ " " + df['nameLast']
    df.to_csv(path_to_new_csv)
    return


if __name__ == "__main__":
    # For local use only
    # If you are running this on your own machine add the path to the
    # Lahman baseball csv and a path for the new csv.
    # The dataset can be downloaded from this website: http://www.seanlahman.com/baseball-archive/statistics
    # We are using the file Master.csv
    path_to_csv = "/Users/Miller/GitHub/NanoDegree/Class_Intro_to_DataScience/Lesson2_DataWrangling/lahman_baseball/Master.csv"
    path_to_new_csv = "/Users/Miller/GitHub/NanoDegree/Class_Intro_to_DataScience/Lesson2_DataWrangling/New_master.csv"
    add_full_name(path_to_csv, path_to_new_csv)

# Run the program 
add_full_name(path_to_csv,path_to_new_csv)
