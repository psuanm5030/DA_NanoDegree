__author__ = 'Miller'

import json

def insert_data(data, db):

    db.arachnid.insert_many(data)

    pass


if __name__ == "__main__":

    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017")
    db = client.examples

    with open('/Users/Miller/GitHub/GhNanoDegree/Class_DataWrangling/Lesson4_MongoDB/PS4_MongoData/arachnid.json') as f:
        data = json.loads(f.read())
        insert_data(data, db)
        print db.arachnid.find_one()