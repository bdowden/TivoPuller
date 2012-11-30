
import tivopuller
import os.path

from tivopuller import db

class TivoEpisode(db.SchemaUpgrade):
    def test(self):
        return self.hasTable("tivo_episode")
    def execute(self):
        query = "CREATE TABLE tivo_episode(EpisodeId TEXT PRIMARY KEY, SeriesId TEXT, EpisodeName TEXT, CaptureDate NUMERIC, Downloaded BIT, DownloadDate NUMERIC)"
        self.connection.action(query)

class TivoSeries(db.SchemaUpgrade):
    def test(self):
        return self.hasTable("tivo_series")
    def execute(self):
        query = "CREATE TABLE tivo_series(SeriesName TEXT, SeriesId TEXT PRIMARY KEY)"
        self.connection.action(query)

class InitialSchema (db.SchemaUpgrade):
    def test(self):
        return 1 == 1

    def execute(self):
        queries = [
            TivoSeries(self.connection),
            TivoEpisode(self.connection)
        ]
        for query in queries:
            if query.test():
                self.connection.action(query)