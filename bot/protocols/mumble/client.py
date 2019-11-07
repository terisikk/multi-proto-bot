import ssl

import bot.protocols.mumble.Mumble_pb2 as mumble_protobuf

from bot.AbstractClient import AbstractClient
from .protocol import MumbleProtocol

MUMBLE_VERSION = 66052  # 1.2.4
PING_INTERVAL = 20


class MumbleClient(AbstractClient):
    def __init__(self, nickname, password):
        super(MumbleClient, self).__init__()
        self.protocol = MumbleProtocol()
        self.username = nickname
        self.password = password
        self.protocol.register_event_listener(self)
        self.client_type = "mumble"

    def on_connection_made(self, event):
        self.send_version()
        self.authenticate(self.username, self.password)

        self.ping()

    def send_version(self):
        client_version = mumble_protobuf.Version()
        client_version.version = MUMBLE_VERSION
        self.protocol.send(client_version)

    def authenticate(self, username=None, password=None):
        client_auth = mumble_protobuf.Authenticate()
        client_auth.username = username
        client_auth.password = password
        client_auth.celt_versions.append(-2147483637)
        client_auth.celt_versions.append(-2147483632)
        client_auth.opus = True
        self.protocol.send(client_auth)

    def public_message(self, target, message):
        self.send_textmessage(message, [target])

    def private_message(self, target, message):
        self.send_textmessage(message, None, [target])

    def ping(self):
        ping = mumble_protobuf.Ping()
        self.protocol.send(ping)
        self.loop.call_later(PING_INTERVAL, self.ping)

    def on_textmessage(self, message):
        print("CLIENT: ", message)

    def send_textmessage(self, text, channels=None, users=None):
        """Send chat message to a list of channels or users by ids"""
        text_message = mumble_protobuf.TextMessage()
        text_message.message = text
        if channels:
            text_message.channel_id.extend(channels)
        if users:
            text_message.session.extend(users)
        self.protocol.send(text_message)

    def join_channel(self, name, password=""):
        user_state = mumble_protobuf.UserState()
        user_state.channel_id = 1
        self.protocol.send(user_state)

    def move_user(self, channel_id, user_id):
        user_state = mumble_protobuf.UserState()
        user_state.session = user_id
        user_state.channel_id = channel_id
        self.protocol.send(user_state)

    def start(self, server, port):
        super().start(server, port)
        ssl_ctxt = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

        coroutine = self.loop.create_connection(lambda: self.protocol, server, port, ssl=ssl_ctxt)
        self.loop.run_until_complete(coroutine)
