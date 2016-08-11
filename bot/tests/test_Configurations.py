# -*- coding: utf-8 -*-
# @Author: teemu
# @Date:   2016-06-12 11:23:42
# @Last Modified by:   Teemu Risikko
# @Last Modified time: 2016-06-18 10:04:05
import unittest
from bot.Configurations import Configurations
from bot.Singleton import Singleton
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


class DummyObserver(object):
    called = False

    def _on_configurations_changed(self):
        self.called = True


class ConfigurationsTestCase(unittest.TestCase):

    def setUp(self):
        self.config = Configurations()
        self.filepath = os.path.join(__location__, "test_connections.conf")
        f = open(self.filepath, "w")
        f.write("""
[DEFAULT]
nick: JanisBot4

[irc]
nick: ${DEFAULT:nick}
servers: open.ircnet.net, irc.atw-inter.net, openirc.snt.utwente.nl, irc.ludd.luth.se, irc.eversible.net
port: 6667
realname: JanisBot4)
""")
        f.close()

    def tearDown(self):
        Singleton._instances = {}
        f = open(self.filepath, "w")
        f.write("")
        f.close()

    def test_configurations_is_singleton(self):
        config2 = Configurations()
        self.assertEqual(self.config, config2)
        self.config.x = "test"
        config2.x = "notest"
        self.assertEqual(self.config.x, config2.x)

    def test_read_configurations_files(self):
        self.config.read(self.filepath)
        self.assertTrue("irc" in self.config.sections())

    def test_read_irc_configuration(self):
        self.config.read(self.filepath)
        self.assertEqual(self.config.get("irc", "nick", None), "JanisBot4")

    def test_set_configuration(self):
        self.config.read(self.filepath)
        self.config.set("irc", "nick", "JanisBot5")
        self.assertEqual(self.config.get("irc", "nick", None), "JanisBot5")

    def test_register_observer(self):
        do = DummyObserver()
        self.config.register_observer(do)
        self.assertTrue(do in self.config.observers)

    def test_notify_observers(self):
        do = DummyObserver()
        self.config.register_observer(do)
        self.config.notify_observers()
        self.assertTrue(do.called)

    def test_remove_failed_observer(self):
        do = DummyObserver()
        self.config.register_observer(do)
        do._on_configurations_changed = None
        self.config.notify_observers()
        self.assertNotIn(do, self.config.observers)
