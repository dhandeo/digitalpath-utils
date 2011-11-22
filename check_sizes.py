"""
 Decodes the path info and fetches the corresponding tile from pymongo
 Accepts urls in the form of 
      server/tile.py/database/collection/filename.jpg:
"""
import pymongo
from pymongo.binary import Binary
import sys
import Image 
import StringIO
import math
import os
import re

debug = False

root_path = '/var/www-imserver'
sys.path.append(root_path)
# Make sure that the serverroot is in current module path
#sys.path.append('/var/www-dj/')
#sys.path.append('/var/www/')

from mongo import m 

def error(message):
	print 'ERROR: ' + message
	sys.exit(1)

def check(col):
	
	# Assume a square shape with given level
	total = col.find().count()
	
	done = 0
	printed_percent = 0
	
	for arec in col.find({},timeout=False):
		percent = float(done) / total * 100.0
		this_name = arec['name']
		prefix = this_name[:-5]
		# Load the chunk 
		im = Image.open(StringIO.StringIO(arec['file']))
		if im.size[0] != 256 or im.size[1] != 256:
			print '#####'
			print im.size, brec
			print '#####'
			# Done processing for neighbors found
			
		# Done an unprocessed ancestor	
		os.write(1,'\r   Done : %2.1f'%(percent) + '%')
		done = done + 1

	# Done processing all records in the previous level
	col.ensure_index('name')
	
	print '\nDone !'

if __name__ == '__main__':
	# Get the command line arguments
	if len(sys.argv) < 5:
		print 'Incorrect usage' 
		print 'Correct Use: python check_sizes.py server database collection tilesize' 
		sys.exit(0)

	server = sys.argv[1]
	database = sys.argv[2]
	collection = sys.argv[3]
	tilesize = int(sys.argv[4])

	# Try opening the database	
	conn = pymongo.Connection(server); 
	db = conn[database]

	if collection == 'all':
		# loop over all collections
		cols = db.collection_names()
		for col_name in cols:
			# skip if not an image collection 
			if col_name[0:3] == 'sys':
				continue

			print 'Opening image : ' + col_name
			coll = db[col_name]
			coll.ensure_index('name')
			title = coll.find_one({'name':'t.jpg'},{'name':1})
			if title == None:
				print col_name + ' is not ready'
				check(coll)
			else:
				print col_name + ' is READY !!'
	else:
		print "Looking for some particular collection"
		coll = db[collection]
		coll.ensure_index('name')
		check(coll)

	sys.exit(0);
