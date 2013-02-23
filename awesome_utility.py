def getSession():
    #--------------------------------------------------------------------------------
    # Connect to local database
    #--------------------------------------------------------------------------------
    from database_operations import create_session
    session = create_session()
    return session

def getMovie(imdbid):
    from Movie import Movie
    session = getSession()
    
    movie = session.query(Movie).filter(Movie.imdbId == imdbid).all()
    
    if len(movie) > 0:
        m = movie[0]
        print "Found movie: "+m.title+" ("+str(m.year)+") - searched: "+str(m.last_searched)+" - downloaded: "+str(m.downloaded)
    else:
        print "No movies found.."

def setNotDownloaded(imdbid):
    from Movie import Movie
    session = getSession()
    movie = session.query(Movie).filter(Movie.imdbId == imdbid).all()
    if len(movie) > 0:
        m = movie[0]
        print "Found movie: "+m.title+" ("+str(m.year)+") - searched: "+str(m.last_searched)+" - downloaded: "+str(m.downloaded)
        print "Setting downloaded to FALSE.."
        print "Setting last_searched to 0.."
        m.last_searched = 0
        m.downloaded = 0
        session.add(m)
        session.commit()
    else:
        print "No movies found.."
