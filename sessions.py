# Unfinished, grant and revoking access
# Follow from main but example usage
# python add_groups.py localhost slideatlas

import pymongo
import sys
import bson.objectid as oid
import argparse

from common_utils import get_object_in_collection
from collection_utils import copy_collection

def check_image_in_session(mongodb_to, session_obj, image_id):
	"""
	Inspects the health in 3 places
	Not implemented yet
	"""
	pass


def sync_session(from_mongodb, to_mongodb, session_key, args={}):
	""" Essentially intelligently copies a session from one place to another.
	"""

	# Get the session and process each images
	session_from = get_object_in_collection(from_mongodb['sessions'], session_key, args['debug'])
	session_to = get_object_in_collection(to_mongodb['sessions'], session_key, args['debug'])

	if session_from == None:
		print 'Source session not found'
		return

	if session_to == None:
		print 'No session found in destination'
		print 'inserting ..'

		# insert an empty session
		session_to_empty = {}
		session_to_empty['_id'] = session_from['_id']
		session_to_empty['name'] = session_from['name']
		session_to_empty['label'] = session_from['label']
		session_to_empty['images'] = []

		if not args['dry']:
			to_mongodb['sessions'].insert(session_to_empty)
			session_to = get_object_in_collection(to_mongodb['sessions'], session_key, args['debug'])
		else:
			print 'need to insert empty collection to continue - ', session_to_empty
			sys.exit(0)

	# at this point both sessions should have objects 
	count = 0
	refs = []

	to_col_list = mongodbto.collection_names()

	for animage in session_to['images']:
		refs.append(animage['ref'])

	for animage in session_from['images']:

		# Synchronize actual image chunks  
		id_str = str(animage['ref'])

		if id_str in to_col_list:
			ref_exist = 'CNK'
		else:
			print 'Starting to copy ', str(id_str)
			if not args['dry']:
				# insert this image collection
				copy_collection(from_mongodb, to_mongodb, str(id_str))
				ref_exit = 'INS'
			else:
				ref_exit = 'NOT'

		# Synchronize image reference in the session
		id_str = animage['ref']

		if id_str in refs:
			col_exist = 'REF'
		else:
			# Insert the reference in the session record

			# Get and modify image record
			images = session_to['mages']
			images.append(animage)

			print 'Inserting reference'

			# Insert it back into target collection if not dry
			if not args['dry']:
				# Insert the image record
				to_mongodb['sessions'].update({'_id': session_to['_id']}, {'$set' :{ 'images':images}})
				# to_mongodb['images'].update({'_id':


			session_to = get_object_in_collection(to_mongodb['sessions'], session_key, args['debug'])
			session_to = get_object_in_collection(to_mongodb['sessions'], session_key, args['debug'])
			image_exists = 'INS'
		else:
			image_exists = 'NOT'


		# Synchronize the record in images collection
		image_obj = get_object_in_collection(to_mongodb['images'], animage['ref'], args['debug'])

		if image_obj == None:
			print 'Inserting image record ...'
			if not args['dry']:
				# Get the image object 
				image_obj = get_object_in_collection(from_mongodb['images'], animage['ref'], args['debug'])

				# Insert the image record
				to_mongodb['images'].insert(image_obj)
				image_exists = 'INS'
			else:
				image_exists = 'NOT'
		else :
			image_exists = 'IMG'

		print animage['ref'], image_exists, col_exit, ref_exit

	# Find if the session exists in the 
	pass


# Main to accept command line and do the operation on images. 
if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Utility to synchronize sessions on two servers')

	parser.add_argument('serverfrom' , help='MongoDB Server from which to read')
	parser.add_argument('databasefrom' , help='Database instance from which to read')
	parser.add_argument('sessionfrom' , help='Session ID or name to synchronize')

	parser.add_argument('serverto' , nargs='?', help='MongoDB Server to which to write (default: %(default)s)', default="127.0.0.1:27017", type=str)

	parser.add_argument('-n', '--no-op', help='Dry run, no updates to the destination database', action='store_true')
	parser.add_argument('-f', '--force', help='Entirely removes the session and re-creates', action='store_true')
	parser.add_argument('-d', '--debug', help='Print more output useful for debugging (default:%(default)s)', default=False, action='store_true')
	parser.set_defaults(debug=False)

	args = parser.parse_args()

	try:
		# Try opening the database	
		conn = pymongo.Connection(args.serverfrom);
		mongodbfrom = conn[args.databasefrom]

	except:
		print "Error opening ", args.databasefrom, " at ", args.serverfrom
		sys.exit(0)


	try:
		connto = pymongo.Connection(args.serverto);
		mongodbto = connto[args.databasefrom]
	except:
		print "Error opening ", args.databasefrom, " at ", args.serverto
		sys.exit(0)

	sync_session(mongodbfrom, mongodbto, args.sessionfrom, args={'debug': args.debug, 'dry' : args.no_op, 'force':args.force })

	sys.exit(0)
