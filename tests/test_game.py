import unittest
import time
from data.game.deltatime import DeltaTime

class TestingDeltaTime(unittest.TestCase):
    def test_delta(self):
        dt = DeltaTime()
        dt.start("test", 1000)
        dt.start("long", 3000)
        dt.start("short", 1500, 1)
        time.sleep(1)
        dt.tick()
        events = dt.get()
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0], "test")
        time.sleep(1)
        dt.tick()
        self.assertIsNone(dt.peek("short"))
        dt.stop("test")
        dt.clear()

