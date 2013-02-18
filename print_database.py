#--------------------------------------------------------------------------------
# Connect to local database
#--------------------------------------------------------------------------------
from database_operations import create_session
session = create_session()

#--------------------------------------------------------------------------------
# Query database
#--------------------------------------------------------------------------------
from Movie import Movie
movies = session.query(Movie).order_by(Movie.title).all()

#--------------------------------------------------------------------------------
# Print output
#--------------------------------------------------------------------------------
print "<--- Movies --->"
for movie in movies:
    print movie.title, ' (', movie.year, ')\t\t\t', movie.imdbId, ' ', movie.last_searched, ' ', movie.downloaded

