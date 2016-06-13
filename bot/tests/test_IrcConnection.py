# -*- coding: utf-8 -*-
# @Author: teemu
# @Date:   2016-05-22 11:48:54
# @Last Modified by:   teemu
# @Last Modified time: 2016-06-11 17:28:05

import unittest
import irc.client
from bot.IrcConnection import IrcConnection


class IrcConnectionTestCase(unittest.TestCase):
    connection = None

    def setUp(self):
        self.connection = IrcConnection()

    def tearDown(self):
        pass

    def test_server_not_connected(self):
        self.connection.nick = "Janiskeisari"
        self.assertEquals(self.connection.nick, "Janiskeisari")
