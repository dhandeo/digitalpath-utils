# Follow from main but example usage
# python add_groups.py localhost slideatlas

# adds or delets images from sessions 
# The image must already exist

import pymongo
import sys
import bson.objectid as oid 
from common_utils import get_object_in_collection
from add_groups import sessions_in_group
import argparse

# Main to accept command line and do the operation on images. 
if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Command utility to manage access rights')

	parser.add_argument('command' , help='Commands: grant, revoke supported')
	parser.add_argument('facebook', nargs='?', help='facebook group to configure')
	parser.add_argument('session' , nargs='?', help='Session ID or name to synchronize')

	# Arguments with defaults 
	parser.add_argument('-b' , '--db' , help='Database instance from which to read', default='slideatasdb',action='store_true')

	parser.add_argument('-m','--mongo' , help='MongoDB Server from which to read', default='127.0.0.1', action='store_true') 

	#parser.add_argument('-n','--noop', help='Dry run, no updates to the destination database', action='store_true')
	parser.add_argument('-d','--debug', help='Print more output useful for debugging (default:%(default)s)', default=False, action='store_true')
	parser.add_argument('-s','--soft', help='Allows soft comparison between image_key and image_label (default:%(default)s)', default=False, action='store_true')

	parser.set_defaults(debug=False)

	args = parser.parse_args()

#	if args.force:
#		print "Using Force .."
#
#	if args.noop:
#		print "No operations"
	
	if args.debug:
		print "Debug"

	if args.soft:
		print "Soft comparisons" 

	print args

	try:
		# Try opening the database	
		conn = pymongo.Connection(args.mongo)
		mongodb = conn[args.db]

	except:
		print "Error opening ", args.db, " at ", args.mongo
		sys.exit(0)

	if args.command == 'list':
		# no other option is necessary
		print 'Current rules:'
		sys.exit(0)
	
	elif args.command == 'grant' or args.command == 'revoke':
		
		# Make sure facebook group is supplied 
		if args.facebook == None:
			print 'Facebook argument required for granting / revoking access'
			sys.exit(0)

		# Make sure facebook group is supplied 
		if args.session == None:
			print 'Session argument required for granting / revoking access'
			sys.exit(0)

		print 'Arguments processed ..'
		#sessions_in_group(mongodb, cmd, facebook_id, which_all):
		if not sessions_in_group(mongodb, args.command, args.facebook, args.session, soft=args.soft, debug = args.debug):
			print 'NOT Done ..'
			sys.exit(0)


