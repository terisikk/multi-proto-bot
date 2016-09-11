import asyncio
import ssl

from bot.ChatProtocol import ChatProtocol
import bot.protocols.mumble.Mumble_pb2 as mumble_protobuf
from .MumbleParser import MumbleParser, PACKET_NUMBERS


MUMBLE_VERSION = 66052  # 1.2.4
LOGGING = True


class UDPTunnelTransport(asyncio.DatagramTransport):
    def __init__(self, control_protocol):
        super().__init__(self)
        self.control_protocol = control_protocol

    def sendto(self, data, addr=None):
        assert addr is None
        self.control_protocol.send_payload(
            PACKET_NUMBERS[mumble_protobuf.UDPTunnel], data)


class MumbleProtocol(ChatProtocol):
    """Implements mumble's protocol for communicating with a murmur server.
    http://mumble.sourceforge.net/Protocol"""
    def __init__(self, username, password):
        super(MumbleProtocol, self).__init__()
        self.username = username
        self.password = password
        self._ping_handler = None
        self.transport = None
        self.parser = MumbleParser()

    def connection_made(self, transport):
        self.transport = transport
        
        self.send_version()
        self.authenticate()
        
        self.ping()
        return self

    def connection_lost(self, reason):
        print("Connection lost", reason)

    def data_received(self, data):
        message = self.parser.process_buffer(data)
        print(message)

    def send(self, protobuf_message):
        packet = self.parser.pack_data(protobuf_message)
        self.send_raw(packet)

    def send_version(self):
        client_version = mumble_protobuf.Version()
        client_version.version = MUMBLE_VERSION
        self.send(client_version)

    def authenticate(self):
        client_auth = mumble_protobuf.Authenticate()
        client_auth.username = "JanisBot4"
        client_auth.password = "mumina1"
        client_auth.celt_versions.append(-2147483637)
        client_auth.celt_versions.append(-2147483632)
        client_auth.opus = True
        self.send(client_auth)

    def ping(self):
        ping = mumble_protobuf.Ping()
        self.send(ping)

    def send_textmessage(self, text, channels=None, users=None):
        """Send chat message to a list of channels or users by ids"""
        text_message = mumble_protobuf.TextMessage()
        text_message.message = text
        if channels:
            text_message.channel_id.extend(channels)
        if users:
            text_message.session.extend(users)
        self.send(text_message)

    def move_user(self, channel_id, user_id):
        user_state = mumble_protobuf.UserState()
        user_state.session = user_id
        user_state.channel_id = channel_id
        self.send(user_state)

loop = asyncio.get_event_loop()

if __name__ == '__main__':
    ssl_ctxt = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    coro = loop.create_connection(lambda: MumbleProtocol("Janisbot4", "mumina1"), "terisikk.dy.fi", 64738, ssl=ssl_ctxt)
    loop.run_until_complete(coro)
    print("paskaa")
    loop.run_forever()
    loop.close()
