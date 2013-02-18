# coding: utf-8
import random
import settings as s
import twill.commands as tc
from pushover import pushover

tc.redirect_output('twill.log')

# # #
# Functions
def doLogin():
    # Login
    tc.go('http://awesome-hd.net/login.php')
    
    # If we are redirected it means that we are already logged in
    try:
        tc.url('http://awesome-hd.net/login.php')
    except:
        return
    
    tc.fv("1", "username", s.username)
    tc.fv("1", "password", s.password)
    tc.submit('0')

def doSearch(movieTitle, movieYear):
    # Convert non-unicode characters
    movieTitle = removeNonUnicodeChars(movieTitle)
    
    # Search
    tc.go('http://awesome-hd.net/torrents.php')
    tc.fv('1','searchstr',movieTitle)
    tc.submit()
    
    # Save html page
    tc.save_html()
    
    # # #
    # Parse HTML
    torrents_html = open('torrents.php', 'r')
    html = torrents_html.readlines()
    torrents_html.close()
    
    return html

def getLink(html, movieTitle, movieYear):
    # Convert non-unicode characters
    movieTitle = removeNonUnicodeChars(movieTitle)
    
    link = ''
    i = 0
    while i < len(html):
        if 'title=\"View Torrent\">'+movieTitle+'</a>'+' ['+str(movieYear)+']' in html[i]:
            i += 1
            while i < len(html):
                if '1080p' in html[i] \
                    and 'Blu-Ray' in html[i] \
                    and '75% Freeleech' in html[i] \
                    and 'Remux' not in html[i]:
                    
                    link = 'http://awesome-hd.net/'+html[i-3].lstrip('\t\t\t\t[<a href="').rstrip('" title="Download">DL</a>\n')
                    link = ''.join(link.split('amp;'))
                if '<td colspan="2">' in html[i]:
                    i = len(html)
                i += 1
        i += 1
    return link

def getValidFilename(filename):
    import string
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    return ''.join(c for c in filename if c in valid_chars)

def removeNonUnicodeChars(string):
    return string.encode('utf8')

def awesomeDownloader():
    # Get current date and time
    import time,datetime
    timeNow = datetime.datetime.now()
    timePosix = int(time.mktime(timeNow.timetuple()))
    
    print "<--------------- Running Downloader ----------------->"
    print "Time: ",timeNow.strftime('%d/%m/%Y %H:%M')
    #--------------------------------------------------------------------------------
    # Connect to local database
    #--------------------------------------------------------------------------------
    from database_operations import create_session
    session = create_session()
    
    #--------------------------------------------------------------------------------
    # Check if we need to search for movies
    #--------------------------------------------------------------------------------
    
    from Movie import Movie
    nDownloaded = session.query(Movie).filter(Movie.downloaded == 1).count()
    nRecent = session.query(Movie).filter(Movie.last_searched+86400 > timePosix).count()
    
    # Get movies we need to search for
    movies = session.query(Movie).filter(Movie.downloaded == 0).filter(Movie.last_searched+86400 < timePosix).limit(5).all()
    
    nSnatched = 0
    if len(movies) > 0:
        #--------------------------------------------------------------------------------
        # Login to Awesome-HD and search for movies
        #--------------------------------------------------------------------------------
        
        doLogin()
        
        for movie in movies:
            print "---> SEARCHING FOR: "+movie.title.encode('utf8')+' ('+str(movie.year)+')'
            html = doSearch(movie.title, movie.year)
            link = getLink(html, movie.title, movie.year)
            if len(link) > 0:
                movie.link = link
                # Make sure we are using only valid chars in the filename
                torrentName = getValidFilename('.'.join(removeNonUnicodeChars(movie.title).split(' '))+'.('+str(movie.year)+').torrent')
                try:
                    tc.go(link)
                    tc.save_html(s.torrentPath+torrentName)
                    movie.downloaded = 1
                    print "======================================================"
                    print "DOWNLOADED TORRENT: "+torrentName
                    print "======================================================"
                    pushover("Snatched", movie.title+' ('+str(movie.year)+')')
                    nSnatched += 1
                except ValueError:
                    print "ERROR: Something went wrong in twill.."
            else:
                print "NO RESULTS FOR: "+movie.title.encode('utf8')+' ('+str(movie.year)+')'
            # Log time of search and add random interval +/- 2 hours to spread out searches
            movie.last_searched = timePosix + abs(movie.year - timeNow.year)*86400 + int(random.uniform(-7200,7200))
            session.add(movie)
            session.commit()
        
        session.commit()
    
    print "======================================================"
    print "No. movies already downloaded: ", nDownloaded
    print "No. movies recently searched: ", nRecent
    print "No. movies searched for: ", len(movies)
    print "No. movies snatched: ", nSnatched
    print "<---------------------------------------------------->"
