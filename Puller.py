
import os
import cherrypy

import tivopuller
from tivopuller import root, db, mainDB, playlistEntry, tivoFetcher, tivoPoller

import urllib2
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import datetime
import html_unescape
import Cookie

APPDIR = os.path.dirname(os.path.abspath(__file__))

tivopuller.PROG_DIR = APPDIR

INI_FILENAME = os.path.join(APPDIR, "cp.ini")

r = root.Root()
database = db.DBConnection()

d = mainDB.InitialSchema(database)
if not d.test():
    d.execute()

cherrypy.quickstart(r, config = INI_FILENAME)
cherrypy.server.start()
cherrypy.server.wait()

#fetcher = tivoFetcher.TivoFetcher(tivopuller.IP, tivopuller.PASSWORD, tivopuller.AUTO_DOWNLOAD_NEW)

#poller = tivoPoller.TivoPoller(fetcher, database);

#poller.start();

#downloads =[]


#for item in fetcher.FetchPlayList():
#  res = database.select("SELECT * FROM tivo_episode WHERE EpisodeId = ?", [item.episodeId])

  #if (len(res) == 0):
   # downloads.add(item)
    #ser = database.select("SELECT * FROM tivo_series WHERE SeriesId = ?", [item.seriesId])

    #if (len(ser) == 0):
     # database.action("INSERT INTO tivo_series(SeriesId, SeriesName) VALUES(?, ?)", [item.seriesId, item.title])

    #database.action("INSERT INTO tivo_episode(EpisodeId, SeriesId, EpisodeName, CaptureDate, Downloaded, DownloadDate) VALUES(?, ?, ?, ?, ?, ?)", [item.episodeId, item.seriesId, item.episode, item.date, False, None])