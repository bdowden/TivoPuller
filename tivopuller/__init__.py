from threading import Lock
from tivopuller import db

PROG_DIR = '.'
DOWNLOAD_DAYS = 1
MAIN_LISTING = ""
PROTOCOL = "https"
USERNAME = "tivo"
PASSWORD = '7769393814'
IP = "192.168.1.70"
AUTO_DOWNLOAD_NEW = False
DOWNLOAD_DIR = ""

INIT_LOCK = Lock()
__INITIALIZED__ = False

def initialize():
    with INIT_LOCK:
        global PROG_DIR, DOWNLOAD_DAYS, MAIN_LISTING, PROTOCOL, USERNAME, PASSWORD, IP,AUTO_DOWNLOAD_NEW, DOWNLOAD_DIR
    if __INITIALIZED__:
        return false
    __INITIALIZED__ = true

def saveConfig():
    myDB = db.DBConnection()

    myDB.action("UPDATE configuration SET SettingValue = ? WHERE SettingName = 'tivoIp'", [IP])
    myDB.action("UPDATE configuration SET SettingValue = ? WHERE SettingName = 'tivoPassword'", [PASSWORD])
    myDB.action("UPDATE configuration SET SettingValue = ? WHERE SettingName = 'downloadDir'", [DOWNLOAD_DIR])
    myDB.action("UPDATE configuration SET SettingValue = ? WHERE SettingName = 'autoDownloadNew'", [AUTO_DOWNLOAD_NEW])