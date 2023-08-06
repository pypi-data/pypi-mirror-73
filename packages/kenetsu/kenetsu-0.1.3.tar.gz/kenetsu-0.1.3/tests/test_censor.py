import unittest


from censor import Censor


class TestCensor(unittest.TestCase):
    def test_censor(self):
        c = Censor()
        target = ("Jan 13 01:08:40 localhost postfix/smtp[123]: "
                  "0A0000123B: to=<alice@example.com>, "
                  "relay=mail.example.com[192.0.2.222]:25, delay=0.42, "
                  "delays=0.1/0/0.08/0.24, dsn=2.0.0, status=sent (250 ok)"
                  )
        got = c.censor(target)
        expected = ("Jan 13 01:08:40 localhost postfix/smtp[123]: "
                    "0A0000123B: to=<censored@example.org>, "
                    "relay=mail.example.com[192.0.2.222]:25, delay=0.42, "
                    "delays=0.1/0/0.08/0.24, dsn=2.0.0, status=sent (250 ok)"
                    )
        self.assertEqual(got, expected)
