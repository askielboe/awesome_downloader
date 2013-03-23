# coding: utf-8
import re
import random
import mechanize
import settings as s
from pushover import pushover

# # #
# Functions
def doLogin():
    url = "https://awesome-hd.net/login.php"
    response = mechanize.urlopen(url)
    
    forms = mechanize.ParseResponse(response, backwards_compat=False)
    form = forms[0]
    form["username"] = s.username
    form["password"] = s.password
    
    mechanize.urlopen(form.click())

def doSearch(movieTitle, movieYear):
    # Convert non-unicode characters
    movieTitle = removeNonUnicodeChars(movieTitle)
    
    url = "https://awesome-hd.net/torrents.php"
    response = mechanize.urlopen(url)
    
    # Search
    forms = mechanize.ParseResponse(response, backwards_compat=False)
    form = forms[0]
    form["searchstr"] = movieTitle
    
    html = mechanize.urlopen(form.click()).readlines()
    
    return html

def getLink(html, movieTitle, movieYear):
    # Convert non-unicode characters
    movieTitle = removeNonUnicodeChars(movieTitle)
    movieTitle = movieTitle.lstrip('The ')
    
    # Make sure movie year is an int
    try:
        movieYear = int(movieYear)
    except ValueError:
        raise "WARNING: Movie Year cannot be converted to integer, skipping movie.."
        return ''

    link = ''
    i = 0
    while i < len(html):
        if re.search('title\=\"View Torrent\"\>(.* \(AKA\: )?(The )?'+movieTitle+'\)?\<\/a\> \['+str(movieYear)+'\]',html[i]):
            i += 1
            while i < len(html):
                if '1080p' in html[i] \
                    and 'Blu-Ray' in html[i] \
                    and '75% Freeleech' in html[i] \
                    and 'Remux' not in html[i]:
                    
                    link = 'https://awesome-hd.net/'+html[i-3].lstrip('\t\t\t\t[<a href="').rstrip('" title="Download">DL</a>\n')
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
    string = string.encode('utf8')
    return string

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
                    filename = s.torrentPath+torrentName
                    with open(filename, 'w') as torrent_file:
                        for line in mechanize.urlopen(link).readlines():
                            torrent_file.write(line)
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
            try:
                movie.last_searched = timePosix + abs(movie.year - timeNow.year)*86400 + int(random.uniform(-7200,7200))
            except TypeError:
                movie.last_searched = timePosix + 30*86400 + int(random.uniform(-7200,7200))
            
            session.add(movie)
            session.commit()
        
        session.commit()
    
    print "======================================================"
    print "No. movies already downloaded: ", nDownloaded
    print "No. movies recently searched: ", nRecent
    print "No. movies searched for: ", len(movies)
    print "No. movies snatched: ", nSnatched
    print "<---------------------------------------------------->"
