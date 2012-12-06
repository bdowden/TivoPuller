import unittest
import sys
import os
sys.path.append(os.path.abspath('..'))
import tivopuller
from tivopuller import playlistEntry, tivoFetcher, tivoPoller, tivoEpisodeDownloader, tivoQueueAdder, db, episodeStatus

class TestTivoPuller(unittest.TestCase):

    def returnVals(self):
        entry = playlistEntry.PlayListEntry()
        entry.episodeId = '1'
        return [entry];

    def download(self, entry, destfilename):
        return

    def test_pull(self):
        tivopuller.initialize()
        fetcher = tivoFetcher.TivoFetcher("", "")
        fetcher.FetchPlayList = self.returnVals
        fetcher.Download = self.download

        tivopuller.QUEUE.addToQueue('1')

        down = tivoEpisodeDownloader.TivoEpisodeDownloader(fetcher)
        down.run()

    def test_addToQueue(self):
        tivopuller.initialize()
        myDB = db.DBConnection()

        myDB.action("Update tivo_episode set Status = ? WHERE EpisodeId = '1'", [episodeStatus.getStatusCode('Wanted')])

        adder = tivoQueueAdder.TivoQueueAdder()

        adder.run()

        self.assertEqual(1, len(tivopuller.QUEUE))

if __name__ == '__main__':
    unittest.main()