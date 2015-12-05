__author__ = 'Miller'
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# All your changes should be in the 'extract_airports' function
# It should return a list of airport codes, excluding any combinations like "All"

from bs4 import BeautifulSoup
html_page = "/Users/Miller/GitHub/DAnanodegree/Class2_DataWrangling/C2L2_ComplexFormats/C2PS2_Complex/options.html"


def extract_airports(page):
    data = []
    with open(page, "r") as html:
        # do something here to find the necessary values
        soup = BeautifulSoup(html, "lxml")
        for item in soup.find_all('option'):
            if len(item['value']) == 3 and item['value'] != 'All' : data.append(item['value'])
    return data


def test():
    data = extract_airports(html_page)
    assert len(data) == 15
    assert "ATL" in data
    assert "ABR" in data

test()