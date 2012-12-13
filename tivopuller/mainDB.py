
import tivopuller
import os.path

from tivopuller import db

class TivoPullerConfig(db.SchemaUpgrade):
    def test(self):
        return self.hasTable("configuration")
    def execute(self):
        query = "CREATE TABLE configuration(ConfigurationId INTEGER PRIMARY KEY AUTOINCREMENT, SettingName TEXT UNIQUE, SettingValue TEXT)"
        self.connection.action(query)

class TivoPullerDefaultConfig(db.SchemaUpgrade):
    def test(self):
        return 1==0
    def execute(self):
        query = "INSERT OR IGNORE INTO configuration(SettingName, SettingValue) VALUES('isConfigured', '0')"
        self.connection.action(query)
        query = "INSERT OR IGNORE INTO configuration(SettingName, SettingValue) VALUES('tivoIp', '')"
        self.connection.action(query)
        query = "INSERT OR IGNORE INTO configuration(SettingName, SettingValue) VALUES('tivoPassword', '')"
        self.connection.action(query)
        query = "INSERT OR IGNORE INTO configuration(SettingName, SettingValue) VALUES('downloadDir', '')"
        self.connection.action(query)
        query = "INSERT OR IGNORE INTO configuration(SettingName, SettingValue) VALUES('autoDownloadNew', '0')"
        self.connection.action(query)
        query = "INSERT OR IGNORE INTO configuration(SettingName, SettingValue) VALUES('downloadScheduleHour', '')"
        self.connection.action(query)
        query = "INSERT OR IGNORE INTO configuration(SettingName, SettingValue) VALUES('downloadScheduleMinute', '')"
        self.connection.action(query)

class TivoEpisode_SaveLoc(db.SchemaUpgrade):
    def test(self):
        return self.hasColumn("tivo_episode", "downloadLoc")
    def execute(self):
        query = "ALTER TABLE tivo_episode ADD COLUMN downloadLoc TEXT"
        self.connection.action(query)

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

class TivoEpisodeStatus(db.SchemaUpgrade):
    def test(self):
        return self.hasColumn("tivo_episode", "Status")
    def execute(self):
        query = "ALTER TABLE tivo_episode ADD COLUMN Status INT DEFAULT(0)"
        self.connection.action(query)

class InitialSchema (db.SchemaUpgrade):
    def test(self):
        return 1 == 0

    def execute(self):
        queries = [
            TivoPullerConfig(self.connection),
            TivoSeries(self.connection),
            TivoEpisode(self.connection),
            TivoEpisodeStatus(self.connection),
            TivoPullerDefaultConfig(self.connection),
            TivoEpisode_SaveLoc(self.connection)
        ]
        for query in queries:
            if not query.test():
                query.execute()