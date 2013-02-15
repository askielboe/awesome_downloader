import re

#--------------------------------------------------------------------------------
# Connect to local database
#--------------------------------------------------------------------------------
from database_operations import create_session
session = create_session()

from Movie import Movie
movies = session.query(Movie).all()

movieTitles = []
# # #
# Open downloaded file
infile = open('downloaded.txt')
for line in infile:
    movieTitle = re.sub(r'\.*[ .(][1-9].*','', line)
    movieTitle = ' '.join(movieTitle.split('.'))
    movieTitle = movieTitle.rstrip('\n')
    movieTitles.append(movieTitle)

for movie in movies:
    if movie.title in movieTitles:
        movie.downloaded = 1
        print movie.title+' ALREADY DOWNLOADED!' 
        session.add(movie)

session.commit()