__author__ = 'Miller'
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# So, the problem is that the gigantic file is actually not a valid XML, because
# it has several root elements, and XML declarations.
# It is, a matter of fact, a collection of a lot of concatenated XML documents.
# So, one solution would be to split the file into separate documents,
# so that you can process the resulting files as valid XML documents.

import xml.etree.ElementTree as ET
PATENTS = '/Users/Miller/GitHub/GhNanoDegree/Class_DataWrangling/Lesson2_ComplexFormats/PS2_Complex/data/patent.data'

def get_root(fname):
    tree = ET.parse(fname)
    return tree.getroot()


def split_file(filename):
    # we want you to split the input file into separate files
    # each containing a single patent.
    # As a hint - each patent declaration starts with the same line that was causing the error
    # The new files should be saved with filename in the following format:
    # "{}-{}".format(filename, n) where n is a counter, starting from 0.
    with open(filename,'r') as data:
        instances = 0
        intList = []
        lineCnt = 0
        global d
        d = []
        for line in data:
            d.append(line) #add data to a list
            if "<?xml version" in line:
                instances += 1
                intList.append(lineCnt)
            lineCnt += 1
        print intList
        for n in range(len(intList)):
            if n < 3:
                with open("{}-{}".format(filename, n),'w') as f:
                    f.writelines(d[intList[n]:intList[n+1]])
            else:
                with open("{}-{}".format(filename, n),'w') as f:
                    f.writelines(d[intList[n]:])


        # for line in data:
        #     print line
        #     with open("{}-{}".format(filename, n),'w') as f:
        #         f.write(line)
        #         if "<?xml version" in line:
        #             n += 1
        #             continue




    # with open(filename,'r') as data:
    #     countList = []
    #     cntLine = 0
    #     instances = 0
    #     for line in data:
    #         if "<?xml version" in line:
    #             instances+=1
    #             countList.append(cntLine)
    #         cntLine+=1
    #     # Start parsing
    #     for n in instances:
    #         if n != 4:
    #             with open("{}-{}".format(filename, n),'w') as f:


    # print instances
    # print countList
    #
    return

def test():
    split_file(PATENTS)
    for n in range(4):
        try:
            fname = "{}-{}".format(PATENTS, n)
            f = open(fname, "r")
            if not f.readline().startswith("<?xml"):
                print "You have not split the file {} in the correct boundary!".format(fname)
            f.close()
        except:
            print "Could not find file {}. Check if the filename is correct!".format(fname)


test()