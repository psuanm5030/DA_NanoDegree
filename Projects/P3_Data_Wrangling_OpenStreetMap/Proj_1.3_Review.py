__author__ = 'Miller'

import pprint as pp

#**************************************************************************
# Review Script for Loaded MongoDB data
# - Goal to write and run pipelines against the MongoDB data, in an effort to better understand the data.
#**************************************************************************

# region Import MongoDB syntax (not python related)
# ~ MongoDB Import JSON Syntax (for use in the command line) ~
# cd /Users/Miller/GitHub/GhNanoDegree/Class_DataWrangling/Project/
# mongoimport --db projects --collection pittsburgh --drop --file pittsburgh_pennsylvania.json
# ~ imports 503.7 MB ~
# endregion

# region Below is a sample of the data structure / schema.
"""
Common Structure of the data:
{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}
"""
# endregion

def get_db(db_name):
    """
    Function to create a connection to the mongoDB database.
    :param db_name: name of the database
    :return: db object
    """
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db

# Pipeline Section -- This section includes the pipelines that were used to explore the data.

def make_pipeline_amenity():
    # List the amenities with their respective counts (in descending order).
    pipeline = [{'$match':{'amenity':{'$exists':1}}},
                {'$group':{'_id':'$amenity',
                           'count':{'$sum':1}}},
                {'$sort':{'count':-1}}]
    return pipeline

def make_pipeline_amenity_casino():
    # Purpose: Investigate the 3 casinos that were noted.  This shows the names of the casinos that were noted.
    # This is of interest as the casino industry is relatively new in Pittsburgh and there are two major
    # casinos: Rivers Casino and Meadows Casino and Racetrack.
    pipeline = [{'$match':{'amenity':'casino'}},
                {'$project':{'name':1,
                             '_id':0,
                             'address':1}}]
    return pipeline

def make_pipeline_amenity_golf():
    # Look for any golf courses, using regex.  Return the name and city (if available).
    pipeline = [{'$match':{'amenity':{'$regex':'golf'}}},
                {'$project':{'name':1,
                             '_id':0,
                             'address.city':1}}]
    return pipeline

def make_pipeline_amenity_cafe():
    # Look for any cafes, using regex. Return the name and city (if available).
    pipeline = [{'$match':{'amenity':{'$regex':'cafe'}}},
                {'$project':{'name':1,
                             '_id':0,
                             'address.city':1}}]
    return pipeline

def make_pipeline_postal():
    # Investigate the postal codes, counting the number of entries per postal code.
    pipeline = [{'$match':{'address.postcode':{'$exists':1}}},
                {'$group':{'_id':'$address.postcode',
                           'count':{'$sum':1}}},
                {'$sort':{'count':-1}}]
    return pipeline

def make_pipeline_postal_specific():
    # Further investigate the cities for a list of specific postal codes (where I have lived).
    pipeline = [{'$match':{'address.postcode': {'$in': ['15317', '15222'] }}},
                {'$group':{'_id':{'postcode':'$address.postcode','city':'$address.city'},
                           'count':{'$sum':1}}},
                {'$sort':{'count':-1}}]
    return pipeline

def make_pipeline_tag_type_distinct_users():
    # Calculate the number of distinct users creating each amenity.  The purpose of this is to try and
    # understand the amenities that get the most user participation.
    # The pipeline returns a sorted list (descending) of the top 10 distinct user created amenities.
    pipeline = [{'$match':{'amenity':{'$exists':1}}},
                {'$group':{'_id':{'amenity':'$amenity'},
                           'users_distinct':{'$addToSet':'$created.user'}}},
                {'$project':{'amenity':1,
                             'users_distinct':{'$size':'$users_distinct'},
                             'count_amenities':1}},
                {'$sort':{'users_distinct':1}},
                {'$limit':10}]
    return pipeline

def data_overview():
    # Display some varying facts about the dataset:
    # print 'Number of Documents in Collection: ',db.pittsburgh.count()
    print 'Pittsburgh Collection Stats: '
    pp.pprint(db.command("collstats", "pittsburgh"))
    return

def aggregate(db, pipeline):
    """
    Function to take the pipeline and return a list of items for printing.
    :param db: Connection to MongoDB
    :param pipeline: the actual query
    :return: list of the query results
    """
    return [doc for doc in db.pittsburgh.aggregate(pipeline)]

if __name__ == '__main__':
    db = get_db('projects')
    # data_overview()
    # pipeline = make_pipeline_amenity()
    # pipeline = make_pipeline_amenity_casino()
    # pipeline = make_pipeline_amenity_golf()
    # pipeline = make_pipeline_amenity_cafe()
    # pipeline = make_pipeline_postal()
    # pipeline = make_pipeline_postal_specific()
    pipeline = make_pipeline_tag_type_distinct_users()

    result = aggregate(db, pipeline)
    import pprint
    if len(result) < 150:
        pprint.pprint(result)
    else:
        pprint.pprint(result[:100])


# region Data Exploration Syntax for use in Mongo Shell:

# db.pittsburgh.find().count()
#
# db.pittsburgh.find({'type':'node'}).count()
# db.pittsburgh.find({'type':'way'}).count()
#
# db.pittsburgh.find({"amenity":"stripclub"}).count()
# db.pittsburgh.find({"amenity":"stripclub"},{"name":true})
#
# db.pittsburgh.distinct("created.user").length
# db.pittsburgh.distinct("cuisine").length
# db.pittsburgh.distinct("amenity").length
#
# db.pittsburgh.distinct("craft").length
# db.runCommand({distinct:"pittsburgh",key:"craft"})
# endregion