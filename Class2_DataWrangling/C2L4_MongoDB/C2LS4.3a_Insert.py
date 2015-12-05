__author__ = 'Miller'

#!/usr/bin/env python
"""
Add a single line of code to the insert_autos function that will insert the
automobile data into the 'autos' collection. The data variable that is
returned from the process_file function is a list of dictionaries, as in the
example in the previous video.
"""

# FYI - Had to bring in the function from the Autos.py file because python was complaining that it couldnt find
# the module.
# from autos import process_file

# def process_file(input_file):
#     input_data = csv.DictReader(open(input_file))
#     autos = []
#     skip_lines(input_data, 3)
#     for row in input_data:
#         auto = {}
#         model_years = {}
#         production_years = {}
#         dimensions = {}
#         for field, val in row.iteritems():
#             if field not in fields or empty_val(val):
#                 continue
#             if field in ["bodyStyle_label", "class_label", "layout_label"]:
#                 val = val.lower()
#             val = strip_automobile(val)
#             val = strip_city(val)
#             val = val.strip()
#             val = parse_array(val)
#             if field in ["length", "width", "height", "weight", "wheelbase"]:
#                 clean_dimension(dimensions, field_map[field], val)
#             elif field in ["modelStartYear", "modelEndYear"]:
#                 clean_year(model_years, field_map[field], val)
#             elif field in ["productionStartYear", "productionEndYear"]:
#                 clean_year(production_years, field_map[field], val)
#             else:
#                 auto[field_map[field]] = val
#         if dimensions:
#             auto['dimensions'] = dimensions
#         auto['modelYears'] = years(row, 'modelStartYear', 'modelEndYear')
#         auto['productionYears'] = years(row, 'productionStartYear', 'productionEndYear')
#         autos.append(auto)
#     return autos

from autos import process_file

def insert_autos(infile, db):
    data = process_file(infile)
    # Add your code here. Insert the data in one command.
    db.autos.insert_many(data)


if __name__ == "__main__":
    # Code here is for local use on your own computer.
    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017")
    db = client.examples

    insert_autos('/Users/Miller/GitHub/DAnanodegree/Class2_DataWrangling/C2L4_MongoDB/autos.csv', db)
    print db.autos.find_one()