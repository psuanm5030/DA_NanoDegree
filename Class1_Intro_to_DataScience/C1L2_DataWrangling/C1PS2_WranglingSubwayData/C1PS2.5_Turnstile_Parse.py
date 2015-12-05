# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 15:53:27 2015

@author: Miller
"""

import csv

def fix_turnstile_data(filenames):
    '''
    Filenames is a list of MTA Subway turnstile text files. A link to an example
    MTA Subway turnstile text file can be seen at the URL below:
    http://web.mta.info/developers/data/nyct/turnstile/turnstile_110507.txt
    
    As you can see, there are numerous data points included in each row of the
    a MTA Subway turnstile text file. 

    You want to write a function that will update each row in the text
    file so there is only one entry per row. A few examples below:
    A002,R051,02-00-00,05-28-11,00:00:00,REGULAR,003178521,001100739
    A002,R051,02-00-00,05-28-11,04:00:00,REGULAR,003178541,001100746
    A002,R051,02-00-00,05-28-11,08:00:00,REGULAR,003178559,001100775
    
    Write the updates to a different text file in the format of "updated_" + filename.
    For example:
        1) if you read in a text file called "turnstile_110521.txt"
        2) you should write the updated data to "updated_turnstile_110521.txt"

    The order of the fields should be preserved. Remember to read through the 
    Instructor Notes below for more details on the task. 
    
    In addition, here is a CSV reader/writer introductory tutorial:
    http://goo.gl/HBbvyy
    
    You can see a sample of the turnstile text file that's passed into this function
    and the the corresponding updated file in the links below:
    
    Sample input file:
    https://www.dropbox.com/s/mpin5zv4hgrx244/turnstile_110528.txt
    Sample updated file:
    https://www.dropbox.com/s/074xbgio4c39b7h/solution_turnstile_110528.txt
    '''       
    for name in filenames:
        path = "/Users/Miller/GitHub/NanoDegree/Class_Intro_to_DataScience/Lesson2_DataWrangling/PS2_WranglingSubwayData/"
        input = path + name
        output = path +"updated_" + name 
        lst = []
        with open(input,'rb') as f:
            reader = csv.reader(f)
            # Iterate through each row in the file. 
            for row in reader:
                first = row[:3] # Capture the prefix for the row.
                last = row[3:]  # Capture the suffix for the row.
                iterations = len(last)/5 # Determine how many new lines should be created (there are 5 items for each new row)
                sub_lst = [] # Create a blank list to later extend the master list (lst).
                num = 0
                for i in range(iterations): # Iterate based upon the number of iterations previously determined.
                    num = i*5 #Create the value for our index slicing.
                    prefix = first[:] # Make a copy of the prefix.
                    prefix.extend(last[num:num+5]) # Extend the prefix for this line by the next 5 items.
                    sub_lst.append(prefix) # Append the sublist (for this row of data) with the 5 items (plus prefix - so 8 items).
                lst.extend(sub_lst) # Extend the main list by the row sublist.
        with open(output,'wb') as f:# Write the master list to a new file.
            writer = csv.writer(f)
            writer.writerows(lst)
    return

files = ["turnstile_110521.txt","turnstile_110528.txt"]
fix_turnstile_data(files)