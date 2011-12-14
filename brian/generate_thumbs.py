
# Template for database util

import sys, pymongo
import re, StringIO, wx
from bson import Binary

DISPLAY = False
UPLOAD = True


def doWork(database):

    app = wx.App()

    for dbName in database.collection_names():
        if re.match('^[0-9a-f]{24}$', dbName):
            imgDataColl = pymongo.collection.Collection(database, dbName)
            if not imgDataColl.find_one({'name': 'thumb.jpg'}, {'_id': 1}):
                imgDoc = imgDataColl.find_one({'name': 't.jpg'})
                print 'Processing for ', dbName
                
                baseImg = imgDoc['file']
                wxImgRaw = wx.ImageFromStream(StringIO.StringIO(str(baseImg)), type = wx.BITMAP_TYPE_JPEG)
                wxImgCrop = AutoCropWhiteSpace(wxImgRaw, 245)

                if wxImgCrop.GetWidth() < wxImgCrop.GetHeight():
                    newWidth = int(256.0 * ( float(wxImgCrop.GetWidth()) / float(wxImgCrop.GetHeight()) ))
                    newHeight = 256
                    newPosX = (256 - newWidth) / 2
                    newPosY = 0
                else:
                    newWidth = 256
                    newHeight = int(256.0 * ( float(wxImgCrop.GetHeight()) / float(wxImgCrop.GetWidth()) ))
                    newPosX = 0
                    newPosY = (256 - newHeight) / 2
                wxImgCrop.Rescale(newWidth, newHeight, wx.IMAGE_QUALITY_HIGH)
                wxImgFinal = wxImgCrop.Size((256, 256), (newPosX, newPosY), 255, 255, 255)

                if DISPLAY:
                    wxBmpRaw = wx.BitmapFromImage(wxImgRaw)
                    wxBmpCrop = wx.BitmapFromImage(wxImgCrop)
                    wxBmpFinal = wx.BitmapFromImage(wxImgFinal)

                    frame = wx.Frame(None)
                    sizer = wx.BoxSizer(wx.VERTICAL)

                    sizer.Add( wx.StaticBitmap(frame, bitmap = wxBmpRaw) )
                    sizer.AddSpacer(25)

                    sizer.Add( wx.StaticBitmap(frame, bitmap = wxBmpCrop) )
                    sizer.AddSpacer(25)

                    sizer.Add( wx.StaticBitmap(frame, bitmap = wxBmpFinal) )
                    sizer.AddSpacer(25)

                    label = wx.StaticText(frame, label = dbName)
                    label.SetForegroundColour('RED')
                    sizer.Add( label )

                    frame.SetSizer(sizer)
                    frame.Show()
                    frame.SetSize((400, 900))
                    frame.SetBackgroundColour('BLUE')
                    app.MainLoop()

                if UPLOAD:
                    outputStream = StringIO.StringIO()
                    wxImgFinal.SaveStream(outputStream, wx.BITMAP_TYPE_JPEG)
                    newDoc = {'name': 'thumb.jpg',
                              'level': imgDoc['level'],
                              'xs': imgDoc['xs'],
                              'xe': imgDoc['xe'],
                              'ys': imgDoc['ys'],
                              'ye': imgDoc['ye'],
                              'file':  Binary(outputStream.getvalue()) # change to use BSON.binary
                             }
                    imgDataColl.insert(newDoc, safe = True)





def AutoCropWhiteSpace(inputImage, channelThreshold):
    class Found(Exception): pass
    imHeight = inputImage.GetHeight()
    imWidth = inputImage.GetWidth()
    clipRect = wx.Rect()

    def underThreshold(x, y):
        return inputImage.GetRed(x,y) < channelThreshold or inputImage.GetGreen(x,y) < channelThreshold or inputImage.GetBlue(x,y) < channelThreshold
    
    # top
    try:
        for y in range(imHeight):
            for x in range(imWidth):
                if underThreshold(x, y):
                    clipRect.SetTop(max(y-1, 0))
                    raise Found
    except Found:
        pass
    
    # bottom
    try:
        for y in reversed(range(imHeight)):
            for x in range(imWidth):
                if underThreshold(x, y):
                    clipRect.SetBottom(min(y+1, imHeight-1)), inputImage.GetBlue(x,y)
                    raise Found
    except Found:
        pass
    
    # left
    try:
        for x in range(imWidth):
            for y in range(imHeight):
                if underThreshold(x, y):
                    clipRect.SetLeft(max(x-1, 0))
                    raise Found
    except Found:
        pass
    
    # right
    try:
        for x in reversed(range(imWidth)):
            for y in range(imHeight):
                if underThreshold(x, y):
                    clipRect.SetRight(min(x+1, imWidth-1))
                    raise Found
    except Found:
        pass
    
    return inputImage.GetSubImage(clipRect)


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



