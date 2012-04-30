import pymongo
import gridfs
import bson
import sys

class MongoBase():
	"""
	In future also manage the secure connection etc
	"""	
	def __init__(db):
		self.db = db

class ItemsInGridFS(MongoBase):
	"""
	Class and functions related with storing large items in gridfs
	Does not stand on its own, requires self.db an initialized mongodb instance
	"""
	def __init__(self, item_type_string, db):
		# create a gridfs session from known information
		self.item_type = self.item_type_string
		self.gf = gridfs.GridFS(self.db, self.item_type_string)
	
	def Flush(self):
		# Remove all records
		ItemsInSession.Flush(self)
		print "Removing", self.item_type + "from system .."
		self.db[self.item_type + ".files"].drop()
		self.db[self.item_type + ".chunks"].drop()

	def Insert(self, data, name):
		""" Accepts the data to store"""
		# Put the attachment in the gridfs and call the base insertion to add the id in the session
		newid = bson.ObjectId()		
		# Store the id in the grid file system
		self.gf.put(data,filename=name, _id=newid)
		return newid

class ItemsInSession(MongoBase):
	"""
	Derived classes neeed to take care of the individual storage and then add to the metadata using base class
	Does not stand on its own, requires self.db an initialized mongodb instance
	"""
	def __init__(self, item_type_string, db, session):
		""" accepts type of object, pymongo db instance, the root string to avoid conflicting names and sessions key """ 
		self.item_type = item_type_string
		self.db = db
		self.session = session
		print 'Root set at ', root

	def Insert(self, newid):
		""" Accepts the data to store"""
		self.db['sessions'].update( { "_id" : self.session['_id']}, {'$push' : { self.root : newid } })
		pass
	
	def List(self):
		print 'GridFS Listing ..', self.gf.list()	

		self.session = self.db['sessions'].find_one({'_id' : self.session['_id']})

		try :
			print 'Session record ..', self.session['attachments']
		except KeyError:
			print 'No attachment record in the session'
		

	def Flush(self):
		# remove attachments field from the session object
		self.db['sessions'].update( { "_id" : self.session['_id']}, {'$unset' : {self.root :1} })

class Attachments(ItemsInSession, ItemsInGridFS):
	def __init__(self, db, root, session):
		""" init subclasses with proper variables """
		MongoBase.__init__(self, db)
		self.igfs = ItemsInGridFS("attachments")
		ItemsInSession.__init__(self, session)

	def Insert(self, data, name):
		""" Accepts the data to store"""
		# Put the attachment in the gridfs and 
		newid =	ItemsInGridFS.Insert(data, name)
		ItemsInSession.Insert(newid)

	def Flush(self):
		# Remove all records
		ItemsInGridFS.Flush(self)
		ItemsInSession.Flush(self)

