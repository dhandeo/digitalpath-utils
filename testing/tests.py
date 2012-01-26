import re, collections, pymongo, bson

imagesRequiredFields = set(['_id', 'name', 'origin', 'dimension', 'spacing'])
imagesOptionalFields = set(['hide', 'startup_view', 'bookmarks'])

sessionsRequiredFields = set(['_id', 'name', 'label', 'images'])
sessionsOptionalFields = set([])

imageDataRequiredFields = set(['_id', 'name', 'level', 'xs', 'xe', 'ys', 'ye', 'file'])
imageDataOptionalFields = set(['size'])


############################################################################################

def failTest(message, code = 1):
    global testValue
    testValue = code
    print message


###################################################################################



# missing collections

# empty collections


def TestImages_RequiredFields(database):
    checkRequiredFields(database, 'images', imagesRequiredFields)


def TestImages_SuperfluousFields(database):
    checkSuperfluousFields(database, 'images', imagesRequiredFields, imagesOptionalFields)


def TestImages_StringFieldsFormat(database):
    checkStringFields(database, 'images', ['name'])


def TestImages_UniqueName(database):
    checkUniqueField(database, 'images', 'name')


def TestImages_CoordFieldsFormat(database):
#for coordField in ['origin', 'dimension', 'spacing']:
#    checkCoordField(docObj, coordField, docErrorStr)
    pass


def TestImages_StartupView(database):
    pass


def TestSessions_RequiredFields(database):
    checkRequiredFields(database, 'sessions', sessionsRequiredFields)


def TestSessions_SuperfluousFields(database):
    checkSuperfluousFields(database, 'sessions', sessionsRequiredFields, sessionsOptionalFields)


def TestSessions_StringFieldsFormat(database):
    checkStringFields(database, 'sessions', ['name', 'label'])


def TestSessions_UniqueName(database):
    checkUniqueField(database, 'sessions', 'name')


def TestSessions_ImagesList(database):
    checkRefListField(database, 'sessions', 'images', 'images')


def TestImageData_RequiredFields(database):
    for collName in imageDataCollNames(database):
        checkRequiredFields(database, collName, imageDataRequiredFields)


def TestImageData_SuperfluousFields(database):
    for collName in imageDataCollNames(database):
        checkSuperfluousFields(database, collName, imageDataRequiredFields, imageDataOptionalFields)


def TestImageImageData_Correspondence(database):
    imageIds = set([str(imageDoc['_id']) for imageDoc in pymongo.collection.Collection(database, 'images').find({}, {'_id': 1})])
    imageDataIds = set(imageDataCollNames(database))
    danglingImageIds = imageIds - imageDataIds
    unrefImageDataIds = imageDataIds - imageIds
    for danglingImageId in sorted(list(danglingImageIds)):
        failTest( "db.images.%s has no corresponding image data collection" % danglingImageId )
    for unrefImageDataId in sorted(list(unrefImageDataIds)):
        failTest( "db.%s is not referenced by any db.images document" % unrefImageDataId )


#####################################################################################################################


def imageDataCollNames(database):
    return [collName for collName in sorted(database.collection_names()) if re.match('^[0-9a-f]{24}$', collName)]


def checkRequiredFields(database, collName, requiredFields):
    collObj = pymongo.collection.Collection(database, collName)
    for docObj in collObj.find({}, {'file': 0}).sort('_id'): # optimization: do not return 'file' field of imageData
        missingFields = requiredFields - set(docObj.keys()) - set(['file']) # bypass checking for 'file' field of imageData
        if missingFields:
            try:
                failTest( "db.%s.%s is missing fields: %s" % (collName, docObj['_id'], sorted(list(missingFields))) )
            except KeyError:
                failTest( "db.%s has document with no '_id' field" )


def checkSuperfluousFields(database, collName, requiredFields, optionalFields):
    collObj = pymongo.collection.Collection(database, collName)
    for docObj in collObj.find({}, {'file': 0}).sort('_id'): # optimization: do not return 'file' field of imageData
        extraFields = set(docObj.keys()) - (requiredFields | optionalFields)
        if extraFields:
            try:
                failTest( "db.%s.%s has extra fields: %s" % (collName, docObj['_id'], sorted(list(extraFields))) )
            except KeyError:
                failTest( "db.%s has document with no '_id' field" )


def checkStringFields(database, collName, fieldNames):
    collObj = pymongo.collection.Collection(database, collName)
    for docObj in collObj.find({}, fieldNames).sort('_id'): # find() also takes a list for its 2nd argument
        for fieldName in fieldNames:
            invalidReason = isValidString(docObj[fieldName])
            if invalidReason:
                failTest( "db.%s.%s.%s %s" % (collName, docObj['_id'], fieldName, invalidReason) )


def checkUniqueField(database, collName, fieldName):
    collObj = pymongo.collection.Collection(database, collName)
    fieldValueCount = collections.defaultdict(int)
    for docObj in collObj.find({}, {fieldName: 1}).sort('_id'):
        fieldValueCount[docObj[fieldName]] += 1
    for duplicateFieldValue in [fieldValue for (fieldValue, count) in fieldValueCount.iteritems() if count > 1]:
        for docObj in collObj.find({fieldName: duplicateFieldValue}, {fieldName: 1}).sort('_id'):
            failTest( "db.%s.%s.%s has non-unique value: %s" % (collName, docObj['_id'], fieldName, duplicateFieldValue) )


def checkRefListField(database, collName, fieldName, refCollName):
    collObj = pymongo.collection.Collection(database, collName)
    for docObj in collObj.find({}, {fieldName: 1}).sort('_id'):
        if not isType(docObj[fieldName], list):
            failTest( "db.%s.%s.%s is of non-list type" % (collName, docObj['_id'], fieldName) )
            continue
        posValueCount = collections.defaultdict(int)
        for listElem in docObj[fieldName]:
            if not isType(listElem, dict):
                failTest( "db.%s.%s.%s contains element of non-dict type" % (collName, docObj['_id'], fieldName) )
                break
            if set(listElem.iterkeys()) != set(['pos', 'ref']): # TODO: update this to allow optional 'label' field
                failTest( "db.%s.%s.%s contains element not of the form '{pos:, ref:}'" % (collName, docObj['_id'], fieldName) )
                break
            if not isType(listElem['pos'], [int, float, long]):
                failTest( "db.%s.%s.%s contains element where 'pos' is of non-numeric type: %s" % (collName, docObj['_id'], fieldName, listElem) )
            else:
                posValueCount[listElem['pos']] += 1
            if not isType(listElem['ref'], bson.objectid.ObjectId):
                failTest( "db.%s.%s.%s contains element where 'ref' is of non-ObjectId type" % (collName, docObj['_id'], fieldName) )
            else:
                if not pymongo.collection.Collection(database, refCollName).find_one({'_id': listElem['ref']}, {'_id': 1}):
                    failTest( "db.%s.%s.%s contains element where 'ref' points to a nonexistent document: db.%s.%s" % (collName, docObj['_id'], fieldName, refCollName, listElem['ref']) )
            # TODO: if 'label' field exists, check isValidString
        for duplicatePosValue in [posValue for (posValue, count) in posValueCount.iteritems() if count > 1]:
            failTest( "db.%s.%s.%s contains multiple elements where 'pos' has non-unique value: %s" % (collName, docObj['_id'], fieldName, duplicatePosValue) )


def checkCoordField(database, collName, fieldName):
    collObj = pymongo.collection.Collection(database, collName)
    for docObj in collObj.find({}, {fieldName: 1}).sort('_id'):
        if not checkType(docObj[fieldName], list):
            failTest( "db.%s.%s.%s is of non-list type" % (collName, docObj['_id'], fieldName) )
            continue
        if len(docObj[fieldName]) != 3:
            failTest( "db.%s.%s.%s has length other than 3" % (collName, docObj['_id'], fieldName) )
        for coordElem in docObj[fieldName]:
            if not isType(coordElem, [int, float, long]):
                failTest( "db.%s.%s.%s contains element of non-numeric type" % (collName, docObj['_id'], fieldName) )
        if docObj[fieldName] == [0, 0, 0] or docObj[fieldName] == [1, 1, 1]:
            failTest( "db.%s.%s.%s is trivial value: %s" % (collName, docObj['_id'], fieldName, docObj[fieldName]) )















# Helper function
def isType(obj, typeObj):
    typeObjList = typeObj if isinstance(typeObj, list) else [typeObj]
    resultList = [isinstance(obj, typeObjItem) for typeObjItem in typeObjList]
    if not reduce(lambda a, b: a or b, resultList):
        return False
    return True


def isValidString(testString):
    if not isType(testString, basestring):
        return "is of non-string type"
    if not testString:
        return "is empty"
    if '\n' in testString:
        return "contains newline character"
    if testString != testString.strip(' \t'):
        return " contains leading/trailing whitespace"
    if not re.match('^[A-Z0-9_ ./()-]*$', testString, re.IGNORECASE):
        return "contains non-alphanumeric character"
    return ""




















