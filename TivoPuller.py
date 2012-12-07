
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

tivopuller.initialize()

tivopuller.PROG_DIR = APPDIR

#INI_FILENAME = os.path.join(APPDIR, "cp.ini")

options = {'server.socket_port': 8777 , 'server.socket_host': '127.0.0.1'} #'192.168.1.65'}

app = cherrypy.tree.mount(root.Root())
cherrypy.config.update(options)
cherrypy.server.start()
cherrypy.server.wait()

tivopuller.start()