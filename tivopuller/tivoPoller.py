from tivopuller import playlistEntry, tivoFetcher

class TivoPoller:
    def __init__(self, fetcher, db):
        self.fetcher = fetcher;
        self.db = db;
    def start(self):
        episodes = self.fetcher.FetchPlayList();
        print str(len(episodes))