__author__ = 'Miller'

from ggplot import *
from pandas import *
import seaborn
pandas.options.mode.chained_assignment = None  # default='warn'

#region Normal Prep Work
# 1 - Prep the main file
mta = pandas.read_csv('/Users/Miller/GitHub/GhNanoDegree/Class_Intro_to_DataScience/PROJECT/turnstile_weather_v2.csv',parse_dates=['DATEn'],index_col = 'DATEn')
mta['day'] = mta.index.day
# 2 - Create a sum by Unit and Day
gbMain = mta.groupby(by=['UNIT','day'])[['ENTRIESn_hourly','EXITSn_hourly']].sum()
gbMain['total'] = gbMain['ENTRIESn_hourly'] + gbMain['EXITSn_hourly']
# 3 - Find top-10 during the period
gb1 = gbMain.groupby(level=0)['total'].sum()
gb1.sort(ascending = False)
gb_top10_total = gb1[:10].reset_index()
gb_top10_total
# 3.1 - Merge back with main data to get weather info
df_temp = mta.copy()
df_temp['unique'] = df_temp['UNIT'] + ' - ' + str(df_temp['day'])

#df_temp.drop_duplicates(subset='unique', inplace = True)
df_weather_unit_day = df_temp[['UNIT','station','day','datetime','hour','day_week','weekday','latitude','longitude','meanprecipi','meanpressurei','meantempi','meanwspdi','weather_lat',	'weather_lon']]
mg = merge(gb_top10_total,df_weather_unit_day,how='left', left_on='UNIT',right_on='UNIT')
#endregion


def timeband(data):
    """
    :param data: takes in a dataframe
    :return: dataframe with time banding based on hour attribute.
    """
    data['timeband'] = 'early morning'
    data['timeband'][(data.datetime.dt.hour > 5) & (data.datetime.dt.hour <= 10)] = 'morning commute'
    data['timeband'][(data.datetime.dt.hour > 10) & (data.datetime.dt.hour < 14)] = 'lunch'
    data['timeband'][(data.datetime.dt.hour >= 14) & (data.datetime.dt.hour < 16)] = 'afternoon'
    data['timeband'][(data.datetime.dt.hour >= 16) & (data.datetime.dt.hour < 20)] = 'evening commute'
    data['timeband'][(data.datetime.dt.hour >= 20) & (data.datetime.dt.hour <= 24)] = 'late evening'
    return data

# General Data Prep
# Copy the data
prp = mta
gb1 = prp.groupby(by=['day','UNIT'])['ENTRIESn_hourly','EXITSn_hourly'].sum()


# Get the average weather values by day
# mta_dateIndex = mta.set_index('DATEn')
# mta_dateIndex.head()
# mta_dateIndex.groupby(mta_dateIndex['DATEn'].map(lambda x: x.day))


# Get the weekends data
df = mta # make copy of data
# df = mta.set_index('DATEn')
# df.index.name = 'date' # you can get the name via: df.index.name



# Top 10 Units by Entries
plot = ggplot(mg,aes('day','total',color='UNIT'))+geom_line()


#region Plotting
# Plot the weekend data
#df1 = df[df['daytype']=='Weekend']
df.set_index('datetime1')
df['day'] = df.datetime1.dt.day
s1 = df.groupby(by=['day'])['ENTRIESn_hourly'].sum()
s2 = df[['day','daytype']].groupby('day').max()
d2 = pandas.DataFrame({'day':range(1,32,1),'count':s1,'daytype':s2['daytype']})
plot = ggplot(d2,aes(x='day',y='count',color='daytype')) + \
            geom_point()
print plot
# plot = ggplot(df,aes(x='ENTRIESn_hourly',color='daytype')) + geom_bar()
# plot
#endregion








#region OTHER
# q_weekend = """
#     SELECT *
#     FROM df
#     WHERE
#     dow > 4
#     """
# q_weekday = """
#     SELECT *
#     FROM df
#     WHERE
#     dow < 5
#     """
# df_weekend = timeband(pandasql.sqldf(q_weekend.lower(), locals()))
# df_weekday = timeband(pandasql.sqldf(q_weekend.lower(), locals()))
#endregion