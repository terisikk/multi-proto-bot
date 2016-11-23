# -*- coding: utf-8 -*-
import asyncio


class AbstractClient(object):
    def __init__(self):
        self._nick = ""
        self.connection = None
        self.servers = []
        self.channels = []
        self.protocol = None
        self.loop = None
        self.listeners = []
        self.register_event_listener(self)
        self.client_type = None

    def authenticate(self, username=None, password=None):
        raise NotImplementedError("authenticate not implemented")

    def join_channel(self, name, password=""):
        raise NotImplementedError("join_channel not implemented")

    def public_message(self, target, message):
        raise NotImplementedError("public_message not implemented")

    def private_message(self, target, message):
        raise NotImplementedError("private_message not implemented")

    def list_users_on_channel(self, channel):
        raise NotImplementedError("list_users not implemented")

    def register_event_listener(self, listener):
        if listener not in self.listeners:
            self.listeners.append(listener)

    def publish_event(self, event):
        for listener in self.listeners:
            handler = getattr(listener, "on_" + event.name, None)
            if handler:
                handler(event)

    def start(self, server, port):
        self.loop = asyncio.get_event_loop()
