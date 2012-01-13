# This program 
# When older uploader is used to upload images, it creates chapter and images in old style. This needs to be converted to session and sessions-list
# If the chapter (from chapters collection) is already present, it will remove that record 

import pymongo
import sys

debug = False

#want command line argument
if len(sys.argv) < 3:
	print 'Error: Missing arguments\n' 
	print 'Usage:  python ' + sys.argv[0] + ' mongo_instance database chapter_name'
	print '    e.g python ' + sys.argv[0] + ' amber11:27017 daniels128 session13'
	sys.exit(0)

# Get command line arguments 
mongo = sys.argv[1]
database = sys.argv[2]
chapter = sys.argv[3]

# connect with the database
try:
	conn = pymongo.Connection(mongo)
	db = conn[database]
	print 'Connection OK'
except:
	print 'Cound not Connect ..'
	sys.exit(0)

# Read chapters in the "chapters" collection and gather information about them
chap = db['chapters'].find_one({'name':chapter})

if chap == None:
	print 'Chapter not found'
	sys.exit(0)

asession = db['sessions'].find_one({'chapter_id' : chap['_id']})
if asession <> None:
	print 'Found ', asession['name']
	print 'Removing ..'
	db['sessions'].remove({'_id':asession['_id']})
else:
	print 'Chapter not found in sessions ..'

print 'Processing ', chap['name']

images = db['images'].find({'title':chap['_id']})

image_list = []
count = 0
for animage in images:
	print '    Processing ', animage['name']
	# add the image to 
	image_list.append({'ref': animage['_id'], 'pos': count})
	count = count + 1
	# update the image record to remove chapter id

# Create a record in sessions 
session = {}
session['images'] = image_list
session['chapter_id'] = chap['_id']
session['label'] = chap['name']
session['name'] = chap['name']

# Now have session
print session


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
