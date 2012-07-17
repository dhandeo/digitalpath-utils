"""
 Checks (and) builds the multiresolution pytamid
 Accepts urls in the form of 
      server/tile.py/database/collection/filename.jpg:
"""
import pymongo
from pymongo.binary import Binary
import sys
import os

debug = False

server = "meru"
database = "orig"

conn = pymongo.Connection(server); 

db = conn[database]
db2 = conn["kasthuri"]

coll2 = db2['orig']

for num in range(1,31):
    coll = db[str(num)]
    coll.update({}, {'$set':{'slice': num } }, multi=True)
    
    for anobj in coll.find():
        coll2.save(anobj)
    
    print "After ", num, db2['orig'].find().count()

   
        