import settings as s
import twill.commands as tc

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

#--------------------------------------------------------------------------------
# Connect to local database
#--------------------------------------------------------------------------------
from database_operations import create_session
session = create_session()

from Movie import Movie
movies = session.query(Movie).limit(25).all()

#--------------------------------------------------------------------------------
# Login to Awesome-HD and search for movies
#--------------------------------------------------------------------------------

doLogin()

# Get current date and time in POSIX
import time,datetime
timeNow = datetime.datetime.now()
timePosix = int(time.mktime(timeNow.timetuple()))

for movie in movies:
    if movie.downloaded or movie.last_searched+86400 > timePosix:
        print "Skipping "+movie.title+' ('+str(movie.year)+') - movie searched for recently!'
        continue
    print "Searching for "+movie.title+' ('+str(movie.year)+')'
    html = doSearch(movie.title, movie.year)
    link = getLink(html, movie.title, movie.year)
    if len(link) > 0:
        movie.link = link
        torrentName = '.'.join(movie.title.split(' '))+'.('+str(movie.year)+').torrent'
        tc.go(link)
        tc.save_html(torrentPath+torrentName)
        print "Downloaded torrent: "+torrentName
    else:
        print "No torrents found for "+movie.title+' ('+str(movie.year)+')'
    movie.last_searched = timePosix
    session.add(movie)

session.commit()

