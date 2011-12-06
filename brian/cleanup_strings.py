
# For 'db.images.name': strip leading and trailing whitespace, replace mid-string newlines with spaces

import sys, pymongo

def doWork(database):
    imgColl = pymongo.collection.Collection(database, 'images')
    for imgDoc in imgColl.find():
        cleanName = imgDoc['name'].replace('\n', ' ').strip()
        imgColl.update( {'_id': imgDoc['_id']}, {'$set': {'name': cleanName}} )
    print "db.images.name cleaned up"





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
        fatalError("Error: database \"%s\" not found on server" % (argDBName))
    try:
        database = pymongo.database.Database(connection, argDBName)
        doWork(database)            
    except pymongo.errors.InvalidName as e:
        fatalError("Error: database name \"%s\" is not valid: %s" %(argDBName, e.message))
except pymongo.errors.AutoReconnect as e:
    fatalError("Error: could not connect to MongoDB server at \"%s:%d\"" % (argHostname, argHostport))
    exit(1)



