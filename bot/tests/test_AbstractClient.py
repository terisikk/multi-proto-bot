import unittest
from bot.AbstractClient import AbstractClient


class AbstractClientTestCase(unittest.TestCase):
    connection = None

    def setUp(self):
        self.connection = AbstractClient()

    def tearDown(self):
        pass

    def test_nick_is_set(self):
        self.connection.nick = "Janiskeisari"
        self.assertEqual(self.connection.nick, "Janiskeisari")
