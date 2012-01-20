
# Adds / fixes ordering in 'db.sessions.images'

import sys, pymongo

def doWork(database):
    sessColl = pymongo.collection.Collection(database, 'sessions')

    for sessDoc in sessColl.find():
        # determine if lists need to be converted
        sampleImgElem = sessDoc['images'][0]

        # ordered list must be created
        if not isinstance(sampleImgElem, dict):
            print "Session %s : \"%s\" to be converted to ordered 'images' list" % (sessDoc['_id'], sessDoc['name'])
            print "  dumping old session document:"
            print sessDoc, "\n"
            newImageList = list()
            for (count, imgElem) in enumerate(sessDoc['images']):
                newImageList.append( {'ref': imgElem, 'pos': count} )
            sessColl.update( {'_id': sessDoc['_id']}, {'$set': {'images': newImageList}} )
            print "  dumping new session document:"
            print sessColl.find_one({'_id': sessDoc['_id']}), "\n"

        # ordered list elements must be renamed 'img' -> 'ref'
        elif 'img' in sampleImgElem.keys():
            print "Session %s : \"%s\" 'images' list to be renamed 'img' -> 'ref'" % (sessDoc['_id'], sessDoc['name'])
            print "  dumping old session document:"
            print sessDoc, "\n"
            newImageList = list()
            for imgElem in sessDoc['images']:
                newImageList.append( {'ref': imgElem['img'], 'pos': imgElem['pos']} )
            sessColl.update( {'_id': sessDoc['_id']}, {'$set': {'images': newImageList}} )
            print "  dumping new session document:"
            print sessColl.find_one({'_id': sessDoc['_id']}), "\n"

        else:
            print "Session %s : \"%s\" not updated, already in the proper format" % (sessDoc['_id'], sessDoc['name'])


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



