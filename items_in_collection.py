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

		# create a gridfs session from known information
		self.gf = gridfs.GridFS(db, root)

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
		pass

	def Delete(self, session_key, item):
		pass
	
	def List(self):
		print 'Base Listing ..'
		# Call mongodb gridfiles to list all the items in the given root
		print self.gf.list()	

	def Flush(self):
		# Remove all records
		self.db[self.root + ".chunks"].drop()
		self.db[root + ".files"].drop()

class Attachments(ItemsInSession):
	def __init__(self, db, root, session):
		ItemsInSession.__init__(self, "file", db, root, session)

	def Insert(self, data, name):
		# Make sure initialized correctly
		pass

		# 

