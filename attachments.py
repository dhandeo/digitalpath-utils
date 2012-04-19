# Follow from main but example usage
# python add_groups.py localhost slideatlas

# adds or delets attachments from sessions 
# The attachment must already exist

import pymongo
import sys
import bson.objectid as oid 
from common_utils import get_object_in_collection

def attachment_in_session(mongodb, cmd, session_key, attachment_key, force=False):

	# Verify that the session exists
	session = get_object_in_collection(mongodb['sessions'], session_key)
	attachment = get_object_in_collection(mongodb['attachments'], attachment_key)
	
	if attachment == None or session == None:
		print "Could not find objects for ", attachment_key, " or ", session_key
		return
	
	if cmd == "add":
		# Update the can_see
		print "Adding .."
		attachments = session['attachments']

		max = 0		
		for anattachment in attachments:
			#print anattachment
			if anattachment['pos'] > max:
				max = anattachment['pos']

		new_attachment = {}
		new_attachment[u'ref'] = attachment['_id']
		new_attachment[u'pos'] = max + 1 
		new_attachment[u'hide'] = False

		attachments.append(new_attachment)
		mongodb['sessions'].update({'_id': session['_id']}, {'$set':{'attachments': attachments}})

		for a in attachments:
			print a
		
		pass
	
	elif cmd == "del":
		print "Deleting .."
		
		# verify if the attachment is listed in the session 
		found = False
		attachments = session['attachments']
		
		for anattachment in attachments:
			#print anattachment
			if anattachment['ref'] == attachment['_id']:
				print 'Found'  
				found = True
				print anattachment
				index = attachments.index(anattachment)
				attachments[index]['hide'] = True
		
		if found == False:
			print "attachment not found in session"
			
		print attachments
		mongodb['sessions'].update({'_id': session['_id']}, {'$set':{'attachments': attachments}})

def copy_attachment(from_mongodb, from_attachment, from_session):
	pass


# Main to accept command line and do the operation on attachments. 
if __name__ == '__main__':
	# get the command line arguments
	if len(sys.argv) < 3:
		print 'incorrect usage' 
		print 'correct use: python attachments.py server database command session attachment [force]' 
		sys.exit(0)

	server   = sys.argv[1]
	database = sys.argv[2]
	command  = sys.argv[3]
	attachment    = sys.argv[4]
	session  = sys.argv[5]
	
	# Cleanup if force parameter specified
	try:	
		force = int(sys.argv[6]) 
	except:
		force = 0

	try:
		# Try opening the database	
		conn = pymongo.Connection(server); 
		mongodb = conn[database]
	
	except:
		print "Error opening ", database, " at ", server
	if force:
		print "Using Force ..", 

	attachment_in_session(mongodb, command, session, attachment, force)

	sys.exit(0)
