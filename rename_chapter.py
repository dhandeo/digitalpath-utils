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
	if len(sys.argv) < 5:
		print 'Incorrect usage' 
		print 'Correct Use: python rename_chapter.py server database chapter new_chapter' 
		sys.exit(0)

	server = sys.argv[1]
	database = sys.argv[2]
	chapter = sys.argv[3]
	new_chapter = sys.argv[4]

	# Try opening the database	
	try:
		conn = pymongo.Connection(server); 
		db = conn[database]
		
		# Get the chapter id

		chapters = db['chapters']
		print "Chapters : " + str( chapters.find().count())

		# Try to find 

		this_chapter = chapters.find_one({'name': chapter})
		print this_chapter
		
		if this_chapter == None:
			print "No chapter of that name"
			print "Exiting"
			sys.exit(1)
		
		print "Found " + str(this_chapter['_id'])

		# Remove this record from chapters
		chapters.update({'_id' : this_chapter['_id']},\
			{'$set': { 'name': new_chapter}})
		
	except:
		strr = 'Error in the operations'
		error(strr)

	print 'Done'
	sys.exit(0);
