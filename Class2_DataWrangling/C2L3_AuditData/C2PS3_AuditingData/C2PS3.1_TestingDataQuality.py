__author__ = 'Miller'
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a
cleaning idea and then clean it up. In the first exercise we want you to audit
the datatypes that can be found in some particular fields in the dataset.
The possible types of values can be:
- NoneType if the value is a string "NULL" or an empty string ""
- list, if the value starts with "{"
- int, if the value can be cast to int
- float, if the value can be cast to float, but CANNOT be cast to int.
   For example, '3.23e+07' should be considered a float because it can be cast
   as float but int('3.23e+07') will throw a ValueError
- 'str', for all other values

The audit_file function should return a dictionary containing fieldnames and a
SET of the types that can be found in the field. e.g.
{"field1: set([float, int, str]),
 "field2: set([str]),
  ....
}

All the data initially is a string, so you have to do some checks on the values
first.
"""
import codecs
import csv
import json
import pprint

CITIES = '/Users/Miller/GitHub/DAnanodegree/Class2_DataWrangling/C2L3_AuditData/C2PS3_AuditingData/cities.csv'

FIELDS = ["name", "timeZone_label", "utcOffset", "homepage", "governmentType_label", "isPartOf_label", "areaCode", "populationTotal",
          "elevation", "maximumElevation", "minimumElevation", "populationDensity", "wgs84_pos#lat", "wgs84_pos#long",
          "areaLand", "areaMetro", "areaUrban"]

def audit_file(filename, fields):
    fieldtypes = {}
    for field in FIELDS:
        fieldtypes[field] = set([])
        with open(CITIES,'r') as f:
            reader = csv.DictReader(f)

            for row in reader:
                # SKIP if the row is not applicable:
                if 'dbpedia' not in row['URI']: continue
                # Perform all checks:
                # --- None Type ---
                if row[field] == 'NULL' or row[field] == '':
                    fieldtypes[field].add(type(None))
                elif row[field].startswith('{'):
                    fieldtypes[field].add(type([]))
                else:
                    try:
                        int(row[field])
                        fieldtypes[field].add(type(1))
                    except:
                        try:
                            float(row[field])
                            fieldtypes[field].add(type(1.1))
                        except:
                            fieldtypes[field].add(type('string'))
    return fieldtypes


def test():
    fieldtypes = audit_file(CITIES, FIELDS)

    pprint.pprint(fieldtypes)

    assert fieldtypes["areaLand"] == set([type(1.1), type([]), type(None)])
    assert fieldtypes['areaMetro'] == set([type(1.1), type(None)])

def other():
    with open(CITIES,'r') as f:
        reader = csv.DictReader(f)
        global area1
        area1 = []
        for row in reader:
            val = row['point']
            area1.append(val)

if __name__ == "__main__":
    test()
    other()

