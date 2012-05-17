
# Follow from main but example usage
# python add_groups.py localhost slideatlas
import pymongo
import sys

def add_group(mongodb, facebook_id, name, db):
	agroup = mongodb["groups"].find_one({"facebook_id" : facebook_id})

	if agroup <> None:
		print "Group exists", agroup['facebook_id'], agroup['name'] 
	else:
		print "No group found, adding newly"

		# create a python dictionary to add 
		group_obj = {}

		group_obj['facebook_id'] = facebook_id 
		group_obj['label'] = name 
		group_obj['name'] = name 
		group_obj['db'] = db

		mongodb['groups'].insert(group_obj)
		print "Added ", group_obj

def session_in_group(mongodb, cmd, facebook_id, which):
	# Verify that the group exists
	print "    ", cmd, facebook_id, which
	if cmd == "add":
		# Update the can_see
		err = 	mongodb["groups"].update({"facebook_id" : facebook_id}, {"$addToSet" : {"can_see" : which}})
		if err <> None:
			print "Error .."

	elif cmd == "del":
		pass
	

def sessions_in_group(mongodb, cmd, facebook_id, which_all, soft=False, debug=False):
	# First find the group
	agroup = mongodb["groups"].find_one({"facebook_id" : facebook_id})

	if agroup <> None:
		print "Group exists", agroup['facebook_id'], agroup['name'] 
	else:
		print "Group", facebook_id, "NOT found"
		return False

	dbase = mongodb['databases'].find_one({'_id' : agroup['db']})

	if dbase == None:
		# We tried to add to a database which is not registered. Die
		print "Database registration record not found"
		return False
 
	#Connect to the registered 	
	conn2 = pymongo.Connection(dbase['host'])
	
	# Open the group and get the name of the database 
	db = conn2[dbase['dbname']] 

	# Gather the sessions  
	col_sessions = db['sessions']
			
	# Create a list of sessions (All by default)
	sessions = col_sessions.find(sort=[('name',pymongo.ASCENDING)])
	sessions_list = []

	print 'List of sessions available in this database :'
	count = 1
	for session in sessions:
		print "   ", count, ') ', session['_id']
		sessions_list.append((session['_id'], session['name']))
		count = count + 1
	print "Done "
	for ases in sessions_list:
		print ases

	if which_all == "all":
		# For all sessions call add_session_to_group
		print "Adding all sessions  ", cmd, facebook_id, "all"
		for asession in sessions_list:
			print "Adding"
			session_in_group(mongodb, cmd, facebook_id, asession[0])

	else:
		isnumber = False 
		try:
			val = int(which_all)
			isnumber = True
		except:
			# most likely it is a string
			isnumber = False

		if not isnumber:
			print 'Adding a particular session :', which_all
			# Create a list of sessions (All by default)
			asession = col_sessions.find_one({"name" : which_all})
			if asession <> None:
				session_in_group(mongodb, cmd, facebook_id, asession['_id'])
			else:
				print "Not found"
		else:
			if which_all < 0:
				print "  ", cmd, facebook_id, "Adding sorted"
				for asession in sessions_list[which_all:]:
					session_in_group(mongodb, cmd, facebook_id, asession[0])
		
def manually_add_groups(conn, database):
	# Calls the add group function for different facebook groups 
	mongodb = conn[database]
	# Not adding sessions

	# Bev;s groups 
	add_group(mongodb, '365400966808177','Pathology Residents and Fellows BIDMC', "bev1") 
	add_group(mongodb, '302644506427080','Dermatology Residents UNM', "bev1")
	add_group(mongodb, '231408953605826', 'Combined Dermatology Residency Training Program',"bev1")

	add_group(mongodb, '320347061312744','Histology WUSM', "paul2") 
	
	# Adding sessions one by one 

	sessions_in_group(mongodb, "add", '365400966808177', -2)
	sessions_in_group(mongodb, "add", '302644506427080', -2)
	sessions_in_group(mongodb, "add", '231408953605826', -2)
                             
	sessions_in_group(mongodb, "add", '320347061312744', "all")

# Mangually updated facebook groups and corresponding databases etc
if __name__ == '__main__':
	# get the command line arguments
	if len(sys.argv) < 3:
		print 'incorrect usage' 
		print 'correct use: python add_groups.py server database [force]' 
		sys.exit(0)

	server = sys.argv[1]
	database = sys.argv[2]

	# Cleanup if force parameter specified
	try:	
		force = int(sys.argv[3]) 
	except:
		force = 0

	# Try opening the database	
	conn = pymongo.Connection(server); 

	if force:
		print "Trying to drop groups collection ..", 
		conn[database].drop_collection('groups')

	manually_add_groups(conn, database)
	sys.exit(0)


	# Open required collections 
	col_sessions = db['sessions']
	col_groups = db['groups']

			
	# Create a list of sessions (All by default)
	sessions = col_sessions.find(sort=[('name',pymongo.DESCENDING)])
	sessions_list = []

	print 'List of sessions available in this database :'
	count = 1
	for session in sessions:
		print count, ') ', session['_id']
		sessions_list.append((session['_id'], session['name']))
		count = count + 1
	
	print "Done "

	print sessions_list

	# clean group 

	numgroups = db['groups'].find().count()
	if numgroups > 0:
		print "Num Count :", numgroups
		print "Already exists, use modify_group"
		sys.exit(0)

	else:
		print 'Continuing ...\n'


	for agroup in groups:
		print 'Processing group : ', agroup
	
		# create a python dictionary to add 
		group_obj = {}

		group_obj['facebook_id'] = agroup[0]
		group_obj['label'] = agroup[1]
		group_obj['can_see'] = sessions_list[:2]

		print group_obj, '\n\n'

		# No Session is visible right now
		# Alphabetically sorted last session

		# Update database record 
		col_groups.insert(group_obj)
