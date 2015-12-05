__author__ = 'Miller'

#**************************************************************************
# Parsing Script for OSM data
# - Goal to read each element, scrub & cleanse, then write to a JSON File
#**************************************************************************

import xml.etree.cElementTree as ET
import re
import codecs
import json

# region Static Values Area
OSMFILE = "/Users/Miller/GitHub/GhNanoDegree/Projects/P3_Data_Wrangling_OpenStreetMap/source/pittsburgh_pennsylvania.osm"
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE) # Looks for the very last word
postal_re = re.compile(r'\d{5}') # Looks for the first 5 digits together.
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons", "Alley", "Circle", "Cove","Expressway","Highway","Pike","Way"]
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
# endregion

def shapeElement(element):
    """
    This function will cleanse each element as the file is iterated over.  The cleansing will address:
    1. Issues with street names (making them more consistent - e.g., St to Street)
    2. Issues with postal codes (keeping only the 5 digit portion and denoting the erroneous values as '00000')
    3. Keeping only necessary data and forming into defined structure.
    :return: Dictionary containing each relevant tag in the element
    """
    node = {} # dictionary that will be filled with the elements details through this function
    if element.tag != "node" and element.tag != "way" : return None
    for elt in element.iter():
        if elt.tag == 'tag':
            # 0 - Check for items that should be skipped (Problem characters and multiple colons)
            if checkSkipItems(elt):
                continue
            # 1 - Address Cleansing
            elif 'addr:' in elt.attrib['k']: # clean up the address detail
                cleanAddress(elt,node)
                continue
            else:
                node[elt.attrib['k']] = elt.attrib['v']
                continue
        # 2 - Nd Tag Cleansing
        elif elt.tag == 'nd':
            if 'node_refs' not in node: node['node_refs']=[]
            node['node_refs'].append(elt.attrib['ref'])
        # 3 - All other tags
        else:
            if 'type' not in node: node['type'] = elt.tag
            for key,val in elt.attrib.iteritems():
                if key in CREATED:
                    if 'created' not in node: node['created'] = {}
                    node['created'][key] = val
                elif key == 'lat' or key == 'lon':
                    if 'pos' not in node: node['pos'] = []

                    if key == 'lat':
                        node['pos'].insert(0,float(val))
                    else:
                        node['pos'].insert(1,float(val))
                else:
                    node[key] = val
    return node

def checkSkipItems(elt):
    """
    Function to check if the item in the element should be skipped.
    :param elt: the element under review at the time
    :return: boolean
    """
    # Skipping any items that match a problem character in the element key or if the key contains more than one
    # colon.
    return ((problemchars.search(elt.attrib['k'])) or (elt.attrib['k'].count(':') > 1))

def cleanAddress(elt,node):
    """
    Return a properly formed address dictionary
    FROM THIS:
    <tag k="addr:housenumber" v="5158"/>
    <tag k="addr:street" v="North Lincoln Avenue"/>
    <tag k="addr:street:name" v="Lincoln"/>
    <tag k="addr:street:prefix" v="North"/>
    <tag k="addr:street:type" v="Avenue"/>
    <tag k="amenity" v="pharmacy"/>

    TO THIS:
    {...
    "address": {
        "housenumber": 5158,
        "street": "North Lincoln Avenue"
    }
    :param elt: the element under review at the time
    :return: nothing - the node passed in is written with the appropriate data
    """
    if 'address' not in node: node['address']={} # Create dict if not yet created for this set.

    newKey = elt.attrib['k'].replace('addr:','')
    # print 'here is new key: ',newKey
    if newKey == 'street':
        node['address'][newKey] = cleanStreet(elt.attrib['v'])
    elif newKey == 'postcode':
        node['address'][newKey] = cleanPostal(elt.attrib['v'])
    else:
        node['address'][newKey] = elt.attrib['v']
    return

def cleanStreet(name):
    """
    Clean up the street names according to the mapping, unless the street name is expected (per the listing).
    :param elt: the element under review at the time
    :return: cleaned street name as a string
    """
    m = street_type_re.search(name)
    if m:
        street_type = m.group()
        if street_type in expected:
            return name
        else: # Else - iterate through the mapping dictionary for the item and replacement.  Make replacement.
            for k, v in street_mapping.iteritems():
                if k in name:
                    name = re.sub(k, v, name)
                    return name
            return name

def cleanPostal(name):
    """
    Clean up the postal codes according to the mapping, unless the street name is expected (per the listing).
    :param elt: the element under review at the time
    :return: cleaned post code as a string
    """
    m = postal_re.search(name)
    if m:
        clean_postal = m.group()
        return clean_postal
    else:
        return '00000'

def process_map(file_in, pretty = False):
    """
    This function controls the entire process where each element is reviewed and cleansed.
    :param file_in: OSM file (iteratively parsed one by one)
    :param pretty: defines the output written to the JSON file
    :return: list of cleansed elements
    """
    file_out = "{0}.json".format(file_in[:-4])
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shapeElement(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

if __name__ == "__main__":
    # global data
    data = process_map(OSMFILE,True)
    print 'Done Processing file...'
