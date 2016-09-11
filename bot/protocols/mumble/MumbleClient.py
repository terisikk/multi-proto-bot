import asyncio
from bot.AbstractClient import AbstractClient
from .MumbleProtocol import MumbleProtocol


class MumbleClient(AbstractClient):
    def __init__(self, nickname, password):
        super(MumbleClient, self).__init__()
        self.protocol = MumbleProtocol(nickname, password)

    def public_message(self, target, message):
        self.protocol.send_textmessage(message, [target])

    def private_message(self, target, message):
        self.protocol.send_textmessage(message, None, [target])
