
# Adds / fixes ordering in 'db.sessions.images'

import sys, pymongo

def doWork(database):

    if 'chapters' not in database.collection_names():
        print "No 'chapters' collection in database; done."
        return

    imgColl = pymongo.collection.Collection(database, 'images')
    sessColl = pymongo.collection.Collection(database, 'sessions')
    chaptersColl = pymongo.collection.Collection(database, 'chapters', create=False)
    i = 0
    for imgDoc in imgColl.find():
        if 'title' in imgDoc.keys():
            i += 1
            print "%d Image %s : \"%s\" to be added to a session" % (i, imgDoc['_id'], imgDoc['name'])
            pyramid = str(imgDoc['_id']) in database.collection_names()
            print "  pyramid exists: %s" % pyramid
            if pyramid:
                print "  pyramid size:", pymongo.collection.Collection(database, str(imgDoc['_id'])).count()
            print "  dumping old image document:"
            print " ", imgDoc
            chapterDoc = chaptersColl.find_one({'_id': imgDoc['title']})
            if not chapterDoc:
                print "  ERROR: image 'title' references nonexistant chapter %s" % imgDoc['title']
                print "Terminating early"
                exit(1)
            if 'name' not in chapterDoc.keys():
                print "  ERROR: chapter %s has no 'name'" % chapterDoc['_id']
                print "Terminating early"
                exit(1)
            oldSessDocs = sessColl.find( {'name': chapterDoc['name']} )
            if oldSessDocs.count() == 0:
                print "  No existing session, creating %s" % chapterDoc['name']
                #sessColl.insert( {'name': chapterDoc['name'], 'label': chapterDoc['name'], 'images': [{'ref': imgDoc['_id'], 'pos': 0}] } )
                print "  dumping new session document:"
                print " ", sessColl.find_one({'name': chapterDoc['name']})
            elif oldSessDocs.count() == 1:
                print "  Updating existing session %s : \"%s\"" % (oldSessDocs[0]['_id'], oldSessDocs[0]['name'])
                print "  dumping old session document:"
                print " ", oldSessDocs[0]
                newPos = int(max([imgElem['pos'] for imgElem in oldSessDocs[0]['images']]) + 1)
                newImageList = oldSessDocs[0]['images']
                newImageList.append( {'ref': imgDoc['_id'], 'pos': newPos} )
                #sessColl.update( {'_id': oldSessDocs[0]['_id']}, {'$set': {'images': newImageList}} )
                print "  dumping new session document:"
                print newImageList
                print " ", sessColl.find_one({'_id': oldSessDocs[0]['_id']})
            else:
                print "  ERROR: multiple sessions with 'name' \"%s\"; will not add image to a session" % chapterDoc['name']
                print "Terminating early"
                exit(1)
            print "  removing 'title' from image document"
            #imgColl.update({'_id': imgDoc['_id']}, {'$unset': {'title': 1}})
            print "  dumping new image document:"
            print " ", imgColl.find_one({'_id': imgDoc['_id']})
            print "\n"

    print "Dropping 'chapters' collection"
    #database.drop_collection('chapters')


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



