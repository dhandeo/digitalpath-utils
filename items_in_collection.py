import pymongo


class item_type():
	def __init__(self, type_name):
		self.type_name = type_name

class items_in_collection():
	def __init__(self, item_type_string):
		self.item_type = item_type_string
		pass

	def SetSession(self, session_key):
		pass
	
	def SetItemType(self, item_type_string):
		pass

	def Insert(self, item):
		pass

	def Delete(self, session_key, item):
		pass


class images_in_collection(items_in_collection):
	def __init__(self):
			items_in_collection.__init__(self, "images")
