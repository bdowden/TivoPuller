from tivopuller import playlistEntry, tivoFetcher

class TivoPoller:
    def __init__(self, fetcher, db, autoDownload):
        self.fetcher = fetcher;
        self.db = db;
        self.autoDownload = autoDownload
        
    def start(self):
        episodes = self.fetcher.FetchPlayList();

        for episode in episodes:
            epi = self.db.select("SELECT 1 FROM tivo_episode where EpisodeId = ?", [episode.episodeId])
            if (len(epi) == 0):
                ser = self.db.select("SELECT * FROM tivo_series WHERE SeriesId = ?", [episode.seriesId])

                if (len(ser) == 0):
                    self.db.action("INSERT INTO tivo_series(SeriesId, SeriesName) VALUES(?, ?)", [episode.seriesId, episode.title])
                self.db.action("INSERT INTO tivo_episode(EpisodeId, SeriesId, EpisodeName, CaptureDate, Downloaded, DownloadDate) VALUES(?, ?, ?, ?, ?, ?)", [episode.episodeId, episode.seriesId, episode.episode, episode.date, False, None])