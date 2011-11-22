# This program 

import pymongo
import sys

#want command line argument
if len(sys.argv) != 8:
  print 'Missing database argument' 
  print 'Usage python xs_xe.py database collection level x1 y1 x2 y2' 
  sys.exit(0)

database = sys.argv[1]
collection = sys.argv[2]
level = int(sys.argv[3])
xs = int(sys.argv[4])
ys = int(sys.argv[5])
xe = int(sys.argv[6])
ye = int(sys.argv[7])

# connect with the database
try:
	conn = pymongo.Connection()
	db = conn[database]
	#db = conn['0']
	print 'Connection OK'
except:
	print 'Cound not Connect ..'
	sys.exit(0)
# loop through all collections 

cols = db.collection_names()
col = db[collection] 

# Find records without field file	
# filter when the requested start is in the tile  

# Translate the requested coordinates to the current level coordinates

# Find the resolution of the level
 
for rec in col.find({'level' : level, 
										  'xs' : { '$gt' : xs,
														   '$lt' : xe
														 },
											'xe' : { '$gt' :

															} 

# do the filtering otherwise 

								
										}):
	print rec['name']
	print str(rec['xs']) + ", " +  str(rec['xe']) + ", " +  str(rec['ys']) + ", " +  str(rec['ye'])

print "\r  Done ...    "
