# -*- coding: utf-8 -*-
import asyncio


class AbstractConnection(object):
    connection = None
    servers = []
    channels = []
    protocol = None
    loop = None

    def __init__(self):
        self._nick = ""

    def join_channel(self, name, password=""):
        raise NotImplementedError("join_channel not implemented")

    def public_message(self, target, message):
        raise NotImplementedError("public_message not implemented")

    def private_message(self, target, message):
        raise NotImplementedError("private_message not implemented")

    def list_users_on_channel(self, channel):
        raise NotImplementedError("list_users not implemented")

    @property
    def nick(self):
        return self._nick

    @nick.setter
    def nick(self, nickname):
        self._nick = nickname

    def start(self, server, port):
        self.loop = asyncio.get_event_loop()
        coro = self.loop.create_connection(self.protocol, server, port)
