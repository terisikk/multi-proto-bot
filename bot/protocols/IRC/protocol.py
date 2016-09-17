# -*- coding: utf-8 -*-

from irc.client import ctcp, features, is_channel
from jaraco.stream import buffer

import asyncio
from bot.ChatProtocol import ChatProtocol

from . import packethandler


class IrcProtocol(ChatProtocol):
    def __init__(self):
        super(IrcProtocol, self).__init__()
        self.connected = False
        self.real_server_name = ""
        self.features = features.FeatureSet()
        self.transport = None
        self.buffer = buffer.LenientDecodingLineBuffer()

    def connection_made(self, transport):
        self.connected = True

        self.transport = transport

        for listener in self.listeners:
            listener.on_connection_made(None)

        return self

    def reconnect(self):
        pass

    def get_server_name(self):
        return self.real_server_name or ""

    def data_received(self, data):
        #print("FROM SERVER: {}".format(data))

        self.buffer.feed(data)

        for line in self.buffer:
            event = packethandler.unpack_data(line)
            print(event.command, event.source, event.arguments)
            setattr(event, "name", event.command.lower())
            self.notify_listeners(event)

    def _handle_message(self, arguments, command, source, tags):
        target, msg = arguments[:2]
        messages = ctcp.dequote(msg)
        if command == "privmsg":
            if is_channel(target):
                command = "pubmsg"
        else:
            if is_channel(target):
                command = "pubnotice"
            else:
                command = "privnotice"
        for m in messages:
            if isinstance(m, tuple):
                if command in ["privmsg", "pubmsg"]:
                    command = "ctcp"
                else:
                    command = "ctcpreply"

                m = list(m)
                print("command: {}, source: {}, target: {}, "
                          "arguments: {}, tags: {}".format(command, source, target, m, tags))
                if command == "ctcp" and m[0] == "ACTION":
                    pass
            else:
                print("command: {}, source: {}, target: {}, "
                          "arguments: {}, tags: {}".format(command, source, target, [m], tags))


    def _handle_other(self, arguments, command, source, tags):
        target = None
        if command == "quit":
            arguments = [arguments[0]]
        elif command == "ping":
            target = arguments[0]
        else:
            target = arguments[0] if arguments else None
            arguments = arguments[1:]
        if command == "mode":
            if not is_channel(target):
                command = "umode"
        print("command: {}, source: {}, target: {}, "
                  "arguments: {}, tags: {}".format(command, source, target, arguments, tags))

    def is_connected(self):
        return self.connected

    def disconnect(self, msg=""):
        if not self.connected:
            return

        self.connected = False

    def connection_lost(self, exc):
        print("Connection lost")
        loop.stop()

    def send(self, command):
        print("TO SERVER: ", command.command, command.arguments, command.tags, command.sentence)
        message = packethandler.pack_data(command)
        self.send_raw(message)

loop = asyncio.get_event_loop()
