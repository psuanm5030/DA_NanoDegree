__author__ = 'Miller'
# -*- coding: utf-8 -*-
# Find the time and value of max load for each of the regions
# COAST, EAST, FAR_WEST, NORTH, NORTH_C, SOUTHERN, SOUTH_C, WEST
# and write the result out in a csv file, using pipe character | as the delimiter.
# An example output can be seen in the "example.csv" file.

import xlrd
import os
import csv
from zipfile import ZipFile

datafile = "/Users/Miller/GitHub/DAnanodegree/Class2_DataWrangling/C2L1_Intro/2013_ERCOT_Hourly_Load_Data.xls"
outfile = "/Users/Miller/GitHub/DAnanodegree/Class2_DataWrangling/C2L1_Intro/2013_Max_Loads.csv"


def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()

# region Solution
def parse_file(datafile):
    datafile1 = datafile + '.xls'
    workbook = xlrd.open_workbook(datafile1)
    sheet = workbook.sheet_by_index(0)
    data = {}
    for n in range(1,9):
        station = sheet.cell_value(0,n)
        cv = sheet.col_values(n, start_rowx=1, end_rowx=None)

        maxval = max(cv)
        maxpos = cv.index(maxval) + 1
        maxtime = sheet.cell_value(maxpos,0)
        realtime = xlrd.xldate_as_tuple(maxtime,0)
        data[station] = {"maxval": maxval,
                         "maxtime": realtime}
    return data
# endregion

#region Solution
def save_file(data, filename):
    with open(filename,'w') as f:
        w = csv.writer(f,delimiter='|')
        w.writerow(["Station", "Year", "Month", "Day", "Hour", "Max Load"])
        for s in data:
            year, month, day, hour, _ , _= data[s]["maxtime"]
            w.writerow([s, year, month, day, hour, data[s]["maxval"]])
    return
#endregion

# region Andy's First Try
# def parse_file(datafile):
#     datafile1 = datafile + '.xls'
#     workbook = xlrd.open_workbook(datafile1)
#     sheet = workbook.sheet_by_index(0)
#     data = []
#     for i in range(sheet._dimncols-1):
#         if i == 0: continue # Skip the date row
#
#         # Start retrieving values:
#         name = sheet.col_values(i, start_rowx=0, end_rowx=1)[0]
#         print 'NAME: ',name
#         detail = sheet.col_values(i, start_rowx=1, end_rowx=None)
#         maxval = 0
#         maxpos = None
#         for k,v in enumerate(detail):
#             if v > maxval:
#                 maxval = v
#                 maxpos = k
#
#         maxtime = sheet.cell_value(maxpos+1,0)
#         realtime = xlrd.xldate_as_tuple(maxtime,0)
#         # Create interim list for the column, then append to the return list.
#         interimList = [name,realtime[0],realtime[1],realtime[2],realtime[3],maxval]
#         data.append(interimList)
#     # Remember that you can use xlrd.xldate_as_tuple(sometime, 0) to convert
#     # Excel date to Python tuple of (year, month, day, hour, minute, second)
#     return data
# endregion

# region Andy's First Try
# def save_file(data, filename):
#     lst = ['Station','Year','Month','Day','Hour','Max Load']
#     with open(filename,'wb') as cv:
#         nWriter = csv.writer(cv,delimiter='|')
#         nWriter.writerow(lst)
#         for row in data:
#             nWriter.writerow(row)
#     return
# endregion


def test():
    open_zip(datafile)
    data = parse_file(datafile)
    save_file(data, outfile)

    number_of_rows = 0
    stations = []

    ans = {'FAR_WEST': {'Max Load': '2281.2722140000024',
                        'Year': '2013',
                        'Month': '6',
                        'Day': '26',
                        'Hour': '17'}}
    correct_stations = ['COAST', 'EAST', 'FAR_WEST', 'NORTH',
                        'NORTH_C', 'SOUTHERN', 'SOUTH_C', 'WEST']
    fields = ['Year', 'Month', 'Day', 'Hour', 'Max Load']

    with open(outfile) as of:
        csvfile = csv.DictReader(of, delimiter="|")
        for line in csvfile:
            station = line['Station']
            if station == 'FAR_WEST':
                for field in fields:
                    # Check if 'Max Load' is within .1 of answer
                    if field == 'Max Load':
                        max_answer = round(float(ans[station][field]), 1)
                        max_line = round(float(line[field]), 1)
                        assert max_answer == max_line

                    # Otherwise check for equality
                    else:
                        assert ans[station][field] == line[field]

            number_of_rows += 1
            stations.append(station)

        # Output should be 8 lines not including header
        assert number_of_rows == 8

        # Check Station Names
        assert set(stations) == set(correct_stations)


if __name__ == "__main__":
    test()
