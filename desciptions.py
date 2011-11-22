import pymongo
import sys

# connect with the database
try:
	conn = pymongo.Connection()
	db = conn['pathdemo']
	#db = conn['clay1']
	print 'Connection OK'
except:
	print 'Cound not Connect ..'

# loop through all collections 

cols = db.collection_names()

desc = {}

desc['1028'] = '1028 urticarial vasculitis'
desc['1090'] = "1090 sweet's syndrome"
desc['2729'] = '2729 abnormal / disrupted mitoses due to etoposide'
desc['1091'] = '1091 granuloma faciale'
desc['1243'] = '1243 disseminated intravascular coagulation'
desc['1613'] = '1613 pyoderma gangrenosum, ulcerated'
desc['3031'] = '3031 atypical lymphocytic infiltrate, due to phenytoin'
desc['3562'] = '3562 rash due to granulocyte / monocyte colony stimulating factor (GMCSF)'
desc['939'] = '939   epidermal dysmaturation due to 5-fluorouracil'
desc['5497'] = '5497 subcorneal pulstular eruption, probably AGEP, in pt on many antibiotics'
desc['1671'] = '1671 erythema elevatum diutinum, early'

for col_name in cols:
	# skip if starts with system
	if col_name[0:6] <> 'system':
		print 'Opening collection : ' + col_name
		col = db[col_name]
		if desc.has_key(col_name):
			col.insert({"name" : "meta",
				    "desc" :  desc[col_name]},safe=True)
		else:
			print 'Description error'
			sys.exit(0)				
	
		print '  With %d records'%(col.count())
		print '  ' + str(col.index_information())
		print '  Creating index ...' 
		col.ensure_index("name")
		print "\r  Done ...    "
