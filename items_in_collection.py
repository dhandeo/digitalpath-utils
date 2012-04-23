import pymongo
import bson
import sys

class ItemsInSession():
	def __init__(self, item_type_string, db, root, session):
		""" accepts type of object, pymongo db instance, the root string to avoid conflicting names and sessions key """ 
		self.item_type = item_type_string
		self.db = db
		self.root = root

	def SetSession(self, session_key):
		# Look for the session 

		# Assign if the session is around else return false
		
		
		pass
	
	def SetItemType(self, item_type_string):
		pass

	def Insert(self, item):
		pass

	def Delete(self, session_key, item):
		pass


class Attachments(ItemsInSession):
	def __init__(self, db, root, session):
		ItemsInSession.__init__(self, "file", db, root, session)

	def Insert(self, item):
		pass
	
	def Delete(self, item_key):
		pass
		
	def List(self):
		pass
 




