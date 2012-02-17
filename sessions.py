# Follow from main but example usage
# python add_groups.py localhost slideatlas
import pymongo
import sys
import bson.objectid as oid 

from common_utils import get_object_in_collection

def sync_session(from_mongodb, to_mongodb, from_session):
	""" Essentially intelligently copies a session from one place to another.
	"""
	
	print from_mongodb, to_mongodb, from_session
	pass


# Main to accept command line and do the operation on images. 
if __name__ == '__main__':
	# get the command line arguments
	if len(sys.argv) < 3:
		print 'incorrect usage' 
		print 'correct use: python sessions.py serverfrom databasefrom sessionfrom [server2]' 
		sys.exit(0)

	print sys.argv

	serverfrom   = sys.argv[1]
	databasefrom = sys.argv[2]
	sessionfrom  = sys.argv[3]
	
	# Cleanup if force parameter specified
	try:	
		serverto = sys.argv[4] 
		is_serverto_specified = True
		print "Got serverto", serverto
	except:
		is_serverto_specified = False

	try:
		# Try opening the database	
		conn = pymongo.Connection(serverfrom); 
		mongodbfrom = conn[databasefrom]

	except:
		print "Error opening ", databasefrom, " at ", serverfrom
		sys.exit(0)

	#try: 
	
	if (is_serverto_specified == True):
		connto = pymongo.Connection(serverto); 
		mongodbto = connto[databasefrom]
	else:
		mongodbto = conn[databasefrom]
		connto = mongodbto.connection 
	
	#except:
	#	print "Error opening ", databasefrom, " at ", serverto
	#	sys.exit(0)

	sync_session(mongodbfrom, mongodbto, sessionfrom)

	sys.exit(0)
