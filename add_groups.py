# Will create first collection for groups and accesses
import pymongo
import sys

# Mangually updated facebook groups and corresponding databases etc


if __name__ == '__main__':
	# get the command line arguments
	if len(sys.argv) < 3:
		print 'incorrect usage' 
		print 'correct use: python add_groups.py server database' 
		sys.exit(0)

	server = sys.argv[1]
	database = sys.argv[2]
	
	# Try opening the database	
	conn = pymongo.Connection(server); 
	db = conn[database]

	# Open required collections 
	col_sessions = db['sessions']
	col_groups = db['groups']

	groups = [('231677260223624','Massachusetts General Hospital'), 
			('320347061312744','BIDMC'), 
			('302644506427080','New Mexico')] 

	# Create a list of sessions (All by default)
	sessions = col_sessions.find()
	sessions_list = []

	print 'List of sessions available in this database :'
	count = 1
	for session in sessions:
		print count, ') ', session['_id']
		sessions_list.append(session['_id'])
		print "Done "

	for agroup in groups:
		print 'Processing group : ', agroup
	
		# create a python dictionary to add 
		group_obj = {}

		group_obj['facebook_id'] = agroup[0]
		group_obj['label'] = agroup[1]
		group_obj['can_see'] = sessions_list

		print group_obj, '\n\n'

		# Update database record 
		col_groups.insert(group_obj)
		


 


