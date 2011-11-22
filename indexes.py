import pymongo


# connect with the database
try:
	conn = pymongo.Connection()
	db = conn['daniels']
	#db = conn['clay1']
	print 'Connection OK'
except:
	print 'Cound not Connect ..'

# loop through all collections 

cols = db.collection_names()

for col_name in cols:
	# skip if starts with system
	if col_name[0:6] <> 'system':
		print 'Opening collection : ' + col_name
		col = db[col_name]
		print '  With %d records'%(col.count())
		print '  ' + str(col.index_information())
		print '  Creating index ...' 
		col.ensure_index("x")
		print "\r  Done ...    "
