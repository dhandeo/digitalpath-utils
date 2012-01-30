# This program 
# This script is specific to a very custom application but has good structure
# This should probably be never run

import pymongo
import sys

debug = False

def add_pos_ref(mondb):
	# Gets db in a mongo instance,
	# and replaces iamges in the list to ref, pos format

	for asession in db['sessions'].find():
		print 'Processing ', asession['name'] 
		
		images = asession['images']
		print images
		image_list = []
		count = 0
		for animageid in images:
			animage = db['images'].find_one({'_id':animageid})
			print '    Processing ', animage['name']
			# add the image to 
			image_list.append({'ref': animage['_id'], 'pos': count})
			count = count + 1
			# update the image record to remove chapter id

		# Create a record in sessions 
		session = {}
		print image_list
		db['sessions'].update({'_id':asession['_id']},{'$set':{'images' : image_list}})

#want command line argument

print 'This should probably be never run as it pertains to old database structures'
sys.exit(0)


if len(sys.argv) < 2:
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

add_pos_ref(db)

sys.exit(0)

