
# Template for database util

import sys, pymongo

includeAyodhya = True

def doWork(database):
    # work here    
    coll = pymongo.collection.Collection(database, 'databases')

    databaseList = [
    {'host': 'slide-atlas.org:27017', 'dbname': 'bev1',
     'label': 'Harvard Combined Dermatology Residency Training Program',
     'copyright': 'Copyright &copy 2011, Charles Palmer, Beverly Faulkner-Jones and Su-jean Seo. All rights reserved',
     'studentpasswd': 'letmein',
     'adminpasswd': 'MAmanage'
    },
    {'host': 'slide-atlas.org:27017', 'dbname': 'paul3',
     'label': 'Washington University School of Medicine',
     'copyright': 'Copyright &copy 2011, Paul Bridgman. All rights reserved',
     'studentpasswd': 'showme',
     'adminpasswd': 'MOmanage'
    },
    {'host': 'slide-atlas.org:27017', 'dbname': 'demo',
     'label': 'Atlas Demonstration (no password)',
     'copyright': 'Copyright &copy 2011, All rights reserved',
     'studentpasswd': 'student',
     'adminpasswd': ''
    }
    ]

    if includeAyodhya:
        databaseList.extend([
        {'host': 'ayodhya:27017', 'dbname': 'bev1',
         'label': 'bev1 (Harvard) [ayodhya]',
         'copyright': 'Copyright &copy 2011, Charles Palmer, Beverly Faulkner-Jones and Su-jean Seo. All rights reserved',
         'studentpasswd': 'letmein',
         'adminpasswd': 'MAmanage'
        },
        {'host': 'ayodhya:27017', 'dbname': 'paul2',
         'label': 'paul2 (Washington U.) [ayodhya]',
         'copyright': 'Copyright &copy 2011, Paul Bridgman. All rights reserved',
         'studentpasswd': 'showme',
         'adminpasswd': 'MOmanage'
        },
        {'host': 'ayodhya:27017', 'dbname': 'paul2copy',
         'label': 'paul2copy (Washington U.) [ayodhya]',
         'copyright': 'Copyright &copy 2011, Paul Bridgman. All rights reserved',
         'studentpasswd': 'showme',
         'adminpasswd': 'MOmanage'
        },
        {'host': 'ayodhya:27017', 'dbname': 'demo',
         'label': 'demo (no password) [ayodhya]',
         'copyright': 'Copyright &copy 2011, All rights reserved',
         'studentpasswd': 'student',
         'adminpasswd': ''
        }
        ])

    for entry in databaseList:
        coll.update( {'label': entry['label']}, entry, upsert=True)


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



