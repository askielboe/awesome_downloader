import re

# Download watchlist
import urllib2
watchlist = urllib2.urlopen('http://rss.imdb.com/user/ur9843189/watchlist')
output = open('imdb_watchlist.xml','wb')
output.write(watchlist.read())
output.close()

import xml.etree.ElementTree as ET
tree = ET.parse('imdb_watchlist.xml')
root = tree.getroot()

# Connect to local database
#--------------------------------------------------------------------------------
# Define database
#--------------------------------------------------------------------------------
from sqlalchemy import create_engine
engine = create_engine('sqlite:///movies.db')

#--------------------------------------------------------------------------------
# Create a session to start talking to the database
#--------------------------------------------------------------------------------
from sqlalchemy.orm import sessionmaker
# Since the engine is already created we can bind to it immediately
Session = sessionmaker(bind=engine)
session = Session()

from Movie import Movie

movies = root[0][5:]
for movie in movies:
    name = movie[1].text
    movieTitle = re.sub(r' \([1-9].*\)','', name)
    movieYear = name.split('(')[1].split(')')[0].split(' ')[0]
    movieImdbId = movie[2].text.split('/')[4]
    
    # Check if the movie is already in the database
    q = session.query(Movie).filter(Movie.imdbId == movieImdbId)
    if len(q.all()) == 0:
        # If not add it to the database
        newMovie = Movie(movieTitle, movieYear)
        newMovie.imdbId = movieImdbId
        newMovie.last_searched = 0
        newMovie.downloaded = 0
        session.add(newMovie)

session.commit()

