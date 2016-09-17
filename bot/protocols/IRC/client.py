import asyncio
from bot.AbstractClient import AbstractClient
import bot.ChatUser as ChatUser

from .protocol import IrcProtocol
from . import message as IrcMessage


class IrcClient(AbstractClient):
    def __init__(self, nickname):
        super(IrcClient, self).__init__()
        self.irc_user = ChatUser.new_ircuser(nickname)
        self.protocol = IrcProtocol()
        self.protocol.register_event_listener(self)

    def join_channel(self, channel_name, password=""):
        command = IrcMessage.Join(channel_name, password)
        self.protocol.send(command)

    def public_message(self, target, message):
        command = IrcMessage.Privmsg(target, message)
        self.protocol.send(command)

    def private_message(self, target, message):
        command = IrcMessage.Privmsg(target, message)
        self.protocol.send(command)

    def list_users_on_channel(self, channel):
        command = IrcMessage.Names([channel])
        self.protocol.send(command)

    def set_nickname(self, nickname):
        command = IrcMessage.Nick(nickname)
        self.protocol.send(command)

    def log_on(self, password):
        command = IrcMessage.Pass(password)
        self.protocol.send(command)

    def on_welcome(self, event):
        self.private_message("Janiskeisari", "SPRIIT SPRAT")
        self.join_channel("#smurkkanat")

    def on_nick(self, event):
        #if event.source.nick == self.irc_user.real_nickname:
        #    self.irc_user.real_nickname = event.arguments[0]
        pass

    def on_connection_made(self, event):
        password = self.irc_user.get("password", None)
        if password:
            self.log_on(password)

        self.set_nickname(self.irc_user.get("nickname"))
        command = IrcMessage.User(self.irc_user.get("username"), self.irc_user.get("ircname"))
        self.protocol.send(command)

    def on_nicknameinuse(self, event):
        print(event)

    def on_featurelist(self, event):
        self.protocol.features.load(event.arguments)

    def on_ping(self, event):
        command = IrcMessage.Pong(event.arguments[0])
        self.protocol.send(command)

    def on_namreply(self, event):
        print(event)

    def on_topic(self, event):
        print("ON TOPIC: ", event.channel, event.topic)


if __name__ == '__main__':
    connection = IrcClient("JanisBot4")
    loop = asyncio.get_event_loop()
    coro = loop.create_connection(lambda: connection.protocol, "open.ircnet.net", 6667)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()
