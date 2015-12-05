# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 17:29:37 2015

@author: Miller
"""

from pandas import *
from ggplot import *
from datetime import *
pandas.options.mode.chained_assignment = None

def plot_weather_data(tw):
    '''
    You are passed in a dataframe called turnstile_weather. 
    Use turnstile_weather along with ggplot to make a data visualization
    focused on the MTA and weather data we used in assignment #3.  
    You should feel free to implement something that we discussed in class 
    (e.g., scatterplots, line plots, or histograms) or attempt to implement
    something more advanced if you'd like.  

    Here are some suggestions for things to investigate and illustrate:
     * Ridership by time of day or day of week
     * How ridership varies based on Subway station (UNIT)
     * Which stations have more exits or entries at different times of day
       (You can use UNIT as a proxy for subway station.)

    If you'd like to learn more about ggplot and its capabilities, take
    a look at the documentation at:
    https://pypi.python.org/pypi/ggplot/
     
    You can check out:
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv
     
    To see all the columns and data points included in the turnstile_weather 
    dataframe. 
     
    However, due to the limitation of our Amazon EC2 server, we are giving you a random
    subset, about 1/3 of the actual data in the turnstile_weather dataframe.
    '''

    # Ridership by day and time of day (banded):
    #plot = ggplot(tw,aes(x='DATEdayname',fill='timebanding')) + geom_bar(position='DATEdow')
    # Ridership by Subway Station (Unit)
    plot = ggplot(tw, aes(x='DATETIME',y='ENTRIESn_hourly')) + \
           geom_point(color='lightblue')

    #Which stations have more exits or entries at different times of day
    # (You can use UNIT as a proxy for subway station.)
    # Create Subset variables - First Weekend
    tw['DAY'] = tw.DATETIME.dt.day
    tw = tw.query('DAY > 6 & DAY < 9') # Queries only
    plot = ggplot(tw, aes('ENTRIESn_hourly','EXITSn_hourly',color='Hour')) + geom_point()
    return plot

#region Prepare the Data
# Import the Data
tw = pandas.read_csv('/Users/Miller/GitHub/GhNanoDegree/Class_Intro_to_DataScience/Lesson4_DataViz/PS4_VisualizingSubwayData/turnstile_data_master_with_weather.csv')

# Turn Date / Time columns into Datetime objects
#   1 - Combine Date and Time fields
tw['DATETIME'] = pandas.to_datetime(tw.DATEn.astype(str) + " " + tw.TIMEn.astype(str))
# tw.DATETIME.dt.hour.value_counts() # Show the hour distribution

#   2 - Turn into Day of Week (0 = Monday, 6=Sunday)
tw['DATEdow'] = tw.DATETIME.dt.dayofweek
tw['DATEdayname'] = 'Monday'
tw['DATEdayname'][tw['DATEdow']==1] = 'Tuesday'
tw['DATEdayname'][tw['DATEdow']==2] = 'Wednesday'
tw['DATEdayname'][tw['DATEdow']==3] = 'Thursday'
tw['DATEdayname'][tw['DATEdow']==4] = 'Friday'
tw['DATEdayname'][tw['DATEdow']==5] = 'Saturday'
tw['DATEdayname'][tw['DATEdow']==6] = 'Sunday'

#   3 - Create time banding
tw['timebanding'] = 'early morning'
tw['timebanding'][(tw.DATETIME.dt.hour > 5) & (tw.DATETIME.dt.hour <= 10)] = 'morning commute'
tw['timebanding'][(tw.DATETIME.dt.hour > 10) & (tw.DATETIME.dt.hour < 14)] = 'lunch'
tw['timebanding'][(tw.DATETIME.dt.hour >= 14) & (tw.DATETIME.dt.hour < 16)] = 'afternoon'
tw['timebanding'][(tw.DATETIME.dt.hour >= 16) & (tw.DATETIME.dt.hour < 20)] = 'evening commute'
tw['timebanding'][(tw.DATETIME.dt.hour >= 20) & (tw.DATETIME.dt.hour <= 24)] = 'late evening'

#   4 - Add dummy units
#dummy_units = pandas.get_dummies(dataframe['UNIT'], prefix='unit')
#endregion



# Perform the Routine
print plot_weather_data(tw)




#region Other - produce bar chart based on time of day
#ts = pandas.DataFrame(tw.DATETIME.dt.hour.value_counts()) # Create DF from counts
#ts['index1']=ts.index # create a new column out of the index
#ts.columns = ['count','index1'] # Rename the columns
#ts1 = ts.sort('index1') # Sort on the new column
#ts1.plot(x='index1',y='count',kind='bar')
#endregion

#region Other - Indexing on the Date value
# Turn time into
#turnstile_weather = turnstile_weather.set_index('DATEn')
#endregion



