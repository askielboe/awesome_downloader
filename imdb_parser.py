import re
import urllib2
import settings as s
from Movie import Movie

# Download watchlist
def getMoviesFromWatchlist(url):
    # Set headers
    hdr = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'User-Agent': 'Mozilla/5.0'}

    # Download watchlist from IMDB using cookie for Original movie titles
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', 'id=BCYuXiiVdBJgg8M80eMlcICM4VGRVgMXxwFo8FyFAfykZKhcPIpYEW4Avk_rqmksEl72AAcRD8E_8Mr0SSl62Z06_jXIjHhob4OtMRltdEvNVFaKhQ-16OZqh8RU5s4pphdFAiWYDBQn6ueRKD3W2sgclFfCw7tJYo0sK7eN3w_a-fOx6TkHsXTq_asId1oWfn33'))
    f = opener.open(url)
    html = f.readlines()

    # Parse movies in CSV watchlist
    movies = []
    line = html[0].split('","')

    # If its our own watchlist en extra column shifts the year column by one
    if line[8].decode('utf-8') == 'You rated':
        yearPosition = 11
    else:
        yearPosition = 10

    # Parse movie information
    for line in html[1:]:
        line = line.split('","')
        # IMDBid, title, year
        movies.append([line[1].decode('utf-8'), line[5].decode('utf-8'), line[yearPosition].decode('utf-8')])

    return movies

def addMoviesToDatabase(session, movies):
    nAdded = 0
    for movie in movies:
        movieImdbId = movie[0]
        movieTitle = movie[1]
        movieYear = movie[2]

        # Check if the movie is already in the database
        q = session.query(Movie).filter(Movie.imdbId == movieImdbId)
        if len(q.all()) == 0:
            print "Adding "+movieImdbId+": "+movieTitle+" ("+movieYear+") to database.."
            # If not add it to the database
            newMovie = Movie(movieTitle, movieYear)
            newMovie.imdbId = movieImdbId
            newMovie.last_searched = 0
            newMovie.downloaded = 0
            session.add(newMovie)
            nAdded += 1

    session.commit()
    session.close()
    return nAdded

def imdbParse():
    #--------------------------------------------------------------------------------
    # Connect to local database
    #--------------------------------------------------------------------------------
    from database_operations import create_session
    session = create_session()

    nAdded = 0
    for watchlist in s.imdb_watchlists:
        movies = getMoviesFromWatchlist(watchlist)
        nAdded += addMoviesToDatabase(session, movies)

    print "Number of movies added from watchlists: ",nAdded

if __name__ == '__main__':
    imdbParse()

