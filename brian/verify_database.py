import sys, re
import pymongo


## Check regular collection
def checkColl(collName, database, baseErrorStr):
    collErrorStr = baseErrorStr + " '%s' collection" % (collName)

    if collName not in database.collection_names():
        fatalError(collErrorStr + " is missing")
    collObj = pymongo.collection.Collection(database, collName)
    if not collObj.count():
        warnError(collErrorStr + " is empty")

    if collName is 'images':
        collRequiredFields = set(['_id', 'name', 'origin', 'dimension', 'spacing'])
        collOptionalFields = set(['hide', 'startup_view', 'bookmarks'])
    elif collName is 'sessions':
        collRequiredFields = set(['_id', 'name', 'label', 'images'])
        collOptionalFields = set([])
    else: # assume collection is image data
        collRequiredFields = set(['_id', 'name', 'level', 'xs', 'xe', 'ys', 'ye'])
        collOptionalFields = set(['size', 'file'])

    seenNamesSet = set()
    for docObj in collObj.find({}, {'file': 0}): # optimization to speed up query
        ## Check field existence
        # '_id' field
        if '_id' not in docObj:
            fatalError(collErrorStr + " has document with missing '_id' field")
        docErrorStr = collErrorStr + ": document '%s'" % (docObj['_id'])
        checkRequiredFields(docObj, collRequiredFields, collOptionalFields, docErrorStr, False)

        ## Validate fields
        if collName is 'images':
            # '_id' ref to image data collection
            if str(docObj['_id']) not in database.collection_names():
                fatalError(docErrorStr + " has no corresponding image data collection")
            # 'name' / 'label'
            for stringField in ['name']:
                checkStringField(docObj, stringField, docErrorStr)
            checkUniqueField(docObj, 'name', docErrorStr, seenNamesSet)
            # 'origin' / 'dimension' / 'spacing' 
            for coordField in ['origin', 'dimension', 'spacing']:
                checkCoordField(docObj, coordField, docErrorStr)
            #'hide'
            pass
            #'startup_view'
            pass
            #'bookmarks'
            pass

        elif collName is 'sessions':
            # 'name' / 'label'
            for stringField in ['name', 'label']:
                checkStringField(docObj, stringField, docErrorStr)
            checkUniqueField(docObj, 'name', docErrorStr, seenNamesSet)
            # 'images'
            checkOrderedRefListField(docObj, 'images', docErrorStr, 'images')
        else: # assume collection is image data
            pass











## Check field functions
## Check field function - checkStringField
def checkStringField(obj, fieldName, errorStr):
    fieldErrorStr = errorStr + ": '%s' field" % (fieldName)
    checkType(obj[fieldName], basestring, "string", fieldErrorStr)
    invalidReason = isValidString(obj[fieldName])
    if invalidReason:
        warnError(fieldErrorStr + " \"%s\" is invalid, because:%s" % (repr(obj[fieldName]), invalidReason))


## Check field function - checkUniqueField
def checkUniqueField(obj, fieldName, errorStr, uniqueSet):
    fieldErrorStr = errorStr + ": '%s' field" % (fieldName)
    if obj[fieldName] in uniqueSet:
        warnError(fieldErrorStr + " has a non-unique value")
    uniqueSet.add(obj[fieldName])


## Check field function - checkOrderedRefListField
def checkOrderedRefListField(obj, fieldName, errorStr, refCollection):
    fieldErrorStr = errorStr + ": '%s' field" % (fieldName)
    checkType(obj[fieldName], list, "list", fieldErrorStr)
    if not obj[fieldName]:
        warnError(fieldErrorStr + " is empty")
    seenPosSet = set()
    for orderedRefElem in obj[fieldName]:
        elemErrorStr = fieldErrorStr + " contains an element which"
        ## Check field existence in each element
        checkType(orderedRefElem, dict, "dict", elemErrorStr)
        checkRequiredFields(orderedRefElem, set(['pos', 'ref']), set(['label']), elemErrorStr, True)
        ## Validate fields in each element
        # 'pos'
        elemFieldErrorStr = elemErrorStr + ": '%s' field" % ('pos')
        checkType(orderedRefElem['pos'], int, "int", elemFieldErrorStr)
        if orderedRefElem['pos'] in seenPosSet:
            warnError(elemFieldErrorStr + " has a non-unique value")
        seenPosSet.add(orderedRefElem['pos'])
        # 'ref'
        elemFieldErrorStr = elemErrorStr + ": '%s' field" % ('ref')
        checkType(orderedRefElem['ref'], pymongo.objectid.ObjectId, "ObjectID", elemFieldErrorStr)
        checkObjectId(orderedRefElem['ref'], refCollection, elemFieldErrorStr)
        # 'label' - optional
        if 'label' in orderedRefElem.keys():
            checkStringField(orderedRefElem, 'label', elemErrorStr)


## Check field function - checkCoordField
def checkCoordField(obj, fieldName, errorStr):
    fieldErrorStr = errorStr + ": '%s' field" % (fieldName)
    checkType(obj[fieldName], list, "list", fieldErrorStr)
    if len(obj[fieldName]) != 3:
        fatalError(fieldErrorStr + " has length other than 3")
    for coordElem in obj[fieldName]:
        elemErrorStr = fieldErrorStr + " contains an element which"
        checkType(coordElem, [int, float, long], "numeric", elemErrorStr)
    if obj[fieldName] == [0, 0, 0] or obj[fieldName] == [1, 1, 1]:
        warnError(fieldErrorStr + " is trivial value: %s" % (obj[fieldName]))


## Helper functions
# Helper function - checkType
def checkType(obj, typeObj, typeStr, errorStr):
    typeObjList = typeObj if isinstance(typeObj, list) else [typeObj]
    resultList = [isinstance(obj, typeObjItem) for typeObjItem in typeObjList]
    if not reduce(lambda a, b: a or b, resultList):
        fatalError(errorStr + " is of non-%s type" % (typeStr))


# Helper function - checkRequiredFields
def checkRequiredFields(obj, requiredFields, optionalFields, errorStr, extraIsFatal = True):
        objFields = set(obj.keys())
        # missing fields
        missingFields = list(requiredFields - objFields)
        if missingFields:
            fatalError(errorStr + " is missing fields: %s" % (missingFields))
        # extra fields
        extraFields = list(objFields - (requiredFields | optionalFields))
        if extraFields:
            errorFunc = fatalError if extraIsFatal else warnError
            errorFunc(errorStr + " has extra fields: %s" % (extraFields))


# Helper function - checkObjectId
def checkObjectId(objId, collName, errorStr):
    if not pymongo.collection.Collection(database, collName).find_one({'_id': objId}, {'_id': 1}):
        fatalError(" is a dangling ObjectID")


# Helper function - isValidString
def isValidString(testString):
    if not testString:
        return " is empty"
    if '\n' in testString:
        return " contains newline character"
    if testString != testString.strip(' \t'):
        return " contains leading/trailing whitespace"
    if not re.match('^[A-Z0-9_ .-]*$', testString, re.IGNORECASE):
        return " contains non-alphanumeric character"
    return ""


## Print error functions
# Print error function - fatalError
def fatalError(errStr):
    print errStr
    exit(1)

# Print error function - warnError
def warnError(errStr):
    print errStr



## MAIN
## ------------------------------------------------

## Get and validate arguments
if len(sys.argv) != 3:
    print "Usage: %s HOST[:PORT] DATABASE" % sys.argv[0]
    exit(1)
# do better validation of hostname, port format
argHostname = sys.argv[1].split(':')[0]
argHostport = int(sys.argv[1].split(':')[1]) if len(sys.argv[1].split(':')) > 1 else 27017
argDBName = sys.argv[2]

try:

    ## Server connection
    connTimeout = 10
    connection = pymongo.connection.Connection(argHostname, argHostport, network_timeout = connTimeout)


    ## Database find and connect
    if argDBName not in connection.database_names():
        fatalError("Error: database \"%s\" not found on server" % (argDBName))
    try:
        database = pymongo.database.Database(connection, argDBName)
        checkColl('images', database, "Error:")
        checkColl('sessions', database, "Error:")
        imgIds = [str(imgItem['_id']) for imgItem in pymongo.collection.Collection(database, 'images').find({}, {'_id': 1})]
        for imgId in imgIds:
            print 'Checking image data collection: %s' % imgId
            checkColl(imgId, database, "Error:")
        unrefImageData = set(imgIds) - set(database.collection_names())
        if unrefImageData:
            warnError("Error: unreferenced image data collections: %s" % (unrefImageData))
        print "Check finished"
    except pymongo.errors.InvalidName as e:
        fatalError("Error: database name \"%s\" is not valid: %s" %(argDBName, e.message))


except pymongo.errors.AutoReconnect as e:
    fatalError("Error: could not connect to MongoDB server at \"%s:%d\"" % (argHostname, argHostport))
    exit(1)

