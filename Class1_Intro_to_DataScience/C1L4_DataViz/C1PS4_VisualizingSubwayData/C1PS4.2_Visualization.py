__author__ = 'Miller'
from pandas import *
from ggplot import *

#region Prepare: Import the data
tw = pandas.read_csv('/Users/Miller/GitHub/GhNanoDegree/Class_Intro_to_DataScience/Lesson4_DataViz/PS4_VisualizingSubwayData/turnstile_data_master_with_weather.csv')
#endregion

def plot_weather_data(tw):
    '''
    plot_weather_data is passed a dataframe called turnstile_weather.
    Use turnstile_weather along with ggplot to make another data visualization
    focused on the MTA and weather data we used in Project 3.

    Make a type of visualization different than what you did in the previous exercise.
    Try to use the data in a different way (e.g., if you made a lineplot concerning
    ridership and time of day in exercise #1, maybe look at weather and try to make a
    histogram in this exercise). Or try to use multiple encodings in your graph if
    you didn't in the previous exercise.

    You should feel free to implement something that we discussed in class
    (e.g., scatterplots, line plots, or histograms) or attempt to implement
    something more advanced if you'd like.

    Here are some suggestions for things to investigate and illustrate:
     * Ridership by time-of-day or day-of-week
     * How ridership varies by subway station (UNIT)
     * Which stations have more exits or entries at different times of day
       (You can use UNIT as a proxy for subway station.)

    If you'd like to learn more about ggplot and its capabilities, take
    a look at the documentation at:
    https://pypi.python.org/pypi/ggplot/

    You can check out the link
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv
    to see all the columns and data points included in the turnstile_weather
    dataframe.

   However, due to the limitation of our Amazon EC2 server, we are giving you a random
    subset, about 1/3 of the actual data in the turnstile_weather dataframe.
    '''
    # Top 10 UNITs - with average entries and exits
    gb = tw.groupby('UNIT') # Create a grouped object by UNIT
    gb1 = gb.agg({'ENTRIESn_hourly': np.sum,'EXITSn_hourly': np.sum}) # Sum the number of entries and exits
    gb2 = gb1.sort('ENTRIESn_hourly',ascending = False)[:10] # sort in descending order and take top 10
    gb2['size'] = gb2['ENTRIESn_hourly'] + gb2['EXITSn_hourly']
    plot = ggplot(gb2,aes('ENTRIESn_hourly','EXITSn_hourly',size = 'size')) + \
           geom_point(color = 'red')
    return plot


print plot_weather_data(tw)