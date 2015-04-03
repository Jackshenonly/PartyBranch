from  PartyBranch import *
import os
def init_db():
    """Creates the database tables.
    please create the database   PartyInfo"""
    output = os.system('mysql -u root -p PartyInfo < schema.sql')
    #print output
init_db();