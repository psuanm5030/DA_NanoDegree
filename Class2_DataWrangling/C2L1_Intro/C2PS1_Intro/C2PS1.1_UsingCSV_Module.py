__author__ = 'Miller'
#!/usr/bin/env python
"""
Your task is to process the supplied file and use the csv module to extract data from it.
The data comes from NREL (National Renewable Energy Laboratory) website. Each file
contains information from one meteorological station, in particular - about amount of
solar and wind energy for each hour of day.

Note that the first line of the datafile is neither data entry, nor header. It is a line
describing the data source. You should extract the name of the station from it.

The data should be returned as a list of lists (not dictionaries).
You can use the csv modules "reader" method to get data in such format.
Another useful method is next() - to get the next line from the iterator.
You should only change the parse_file function.
"""
import csv
import os

DATADIR = "/Users/Miller/GitHub/DAnanodegree/Class2_DataWrangling/C2L1_Intro/C2PS1_Intro/"
DATAFILE = "745090.csv"

# Andy's Second try - using the next() function:
def parse_file(datafile):
    name = ""
    data = []
    with open(datafile,'rb') as f:
        nReader = csv.reader(f, delimiter =',')
        name = nReader.next()[1] # Extracting out the name: MOUNTAIN VIEW MOFFETT FLD NAS
        header = nReader.next() # Putting the header in this variable, but its never used (basicially skiping it)
        next(nReader) # skip past the header row..
        data = list(nReader) # Read in the data into a list.
        # data = [row for row in nReader]  <----- or you can do this
    f.close()
    # Do not change the line below
    return (name, data)

# region Andy's first try:
# def parse_file(datafile):
#     name = ""
#     data = []
#     with open(datafile,'rb') as f:
#         nReader = csv.reader(f, delimiter =',')
#         cnt = 0
#         for line in nReader:
#             if cnt == 0:
#                 name = line[1]
#             elif cnt == 1:
#                 pass
#             else:
#                 data.append(line)
#             cnt += 1
#     f.close()
#     print (name, data)
#     # Do not change the line below
#     return (name, data)
# endregion


def test():
    datafile = os.path.join(DATADIR, DATAFILE)
    global data
    name, data = parse_file(datafile)

    assert name == "MOUNTAIN VIEW MOFFETT FLD NAS"
    assert data[0][1] == "01:00"
    assert data[2][0] == "01/01/2005"
    assert data[2][5] == "2"


if __name__ == "__main__":
    test()