import pymongo

conn = pymongo.Connection()

db = conn['daniels']
cols = db.collection_names()

for col_name in cols:
	try:
		num = int(col_name)
	except:
		num = 99999

	if num < 201:
		print col_name + ' is being deleted' 
		#db[col_name].drop() 
