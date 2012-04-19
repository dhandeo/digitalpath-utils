import pymongo
import bson
import sys

class ItemsInCollection():
	def __init__(self, item_type_string, db, root, session_key=None):
		self.item_type = item_type_string
		self.db = db
		self.root = root

		if not session_key == None:
			self.SetSession(session_key)

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


class Attachments(ItemsInCollection):
	def __init__(self, db, root):
		items_in_collection.__init__(self, "attachments")

	def Insert(self, item):
		pass
	
	def Delete(self, item_key):
		
	def List(self):
 




