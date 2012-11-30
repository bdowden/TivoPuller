import unittest
import sys
import os
sys.path.append(os.path.abspath('..'))
import tivopuller
from tivopuller import playlistEntry, tivoFetcher, tivoPoller

class TestTivoPuller(unittest.TestCase):
    def setUp(self):
        self.name = "hi"

    def returnVals(self):
        return [playlistEntry.PlayListEntry()];

    def test_pull(self):
        fetcher = tivoFetcher.TivoFetcher("", "")
        fetcher.FetchPlayList = self.returnVals

        poll = tivoPoller.TivoPoller(fetcher, None)

        poll.start()

if __name__ == '__main__':
    unittest.main()