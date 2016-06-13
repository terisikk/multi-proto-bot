# -*- coding: utf-8 -*-
# @Author: teemu
# @Date:   2016-05-22 11:14:58
# @Last Modified by:   teemu
# @Last Modified time: 2016-06-12 14:19:55

import irc.client

from bot.AbstractConnection import *


class IrcConnection(AbstractConnection):
    def __init__(self):
        super(IrcConnection, self).__init__()
        self.client = irc.client.SimpleIRCClient()

        for operation in ["welcome", "join"]:
            methodname = "_on_" + operation
            method = getattr(self, methodname)
            self.client.connection.add_global_handler(operation, method)

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

    def start(self):
        self._connect()
        self.client.start()

if __name__ == '__main__':
    connection = IrcConnection()
    connection.start()
