import tivopuller
from tivopuller import db, episodeStatus

class TivoQueueAdder:
    def __init__(self):
        self.running = False
    def run(self):
        if (self.running):
            return
        self.running = True
        query = "SELECT EpisodeId FROM tivo_episode WHERE Status = ?"

        myDB = db.DBConnection()
        results = myDB.select(query, [episodeStatus.getStatusCode("Wanted")])

        episodesToAdd = [x["EpisodeId"] for x in results]

        eps = ['?' for k in episodesToAdd]

        episodesToAdd.insert(0, episodeStatus.getStatusCode("Queued"))

        myDB.action("UPDATE tivo_episode set Status = ? where EpisodeId IN (" + (',').join(eps) + ")", episodesToAdd)

        for x in results:
            tivopuller.QUEUE.addToQueue(x["EpisodeId"])

        self.running = False