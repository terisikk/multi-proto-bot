import asyncio
from .AbstractConnection import AbstractConnection


class MumbleConnection(AbstractConnection):
    def __init__(self):
        super(MumbleConnection, self).__init__()
