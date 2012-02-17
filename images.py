
# Follow from main but example usage
# python add_groups.py localhost slideatlas
import pymongo
import sys
import bson.objectid as oid 

from common import get_object_in_collection

def image_in_session(mongodb, cmd, session_key, image_key, force=False):

	# Verify that the session exists
	session = get_object_in_collection(mongodb['sessions'], session_key)
	image = get_object_in_collection(mongodb['images'], image_key)
	
	if image == None or session == None:
		print "Could not find objects for ", image_key, " or ", session_key
		return
	
	if cmd == "add":
		# Update the can_see
		print "Adding .."
		images = session['images']

		max = 0		
		for animage in images:
			#print animage
			if animage['pos'] > max:
				max = animage['pos']

		new_image = {}
		new_image[u'ref'] = image['_id']
		new_image[u'pos'] = max + 1 
		new_image[u'hide'] = False

		images.append(new_image)
		mongodb['sessions'].update({'_id': session['_id']}, {'$set':{'images': images}})

		for a in images:
			print a
		
		pass
	
	elif cmd == "del":
		print "Deleting .."
		
		# verify if the image is listed in the session 
		found = False
		images = session['images']
		
		for animage in images:
			#print animage
			if animage['ref'] == image['_id']:
				print 'Found'  
				found = True
				print animage
				index = images.index(animage)
				images[index]['hide'] = True
		
		if found == False:
			print "Image not found in session"
			
		print images
		mongodb['sessions'].update({'_id': session['_id']}, {'$set':{'images': images}})

def copy_image(from_mongodb, from_image, from_session)
	pass


# Main to accept command line and do the operation on images. 
if __name__ == '__main__':
	# get the command line arguments
	if len(sys.argv) < 3:
		print 'incorrect usage' 
		print 'correct use: python images.py server database command image session [force]' 
		sys.exit(0)

	server   = sys.argv[1]
	database = sys.argv[2]
	command  = sys.argv[3]
	image    = sys.argv[4]
	session  = sys.argv[5]
	
	# Cleanup if force parameter specified
	try:	
		force = int(sys.argv[6]) 
	except:
		force = 0

	try:
		# Try opening the database	
		conn = pymongo.Connection(server); 
		mongodb = conn[database]
	
	except:
		print "Error opening ", database, " at ", server
	if force:
		print "Using Force ..", 

	image_in_session(mongodb, command, session, image, force)

	sys.exit(0)
