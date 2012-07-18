#vim:tabstop=2:softtabstop=2:shiftwidth=2:noexpandtab
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

def error(message):
	print 'ERROR: ' + message
	sys.exit(1)

def build_level(col, level, force=0):

	print 'Building a level: ' + str(level)

	# Assume a square shape with given level
	total = col.find({'level' : level-1}).count()
	if debug:
		print total

	done = 0
	printed_percent = 0
	for arec in col.find({'level' : level-1}, {'name' : 1},timeout=False):
		percent = float(done) / total * 100.0
		this_name = arec['name']
		prefix = this_name[:-5]

		# Find if already processed
		if col.find_one({'name' : prefix + '.jpg', 'level' : level }) and not force:
			if debug:
				print 'Already processed ..' + str(prefix)
			# Find if the output exists and the neighbors
			pass
		else:
			#Find neighbors
			regexp = re.compile('^' + prefix)
			if col.find({'name' : regexp , 'level' : level -1}).count():
				# Create output image
				newim = Image.new('RGB' ,
					 (tilesize * 2, tilesize * 2), (255, 255, 255))
				if debug:
					print 'Prefix: ' + prefix

#				num_found = col.find({'name' : regexp, 'level' : level -1},timeout=False).count()
#				if num_found > 4:
#					print 'Num found ', num_found
#
				# Paste all the ancestors
				for brec in col.find({'name' : regexp, 'level' : level -1},timeout=False):
					chunk_name = brec['name']

					if chunk_name[-5] == 'q':
						box = (0,0)
						pass
					elif chunk_name[-5] == 'r':
						box = (tilesize,0)
						pass
					elif chunk_name[-5] == 's':
						box = (tilesize,tilesize)
						pass
					elif chunk_name[-5] == 't':
						box = (0,tilesize)

					# Load the chunk
					im = Image.open(StringIO.StringIO(brec['file']))
					if im.size[0] != tilesize or im.size[1] != tilesize:
						print '#####'
						print im.size
						print '#####'
					newim.paste(im, box)
				# Done all the ancestors

				# Resize it
				smallim = newim.resize((tilesize,tilesize),Image.ANTIALIAS)
				if debug:
					print smallim.size
					smallim.save(prefix + '.jpg')

				# Compress it in memory
				output = StringIO.StringIO()
				smallim.save(output, format='JPEG')
				contents = output.getvalue()
				output.close()

				# Insert it back
				try:
					# Now we know we have some result
					# Try to store result in database
					res_obj = {
						'name' : prefix + '.jpg',
						'level' : level,
						'xs' : 0,
						'ys' : 0,
						'xe' : 0,
						'ye' : 0,
						'file' :  Binary(contents)
						}
					idd = coll.insert(res_obj)
				except:
					error('Could not insert')

			# Done processing for neighbors found

		# Done an unprocessed ancestor
		os.write(1,'\r   Done : %2.1f'%(percent) + '%')
		done = done + 1

	# Done processing all records in the previous level
	col.ensure_index('name')
	col.ensure_index('level')
	col.ensure_index([('name', pymongo.ASCENDING), ('level',pymongo.ASCENDING)])
	print '\nDone Level !'

def construct_pyramid(col, level, force=0):
	# Determine the highest level
	item = col.find_one({'level' : 0},{'name' : 1, '_id' : 0})
	highest_level = 	len(item['name']) - 4

	print 'Highest Level: ' + str(highest_level)

	for i in range(level+1, highest_level):
		build_level(col, i,force)

	# Until the level is zero
	#if level >=1 :



if __name__ == '__main__':
	# Get the command line arguments
	if len(sys.argv) < 5:
		print 'Incorrect usage'
		print 'Correct Use: python build_pyramid.py server database collection tilesize [force]'
		sys.exit(0)
	global tilesize
	server = sys.argv[1]
	database = sys.argv[2]
	collection = sys.argv[3]
	tilesize = int(sys.argv[4])
	force = 0
	level = 0

	if len(sys.argv) >= 6:
		force = int(sys.argv[5])
	print 'force', force

	# Try opening the database
	conn = pymongo.Connection(server);
	db = conn[database]

	if collection == 'all':

		# loop over all collections

		cols = db.collection_names()
		cols.reverse()
		print cols
		for col_name in cols:
			# skip if not an image collection
			if col_name[0:3] == 'sys':
				continue

			print 'Opening image : ' + col_name
			coll = db[col_name]
			coll.ensure_index('name')
            if force:
				print 'Removing ..', coll.find({'level':{'$gt':0}}).count()
				coll.remove({'level':{'$gt':0}});

			title = coll.find_one({'name':'t.jpg'},{'name':1})
			if title == None or force:
				print col_name + ' is not ready'

				construct_pyramid(coll, level)
			else:
				print col_name + ' is READY !!'
	else:
		print "Looking for some particular collection"
		coll = db[collection]
		coll.ensure_index('name')
		coll.ensure_index('level')
		coll.ensure_index([('name', pymongo.ASCENDING), ('level', pymongo.ASCENDING)])
		if force:
			print 'Removing ..', coll.find({'level':{'$gt':0}}).count()
			coll.remove({'level':{'$gt':0}});
		construct_pyramid(coll, level)

		#incorrect syntax
		# Create error string
#		strr = 'Error opening database'
#		error(strr)

	sys.exit(0);
