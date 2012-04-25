import pymongo
import gridfs
import bson
import sys

class ItemsInSession():
	def __init__(self, item_type_string, db, root, session):
		""" accepts type of object, pymongo db instance, the root string to avoid conflicting names and sessions key """ 
		self.item_type = item_type_string
		self.db = db
		self.root = root
		self.session = session

		# create a gridfs session from known information
		self.gf = gridfs.GridFS(self.db, self.root)

		print 'Root set at ', root

	def SetSession(self, session_key):
		# Look for the session 

		# Assign if the session is around else return false
		
		
		pass
	
	def SetItemType(self, item_type_string):
		pass

	def Insert(self, data, name):
		""" Accepts the data to store"""

		newid = bson.ObjectId()		
		# Store the id in the grid file system
		self.gf.put(data,filename=name, _id=newid)
		# Store the id and metadata in the session
		
		self.db['sessions'].update( { "_id" : self.session['_id']}, {'$push' : { 'attachments' : newid } })
		pass

	def Delete(self, session_key, item):
		
		pass
	
	def List(self):
		print 'GridFS Listing ..', self.gf.list()	

		self.session = self.db['sessions'].find_one({'_id' : self.session['_id']})

		try :
			print 'Session record ..', self.session['attachments']
		except KeyError:
			print 'No attachment record in the session'
		

	def Flush(self):
		# Remove all records
		print "Removing files .. "
		self.db[self.root + ".files"].drop()
		print "Removing chunks .. "
		self.db[self.root + ".chunks"].drop()
		
		# remove attachments field from the session object
		self.db['sessions'].update( { "_id" : self.session['_id']}, {'$unset' : {'attachments' :1} })


class Attachments(ItemsInSession):
	def __init__(self, db, root, session):
		ItemsInSession.__init__(self, "file", db, root, session)

