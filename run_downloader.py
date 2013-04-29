#!/opt/bin/python2.6

# Abort if diskspace is below 100 GB
import os
import sys
from settings import torrentPath, minDiskSpace

s = os.statvfs(torrentPath)
if (s.f_bavail * s.f_frsize / 1e9) < minDiskSpace:
	sys.exit("FATAL: Disk space too low (< "+str(minDiskSpace)+" GB)!")

# Run downloader
from imdb_parser import imdbParse
from awesome_downloader import awesomeDownloader

imdbParse()
awesomeDownloader()
