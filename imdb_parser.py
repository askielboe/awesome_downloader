import re
import settings as s
from Movie import Movie

# Download watchlist
def getMoviesFromWatchlist(url):
    import urllib2
    hdr = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    req = urllib2.Request(url, headers=hdr)
    watchlist = urllib2.urlopen(req)
    output = open('imdb_watchlist.xml','wb')
    output.write(watchlist.read())
    output.close()
    
    import xml.etree.ElementTree as ET
    tree = ET.parse('imdb_watchlist.xml')
    root = tree.getroot()
    
    movies = root[0][5:]
    
    return movies

def addMoviesToDatabase(movies):
    for movie in movies:
        name = movie[1].text
        movieTitle = re.sub(r' \([1-9].*\)','', name)
        movieYear = name.split('(')[1].split(')')[0].split(' ')[0]
        movieImdbId = movie[2].text.split('/')[4]
        
        # Check if the movie is already in the database
        q = session.query(Movie).filter(Movie.imdbId == movieImdbId)
        if len(q.all()) == 0:
            print "Adding "+movieTitle+" to database.."
            # If not add it to the database
            newMovie = Movie(movieTitle, movieYear)
            newMovie.imdbId = movieImdbId
            newMovie.last_searched = 0
            newMovie.downloaded = 0
            session.add(newMovie)
    
    session.commit()

#--------------------------------------------------------------------------------
# Connect to local database
#--------------------------------------------------------------------------------
from database_operations import create_session
session = create_session()

for watchlist in s.imdb_watchlists:
    movies = getMoviesFromWatchlist(watchlist)
    addMoviesToDatabase(movies)

