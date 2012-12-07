from tivopuller import playlistEntry, tivoFetcher, episodeStatus, db
import tivopuller
import datetime
import threading
import time

class TivoPoller:
    def __init__(self, fetcher, dba):
        self.fetcher = fetcher;
        self.dba = db.DBConnection();
        self.amActive = False

    def addEpisodeToDb(self, episode, dba):
        epi = dba.select("SELECT * FROM tivo_episode where EpisodeId = ?", [str(episode.episodeId)])

        if (len(epi) == 0):
            ser = dba.select("SELECT * FROM tivo_series WHERE SeriesId = ?", [episode.seriesId])

            if (len(ser) == 0):
                dba.action("INSERT INTO tivo_series(SeriesId, SeriesName) VALUES(?, ?)", [episode.seriesId, episode.title])

            status = episodeStatus.getStatusCode("Ignored")

            if (tivopuller.AUTO_DOWNLOAD_NEW == True):
                status = episodeStatus.getStatusCode("Wanted")

            dba.action("INSERT INTO tivo_episode(EpisodeId, SeriesId, EpisodeName, CaptureDate, Downloaded, DownloadDate, Status) VALUES(?, ?, ?, ?, ?, ?, ?)", [episode.episodeId, episode.seriesId, episode.episode, episode.date, False, None, status])

    def markDeletedEpisodes(self, episodes, dba):
        episodeIds = [x.episodeId for x in episodes]
        parms = ['?' for x in episodeIds]

        query = "UPDATE tivo_episode SET Status = ? WHERE Status <> ? AND episodeId NOT IN (" + ",".join(parms) + ")"

        removed = episodeStatus.getStatusCode("Removed from Tivo")
        downloaded = episodeStatus.getStatusCode("Downloaded")

        statuses = [removed, downloaded]
        statuses.extend(episodeIds)
        dba.action(query, statuses)

    def run(self):
        if (self.amActive):
            return

        self.amActive = True
        print "beginning to poll for new episodes"
        episodes = self.fetcher.FetchPlayList();
        dba = db.DBConnection()
        for episode in episodes:
            self.addEpisodeToDb(episode, dba)
            
        self.markDeletedEpisodes(episodes, dba)
        print "polling complete"
        self.amActive = False