import os
import cherrypy

APPDIR = os.path.dirname(os.path.abspath(__file__))
INI_FILENAME = os.path.join(APPDIR, "cp.ini")

class Root:
    @cherrypy.expose
    def index(self):
        return "hi"