# This program 
# When older uploader is used to upload images, it creates chapter and images in old style. This needs to be converted to session and sessions-list
# If the chapter (from chapters collection) is already present, it will remove that record 

import pymongo
import sys

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

# Read chapters in the "chapters" collection and gather information about them
chap = db['chapters'].find_one()

asession = db['sessions'].find_one({'chapter_id' : chap['_id']})
if asession <> None:
	print 'Found ', asession['name']
	print 'Removing ..'
	db['sessions'].remove({'_id':asession['_id']})
else:
	print 'Not found ..'

print 'Processing ', chap['name']

images = db['images'].find({'title':chap['_id']})

image_list = []

for animage in images:
	print '    Processing ', animage['name']
	# add the image to 
	image_list.append(animage['_id'])
	# update the image record to remove chapter id

# Create a record in sessions 
session = {}
session['images'] = image_list
session['chapter_id'] = chap['_id']
session['label'] = chap['name']
session['name'] = chap['name']

db['sessions'].insert(session)

# db.images.update( {}, {$unset: {'title': 1} } )
# db.sessions.update( {}, {$unset: {'chapter_id': 1} } )

sys.exit(0)

#db.images.find().forEach( function(img) {db.sessions.update( {'chapter_id': img.title} , { $set: {'chapter_id': img.title}, $addToSet: {'images': img._id} }, true, false)} )
#db.sessions.find().forEach( function(sess) { db.sessions.update( {'_id':sess._id}, {$set: {'label': db.chapters.findOne({'_id': sess.chapter_id}).name}} ) } )
#db.sessions.find().forEach( function(sess) { db.sessions.update( {'_id':sess._id}, {$set: {'name': db.chapters.findOne({'_id': sess.chapter_id}).name}} ) } )
#
#db.images.update( {}, {$unset: {'title': 1} } )
#db.sessions.update( {}, {$unset: {'chapter_id': 1} } )
#db.chapters.drop()
#
