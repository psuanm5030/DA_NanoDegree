# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 14:40:25 2015

@author: Miller
"""

import json
import requests
import pprint

# Andy note - Udacity provided the country and API key parameters.

def api_get_request(url):
    # In this exercise, you want to call the last.fm API to get a list of the
    # top artists in Spain.
    #
    # Once you've done this, return the name of the number 1 top artist in Spain.
    data = requests.get(url).text
    data = json.loads(data)
    pp = pprint.PrettyPrinter(indent=2)
    #pp.pprint(data)
    top = data['topartists']['artist'][0]['name']
    return top # return the top artist in Spain