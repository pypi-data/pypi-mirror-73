import unittest
import inspect
import time
import os

from tail_loader import TailLoader


class TestTailLoader(unittest.TestCase):
    START_TS = time.localtime(time.mktime((2006, 1, 14, 12, 59, 00, 0, 0, -1)))
    TEST_DIR = os.path.abspath(os.path.dirname(__file__))
    SAMPLE_PATH = os.path.join(TEST_DIR, "sample.log")

    def test_isgenerator(self):
        duration = 10
        tl = TailLoader(TestTailLoader.SAMPLE_PATH, duration)
        lines = tl.readlines()
        self.assertTrue(inspect.isgenerator(lines))

    def test_immediate(self):
        duration = 10
        tl = TailLoader(TestTailLoader.SAMPLE_PATH, duration)
        tl.current = TestTailLoader.START_TS
        lines = tl.readlines()
        self.assertEqual(len(list(lines)), 0)

    def test_short(self):
        duration = 20
        tl = TailLoader(TestTailLoader.SAMPLE_PATH, duration)
        tl.current = TestTailLoader.START_TS
        lines = tl.readlines()
        self.assertEqual(len(list(lines)), 9)

    def test_middle(self):
        duration = 120
        tl = TailLoader(TestTailLoader.SAMPLE_PATH, duration)
        tl.current = TestTailLoader.START_TS
        lines = tl.readlines()
        self.assertEqual(len(list(lines)), 12)

    def test_isnew_new(self):
        line = "Jan  2 15:04:05 localhost"
        tl = TailLoader("dummy", 10)
        timestamp = time.mktime((2006, 1, 2, 15, 05, 06, 0, 0, -1))
        t = time.localtime(timestamp)
        tl.current = t
        self.assertFalse(tl.is_new(line))

    def test_isnew_old(self):
        line = "Jan  2 15:04:05 localhost"
        tl = TailLoader("dummy", 10)
        timestamp = time.mktime((2006, 1, 2, 15, 04, 06, 0, 0, -1))
        t = time.localtime(timestamp)
        tl.current = t
        self.assertTrue(tl.is_new(line))
