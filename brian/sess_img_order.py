
# Adds / fixes ordering in 'db.sessions.images'

import sys, pymongo

def doWork(database):
    sessColl = pymongo.collection.Collection(database, 'sessions')

    # determine if lists need to be converted
    sampleImgElem = sessColl.find()[0]['images'][0]

    # ordered list must be created
    if not isinstance(sampleImgElem, dict):
        for sessDoc in sessColl.find():
            for (count, imgElem) in enumerate(sessDoc['images']):
                new_item = {'ref': imgElem, 'pos': count}
                sessColl.update( {'_id': sessDoc['_id']}, {'$push': {'images_new': new_item}} )
            sessColl.update( {'_id': sessDoc['_id']}, {'$unset': {'images': 1}} )
            sessColl.update( {'_id': sessDoc['_id']}, {'$rename': {'images_new': 'images'}} )
        print "db.sessions.images updated to ordered ref list"

    # ordered list elements must be renamed 'img' -> 'ref'
    elif 'img' in sampleImgElem.keys():
        for sessDoc in sessColl.find():
            for imgElem in sessDoc['images']:
                new_item = {'ref': imgElem['img'], 'pos': imgElem['pos']}
                sessColl.update( {'_id': sessDoc['_id']}, {'$push': {'images_new': new_item}} )
            sessColl.update( {'_id': sessDoc['_id']}, {'$unset': {'images': 1}} )
            sessColl.update( {'_id': sessDoc['_id']}, {'$rename': {'images_new': 'images'}} )
        print "db.sessions.images updated: elements renamed 'img' -> 'ref'"\

    else:
        print "db.sessions.images not updated, already in the proper format"


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



