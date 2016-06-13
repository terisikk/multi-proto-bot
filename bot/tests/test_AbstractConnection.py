import unittest
from bot.AbstractConnection import AbstractConnection


class AbstractConnectionTestCase(unittest.TestCase):
    connection = None

    def setUp(self):
        self.connection = AbstractConnection()

    def tearDown(self):
        pass

    def test_nick_is_set(self):
        self.connection.nick = "Janiskeisari"
        self.assertEqual(self.connection.nick, "Janiskeisari")
