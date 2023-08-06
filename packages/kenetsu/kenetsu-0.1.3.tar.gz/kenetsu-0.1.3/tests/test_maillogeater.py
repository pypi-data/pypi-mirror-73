import unittest
import copy
import json

from maileater import MailLogEater


class TestTailLoader(unittest.TestCase):
    EMPTY_COUNTER = {
        "bounced": 0,
        "deferred": 0,
        "sent": 0,
        "expired": 0,
    }

    def setUp(self):
        self.expected = copy.deepcopy(TestTailLoader.EMPTY_COUNTER)

    # line is properly parsed and counted/uncounted
    def test_eat_sent(self):
        eater = MailLogEater()
        eater.eat("xxx status=sent xxx")
        self.expected["sent"] = 1
        self.assertEqual(eater.counter, self.expected)

    def test_eat_deferred(self):
        eater = MailLogEater()
        eater.eat("xxx status=deferred xxx")
        self.expected["deferred"] = 1
        self.assertEqual(eater.counter, self.expected)

    def test_eat_bounced(self):
        eater = MailLogEater()
        eater.eat("xxx status=bounced xxx")
        self.expected["bounced"] = 1
        self.assertEqual(eater.counter, self.expected)

    def test_eat_expired(self):
        eater = MailLogEater()
        eater.eat("xxx status=expired xxx")
        self.expected["expired"] = 1
        self.assertEqual(eater.counter, self.expected)

    # counter is retained over loop
    def test_retention(self):
        eater = MailLogEater()
        eater.eat("xxx status=sent xxx")
        eater.eat("xxx status=sent xxx")
        eater.eat("xxx status=deferred xxx")
        self.expected["sent"] = 2
        self.expected["deferred"] = 1
        self.assertEqual(eater.counter, self.expected)

    # status is properly formatted
    # - included counter is correct
    # - formatted as one line string (without newline)
    def test_retention(self):
        eater = MailLogEater()
        eater.eat("xxx status=sent xxx")
        eater.eat("xxx status=sent xxx")
        eater.eat("xxx status=deferred xxx")
        self.expected["sent"] = 2
        self.expected["deferred"] = 1
        output = str(eater)
        self.assertFalse("\n" in output)
        json_output = json.loads(output)
        self.assertEqual(json_output, self.expected)
