import unittest
import sys
import os
import datetime
import time
sys.path.append(os.path.abspath('..'))
import tivopuller
from tivopuller import playlistEntry, tivoFetcher, tivoPoller, tivoEpisodeDownloader, tivoQueueAdder, db, episodeStatus, scheduler

class TestRunner:
    def __init__(self):
        self.hasRun = False
    def run(self):
        self.hasRun = True

class TestScheduler(unittest.TestCase):

    def test_RunImmediately_OneSecond_WillRun(self):
        runner = TestRunner()
        schedule = scheduler.Scheduler(runner, cycleTime=datetime.timedelta(seconds = 1))
        time.sleep(1)
        schedule.abort = True
        schedule.runAction()

        self.assertEqual(True, runner.hasRun)

    def test_RunImmediately_TenMinutes_WillRun(self):
        runner = TestRunner()
        schedule = scheduler.Scheduler(runner, cycleTime=datetime.timedelta(minutes = 10))
        time.sleep(1)
        schedule.abort = True
        schedule.runAction()

        self.assertEqual(True, runner.hasRun)

    def test_TenMinutes_WillNotRun(self):
        runner = TestRunner()
        schedule = scheduler.Scheduler(runner, cycleTime=datetime.timedelta(minutes = 10),runImmediately=False)
        time.sleep(1)
        schedule.abort = True
        schedule.runAction()

        self.assertEqual(False, runner.hasRun)

    def test_ScheduledAtTime_LastRunDaysBefore_WillRun(self):
        runner = TestRunner()
        schedule = scheduler.Scheduler(runner,runImmediately=True)
        schedule.getCurrentDate = lambda: datetime.datetime.now().replace(hour = 13, minute = 1)
        schedule.scheduleTime = True
        schedule.scheduleHour = 3
        schedule.scheduleMinute = 15
        schedule.abort = True
        schedule.runAction()

        self.assertEqual(True, runner.hasRun)

    def test_ScheduledAtTime_TimeNotHit_WillNotRun(self):
        runner = TestRunner()
        schedule = scheduler.Scheduler(runner,runImmediately=False)
        schedule.getCurrentDate = lambda: datetime.datetime.now().replace(hour = 2, minute = 1)
        schedule.scheduleTime = True
        schedule.scheduleHour = 3
        schedule.scheduleMinute = 15
        schedule.abort = True
        schedule.runAction()

        self.assertEqual(False, runner.hasRun)

    def test_ScheduledAtTime_LastRunAfter_NotDay_WillNotRun(self):
        runner = TestRunner()
        schedule = scheduler.Scheduler(runner,runImmediately=False)
        schedule.getCurrentDate = lambda: datetime.datetime.now().replace(hour = 4, minute = 1)
        schedule.scheduleTime = True
        schedule.scheduleHour = 3
        schedule.scheduleMinute = 15
        schedule.lastRun = datetime.datetime.now().replace(hour = 3, minute = 16)
        schedule.abort = True
        schedule.runAction()

        self.assertEqual(False, runner.hasRun)

if __name__ == '__main__':
    unittest.main()