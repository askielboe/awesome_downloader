#!/opt/bin/python2.6

# Abort if diskspace is below limit set in settings.py
import os
import sys
from pushover import pushover
from settings import torrentPath, minDiskSpace

s = os.statvfs(torrentPath)
spaceLeft = (s.f_bavail * s.f_frsize / 1e9)
if spaceLeft < minDiskSpace:
	f = open('.isdiskfull', 'r')
	if f.readline() == '0':
		pushover('Awesome-DL','WARNING: Low disk space: '+str(spaceLeft)+' GB. Suspending downloads..')
		f.close()
		f = open('.isdiskfull', 'w')
		f.write('1')
		f.close()

	sys.exit("FATAL: Disk space too low (< "+str(minDiskSpace)+" GB)!")


f = open('.isdiskfull', 'w')
f.write('0')
f.close()

# Run downloader
from imdb_parser import imdbParse
from awesome_downloader import awesomeDownloader

imdbParse()
awesomeDownloader()
