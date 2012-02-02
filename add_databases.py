
# Template for database util

import sys, pymongo

includeAyodhya = True

def add_database(mongodb, host, dbname, label, copyright, studentpasswd, adminpasswd):
	# Create an entry 
	entry = {	'host': host, 'dbname': dbname, 'label': label, 'copyright':copyright, 'studentpasswd': studentpasswd, 'adminpasswd': adminpasswd }
	return mongodb['databases'].insert(entry)

# Main boilerplate
if __name__ == '__main__':

	if len(sys.argv) != 3:
			print "Usage: %s HOST[:PORT] DATABASE" % sys.argv[0]
			exit(1)
	argHostname = sys.argv[1].split(':')[0]
	argHostport = int(sys.argv[1].split(':')[1]) if len(sys.argv[1].split(':')) > 1 else 27017
	argDBName = sys.argv[2]
	try:
			connTimeout = 10
			connection = pymongo.connection.Connection(argHostname, argHostport, network_timeout = connTimeout)
			try:
					database = pymongo.database.Database(connection, argDBName)
					doWork(database)            
			except pymongo.errors.InvalidName as e:
					print "Error: database name \"%s\" is not valid: %s" %(argDBName, e.message)
					exit(1)
	except pymongo.errors.AutoReconnect as e:
			print "Error: could not connect to MongoDB server at \"%s:%d\"" % (argHostname, argHostport)
			exit(1)



