# First priority to have sim ilar functionality

import pymongo
import sys

from add_databases import add_database
from add_groups import add_group, sessions_in_group

print "Reached here 1"
# This will probably be called only for custom execution so no explicit main function. In fact this calls routines from add_database and add_groups

#server_name = "127.0.0.1";
#server_name = "140.247.106.97";
server_name = "slide-atlas.org";
database_name = "slideatlas"

# Open the database
conn = pymongo.Connection(server_name);

# Delete database if exists
conn.drop_database(database_name)

# Open the database
mongodb = conn[database_name]
# Add BEV

# Add the databases
db_obj = add_database(mongodb, server_name, "bev1", 'Harvard Combined Dermatology Residency Training Program', 'Copyright &copy 2011-12, Charles Palmer, Beverly Faulkner-Jones and Su-jean Seo. All rights reserved', 'letmein', 'MAmanage')

# Bev;s groups
add_group(mongodb, '365400966808177', 'Pathology Residents and Fellows BIDMC', db_obj)
add_group(mongodb, '302644506427080', 'Dermatology Residents UNM', db_obj)
add_group(mongodb, '231408953605826', 'Combined Dermatology Residency Training Program', db_obj)


# UNM
sessions_in_group(mongodb, "add", '302644506427080', "Slide Review 1")
sessions_in_group(mongodb, "add", '302644506427080', "Slide Review 2")

# Combined Derm Residents get access to both
sessions_in_group(mongodb, "add", '231408953605826', "Slide Review 1")
sessions_in_group(mongodb, "add", '231408953605826', "Slide Review 2")
sessions_in_group(mongodb, "add", '231408953605826', "Slide Review 3")
sessions_in_group(mongodb, "add", '231408953605826', "2012DBCmajorrxnpatterns")
sessions_in_group(mongodb, "add", '231408953605826', "2012DBCnormal")
sessions_in_group(mongodb, "add", '231408953605826', "2012DBCrxnpatterns")


# Path residents
sessions_in_group(mongodb, "add", '365400966808177', "Slide Review 1")
sessions_in_group(mongodb, "add", '365400966808177', "Slide Review 2")
sessions_in_group(mongodb, "add", '365400966808177', "Surgical Slide")

# Add PAUL
db_obj = add_database(mongodb, server_name, "paul3", 'Washington University School of Medicine', 'Copyright &copy 2011-12, Paul Bridgman. All rights reserved', 'showme', 'MOmanage')

add_group(mongodb, '320347061312744', 'Histology WUSM', db_obj)

sessions_in_group(mongodb, "add", '320347061312744', "all")

# Add DEMO
add_database(mongodb, server_name, "demo", 'Atlas Demonstration (No password)', 'Copyright &copy 2011-12, All rights reserved', '', '')

# Add JEREMY
db_obj = add_database(mongodb, server_name, "jnk1", 'WSI Jeremy Kay', 'Copyright &copy 2012, Jeremy Kay. All rights reserved', 'Easter', 'Easter12')

add_group(mongodb, '199923673454359', 'WSI Jeremy Kay', db_obj)

sessions_in_group(mongodb, "add", '199923673454359' , "all")

# Add K12 education
db_obj = add_database(mongodb, server_name, "edu1", 'K-12 Education', 'Copyright &copy 2012, All rights reserved', 'April', 'April12')

add_group(mongodb, '291414254276923', 'K-12 Education', db_obj)

sessions_in_group(mongodb, "add", '291414254276923' , "all")


# Add Wash U School of Medicine Neuroscience 
db_obj = add_database(mongodb, server_name, "wusmneuro1", 'Washington University School of Medicine Neuroscience', 'Copyright &copy 2011-12, WUSM Neuroscience. All rights reserved', 'neuro', 'science')
add_group(mongodb, '424621897590174', 'Neuroscience WUSM', db_obj)
sessions_in_group(mongodb, "add", '424621897590174', "all")

# Add BIDMC Pathology
#BIDMC Pathology

print "Done .."

