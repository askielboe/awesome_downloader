import sys
from awesome_utility import setNotDownloaded
from awesome_downloader import awesomeDownloader

setNotDownloaded(sys.argv[0])
awesomeDownloader()
