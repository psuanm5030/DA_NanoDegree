__author__ = 'Miller'

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Please note that the function 'make_request' is provided for your reference only.
# You will not be able to to actually use it from within the Udacity web UI.
# Your task is to process the HTML using BeautifulSoup, extract the hidden
# form field values for "__EVENTVALIDATION" and "__VIEWSTATE" and set the appropriate
# values in the data dictionary.
# All your changes should be in the 'extract_data' function
from bs4 import BeautifulSoup
import requests
import pprint
import json

html_page = "/Users/Miller/GitHub/DAnanodegree/Class2_DataWrangling/C2L2_ComplexFormats/page_source.html"

# region Solution
def extract_data(page):
    data = {"eventvalidation": "",
            "viewstate": ""}
    with open(page, "r") as html:
        global soup
        soup = BeautifulSoup(html)
        ev = soup.find(id='__EVENTVALIDATION')
        data['eventvalidation'] = ev['value']

        vs = soup.find(id='__VIEWSTATE')
        data['viewstate'] = vs['value']

    html.close()
    return data
# endregion


# region Andy's First try
# def extract_data(page):
#     data = {"eventvalidation": "",
#             "viewstate": ""}
#     with open(page, "r") as html:
#         # do something here to find the necessary values
#         global soup
#         soup = BeautifulSoup(html)
#         # print soup.prettify()
#         #soup.find_all(id='__EVENTVALIDATION')
#         #soup.find_all('input',attrs={'name':"__EVENTVALIDATION"})
#         for item in soup.find_all('input'):
#             if item.get('name') == '__EVENTVALIDATION' : data['eventvalidation'] = item._attr_value_as_string('value')
#             elif item.get('name') == '__VIEWSTATE' : data['viewstate'] = item._attr_value_as_string('value')
#             else:
#                 pass
#     html.close()
#     return data
# endregion


def make_request(data):
    eventvalidation = data["eventvalidation"]
    viewstate = data["viewstate"]

    r = requests.post("http://www.transtats.bts.gov/Data_Elements.aspx?Data=2",
                    data={'AirportList': "BOS",
                          'CarrierList': "VX",
                          'Submit': 'Submit',
                          "__EVENTTARGET": "",
                          "__EVENTARGUMENT": "",
                          "__EVENTVALIDATION": eventvalidation,
                          "__VIEWSTATE": viewstate
                    })

    return r.text


def test():
    data = extract_data(html_page)
    assert data["eventvalidation"] != ""
    assert data["eventvalidation"].startswith("/wEWjAkCoIj1ng0")
    assert data["viewstate"].startswith("/wEPDwUKLTI")


test()