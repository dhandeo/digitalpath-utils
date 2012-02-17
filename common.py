
# Follow from main but example usage
# python add_groups.py localhost slideatlas
import pymongo
import sys
import bson.objectid as oid 

def get_object_in_collection(col, key):

	# Find if the key is id
	obj = None
	try:
		obj = col.find_one({'_id' : oid.ObjectId(key)})
		if obj <> None:
			return obj
	except:
		print "Error "
		pass
	
	# else check in the 
	obj = col.find_one({'name':key})

	if obj <> None:
		return obj
	
	# Return None or return false
	else:
		return None

