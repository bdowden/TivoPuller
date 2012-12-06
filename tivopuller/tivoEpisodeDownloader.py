import tivopuller
from tivopuller import tivoFetcher, downloadQueue, db, episodeStatus
import os.path

def find(f, seq):
  for item in seq:
    if f(item): 
      return item

class TivoEpisodeDownloader:
    def __init__(self, fetcher):
        self.fetcher = fetcher
        self.isDownloading = False
        self.amActive = False
    def run(self):
        if (self.amActive or tivopuller.IP is None or tivopuller.IP == ""):
            return
        print "beginning to download"
        self.amActive = True
        element = tivopuller.QUEUE.getNextFromQueue()
        while (element is not None):
            entries = self.fetcher.FetchPlayList()
            episode = find(lambda x: x.episodeId == element, entries)
            
            if (episode is not None):
                conn = db.DBConnection()
                self.isDownloading = True
                conn.action("UPDATE tivo_episode SET Status = ? WHERE EpisodeId = ?", [episodeStatus.getStatusCode('Downloading'), element])
                self.downloadEpisode(episode)
                self.isDownloading = False
                conn.action("UPDATE tivo_episode SET Status = ? WHERE EpisodeId = ?", [episodeStatus.getStatusCode('Downloaded'), element])
            element = tivopuller.QUEUE.getNextFromQueue()
        self.amActive = False
        print "download complete"
    def downloadEpisode(self, episode):
        downloadFile = os.path.join(tivopuller.DOWNLOAD_DIR, episode.getFileName())
        print "beginning download to " + downloadFile
        self.fetcher.Download(episode, episode.getFileName(), downloadFile)
        print "episode downloaded"