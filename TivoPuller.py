import urllib2
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import datetime
import html_unescape
import Cookie
import os
import TivoFetcher

dayLength = 3

MAK = 7769393814
IP = "192.168.1.70"
unauthIP = "192.168.1.70:80"
MAIN_LISTING = "/TiVoConnect?Container=%2FNowPlaying&Command=QueryContainer&Recurse=Yes"

protocol = "https://"

username = "tivo"


fetcher = TivoFetcher(IP, MAK)
today = datetime.datetime.today()

downloads =[]

for item in fetcher.FetchPlayList():
	date = datetime.datetime.fromtimestamp(item.date)
	diff = today - date
	if (diff.days <= dayLength):
    downloads.append(item)
    print "will download " + item.title + "." + item.episode 

for item in downloads:
    filename = item.title + "." + item.episode
    filename = filename.replace(" ", ".")
    print "downloading " + filename
    fetcher.Download(item, filename + ".tivo")