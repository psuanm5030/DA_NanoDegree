__author__ = 'Miller'


from autos import process_file
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client.examples
col = db.autos

autos = process_file('autos.csv')
col.insert(autos)