from threading import Lock
from tivopuller import db, tivoPoller, scheduler, downloadQueue, mainDB, tivoEpisodeDownloader, tivoQueueAdder
import datetime

tivoPoll = None
tivoPollerScheduler = None
tivoDownloader = None
tivoDownloaderScheduler = None
started = False
tivoQueue = None
tivoQueueScheduler = None

PROG_DIR = '.'
DOWNLOAD_DAYS = 1
MAIN_LISTING = ""
PROTOCOL = "https"
USERNAME = "tivo"
PASSWORD = '7769393814'
IP = "192.168.1.70"
AUTO_DOWNLOAD_NEW = False
DOWNLOAD_DIR = ""
POLL_FREQUENCY = 60
DOWNLOAD_FREQUENCY = 1
QUEUE = None
QUEUE_FREQUENCY = 1

DOWNLOAD_HOUR = None
DOWNLOAD_MINUTE = None
DOWNLOAD_SCHEDULE = False

INIT_LOCK = Lock()
__INITIALIZED__ = False

def initialize():
    with INIT_LOCK:
        global __INITIALIZED__, PROG_DIR, DOWNLOAD_DAYS, MAIN_LISTING, PROTOCOL, USERNAME, PASSWORD, IP,AUTO_DOWNLOAD_NEW, DOWNLOAD_DIR, tivoPoll, tivoDownloader, \
        tivoPollerScheduler, tivoDownloaderScheduler, started, QUEUE, DOWNLOAD_FREQUENCY, POLL_FREQUENCY, tivoQueue, tivoQueueScheduler, QUEUE_FREQUENCY, \
        DOWNLOAD_HOUR, DOWNLOAD_MINUTE, DOWNLOAD_SCHEDULE
    if __INITIALIZED__:
        return False

    myDB = db.DBConnection()

    d = mainDB.InitialSchema(myDB)
    if not d.test():
        d.execute()

    d = myDB.select("select * from configuration")
    settings = dict((x["SettingName"], x["SettingValue"]) for x in d)

    PASSWORD = settings["tivoPassword"]
    IP = settings["tivoIp"]
    AUTO_DOWNLOAD_NEW = settings["autoDownloadNew"]
    DOWNLOAD_DIR = settings["downloadDir"]
    DOWNLOAD_HOUR = settings["downloadScheduleHour"]
    DOWNLOAD_MINUTE = settings["downloadScheduleMinute"]
    DOWNLOAD_SCHEDULE = DOWNLOAD_HOUR and DOWNLOAD_HOUR > 0 and DOWNLOAD_MINUTE

    QUEUE = downloadQueue.DownloadQueue()

    fetcher = tivoFetcher.TivoFetcher(IP, PASSWORD)
    tivoPoll = tivoPoller.TivoPoller(fetcher, db.DBConnection())

    tivoPollerScheduler = scheduler.Scheduler(tivoPoll,
                                             cycleTime=datetime.timedelta(minutes=POLL_FREQUENCY),
                                             threadName="POLL",
                                             runImmediately=True)

    tivoDownloader = tivoEpisodeDownloader.TivoEpisodeDownloader(fetcher)
    tivoDownloaderScheduler = scheduler.Scheduler(tivoDownloader, cycleTime = datetime.timedelta(minutes = DOWNLOAD_FREQUENCY), threadName = "DOWNLOADER", runImmediately =True)
    resetDownloadSchedule(DOWNLOAD_SCHEDULE, DOWNLOAD_HOUR, DOWNLOAD_MINUTE)

    tivoQueue = tivoQueueAdder.TivoQueueAdder()
    tivoQueueScheduler = scheduler.Scheduler(tivoQueue, cycleTime = datetime.timedelta(minutes = QUEUE_FREQUENCY), threadName = "QUEUE_ADDER", runImmediately = True)

    __INITIALIZED__ = True

def forceQueryTivo():
    tivoPollerScheduler.forceRun()

def forceQueueAdder():
    tivoQueueScheduler.forceRun()

def forceDownload():
    tivoDownloaderScheduler.forceRun()

def resetDownloadSchedule(scheduled=False, hours=None, minutes=None):
    tivoDownloaderScheduler.scheduleTime = scheduled
    tivoDownloaderScheduler.scheduleHour= hours
    tivoDownloaderScheduler.scheduleMinute = minutes

def start():

    global __INITIALIZED__, tivoPollerScheduler, tivoDownloaderScheduler, tivoQueueScheduler, \
            started

    with INIT_LOCK:
        if __INITIALIZED__:
            #tivoPollerScheduler.thread.start()
            #tivoDownloaderScheduler.thread.start()
            #tivoQueueScheduler.thread.start()
            started = True

def saveConfig():
    global IP, PASSWORD, DOWNLOAD_DIR, AUTO_DOWNLOAD_NEW, DOWNLOAD_HOUR, DOWNLOAD_MINUTE
    myDB = db.DBConnection()

    myDB.action("UPDATE configuration SET SettingValue = ? WHERE SettingName = 'tivoIp'", [IP])
    myDB.action("UPDATE configuration SET SettingValue = ? WHERE SettingName = 'tivoPassword'", [PASSWORD])
    myDB.action("UPDATE configuration SET SettingValue = ? WHERE SettingName = 'downloadDir'", [DOWNLOAD_DIR])
    myDB.action("UPDATE configuration SET SettingValue = ? WHERE SettingName = 'autoDownloadNew'", [AUTO_DOWNLOAD_NEW])
    myDB.action("UPDATE configuration SET SettingValue = ? WHERE SettingName = 'downloadScheduleHour'", [DOWNLOAD_HOUR])
    myDB.action("UPDATE configuration SET SettingValue = ? WHERE SettingName = 'downloadScheduleMinute'", [DOWNLOAD_MINUTE])