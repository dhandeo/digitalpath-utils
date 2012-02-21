# Follow from main but example usage
# python add_groups.py localhost slideatlas
import pymongo
import sys
import bson.objectid as oid 
import argparse

import time

from common_utils import get_object_in_collection

def copy_collection(from_mongodb, to_mongodb, collection_name):
	""" Essentially intelligently copies a session from one place to another.
	"""
	for obj in from_mongodb[collection_name].find():
		to_mongodb[collection_name].insert(obj)

# Main to accept command line and do the operation on images. 
if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Utility to copy collection between servers')
	parser.add_argument('serverfrom' , help='MongoDB Server from which to read') 
	parser.add_argument('databasefrom' , help='Database instance from which to read')
	parser.add_argument('collection_name' , help='Collection name')

	parser.add_argument('databaseto' ,nargs='?', help='MongoDB Server to which to write (default: %(default)s)',default=" ", type=str)
	
	parser.add_argument('serverto' ,nargs='?', help='MongoDB Server to which to write (default: %(default)s)',default="127.0.0.1:27017", type=str)
	
	parser.add_argument('-n','--no-op', help='Dry run, no updates to the destination database', action='store_true')
	parser.add_argument('-f','--force', help='Entirely removes the session and re-creates', action='store_true')
	parser.add_argument('-d','--debug', help='Print more output useful for debugging (default:%(default)s)', default=False, action='store_true')
	parser.set_defaults(debug=False)

	args = parser.parse_args()

	if args.databaseto == " ":
		args.databaseto = args['databasefrom']

	print args

	try:
		# Try opening the database	
		conn = pymongo.Connection(args.serverfrom); 
		mongodbfrom = conn[args.databasefrom]

	except:
		print "Error opening ", args.databasefrom, " at ", args.serverfrom
		sys.exit(0)


	try:
		connto = pymongo.Connection(args.serverto); 
		mongodbto = connto[args.databaseto]
	except:
		print "Error opening ", args.databasefrom, " at ", args.serverto
		sys.exit(0)

	start = time.time()

	copy_collection(mongodbfrom, mongodbto, args.collection_name)

	print 'Time :', time.time() - start
	sys.exit(0)
