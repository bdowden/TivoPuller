from threading import Lock

TIVOPULLER_DIR = '.'
DOWNLOAD_DAYS = 1
MAIN_LISTING = ""
PROTOCOL = "https"
USERNAME = "tivo"
PASSWORD = "7769393814",
IP = "192.168.1.70"

INIT_LOCK = Lock()
__INITIALIZED__ = False

def initialize():
    with INIT_LOCK:
        global TIVOPULLER_DIR, DOWNLOAD_DAYS, MAIN_LISTING, PROTOCOL, USERNAME, PASSWORD, IP
    if __INITIALIZED__:
        return false
    __INITIALIZED__ = true