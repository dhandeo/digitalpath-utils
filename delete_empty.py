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
	if len(sys.argv) < 4:
		error('Incorrect usage\n\tCorrect Use: python delete_empty.py server database chapter')

	server = sys.argv[1]
	database = sys.argv[2]
	chapter = sys.argv[3]

	# Try opening the database	
	try:
		conn = pymongo.Connection(server); 
		db = conn[database]
		
		# Get the chapter id

		chapters = db['chapters']
		print "Chapters : " + str( chapters.find().count())

		# Try to find 

		this_chapter = chapters.find_one({'name': chapter})
		
		if this_chapter == None:
			error( "No chapter named \"%s\""%(chapter))
		
		print "Found " + str(this_chapter['_id'])

		# Find the record in the images
		images = db['images']
		for image in images.find({'title':this_chapter['_id']}):
			count = db[str(image['_id'])].count()
			if count == 0:
				print 'Deleting ' + image['name'],	
				images.remove({'_id':image['_id']})

	except:
		strr = 'Error in the operations'
		error(strr)

	print 'Done'
	sys.exit(0);
