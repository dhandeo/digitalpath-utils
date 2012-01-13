# This program 
# When older uploader is used to upload images, it creates chapter and images in old style. This needs to be converted to session and sessions-list
# If the chapter (from chapters collection) is already present, it will remove that record 

import pymongo
import sys
import os
from subprocess import call

debug = False

#want command line argument
if len(sys.argv) < 3:
	print 'Error: Missing arguments\n' 
	print 'Usage:  python ' + sys.argv[0] + ' mongo_instance database'
	print '    e.g python ' + sys.argv[0] + ' amber11:27017 daniels128'
	sys.exit(0)

# Get command line arguments 
mongo = sys.argv[1]
database = sys.argv[2]

# connect with the database
try:
	conn = pymongo.Connection(mongo)
	db = conn[database]
	print 'Connection OK'
except:
	print 'Cound not Connect ..'
	sys.exit(0)

cols = db.collection_names()
cols.reverse()
num = len(cols)
print num
count = 0

for acol in cols:
	backup = True
	print acol,

	# If the collection is image collection
	if acol[0] =='4':
		if os.path.exists(acol+".bson"):
			print "Already exists"
			backup = False
		else :
			backup = True

	if backup:
		print " ",
		call(["mongodump", "--host", mongo, "-d",database,"-c",acol, "-o",".."])
	count = count + 1	
	print "Done .." + str(count) + "/" + str(num)

	
		# Find if that file exists


