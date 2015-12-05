__author__ = 'Miller'

#**************************************************************************
# Audit Script for OSM data
# - Goal to understand and audit the OSM data, enabling for efficient parsing in the parse script.
#**************************************************************************

import pymongo
import xml.etree.cElementTree as ET
import pprint as pp
import pandas as pd
import re
from collections import defaultdict
import codecs
import json

# Static Values Area
OSMFILE = "/Users/Miller/GitHub/GhNanoDegree/Projects/P3_Data_Wrangling_OpenStreetMap/source/pittsburgh_pennsylvania.osm"
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE) # Looks for the very last word
postal_re = re.compile(r'\d{5}') # Looks for the first 5 digits together.
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons", "Alley", "Circle", "Cove","Expressway","Highway","Pike","Way"]
inside_codes = ["15201","15203","15206","15207","15208","15211","15213","15217","15219","15222","15224","15230","15232","15233"]
outside_codes = ["15202","15209","15223","15225","15228","15229","15231","15236","15237","15238","15239","15240","15241","15242","15243"]
both_codes = ["15204","15205","15210","15212","15215","15214","15216","15218","15220","15221","15226","15227","15234","15235","15120","15106"]
street_mapping = { "St" : "Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Rd.": "Road",
            "Av":"Avenue",
            "Ave.":"Avenue",
            "Blvd":"Boulevard",
            "Blvd.":"Boulevard",
            "Dr":"Drive",
            "Hwy":"Highway",
            "Pl":"Place",
            "Rd":"Road",
            "Sq":"Square",
            }
CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

def auditOSM():
    """
    This function will be commented out for final import, but was used initially to learn about the OSM dataset.
    :return: nothing (but there will be printouts for the user).
    """
    #**************************************************************************
    # ****  User to Uncomment Lines to Gain Results from this Audit Script ****
    #**************************************************************************

    # 1 - Understand the number of tags in the OSM File
    # counts = auditOSMCountTags()
    # print pp.pprint(counts)
    # RESULTS Example:
    # {'bounds': 1,
    #  'member': 17724,
    #  'nd': 1894753,
    #  'node': 1651384,
    #  'osm': 1,
    #  'relation': 1633,
    #  'tag': 1232018,
    #  'way': 168764}

    # 2 - Print out the first XX items's attributes for viewing purposes, starting where defined by user.
    # start = 0
    # num = 2
    # attributes = auditOSMView(start, num)
    # pp.pprint(attributes)

    # 3 - Understand the types of tags in the map file
    global tagtypes
    tagtypes = auditOSMTagsTypes()
    print tagtypes
    # highway               130601
    # name                   92894
    # tiger:cfcc             86435
    # tiger:reviewed         77237
    # tiger:name_base        69860
    # building               65809
    # tiger:name_type        65580
    # addr:street            48705
    # tiger:zip_left         48358
    # addr:postcode          47517
    # addr:housenumber       45916
    # tiger:zip_right        44757
    # tiger:county           31885
    # ...

    # 4 - Check for problem type characters
    # problems = auditOSMProblemChars()
    # pp.pprint(problems)

    # 5 - Check how many unique users
    # users = auditOSMUniqueUsers()
    # pp.pprint(users)
    # print 'Num. of Users: ', len(users)

    # 6 - Check for unusual values as the suffix of street names.
    # global streets
    # streets = auditOSMPStreetSuffix()
    # pp.pprint(dict(streets))

    # 7 - Check the postal codes
    codes = auditOSMPostalCodes()
    pp.pprint(codes)

    pass

def auditOSMCountTags():
    """
    Iteratively parse the map file and count the number of tags.
    :return: dictionary of counts
    """
    d = {}
    tree = ET.iterparse(OSMFILE) # Create an iterparse object
    for _,element in tree:
        d[element.tag] = d.get(element.tag,0) + 1
    return d

def auditOSMView(start, num):
    """
    Iteratively parse the map file starting at the user defined row (start) and for XX tags (num)
    :return: list of dictionarys containing attributes
    """
    tree = ET.iterparse(OSMFILE) # Create an iterparse object
    # Skip to the line defined by the user
    for i in range(start):
        tree.next()
    # Create
    cnt = 0
    l = []
    for _,element in tree:
        if cnt > num: break
        l.append(element.attrib)
        cnt += 1
    return l

def auditOSMTagsTypes():
    """
    Understand the types of tags that are within the map file.
    :return: dictionary of tags with counts
    """
    tree = ET.iterparse(OSMFILE) # Create an iterparse object
    d = {}
    for _,element in tree:
        if element.tag != 'tag': continue
        d[element.attrib['k']] = d.get(element.attrib['k'],0) + 1
    # Create a sorted series
    ser = pd.Series(d)
    ser.sort(ascending = False,inplace = True)
    # Create a CSV File
    ser.to_csv('/Users/Miller/GitHub/GhNanoDegree/Projects/P3_Data_Wrangling_OpenStreetMap/extracted_files/TagTypes.csv',sep='|')
    return ser

def auditOSMProblemChars():
    """
    Check for Problem Characters in the tags.
    :return: dictionary with count of problem characters
    """
    tree = ET.iterparse(OSMFILE) # Create an iterparse object
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _,element in tree:
        if element.tag != 'tag':
            continue
        else:
            if lower.search(element.attrib['k']):
                keys['lower'] += 1
            elif lower_colon.search(element.attrib['k']):
                keys['lower_colon'] += 1
            elif problemchars.search(element.attrib['k']):
                keys['problemchars'] += 1
                # found issue: {'k': 'business tyoe', 'v': 'Insurance Agency'}
            else:
                keys['other'] += 1
    return keys

def auditOSMUniqueUsers():
    """
    Check for unique users
    :return: set of unique users
    """
    tree = ET.iterparse(OSMFILE) # Create an iterparse object
    users = set()
    for _,element in tree:
        try:
            name = element.attrib['uid'] + ' - ' + element.attrib['user']
            users.add(name)
        except:
            pass
    return users

def auditOSMPStreetSuffix():
    """
    Count the different types of street suffixes.
    :return: set of unique users
    """
    tree = ET.iterparse(OSMFILE) # Create an iterparse object
    street_types = defaultdict(set) # Create a defaultdict of set variety.  Allows me to avoid having to check
    # if the key is already in the dictionary.  Its a convenience.
    for _,element in tree:
        if element.tag == 'way': # ensure we are only looking at "Way" tags
            for tag in element.iter('tag'): # for each tag in the "Way"
                if isStreetName(tag): # Check to make sure its a 'addr:street' key
                    auditStreetType(street_types,tag.attrib['v']) # If it is, then audit it

    return street_types

def isStreetName(elem):
    return (elem.attrib['k'] == 'addr:street')

def auditStreetType(street_types,street_name):
    """
    For all 'Way' tags where the key is 'addr:street' check to see if the suffix is in the expected listing.  If not, return add that street name to the dictionary (with the matched item (e.g., 'St') as the key and a
    list of the street names as the value.
    :param street_types: default dict (set variety)
    :param element: the currently iterating element
    :return: nothing - will add to the street types dictionary
    """
    m = street_type_re.search(street_name)
    if m: # If there was a match
        street_type = m.group()
        if street_type not in expected: # If the match (last word) is not in the listing, then add to dictionary
            street_types[street_type].add(street_name)

def auditOSMPostalCodes():
    """
    Understand the postal codes within the data.
    :return:
    """
    tree = ET.iterparse(OSMFILE) # Create an iterparse object
    postals = {}
    for _,element in tree:
        for tag in element.iter('tag'):
            if tag.attrib['k'] == 'addr:postcode':
                postals[tag.attrib['v']] = postals.get(tag.attrib['v'],0) + 1
    # Create a series that is sorted
    ser = pd.Series(postals)
    ser.sort(ascending = False,inplace = True)
    ser.to_csv('/Users/Miller/GitHub/GhNanoDegree/Projects/P3_Data_Wrangling_OpenStreetMap/extracted_files/Postals.csv',sep='|')
    return ser

if __name__ == "__main__":
    # Audit the Data
    auditOSM()



#region Working / Draft Audit Notes
# 1. One problem character - due to space (and typo): {'k': 'business tyoe', 'v': 'Insurance Agency'}
# 2. Issues with street names:
#   a. '519': set(['PA 519', 'Route 519']) - I know that these should both be Route 519
#   b. Many types of streets outside the expected list... Some of which are value (e.g, Alley, Circle, Cove,
# Expressway, Highway, etc.).
#   c. Many types of streets that should be reworked (abbreviations) before adding to db (e.g., Dr, Ave, Ave.,
# Hwy, etc.)
#   d. From this exercise, I can tell there are some PREFIXES that could be cleansed (S to South),
# but this could be tedious.
#   e. No suffix - e.g., 'McAleer': set(['McAleer']) |  'PA-910': set(['PA-910']) | 'PA-982': set(['PA-982'])
#   f. UPDATED the expected list with: "Alley", "Circle", "Cove","Expressway","Highway","Pike","Way"
#   g. Created mapping to make the suffixes more clear.
# 3. Issues with postal codes - All Pittsburgh postal codes start with 15XXX
#   Overall - checking with the postal codes of pittsburgh, there are several postal codes that are not noted as
#  pittsburgh post office zip codes (in, out or both in / out of the city.
#   a. Many that have 9 digit postal code varieties
#   b. Many that are erroneous: 425 1/2, California PA, 15419, PA 15033, PA 15601
#   c. Many that are not even in PA: 26070
#   Conclusion: Replace postals with the correct 5 digit postal code.
#
#
#endregion

#region Other Output for Reference
# Street Suffixes not in the expected list
# {'18': set(['PA 18']),
#  '19': set(['Route 19', 'US 19']),
#  '228': set(['Pennsylvania 228', 'Pennylvania 228']),
#  '519': set(['PA 519', 'Route 519']),
#  '941': set(['941']),
#  'Alley': set(['Oak Alley', 'Summit Alley', 'Taylor Alley']),
#  'Allies': set(['Boulevard of the Allies']),
#  'Av': set(['Center Av']),
#  'Ave': set(['5th Ave',
#              '6th Ave',
#              'Centre Ave',
#              'Elizabeth Ave',
#              'Fifth Ave',
#              'Forbes Ave',
#              'Friendship Ave',
#              'Highland Ave',
#              'Liberty Ave',
#              'Lynnwood Ave',
#              'Morewood Ave',
#              'North Highland Ave',
#              'S Highland Ave',
#              'S Millvale Ave',
#              'S Negley Ave',
#              'S. Aiken Ave',
#              'Shadeland Ave',
#              'Shady Ave',
#              'South Aiken Ave',
#              'University Ave']),
#  'Ave.': set(['4th Ave.', '5th Ave.', 'Macon Ave.', 'Murray Ave.']),
#  'Blvd': set(['Beechwood Blvd']),
#  'Blvd.': set(['Ohio River Blvd.']),
#  'Circle': set(['Glen Spring Circle',
#                 'Hickory Circle',
#                 'Locust Circle',
#                 'Trotwood Circle',
#                 'Winners Circle']),
#  'Cove': set(['Pheasant Cove']),
#  'Dr': set(['Corporate Dr']),
#  'East': set(['Horseshoe Circle East', 'Squaw Run Road East']),
#  'Expressway': set(['Tri-Boro Expressway']),
#  'Highway': set(['Golden Mile Highway',
#                  'Lincoln Highway',
#                  'Old Perry Highway',
#                  'Old William Penn Highway',
#                  'Perry Highway',
#                  'William Penn Highway']),
#  'Hwy': set(['Perry Hwy']),
#  'McAleer': set(['McAleer']),
#  'North': set(['Lakeside Drive North']),
#  'PA-910': set(['PA-910']),
#  'PA-982': set(['PA-982']),
#  'Park': set(['Blueberry Hill Park']),
#  'Pike': set(['Greensburg Pike',
#               'Kittanning Pike',
#               'Northern Pike',
#               'Washington Pike']),
#  'Pl': set(['Washington Pl']),
#  'Plaza': set(['Penn Plaza']),
#  'Rd': set(['Bayard Rd',
#             'Browns Hill Rd',
#             'California Rd',
#             'Camp Hollow Rd',
#             'State Line Rd']),
#  'South': set(['Penn Circle South']),
#  'Sq': set(['Harvard Sq']),
#  'St': set(['8th St',
#             'Castleman St',
#             'First St',
#             'Henry St',
#             'Main St',
#             'N Craig St',
#             'N Dithridge St',
#             'North Bellefield St',
#             'S Craig St',
#             'S Graham St',
#             'S Whitfield St',
#             'Saline St',
#             'South Craig St',
#             'South Dithridge St',
#             'Stanwix St',
#             'Winthrop St',
#             'Wood St']),
#  'St.': set(['West 11th St.']),
#  'Terrace': set(['Garden Terrace']),
#  'Way': set(['Berlin Way',
#              'Burds Way',
#              'Carey Way',
#              'Carriage Way',
#              'Ganchuk Way',
#              'Hager Way',
#              'Hospital Way',
#              'Mackenzie Way',
#              'Marshall Way',
#              'Orchard Way',
#              'Park Way',
#              'Partridge Way',
#              'Towne Square Way',
#              'Trojan Way',
#              'White Way',
#              'Wittenberg Way',
#              'Wrights Way']),
#  'West': set(['Horseshoe Circle West',
#               'Route 40 West',
#               'Waterfront Drive West']),
#  'center': set(['Hillcrest shopping center'])}
# endregion
