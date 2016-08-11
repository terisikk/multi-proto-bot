# -*- coding: utf-8 -*-

import irc.client

from bot.AbstractConnection import *
from bot.Configurations import Configurations


class IrcConnection(AbstractConnection):
    def __init__(self):
        super(IrcConnection, self).__init__()
        self.client = irc.client.SimpleIRCClient()

        for operation in ["welcome", "join"]:
            methodname = "_on_" + operation
            method = getattr(self, methodname)
            self.client.connection.add_global_handler(operation, method)

    def load_configurations(self):
        confs = Configurations()
        self.nick = confs.get("irc", "nick")

    def start(self):
        self._connect()
        self.client.start()

    def _connect(self):
        print("connecting...")
        try:
            self.client.connect("open.ircnet.net", 6667, "JanisBot4")
        except irc.client.ServerConnectionError as e:
            print(e)

    def join_channel(self, name, key=""):
        self.client.join(name, key)
        self.channels.append(name)
        return

    @property
    def nick(self):
        return self.client.nick

    @nick.setter
    def nick(self, nickname):
        self.client.nick = nickname
        self._nick = nickname

    def disconnect(self):
        self.client.disconnect("Bye!")

    def _on_welcome(self, conn, event):
        print(event.target)
        print(conn)

    def _on_join(self, conn, event):
        return

    def _on_configurations_changed(self):
        pass

if __name__ == '__main__':
    connection = IrcConnection()
    connection.start()
