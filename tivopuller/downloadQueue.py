from threading import Lock
from collections import deque

class DownloadQueue:
    def __init__(self):
        self.INIT_LOCK = Lock()
        self.queue = deque([])

    def addToQueue(self, element):
        with self.INIT_LOCK:
            self.queue.append(element)

    def getNextFromQueue(self):
        with self.INIT_LOCK:
            if len(self.queue) > 0:
                return self.queue.pop()
            else:
                return None
    def __len__(self):
        return len(self.queue)