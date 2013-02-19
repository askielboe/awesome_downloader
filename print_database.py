#--------------------------------------------------------------------------------
# Connect to local database
#--------------------------------------------------------------------------------
from database_operations import create_session
session = create_session()

#--------------------------------------------------------------------------------
# Query database
#--------------------------------------------------------------------------------
from Movie import Movie
movies = session.query(Movie).filter(Movie.downloaded == 0).order_by(Movie.title).all()

#--------------------------------------------------------------------------------
# Print output
#--------------------------------------------------------------------------------
# Get current date and time
import time,datetime
timeNow = datetime.datetime.now()
timePosix = int(time.mktime(timeNow.timetuple()))

print "<--- Movies --->"
for movie in movies:
    
    hoursToNextSearch = int((movie.last_searched+86400 - timePosix)/3600.0)
    
    if movie.last_searched == 0:
        string = movie.title+' ('+str(movie.year)+')'+' '*(50-len(movie.title))+movie.imdbId+' '+str(movie.last_searched)+'\t\t'+'\t'+str(movie.downloaded)
    else: 
    	string = movie.title+' ('+str(movie.year)+')'+' '*(50-len(movie.title))+movie.imdbId+' '+str(movie.last_searched)+'\t'+str(hoursToNextSearch)+'\t'+str(movie.downloaded)
    
    print string
