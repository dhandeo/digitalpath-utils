"""
	Used to manually delete session and all associated images
	Risky
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
		print 'Incorrect usage' 
		print 'Correct Use: python delete_chapter.py server database session_name' 
		sys.exit(0)

	server = sys.argv[1]
	database = sys.argv[2]
	chapter = sys.argv[3]

	# Try opening the database	
	#try:
	conn = pymongo.Connection(server); 
	db = conn[database]
	
	# Get the chapter id

	chapters = db['sessions']
	images = db['images']
	
	print "Chapters : " + str( chapters.find().count())
	print "Images : " + str( images.find().count())

	# Try to find 

	this_session = chapters.find_one({'name': chapter})
	print this_session
	
	if this_session == None:
		print "No session of that name"
		print "Exiting"
		sys.exit(1)
	
	print "Found " + str(this_session['_id'])

	print "Getting a list of images"

	
	chap_images = this_session['images']
	print '  ' + str(len(chap_images)) + ' found .. '

	for animage in chap_images :
		print "  " + str(animage['ref']),
		# Remove the image collection
		dropped = db.drop_collection(str(animage['ref']))
		# Remove this record from images
		images.remove(animage['ref'],safe=True)
		
	pass
	# Remove this record from chapters
	chapters.remove(this_session['_id'],safe=True)

	#except:
	#	strr = 'Error in the operations'
	#	error(strr)

	print 'Done'
	sys.exit(0);
