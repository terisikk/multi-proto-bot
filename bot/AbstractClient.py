# -*- coding: utf-8 -*-
import asyncio
import bot.generics as generics

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
        self.eventmappers = {}

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

    def publish_event(self, name, event):
        for listener in self.listeners:

            generic_event = self.event_to_generic(event, name)

            handler = getattr(listener, "on_" + name, None)
            if handler:
                handler(generic_event)

    def event_to_generic(self, event, name):
        mapper = self.eventmappers.get(name, None)
        if mapper:
            return mapper(event)
        return generics.GenericEvent(self.client_type, event)


    def start(self, server, port):
        self.loop = asyncio.get_event_loop()
