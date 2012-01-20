
# Template for database util

import sys, pymongo

def doWork(database):
    sessColl = pymongo.collection.Collection(database, 'sessions')

    # ordered list must be created
    for sessDoc in sessColl.find():
		newImageList = dict()
		for imgElem in sessDoc['images']:
			 imgElemName = pymongo.collection.Collection(database, 'images').find_one({'_id': imgElem['ref']})['name']
			 newImageList[imgElemName] = imgElem
		for (count, imgElemName) in enumerate(sorted(newImageList.keys())):
			newImageList[imgElemName]['pos'] = count
			sessColl.update( {'_id': sessDoc['_id']}, {'$push': {'images_new': newImageList[imgElemName]}} )
        #sessColl.update( {'_id': sessDoc['_id']}, {'$unset': {'images': 1}} )
        #sessColl.update( {'_id': sessDoc['_id']}, {'$rename': {'images_new': 'images'}} )
    print "db.sessions.images reordered by name"




# Main boilerplate
if len(sys.argv) != 3:
    print "Usage: %s HOST[:PORT] DATABASE" % sys.argv[0]
    exit(1)
argHostname = sys.argv[1].split(':')[0]
argHostport = int(sys.argv[1].split(':')[1]) if len(sys.argv[1].split(':')) > 1 else 27017
argDBName = sys.argv[2]
try:
    connTimeout = 10
    connection = pymongo.connection.Connection(argHostname, argHostport, network_timeout = connTimeout)
    if argDBName not in connection.database_names():
        print "Error: database \"%s\" not found on server" % (argDBName)
    try:
        database = pymongo.database.Database(connection, argDBName)
        doWork(database)
    except pymongo.errors.InvalidName as e:
        print "Error: database name \"%s\" is not valid: %s" %(argDBName, e.message)
except pymongo.errors.AutoReconnect as e:
    print "Error: could not connect to MongoDB server at \"%s:%d\"" % (argHostname, argHostport)
    exit(1)



