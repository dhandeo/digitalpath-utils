#! /usr/bin/python

import sys, pymongo
import tests


def main():

    ## Get and validate arguments
    if len(sys.argv) != 4:
        print "Usage: %s TestName host[:port] database" % sys.argv[0]
        exit(3)
    # do better validation of hostname, port format
    argTestName = sys.argv[1]
    argHostname = sys.argv[2].split(':')[0]
    argHostport = int(sys.argv[2].split(':')[1]) if len(sys.argv[2].split(':')) > 1 else 27017
    argDBName = sys.argv[3]

    try:
        ## Server connection
        connTimeout = 10
        connection = pymongo.connection.Connection(argHostname, argHostport, network_timeout = connTimeout)

        ## Database find and connect
        if argDBName not in connection.database_names():
            print "Error: database \"%s\" not found on server" % (argDBName)
            exit(2)

        database = pymongo.database.Database(connection, argDBName)

        tests.testValue = 0
        eval('tests.' + argTestName)(database)
        exit(tests.testValue)

    except pymongo.errors.AutoReconnect as e:
        print "Error: could not connect to MongoDB server at \"%s:%d\"" % (argHostname, argHostport)
        exit(2)
    except pymongo.errors.InvalidName as e:
        print "Error: database name \"%s\" is not valid: %s" %(argDBName, e.message)
        exit(2)
#    except NameError:
#        print "Error, unknown test: %s" % argTestName
#        exit(3)


if __name__ == "__main__":
    main()
