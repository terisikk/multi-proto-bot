# -*- coding: utf-8 -*-
# @Author: teemu
# @Date:   2016-05-22 11:48:54
# @Last Modified by:   Teemu Risikko
# @Last Modified time: 2016-06-18 10:03:56

import unittest
import irc.client
from bot.IrcConnection import IrcConnection
from bot.Singleton import Singleton


class IrcConnectionTestCase(unittest.TestCase):
    connection = None

    def setUp(self):
        Singleton._instances = {}
        self.connection = IrcConnection()

    def tearDown(self):
        pass

    def test_server_not_connected(self):
        self.connection.nick = "JanisBotti"
        self.assertEquals(self.connection.nick, "JanisBotti")

    def test_load_configurations(self):
        self.connection.load_configurations()
        self.assertEqual(self.connection.nick, "JanisBot4")
