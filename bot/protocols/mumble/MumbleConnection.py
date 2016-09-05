import asyncio
from bot.AbstractConnection import AbstractConnection
from .MumbleProtocol import MumbleProtocol


class MumbleConnection(AbstractConnection):
    def __init__(self, nickname, password):
        super(MumbleConnection, self).__init__()
        self.protocol = MumbleProtocol(nickname, password)

    def public_message(self, target, message):
        self.protocol.send_textmessage(message, [target])

    def private_message(self, target, message):
        self.protocol.send_textmessage(message, None, [target])
