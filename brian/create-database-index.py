
# Template for database util

import sys

import bson
import pymongo


def doWork(database):
    databases_coll = [
        {
        '_id': bson.objectid.ObjectId('4fd768c7114d970bc1000000'),
        'label': 'Harvard Combined Dermatology Residency Training Program',
        'host': 'slide-atlas.org:27017',
        'dbname': 'bev1',
        'copyright': 'Copyright &copy; 2011-12, Charles Palmer, Beverly Faulkner-Jones and Su-jean Seo. All rights reserved.'
        },
        {
        '_id': bson.objectid.ObjectId('4fd768c9114d970bc1000004'),
        'label': 'Washington University School of Medicine',
        'host': 'slide-atlas.org:27017',
        'dbname': 'paul3',
        'copyright': 'Copyright &copy 2011-12, Paul Bridgman. All rights reserved.'
        },
        {
        '_id': bson.objectid.ObjectId('4fd768c9114d970bc1000006'),
        'label': 'Atlas Demonstration',
        'host': 'slide-atlas.org:27017',
        'dbname': 'demo',
        'copyright': 'Copyright &copy; 2011-12. All rights reserved.'
        },
        {
        '_id': bson.objectid.ObjectId('4fd768c9114d970bc1000007'),
        'label': 'WSI Jeremy Kay',
        'host': 'slide-atlas.org:27017',
        'dbname': 'jnk1',
        'copyright': 'Copyright &copy; 2012, Jeremy Kay. All rights reserved.'
        },
        {
        '_id': bson.objectid.ObjectId('4fd768c9114d970bc1000009'),
        'label': 'K-12 Education',
        'host': 'slide-atlas.org:27017',
        'dbname': 'edu1',
        'copyright': 'Copyright &copy; 2012. All rights reserved.'
        },
        ]

    groups_coll = [
        {
        '_id': bson.objectid.ObjectId('50092247d6dc1e5514b8b5aa'),
        'name': 'all_bev1',
        'label': 'Harvard Combined Dermatology Residency Training Program',
        'db': databases_coll[0]['_id'],
        'can_see': [],
        'can_see_all': True
        },
        {
        '_id': bson.objectid.ObjectId('50092303d6dc1e5514b8b5ab'),
        'name': 'all_paul3',
        'label': 'Washington University School of Medicine',
        'db': databases_coll[1]['_id'],
        'can_see': [],
        'can_see_all': True
        },
        {
        '_id': bson.objectid.ObjectId('5009230ad6dc1e5514b8b5ac'),
        'name': 'all_demo',
        'label': 'Atlas Demonstration',
        'db': databases_coll[2]['_id'],
        'can_see': [],
        'can_see_all': True
        },
        {
        '_id': bson.objectid.ObjectId('5009230fd6dc1e5514b8b5ad'),
        'name': 'all_jnk1',
        'label': 'WSI Jeremy Kay',
        'db': databases_coll[3]['_id'],
        'can_see': [],
        'can_see_all': True
        },
        {
        '_id': bson.objectid.ObjectId('50092313d6dc1e5514b8b5ae'),
        'name': 'all_edu1',
        'label': 'K-12 Education',
        'db': databases_coll[4]['_id'],
        'can_see': [],
        'can_see_all': True
        },
        ]

    users_coll = [
        {
        '_id': bson.objectid.ObjectId('500923d8a4219560c57b8392'),
        'type': 'passwd',
        'name': 'all_bev1',
        'label': 'Harvard Combined Dermatology Residency Training Program',
        'passwd': 'letmein',
        'groups': [
            groups_coll[0]['_id']
            ]
        },
        {
        '_id': bson.objectid.ObjectId('500923e1a4219560c57b8393'),
        'type': 'passwd',
        'name': 'all_paul3',
        'label': 'Washington University School of Medicine',
        'passwd': 'showme',
        'groups': [
            groups_coll[1]['_id']
            ]
        },
        {
        '_id': bson.objectid.ObjectId('500923e2a4219560c57b8394'),
        'type': 'passwd',
        'name': 'all_demo',
        'label': 'Atlas Demonstration (no password)',
        'passwd': '',
        'groups': [
            groups_coll[2]['_id']
            ]
        },
        {
        '_id': bson.objectid.ObjectId('500923e2a4219560c57b8395'),
        'type': 'passwd',
        'name': 'all_nk1',
        'label': 'WSI Jeremy Kay',
        'passwd': 'Easter',
        'groups': [
            groups_coll[3]['_id']
            ]
        },
        {
        '_id': bson.objectid.ObjectId('500923e3a4219560c57b8396'),
        'type': 'passwd',
        'name': 'all_edu1',
        'label': 'K-12 Education',
        'passwd': 'April',
        'groups': [
            groups_coll[4]['_id']
            ]
        },
        ]

    users_coll.append({
        '_id': bson.objectid.ObjectId('500923e3a4219560c57b8397'),
        'type': 'passwd',
        'name': 'all',
        'label': 'All Databases',
        'passwd': 'foo',
        'groups': [group['_id'] for group in groups_coll]
        })

    coll = pymongo.collection.Collection(database, 'databases')
    for entry in databases_coll:
        coll.update( {'_id': entry['_id']}, entry, upsert=True)

    coll = pymongo.collection.Collection(database, 'groups')
    for entry in groups_coll:
        coll.update( {'_id': entry['_id']}, entry, upsert=True)

    coll = pymongo.collection.Collection(database, 'users')
    for entry in users_coll:
        coll.update( {'_id': entry['_id']}, entry, upsert=True)


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
    try:
        database = pymongo.database.Database(connection, argDBName)
        doWork(database)
    except pymongo.errors.InvalidName as e:
        print "Error: database name \"%s\" is not valid: %s" %(argDBName, e.message)
        exit(1)
except pymongo.errors.AutoReconnect as e:
    print "Error: could not connect to MongoDB server at \"%s:%d\"" % (argHostname, argHostport)
    exit(1)



