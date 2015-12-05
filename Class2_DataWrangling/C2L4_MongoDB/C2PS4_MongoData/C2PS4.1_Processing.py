__author__ = 'Miller'

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with another type of infobox data, audit it, clean it,
come up with a data model, insert it into a MongoDB and then run some queries against your database.
The set contains data about Arachnid class.
Your task in this exercise is to parse the file, process only the fields that are listed in the
FIELDS dictionary as keys, and return a list of dictionaries of cleaned values.

The following things should be done:
- keys of the dictionary changed according to the mapping in FIELDS dictionary
- trim out redundant description in parenthesis from the 'rdf-schema#label' field, like "(spider)"
- if 'name' is "NULL" or contains non-alphanumeric characters, set it to the same value as 'label'.
- if a value of a field is "NULL", convert it to None
- if there is a value in 'synonym', it should be converted to an array (list)
  by stripping the "{}" characters and splitting the string on "|". Rest of the cleanup is up to you,
  eg removing "*" prefixes etc. If there is a singular synonym, the value should still be formatted
  in a list.
- strip leading and ending whitespace from all fields, if there is any
- the output structure should be as follows:
{ 'label': 'Argiope',
  'uri': 'http://dbpedia.org/resource/Argiope_(spider)',
  'description': 'The genus Argiope includes rather large and spectacular spiders that often ...',
  'name': 'Argiope',
  'synonym': ["One", "Two"],
  'classification': {
                    'family': 'Orb-weaver spider',
                    'class': 'Arachnid',
                    'phylum': 'Arthropod',
                    'order': 'Spider',
                    'kingdom': 'Animal',
                    'genus': None
                    }
}
  * Note that the value associated with the classification key is a dictionary with
    taxonomic labels.
"""
import codecs
import csv
import json
import pprint
import re

DATAFILE = '/Users/Miller/GitHub/GhNanoDegree/Class_DataWrangling/Lesson4_MongoDB/PS4_MongoData/arachnid.csv'
FIELDS ={'rdf-schema#label': 'label',
         'URI': 'uri',
         'rdf-schema#comment': 'description',
         'synonym': 'synonym',
         'name': 'name',
         'family_label': 'family',
         'class_label': 'class',
         'phylum_label': 'phylum',
         'order_label': 'order',
         'kingdom_label': 'kingdom',
         'genus_label': 'genus'}
#
# synonym
# name??
# family
# order
# genus



def process_file(filename, fields):
    import re
    process_fields = fields.keys()
    data = []
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for i in range(3):
            l = reader.next()

        for line in reader:
            dt = {}
            dt[FIELDS['rdf-schema#label']] = parse_regex(line['rdf-schema#label'])
            dt[FIELDS['URI']] = parse_null(line['URI'])
            dt[FIELDS['rdf-schema#comment']] = parse_null(line['rdf-schema#comment'])
            dt[FIELDS['synonym']] = check_array(parse_null(line['synonym']))
            matchObj = re.match(r'[^A-z0-9]',line['name'])
            # print line['name']
            if line['name'] =='NULL' or matchObj:
                dt[FIELDS['name']] = dt[FIELDS['rdf-schema#label']]
                # print 'first', dt[FIELDS['name']]
            else:
                dt[FIELDS['name']] = line['name'].strip()
                # print 'second', line['name']
            dt['classification'] = {
                FIELDS['family_label'] : parse_null(line['family_label']),
                FIELDS['class_label'] : parse_null(line['class_label']),
                FIELDS['phylum_label'] : parse_null(line['phylum_label']),
                FIELDS['order_label'] : parse_null(line['order_label']),
                FIELDS['kingdom_label'] : parse_null(line['kingdom_label']),
                FIELDS['genus_label'] : parse_null(line['genus_label'])
            }
            data.append(dt)
    return data

def parse_item(v):
    pass

def parse_null(v):
    print v
    if v == 'NULL':
        return None
    else:
        return v.strip()

def check_array(v):
    if v != None:
        if v[:1] == '{':
            new = v[1:-1]
            newer = new.split("|")
            newest = [s.split() for s in newer]
            return newer
        else:
            return [v.strip()]
    else:
        return v

def parse_regex(v):
    return re.sub(r'\(\w*\)','',v).strip()

def parse_null(v):
    if v == 'NULL':
        return None
    else:
        return v

def parse_array(v):
    if (v[0] == "{") and (v[-1] == "}"):
        v = v.lstrip("{")
        v = v.rstrip("}")
        v_array = v.split("|")
        v_array = [i.strip() for i in v_array]
        return v_array
    return [v]


def test():
    global data
    data = process_file(DATAFILE, FIELDS)
    print "Your first entry:"
    pprint.pprint(data[0])
    first_entry = {
        "synonym": None,
        "name": "Argiope",
        "classification": {
            "kingdom": "Animal",
            "family": "Orb-weaver spider",
            "order": "Spider",
            "phylum": "Arthropod",
            "genus": None,
            "class": "Arachnid"
        },
        "uri": "http://dbpedia.org/resource/Argiope_(spider)",
        "label": "Argiope",
        "description": "The genus Argiope includes rather large and spectacular spiders that often have a strikingly coloured abdomen. These spiders are distributed throughout the world. Most countries in tropical or temperate climates host one or more species that are similar in appearance. The etymology of the name is from a Greek name meaning silver-faced."
    }

    assert len(data) == 76
    assert data[0] == first_entry
    assert data[17]["name"] == "Ogdenia"
    assert data[48]["label"] == "Hydrachnidiae"
    assert data[14]["synonym"] == ["Cyrene Peckham & Peckham"]

if __name__ == "__main__":
    test()