import tivopuller
from tivopuller import db, episodeStatus

class TivoQueueAdder:
    def __init__(self):
        self.amActive = False
    def run(self):
        if (self.amActive):
            return
        self.amActive = True
        print "beginning to add to queue"
        query = "SELECT EpisodeId FROM tivo_episode WHERE Status = ?"

        myDB = db.DBConnection()
        results = myDB.select(query, [episodeStatus.getStatusCode("Wanted")])

        episodesToAdd = [x["EpisodeId"] for x in results]

        eps = ['?' for k in episodesToAdd]

        episodesToAdd.insert(0, episodeStatus.getStatusCode("Queued"))

        myDB.action("UPDATE tivo_episode set Status = ? where EpisodeId IN (" + (',').join(eps) + ")", episodesToAdd)

        for x in results:
            print "adding " + str(x["EpisodeId"]) + " to the queue"
            tivopuller.QUEUE.addToQueue(x["EpisodeId"])

        self.amActive = False

        print "add to queue complete"