# Create database
from sqlalchemy import create_engine

engine = create_engine('sqlite:///movies.db', echo=True)

from Movie import Movie

########################################################################
# create tables
Movie.metadata.create_all(engine)
