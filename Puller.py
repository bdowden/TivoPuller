
import os
import cherrypy
from web import tp_web

APPDIR = os.path.dirname(os.path.abspath(__file__))
INI_FILENAME = os.path.join(APPDIR, "web\cp.ini")

cherrypy.quickstart(Root(), config = INI_FILENAME)
cherrypy.server.start()
cherrypy.server.wait()