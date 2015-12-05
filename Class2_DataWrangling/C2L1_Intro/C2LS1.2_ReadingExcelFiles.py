__author__ = 'Miller'

#!/usr/bin/env python
"""
Your task is as follows:
- read the provided Excel file
- find and return the min, max and average values for the COAST region
- find and return the time value for the min and max entries
- the time values should be returned as Python tuples

Please see the test function for the expected return format
"""

import xlrd, pprint
from zipfile import ZipFile
datafile = "/Users/Miller/GitHub/DAnanodegree/Class2_DataWrangling/Source_Data/2013_ERCOT_Hourly_Load_Data.xls"

def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()

# Solution from Teacher
def parse_file(datafile):
    workbook = xlrd.open_workbook('{0}.xls'.format(datafile))
    sheet = workbook.sheet_by_index(0)
    data = [[sheet.cell_value(r,col) for col in range(sheet.ncols)] for r in range(sheet.nrows)]

    # List of column values for column 1 (which is the "Coast" Column)
    cv = sheet.col_values(1, start_rowx=1, end_rowx=None)

    maxval = max(cv)
    minval = min(cv)

    maxpos = cv.index(maxval) + 1
    minpos = cv.index(minval) + 1

    maxtime = sheet.cell_value(maxpos, 0)
    realtime = xlrd.xldate_as_tuple(maxtime,0)
    mintime = sheet.cell_value(minpos, 0)
    realmintime = xlrd.xldate_as_tuple(mintime,0)

    try:
        data = {
            'maxtime': realtime,
            'maxvalue': maxval,
            'mintime': realmintime,
            'minvalue': minval,
            'avgcoast': sum(cv) / float(len(cv))
        }
    except:
        data = {
            'maxtime': (0, 0, 0, 0, 0, 0),
            'maxvalue': 0,
            'mintime': (0, 0, 0, 0, 0, 0),
            'minvalue': 0,
            'avgcoast': 0
        }
    return data


# region Andy's Original Solution!
# def parse_file(datafile):
#     workbook = xlrd.open_workbook('{0}.xls'.format(datafile))
#     sheet = workbook.sheet_by_index(0)
#     sheet_data = [[sheet.cell_value(r,col) for col in range(sheet.ncols)] for r in range(sheet.nrows)]
#     checkList = []
#     for k, line in enumerate(sheet_data):
#         if k == 0: continue
#         checkList.append(line[1])
#     # Find the necessary values:
#     min_val = 100000000
#     max_val = 0
#     total = 0
#     cnt = 0
#     for k, val in enumerate(checkList):
#         # Do Average Setup
#         cnt += 1
#         total += val
#         # Do Minimum
#         if val < min_val:
#             min_key = k
#             min_val = val
#         # Do Maximum
#         if val > max_val:
#             max_key = k
#             max_val = val
#
#     ave_val = total / cnt
#
#
#     ### example on how you can get the data
#     #sheet_data = [[sheet.cell_value(r, col) for col in range(sheet.ncols)] for r in range(sheet.nrows)]
#
#     ### other useful methods:
#     # print "\nROWS, COLUMNS, and CELLS:"
#     # print "Number of rows in the sheet:",
#     # print sheet.nrows
#     # print "Type of data in cell (row 3, col 2):",
#     # print sheet.cell_type(3, 2)
#     # print "Value in cell (row 3, col 2):",
#     # print sheet.cell_value(3, 2)
#     # print "Get a slice of values in column 3, from rows 1-3:"
#     # print sheet.col_values(3, start_rowx=1, end_rowx=4)
#
#     # print "\nDATES:"
#     # print "Type of data in cell (row 1, col 0):",
#     # print sheet.cell_type(1, 0)
#     # exceltime = sheet.cell_value(1, 0)
#     # print "Time in Excel format:",
#     # print exceltime
#     # print "Convert time to a Python datetime tuple, from the Excel float:",
#     # print xlrd.xldate_as_tuple(exceltime, 0)
#     print 'check max key: ',max_key
#     min_excel_time = sheet.cell_value(min_key+1,0) # Adjust key for header removed above
#     min_time = xlrd.xldate_as_tuple(min_excel_time,0)
#
#     max_excel_time = sheet.cell_value(max_key+1,0) # Adjust key for header removed above
#     max_time = xlrd.xldate_as_tuple(max_excel_time,0)
#     try:
#         data = {
#             'maxtime': max_time,
#             'maxvalue': max_val,
#             'mintime': min_time,
#             'minvalue': min_val,
#             'avgcoast': ave_val
#         }
#     except:
#         data = {
#             'maxtime': (0, 0, 0, 0, 0, 0),
#             'maxvalue': 0,
#             'mintime': (0, 0, 0, 0, 0, 0),
#             'minvalue': 0,
#             'avgcoast': 0
#         }
#     return data
# endregion


def test():
    open_zip(datafile)
    data = parse_file(datafile)
    pprint.pprint(data)
    assert data['maxtime'] == (2013, 8, 13, 17, 0, 0)
    assert round(data['maxvalue'], 10) == round(18779.02551, 10)


test()