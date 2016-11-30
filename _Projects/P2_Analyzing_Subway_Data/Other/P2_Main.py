__author__ = 'Miller'

import pandas as pd
from ggplot import *
import matplotlib.pyplot as plt
from scipy import stats
from datetime import datetime

pd.set_option('display.mpl_style', 'default') # Make the graphs a bit prettier
plt.rcParams['figure.figsize'] = (15, 5)

# Import the data from the provided CSV File
ts = pd.read_csv('/Users/Miller/GitHub/GhNanoDegree/Projects/P2_Analyzing_Subway_Data/Dataset/turnstile_weather_v2.csv')

# region Setup the DF
# Change all column headings to the lowercase form
ts.columns = [x.lower() for x in ts.columns]
ts['c_date'] = pd.to_datetime(ts['daten']) # Convert date to a datetime object
# endregion

ts.head(10) # Show the first 5 rows
ts.info() # Show the structure of the data

# Top 10 - Entries and Exits
# Get the top 10 Units by Entries and Exits - DataFrame
ts_keep = ts.ix[:,['unit','entriesn_hourly','exitsn_hourly']]
ts_top10 = ts_keep.groupby('unit').sum().sort('entriesn_hourly',ascending=False)[:10]
ts_top10.plot(kind='bar')

# Top 10 - Counting Rain during each day by unit
# By day - sum the Entries, Exits and Rain (number of times reporting during the day)
total = ts.groupby(['unit','c_date'])['entriesn_hourly','exitsn_hourly','rain'].sum()
# Reset the index
total = total.reset_index()
# Take the top 10 Units by Entries
totalS1 = total.groupby('unit')['entriesn_hourly'].sum()
totalS1.sort()
totalS2 = totalS1[-10:]
top10_lst = list(totalS2.index)
top10 = total[total['unit'].isin(top10_units)]
top10 = top10.set_index('c_date')

# Single Unit Plot
fig, axes = plt.subplots(1, 1)
top10[top10['unit']=='R179'].ix[:,['entriesn_hourly','exitsn_hourly']].plot(kind='line', ax=axes[0], color='k', alpha=0.7)

# Plot Multiple Unites
cnt = 0
fig, axes = plt.subplots(3, 1)
for unt in top10_lst:
    data = top10[top10['unit']==unt].ix[:,['entriesn_hourly','exitsn_hourly']]
    data.plot(kind='line',ax = axes[cnt],alpha=0.7,linewidth=3)
    #data2 = top10[top10['unit']==unt]['rain']
    #data2.plot(kind='bar',ax = axes[cnt])
    cnt += 1
    if cnt == 3:
        data
        break


data1 = data.ix[:,['entriesn_hourly','exitsn_hourly']]
data2 = top10[top10['unit']==unt]['rain']
data1.plot(kind='line')
data2.plot(kind='bar')

totalUnits = total
rainDays = ts.groupby(['unit','c_date'])['rain'].sum()
rainDays.plot(kind='bar')


# Statistical Analysis






















ts_top10_stk = ts_top10.stack().reset_index(1) # New Stack and Reset
ts_top10_stk.columns = ['type','value'] # Fix the Labels
ts_top10_stk['unit2'] = ts_top10_stk.index


# Get the top 10 Units by Entries and Exits - Create a Series
ts_series = ts.groupby('unit').entriesn_hourly.sum()
ts_series.sort(axis=1,ascending=False)
ts_top10 = ts_series[0:10]
ts_top10

plot_top10 = ggplot(aes(x = 'unit2',y='value',fill='type'),data=ts_top10_stk) + geom_bar(stat = 'identity')
p = ggplot(aes(ts_top10_stk.index,y='value'),ts_top10_stk,fill='type') + geom_bar()

# Setup a New Field Called Week
# datetime.date(2010, 6, 16).isocalendar()[1]
ts['date_dt'] = datetime.datetime.strptime(ts.daten, "%m%d%Y").date()
#datetime.ts['daten'][0].isocalendar()[1]








































































