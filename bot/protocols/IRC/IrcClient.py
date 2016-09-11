import asyncio
from bot.AbstractClient import AbstractClient
import bot.ChatUser as ChatUser

from .IrcProtocol import IrcProtocol


class IrcClient(AbstractClient):
    def __init__(self, nickname):
        super(IrcClient, self).__init__()
        self.irc_user = ChatUser.new_ircuser(nickname)
        self.protocol = IrcProtocol()
        self.protocol.register_event_listener(self)

    def join_channel(self, name, password=""):
        self.protocol.join(name, password)

    def public_message(self, target, message):
        self.protocol.privmsg(target, message)

    def private_message(self, target, message):
        self.protocol.privmsg(target, message)

    def list_users_on_channel(self, channel):
        self.protocol.names([channel])

    def set_nickname(self, nickname):
        self.protocol.nick(nickname)
        self._nick = self.irc_user.get("nickname", self._nick)

    def on_welcome(self, event):
        self.private_message("Janiskeisari", "SPRIIT SPRAT")
        self.join_channel("#smurkkanat")

    def on_nick(self, event):
        #if event.source.nick == self.irc_user.real_nickname:
        #    self.irc_user.real_nickname = event.arguments[0]
        pass

    def on_connection_made(self, event):
        self.protocol.nick(self.irc_user.get("nickname"))
        self.protocol.user(self.irc_user.get("username"), self.irc_user.get("ircname"))

    def on_nicknameinuse(self, event):
        print(event)

    def on_featurelist(self, event):
        self.protocol.features.load(event.arguments)

    def on_ping(self, event):
        self.protocol.pong(event.source)

    def on_namreply(self, event):
        print(event)

    def on_privmsg(self, event):
        print(event)


if __name__ == '__main__':
    connection = IrcClient("JanisBot4")
    loop = asyncio.get_event_loop()
    coro = loop.create_connection(lambda: connection.protocol, "open.ircnet.net", 6667)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()
