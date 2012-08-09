# This program 
# Add xs xe ys ye 

import pymongo
import sys

debug = False

#want command line argument
if len(sys.argv) < 3:
	print 'Error: Missing arguments\n'
	print 'Usage:  python ' + sys.argv[0] + ' mongo_instance database'
	print '    e.g python ' + sys.argv[0] + ' amber11:27017 daniels128'
	sys.exit(0)

mongo = sys.argv[1]
database = sys.argv[2]

# connect with the database
try:
	conn = pymongo.Connection('amber11:27017')
	db = conn[database]
	print 'Connection OK'
except:
	print 'Cound not Connect ..'
	sys.exit(0)

# loop through all collections 
cols = db.collection_names()

# Find the number of levels in the image
for col_name in cols[0:5]:
	# skip if starts with system
	col = db[col_name]

	print 'Collection: %s' % (col_name)

	if col_name[0:3] == 'sys' or  col_name[0:3] == 'res':
		if debug:
			print 'Quitting'
		pass
	else:
		#Find things 
		col = db[col_name]
		col.ensure_index("name")
		tstr = 't.jpg'
		while 1:
			res = db[col_name].find_one({ "name" : tstr })
			if res:
				tstr = 't' + tstr
			else:
				break;

		levels = len(tstr) - 5
		print '	Levels: %d' % (levels)

		# Find tilesize

		tile = col.find_one({ 'name' : 't.jpg'}, {'file': 0})
		size = tile['y'] + 1;
		print ' Size: %d' % (size)
		count = 0
		# Deduce the dimensions from the tilename
		for rec in col.find({}, {'file':0}):
			#initialize
			xs = 0
			ys = 0

			whole = size / 2

			# From the tilename get the extents			
			name = rec['name'][0:-4]
			name = name[::-1]

			# Until all letters are processed 
			for char in name:
				# Double the whole space
				whole = whole * 2
				#work on the column name to find out the dimensions
				if char == 't':
					# Ignore leading t 
					pass
				elif char == 'q':
					ys = ys + whole
				elif char == 'r':
					xs = xs + whole
					ys = ys + whole
				elif char == 's':
					xs = xs + whole

			if debug:
				print '  Name: %s' % (rec['name'])
				print '  Start: %d, %d' % (xs, ys)

			col.update({'name' : rec['name']}, {'$set': { 'xs' : xs, 'xe' : xs + size - 1, 'ys' : ys, 'ye' : ys + size - 1 } })

print "\r  Done ...    "
