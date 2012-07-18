# Follow from main but example usage
# python add_groups.py localhost slideatlas

# adds or delets images from sessions 
# The image must already exist

import pymongo
import sys
import bson.objectid as oid
from common_utils import get_object_in_collection

import argparse

def image_in_session(mongodb, cmd, session_key, image_key, force=False, soft=False, debug=False, noop=False):
	# Verify that the session exists
	session = get_object_in_collection(mongodb['sessions'], session_key, soft=soft)
	image = get_object_in_collection(mongodb['images'], image_key, soft=soft)

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
		if debug:
			print session
		images = session['images']

		for animage in images:
			#print animage
			if animage['ref'] == image['_id']:
				if debug:
					print 'Found'
				found = True
				if debug:
					print animage
				index = images.index(animage)
				images[index]['hide'] = True
				# Possibly delete the image collection
				col_to_del = str(images[index]['ref'])
				print col_to_del
				mongodb.drop_collection(col_to_del)

		if found == False:
			print "Image not found in session"

		mongodb['sessions'].update({'_id': session['_id']}, {'$set':{'images': images}})

	elif 1:
		print 'Unknown command', cmd
		sys.exit(0)

def copy_image(from_mongodb, from_image, from_session):
	pass


# Main to accept command line and do the operation on images. 
if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Utility to synchronize sessions on two servers')

	parser.add_argument('server' , help='MongoDB Server from which to read')
	parser.add_argument('db' , help='Database instance from which to read')
	parser.add_argument('command' , help='Commands, add, del supported')
	parser.add_argument('session' , help='Session ID or name to synchronize')
	parser.add_argument('image' , nargs='?', help='Image ID or name to manipulate. use -s for soft name comparisons')

	parser.add_argument('-n', '--noop', help='Dry run, no updates to the destination database', action='store_true')
	parser.add_argument('-f', '--force', help='Entirely removes the session and re-creates', action='store_true')
	parser.add_argument('-d', '--debug', help='Print more output useful for debugging (default:%(default)s)', default=False, action='store_true')
	parser.add_argument('-s', '--soft', help='Allows soft comparison between image_key and image_label (default:%(default)s)', default=False, action='store_true')

	parser.set_defaults(debug=False)

	args = parser.parse_args()

	try:
		# Try opening the database	
		conn = pymongo.Connection(args.server)
		mongodb = conn[args.db]

	except:
		print "Error opening ", args.db, " at ", args.server
		sys.exit(0)

	if args.force:
		print "Using Force .."

	if args.noop:
		print "No operations"

	if args.debug:
		print "Debug"

	if args.soft:
		print "Soft comparisons"

	print args

	image_in_session(mongodb, args.command, args.session, args.image, force=args.force, soft=args.soft, debug=args.debug, noop=args.noop)

	sys.exit(0)
