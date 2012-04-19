import pymongo
import sys

from add_databases import add_database
from add_groups import add_group, sessions_in_group

# This will probably be called only for custom execution so no explicit main function. In fact this calls routines from add_database and add_groups

server_name = "127.0.0.1";
#server_name = "140.247.106.97";
#server_name = "slide-atlas.org";
database_name = "slideatlas"

# Open the database
conn = pymongo.Connection(server_name); 

# Delete database if exists
conn.drop_database(database_name)

# Open the database
mongodb = conn[database_name]

# Add DEMO 
add_database(mongodb, server_name, "demo", 'Atlas Demonstration (No password)', 'Copyright &copy 2011, All rights reserved', '', '')

print "Done .."

