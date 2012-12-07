import os
import cherrypy
from Cheetah.Template import Template
import tivopuller
from tivopuller import db
from tivopuller import tivoEpisode
from tivopuller import episodeStatus
from itertools import groupby 


class PageTemplate (Template):
    def __init__(self, *args, **KWs):
        KWs['file'] = os.path.join(tivopuller.PROG_DIR, "web/", KWs['file'])
        super(PageTemplate, self).__init__(*args, **KWs)
        #self.sbRoot = sickbeard.WEB_ROOT
        #self.sbHttpPort = sickbeard.WEB_PORT
        #self.sbHttpsPort = sickbeard.WEB_PORT
        #self.sbHttpsEnabled = sickbeard.ENABLE_HTTPS
        #if cherrypy.request.headers['Host'][0] == '[':
        #    self.sbHost = re.match("^\[.*\]", cherrypy.request.headers['Host'], re.X|re.M|re.S).group(0)
        #else:
        #    self.sbHost = re.match("^[^:]+", cherrypy.request.headers['Host'], re.X|re.M|re.S).group(0)
        #self.projectHomePage = "http://code.google.com/p/sickbeard/"

        #if sickbeard.NZBS and sickbeard.NZBS_UID and sickbeard.NZBS_HASH:
        #    logger.log(u"NZBs.org has been replaced, please check the config to configure the new provider!", logger.ERROR)
        #    ui.notifications.error("NZBs.org Config Update", "NZBs.org has a new site. Please <a href=\""+sickbeard.WEB_ROOT+"/config/providers\">update your config</a> with the api key from <a href=\"http://beta.nzbs.org/login\">http://beta.nzbs.org</a> and then disable the old NZBs.org provider.")

        if "X-Forwarded-Host" in cherrypy.request.headers:
            self.sbHost = cherrypy.request.headers['X-Forwarded-Host']
        if "X-Forwarded-Port" in cherrypy.request.headers:
            self.sbHttpPort = cherrypy.request.headers['X-Forwarded-Port']
            self.sbHttpsPort = self.sbHttpPort
        if "X-Forwarded-Proto" in cherrypy.request.headers:
            self.sbHttpsEnabled = True if cherrypy.request.headers['X-Forwarded-Proto'] == 'https' else False

        #logPageTitle = 'Logs &amp; Errors'
        #if len(classes.ErrorViewer.errors):
        #    logPageTitle += ' ('+str(len(classes.ErrorViewer.errors))+')'
        #self.logPageTitle = logPageTitle
        #self.sbPID = str(sickbeard.PID)
        #self.menu = [
        #    { 'title': 'Home',            'key': 'home'           },
        #    { 'title': 'Coming Episodes', 'key': 'comingEpisodes' },
        #    { 'title': 'History',         'key': 'history'        },
        #    { 'title': 'Manage',          'key': 'manage'         },
        #    { 'title': 'Config',          'key': 'config'         },
        #    { 'title': logPageTitle,      'key': 'errorlogs'      },
        #]

def redirect(abspath, *args, **KWs):
    assert abspath[0] == '/'
    raise cherrypy.HTTPRedirect(abspath, *args, **KWs)

class Config:
    @cherrypy.expose
    def index(self):
        page = PageTemplate(file = "config.tmpl")

        data = db.DBConnection()

        d = data.select("select * from configuration")
        settings = dict((x["SettingName"], x["SettingValue"]) for x in d)

        page.tivoIp = settings["tivoIp"]
        page.tivoPassword = settings["tivoPassword"]
        page.downloadDir = settings["downloadDir"]

        page.autoDownloadNew  = settings["autoDownloadNew"] == "1"

        page.scheduleHour = settings["downloadScheduleHour"]
        page.scheduleMinute = settings["downloadScheduleMinute"]
        print page.autoDownloadNew

        return str(page)

    @cherrypy.expose
    def saveConfig(self, tivoIp = None, tivoPassword = None, downloadDir = None, autoDownloadNew = None, scheduleHour = None, scheduleMinute = None):
        tivopuller.AUTO_DOWNLOAD_NEW = autoDownloadNew != None and autoDownloadNew != ""
        tivopuller.PASSWORD = tivoPassword
        tivopuller.IP = tivoIp
        tivopuller.DOWNLOAD_DIR = downloadDir

        tivopuller.DOWNLOAD_HOUR = scheduleHour
        tivopuller.DOWNLOAD_MINUTE = scheduleMinute
        tivopuller.DOWNLOAD_SCHEDULE = scheduleHour and scheduleHour > 0 and scheduleMinute

        tivopuller.resetDownloadSchedule(tivopuller.DOWNLOAD_SCHEDULE, tivopuller.DOWNLOAD_HOUR, tivopuller.DOWNLOAD_MINUTE)

        tivopuller.saveConfig()
        redirect("/config/")

class Home:
    @cherrypy.expose
    def halt(self):
        cherrypy.engine.exit()

    @cherrypy.expose 
    def forceQuery(self):
        tivopuller.forceQueryTivo()
        redirect("/home")

    @cherrypy.expose 
    def forceDownload(self):
        tivopuller.forceDownload()
        redirect("/home")
        
    @cherrypy.expose 
    def forceQueue(self):
        tivopuller.forceQueueAdder()
        redirect("/home")

    @cherrypy.expose
    def updateStatuses(self, episode = None, status = None):

        print "episodes: " + episode + " status: " + status

        episodeIds = episode.split(',')

        myDb = db.DBConnection()

        eps = ['?' for k in episodeIds]

        episodeIds.insert(0, status)

        myDb.action("UPDATE tivo_episode set Status = ? where EpisodeId IN (" + (',').join(eps) + ")", episodeIds)

        redirect("/home")

    @cherrypy.expose
    def index(self):
        page = PageTemplate(file = "mainpage.tmpl")

        data = db.DBConnection()

        d = data.select("select tivo_series.SeriesId, SeriesName, EpisodeId, EpisodeName, Status from tivo_episode join tivo_series on (tivo_series.SeriesId = tivo_episode.SeriesId)")

        episodes = []

        for res in d:
            e = tivoEpisode.TivoEpisode(res["SeriesId"], res["EpisodeId"], res["SeriesName"], res["EpisodeName"], episodeStatus.EpisodeStatus[res["Status"]])
            episodes.append(e)

        groupedEpisodes = []

        for key, e in groupby(sorted(episodes, key=lambda episode:episode.SeriesName), lambda x: x.SeriesName):

            eps = []
            for ep in e:
                eps.append(ep)

            groupedEpisodes.append([key, eps])


        page.episodes = groupedEpisodes
        page.statuses = episodeStatus.getStatuses()

        return str(page)

class Root:
    @cherrypy.expose
    def index(self):
        redirect("/home")

    home = Home()
    config = Config()