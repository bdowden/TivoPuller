from tivopuller import playlistEntry, tivoFetcher, episodeStatus
import tivopuller

class TivoPoller:
    def __init__(self, fetcher, db):
        self.fetcher = fetcher;
        self.db = db;
        
    def start(self):
        episodes = self.fetcher.FetchPlayList();

        for episode in episodes:
            epi = self.db.select("SELECT 1 FROM tivo_episode where EpisodeId = ?", [episode.episodeId])
            if (len(epi) == 0):
                ser = self.db.select("SELECT * FROM tivo_series WHERE SeriesId = ?", [episode.seriesId])

                if (len(ser) == 0):
                    self.db.action("INSERT INTO tivo_series(SeriesId, SeriesName) VALUES(?, ?)", [episode.seriesId, episode.title])

                status = episodeStatus.getStatusCode("Ignored")

                if (tivopuller.AUTO_DOWNLOAD_NEW):
                    status = episodeStatus.getStatusCode("Wanted")

                self.db.action("INSERT INTO tivo_episode(EpisodeId, SeriesId, EpisodeName, CaptureDate, Downloaded, DownloadDate, Status) VALUES(?, ?, ?, ?, ?, ?, ?)", [episode.episodeId, episode.seriesId, episode.episode, episode.date, False, None])