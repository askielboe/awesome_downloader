# 
# File:    database_operations.py 
# 
# Author:  Andreas Skielboe (skielboe@gmail.com)
# Date:     August 2012
# 
# Summary of File: 
# 
#   Functions that connect to and modify the database at the lowest levels in SQLalchemy
# 

import settings as s

def create_session():
    #--------------------------------------------------------------------------------
    # Define database
    #--------------------------------------------------------------------------------
    from sqlalchemy import create_engine
    engine = create_engine('sqlite:///'+s.dbPath)
    
    #--------------------------------------------------------------------------------
    # Create a session to start talking to the database
    #--------------------------------------------------------------------------------
    from sqlalchemy.orm import sessionmaker
    # Since the engine is already created we can bind to it immediately
    Session = sessionmaker(bind=engine)
    return Session()
