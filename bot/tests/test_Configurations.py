# -*- coding: utf-8 -*-
# @Author: teemu
# @Date:   2016-06-12 11:23:42
# @Last Modified by:   teemu
# @Last Modified time: 2016-06-12 16:10:14
import unittest
from bot.Configurations import Configurations
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


class ConfigurationsTestCase(unittest.TestCase):

    def setUp(self):
        self.config = Configurations()
        self.filepath = os.path.join(__location__, "../conf/connections.conf")

    def tearDown(self):
        pass

    def test_configurations_is_singleton(self):
        config2 = Configurations()
        self.assertEqual(self.config, config2)
        self.config.x = "test"
        config2.x = "notest"
        self.assertEqual(self.config.x, config2.x)

    def test_read_configurations_files(self):
        self.config.read(self.filepath)
        self.assertTrue("default" in self.config.sections())

    def test_read_irc_configuration(self):
        self.config.read(self.filepath)
        self.assertEqual(self.config.get("irc", "nick", None), "JanisBot4")
