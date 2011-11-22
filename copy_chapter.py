"""
	Used to manually delete chapters and all associated images.
	This pseudo code will be later used to write php function
"""
import pymongo
from pymongo.binary import Binary
import sys
import os

debug = False

def error(message):
	print 'ERROR: ' + message
	sys.exit(1)

if __name__ == '__main__':
	# Get the command line arguments
	if len(sys.argv) < 6:
		error('Incorrect usage\nCorrect Use: python copy_chapter.py serverfrom databasefrom chapterfrom serverto databaseto') 
		sys.exit(0)

	server = sys.argv[1]
	database = sys.argv[2]
	chapter = sys.argv[3]
	server2 = sys.argv[4]
	database2 = sys.argv[5]

	# Try opening the database	
	try:
		conn = pymongo.Connection(server) 
		conn2 = pymongo.Connection(server2)
	
		db = conn[database]
		db2 = conn2[database2]
		
		# Get the chapter id
		chapters = db['chapters']
		images = db['images']
	
	except:
		error("Error opening databases")
	
	try:	
		# Find the requested chapter 
		this_chapter = chapters.find_one({'name': chapter})
		
		if this_chapter == None:
			error("Source chapter named %s not found"%(chapter))
		
		print "Found " + str(this_chapter['_id'])
		print "Getting a list of images"
		
		chap_images = images.find({'title': this_chapter['_id']})
		print '  ' + str(chap_images.count()) + ' found .. '

		# Create a new chapter instance	
		new_chapter = this_chapter
		
		# Get the id for new chapter
		chapter2_id = db2['chapters'].insert(new_chapter)
		
		
		for animage in chap_images :
			print "  " + str(animage['_id']),
			count = db[str(animage['_id'])].count()	
			print "To Copy: " + str(count),
			fromid = str(animage['_id'])
	
			# Create the record for new image 
			new_image = animage
			new_image['title'] = chapter2_id
			image2_id = db2['images'].insert(new_image)
		
			print '\nTo Image: ', image2_id,  '\nfrom ', animage['_id'], '\n'
			
			# Get the new ID for the collection
			image2 = str(image2_id)
			# Creating a collection of that name
		
			print '    ' , animage['_id']
			chunks = db[fromid].find()	
			for achunk in chunks:
				db2[image2].insert(achunk)
		
			print 'Creating index ..'	
			db2[image2].ensure_index('name')
			print 'Done image'
			
		# Remove this record from chapters
		# chapters.remove(this_chapter['_id'],safe=True)

	except:
		error('Operations could not be completed')

	print 'Done'
	sys.exit(0);
