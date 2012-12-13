
import datetime
import time
import threading
import traceback

class Scheduler:

    def __init__(self, action, cycleTime=datetime.timedelta(minutes=10), runImmediately=True, threadName="ScheduledThread", silent=False):

        if runImmediately:
            self.lastRun = datetime.datetime.fromordinal(1)
        else:
            self.lastRun = self.getCurrentDate()

        self.action = action
        self.cycleTime = cycleTime

        self.thread = None
        self.threadName = threadName
        self.silent = silent

        self.scheduleTime = False

        self.scheduleHour = 0
        self.scheduleMinute = 0
        self.hasRun = False
        self.initThread()

        self.abort = False

    def initThread(self):
        if self.thread == None or not self.thread.isAlive():
            self.thread = threading.Thread(None, self.runAction, self.threadName)

    def timeLeft(self):
        return self.cycleTime - (datetime.datetime.now() - self.lastRun)

    def forceRun(self):
        if not self.action.amActive:
            self.lastRun = datetime.datetime.fromordinal(1)
            return True
        return False

    def getCurrentDate(self):
        return datetime.datetime.now()

    def runAction(self):

        while True:
            shouldRun = False
            currentTime = self.getCurrentDate()

            if not self.scheduleTime:
                shouldRun = currentTime - self.lastRun > self.cycleTime
            else:
                wantedTime = currentTime.replace(hour = int(self.scheduleHour), minute = int(self.scheduleMinute))

                if (currentTime >= wantedTime and (currentTime - self.lastRun).days >= 1):
                    shouldRun = True

            if shouldRun:
                self.lastRun = currentTime
                try:
                    self.action.run()
                except Exception, e:
                    print u"Exception generated in thread "+self.threadName+": " + e.args[0]

            if self.abort:
                self.abort = False
                self.thread = None
                return

            time.sleep(1)
