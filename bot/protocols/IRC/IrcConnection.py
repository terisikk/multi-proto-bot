import asyncio
from .IrcProtocol import IrcProtocol, IrcUser
from .AbstractConnection import AbstractConnection


class IrcConnection(AbstractConnection):
    def __init__(self, nickname):
        super(IrcConnection, self).__init__()
        self.protocol = IrcProtocol(IrcUser(nickname))

    def join_channel(self, name, password=""):
        self.protocol.join(name, password)

    def public_message(self, target, message):
        self.protocol.privmsg(target, message)

    def private_message(self, target, message):
        self.protocol.privmsg(target, message)

    def list_users_on_channel(self, channel):
        self.protocol.names([channel])

    @AbstractConnection.nick.setter
    def nick(self, nickname):
        self.protocol.nick(nickname)
        self._nick = self.protocol.ircuser.nickname


if __name__ == '__main__':
    connection = IrcConnection("JanisBot4")
    loop = asyncio.get_event_loop()
    coro = loop.create_connection(lambda: connection.protocol, "open.ircnet.net", 6667)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()
