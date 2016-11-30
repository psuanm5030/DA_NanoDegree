
# P3: Wrangle OpenStreetMap Data
### Student: Andy Miller
#### Map Area: Pittsburgh, Pennsylvania [Link to MapZen OSM Download Page](https://mapzen.com/data/metro-extracts)

#### December 4th 2015

### Overview
#### I selected my hometown of Pittsburgh, PA to complete this project.  Using the MongoDB Data Wrangling lecture problems and problem sets as my foundation, I believe I have sufficiently audited, parsed and explored this dataset.  

#### The following is a list of the steps I took to complete this project:
1. Downloaded the OSM XML data for Pittsburgh (via Mapzen).  The file was 372.9 MB (5,214,306 lines).
2. Iteratively audited the data using Python (Proj_1.1_Audit_XML.py).
3. Iteratively parsed and cleansed the data into a JSON file (Proj_1.2_Parse_to_JSON.py).  The JSON file was 528.1 MB.
4. Imported the JSON file into a MongoDB database and collection.  1,820,148 documents were imported.
5. Analyzed the new collection using pymongo in python by creating pipelines that queried the collection (Proj_1.3_Review.py).

#### Below, I present several major areas of discussion as I progressed through this project.

It should be noted that I re-wrote all the class scripts locally, adding my own efficiencies and documentation, to audit, parse and review the OSM Pittsburgh data.

### 1. Problems Encountered in the Map
Overall, it should be noted that I encountered relatively minor issues when reviewing the data in python. They are listed below:  

##### Postal Codes 
* Pittsburgh zip codes most commonly begin with 15, however I noticed there were 13 zip codes that did not start with 15. Upon further review, I noticed that the dataset contained more than simply Pittsburgh Metro [Link for MapZen](https://mapzen.com/data/metro-extracts) - it contained more more expansive data.  I chased down each of the 13 postal codes and noted they were appropriate (most were in neighboring Ohio and West Virginia).  
* During the audit process, I noticed some erroneous looking postal codes: "425 1/2", "California PA, 15419", "PA 15033, and "PA 15601".  With the exception of "425 1/2", I noticed these items actually had a legitimate zip code.  Therefore, when parsing (script Proj_1.2_Parse_to_JSON.py), I wrote a function "cleanPostal" which returned the first 5 digits together.  This enabled "California PA, 15419" to be input as "15419", discarding "California PA,".  Additionally, this took care of instances where the 9 digit postal code was noted (something I was not interested in keeping).  If the regular expression could not be matched, "00000" was returned (signaling to me the erroneous items, but still fitting the format).  

##### Street Mapping
* As discussed during the class, I made several additions the the mapping dictionary to ensure that items such as "Sq" were replaced with "Square".  I made 13 such mappings, 3 of which were related to variations of avenue.  Further, I made many additions to the expected list to ensure that items such as Circle, Cove, and Pike were deemed acceptable (among others).

##### Problem Characters
* Luckily, there was only one tag type with a problem character present - a space, which actually coincided with a typo in the amenity tag name --> {'k': 'business tyoe', 'v': 'Insurance Agency'} - this item was excluded during the parsing phase (see function checkSkipItems).  This led me to some conclusions regarding the depth of data - particularly that there are alot of tags types (1,038 to be exact). Of those I noted:
    - Highway, Name and several tiger fields were most popular.
    - 853 of the 1,038 tag types were used less than 100 times. 379 of these 853 were only used once!  
    - Upon further review, many of these belong to relation elements and therefore are correctly ignored during my parsing process.
    

---
### 2. Understanding the Data
I spent nearly 6 hours working through the parsing scripts (from class) again, ensuring that I understood everything that was happening, however I believe I may have spent a similar amount of time exploring the data in MongoDB - through pipelines created in python (via pymongo package) and in the mongo shell.  Here is detail that I thought interesting from this exercise:  

##### Overview of the Pittsburgh Dataset
* Size of the file 
> \> db.pittsburgh.count() <br>
> 1820148
> <br>
> \> db.pittsburgh.totalSize() <br>
> 689370976 
* Number of unique users 
> \> db.pittsburgh.distinct("created.user").length <br>
> 1093
* Number of nodes and ways 
> \> db.pittsburgh.find({'type':'node'}).count() <br>
> 1651346
> <br>
> \> db.pittsburgh.find({'type':'way'}).count() <br>
> 168740
* Search for golf courses - Unfortunately, this yields no results!  :( <br>
> \> db.pittsburgh.find({'amenity':{'$regex':'golf'}}) <br>
> 0
* Unfortunately, stripclubs ARE present!  But not golf courses?  Surprising!! 
> \> db.pittsburgh.find({'amenity':{'\$regex':'strip'}},{'name':1,'_id':0}) <br>
\> { "name" : "Blush" } <br>
\> { "name" : "Cheerleaders" } <br>
\> { "name" : "Silky's Gentleman's Club" } <br>
\> { "name" : "Club Erotica Gentleman's Club" } <br>


---
### 3. Other Ideas about this Dataset
Now I am having some fun with pipelines, including all the various pipeline operators.  These operations were performed in the Proj_1.3_Review.py script, using the pymongo package.  Here are some of the interesting ideas I had and the resulting conclusions I came to:

#### Idea 1: I wanted to understand the amenities that had the most unique user creators. The reason for this was to guage the participation from the community and to understand what items motivated others to get involved.  
<br>_Pipeline Code:_
```python
def make_pipeline_tag_type_distinct_users():
    pipeline = [{'$match':{'amenity':{'$exists':1}}},
                {'$group':{'_id':{'amenity':'$amenity'},
                           'users_distinct':{'$addToSet':'$created.user'}}},
                {'$project':{'amenity':1,
                             'users_distinct':{'$size':'$users_distinct'},
                             'count_amenities':1}},
                {'$sort':{'users_distinct':-1}},
                {'$limit':10}]
    return pipeline
```

_Results:_
```python
[{u'_id': {u'amenity': u'restaurant'}, u'users_distinct': 147},
 {u'_id': {u'amenity': u'parking'}, u'users_distinct': 141},
 {u'_id': {u'amenity': u'school'}, u'users_distinct': 125},
 {u'_id': {u'amenity': u'place_of_worship'}, u'users_distinct': 121},
 {u'_id': {u'amenity': u'fuel'}, u'users_distinct': 78},
 {u'_id': {u'amenity': u'library'}, u'users_distinct': 73},
 {u'_id': {u'amenity': u'fast_food'}, u'users_distinct': 65},
 {u'_id': {u'amenity': u'bank'}, u'users_distinct': 57},
 {u'_id': {u'amenity': u'post_office'}, u'users_distinct': 55},
 {u'_id': {u'amenity': u'pharmacy'}, u'users_distinct': 53}]
```

#### Conclusion 1: I found that restaurants were number 1, with 147 unique users creating these tags.  This was of little surprise, as restuarants are constently opening / shutting down.  Maybe there are some owners that thought it was important to get their establishment listed within OSM data (obviously the more places your establishment is defined, the more traffic you can drive to your business).  Further, I imagine it is difficult for one user to cover them all, with the thought that regular contributors are not checking / editing to ensure restaurants are accurately reflected / updated.  

#### Improvement 1: Below is a listing of 10 amenities that had only one tag within the data.  Knowing my city, I know that there are more than one trailer park or ev charinging station.  
<br>_Pipeline Code:_
```python
def make_pipeline_tag_type_distinct_users():
    pipeline = [{'$match':{'amenity':{'$exists':1}}},
                {'$group':{'_id':{'amenity':'$amenity'},
                           'users_distinct':{'$addToSet':'$created.user'}}},
                {'$project':{'amenity':1,
                             'users_distinct':{'$size':'$users_distinct'},
                             'count_amenities':1}},
                {'$sort':{'users_distinct':1}},
                {'$limit':10}]
    return pipeline
```

_Results:_
```python
[{u'_id': {u'amenity': u'trailer_park'}, u'users_distinct': 1},
 {u'_id': {u'amenity': u'gambling'}, u'users_distinct': 1},
 {u'_id': {u'amenity': u'shower'}, u'users_distinct': 1},
 {u'_id': {u'amenity': u'rental'}, u'users_distinct': 1},
 {u'_id': {u'amenity': u'storage'}, u'users_distinct': 1},
 {u'_id': {u'amenity': u'ev_charging'}, u'users_distinct': 1},
 {u'_id': {u'amenity': u'compressed_air'}, u'users_distinct': 1},
 {u'_id': {u'amenity': u'bleachers'}, u'users_distinct': 1},
 {u'_id': {u'amenity': u'education_centre'}, u'users_distinct': 1},
 {u'_id': {u'amenity': u'watering_place'}, u'users_distinct': 1}]
```
 
#### Improvement 1 (continued): How could we improve upon this?  My favorite idea is "gamification" - the practice of turning tasks (e.g., data entry for OSM data) into a game / contest - where users are rewarded with points for helping improve the quality and robustness of their data.  The points system would be wise to take into account amenities / areas that are not being well covered (e.g., increase the points offered for minimally covered amenities).  However, the points system should have some validation and monitoring, as some users may go to the extreme (and falsify entries to get points, especially items that award them more points).  It would be wise to implement a system to track and notify administrators of "fast-rising users" or users that present suspicious patterns of data entry (e.g., adding public toilets at a high right in a small area).**

---
#### Idea 2: After investigating all the amenities noted, I noticed there were three (3) casinos noted, so I wanted to find out which ones. I wanted to validate my knowledge! 
<br>_Pipeline Code:_
```python
def make_pipeline_amenity_casino():
    # Purpose: Investigate the 3 casinos that were noted.  This shows the names of the casinos that were noted.
    # This is of interest as the casino industry is relatively new in Pittsburgh and there are two major
    # casinos: Rivers Casino and The Meadows Casino and Racetrack.
    pipeline = [{'$match':{'amenity':'casino'}},
                {'$project':{'name':1,
                             '_id':0,
                             'address':1}}]
    return pipeline
```

_Results:_
```python
[{u'address': {u'city': u'Pittsburgh',
               u'housenumber': u'777',
               u'postcode': u'15233',
               u'state': u'PA',
               u'street': u'Casino Drive'},
  u'name': u'Rivers Casino'},
 {u'name': u'Mountaineer Casino'},
 {u'name': u'Mountaineer Casino, Racetrack and Resort'}]
```

#### Conclusion 2: When I saw the listing of casinos noted, I was immediately surprised.  I expected: Rivers Casino, Moutaineer Casino (actually in West Virginia) and the Meadows Racetrack Casino. The Meadows Racetrack Casino was not listed and the Mountaineer Casino was listed twice, under two similar names.  There were two issues here: 
    - The "Mountaineer" entries seem to be duplicates and "The Meadows Casino and Racetrack" wasnt listed! 
    - There is no address detail for the last two (Mountaineer Casino and Mountaineer Casino, Racetrack and Resort).  This further prevented me from understanding whether someone named the "Mountaineer Casino, Racetrack and Resort" wrong (when it could be "Meadows Casino, Racetrack and Resort" (that was a longshot).  But most importantly, the detail wasnt there (and probably should be). 
    
#### Improvement 2: These situations could be improved in two distinct ways: 
    - 1) Add an algorithm to detect potential duplicates.  One of my favorite packages for reviewing for duplicates is fuzzywuzzy [link to github repo](https://github.com/seatgeek/fuzzywuzzy).  This allows you to perform duplicate searching using the following fuzzy matching methods: Levenshtein distance, token sort, and token set. These functions generate scores (e.g., 90 / 100 potential match), which could be reviewed.  This would likely have noted the 'Mountaineer Casino' & 'Mountaineer Casino, Racetrack and Resort' items for review by an administrator (would have been scored 100 on the token set method). 
    - 2) Second, and much more advanced, there could be some checking with other external sources, such as Yelp or Google, via their API.  This could be done in a basic way, building on the gamification theme presented above, where areas of a map are compared with yelp or google via their APIs (e.g., compare the number of restaurants), where shortfalls in the OSM data leads to campaigns to improve the data in that area.  Users would received a multiple (e.g., 2X or 4X) of the standard amount of points for entering data.

---
#### Idea 3: I also wanted to check out the postal codes that I have lived in!  Below is the code I used to find only those items for the two post codes (15317 and 15222).     
<br>_Pipeline Code:_
```python
def make_pipeline_postal_specific():
    # Further investigate the cities for a list of specific postal codes (where I have lived).
    pipeline = [{'$match':{'address.postcode': {'$in': ['15317', '15222'] }}},
                {'$group':{'_id':{'postcode':'$address.postcode','city':'$address.city'},
                           'count':{'$sum':1}}},
                {'$sort':{'count':-1}}]
    return pipeline
```

_Results:_
```python
[{u'_id': {u'city': u'Canonsburg', u'postcode': u'15317'}, u'count': 2424},
 {u'_id': {u'postcode': u'15317'}, u'count': 284},
 {u'_id': {u'city': u'Pittsburgh', u'postcode': u'15222'}, u'count': 253},
 {u'_id': {u'postcode': u'15222'}, u'count': 4},
 {u'_id': {u'city': u'McMurray', u'postcode': u'15317'}, u'count': 1}]
```

#### Conclusion 3: This presents another shortfall of the OSM data. 
    - First I didnt return two (2) results, but four (4).  This means that 284 (for post code 15317) & 4 elements (for post code 15222) didnt have the associated city name.  
    - Second: Post code 15222 is a more prominent zip code in the city of pittsburgh (I lived in Shadyside at one point - a very hip area to live in), but it had less items than 15317.  Yes, I understand that 15317 probably covers more area, but I was still surprised, as there is a great number of amenities within 15222 (restaurants, shops, business, hospitals).  
    - Finally: If I had more time and curiosity, I would want to investigate just how significant this thought is (whats the area covered by each post code).  That will be for another time!

#### Improvement 3: I will conclude with strengthening my gamification point of view here - noting this is another situation which could be improved through this approach.  An alogrithm could easily be developed which identifies complimentary data which is not complete (e.g., postcode without a city, restaurant without a "cuisine" tag, etc.).  Users could be rewarded with points for filling in these missing data points.
