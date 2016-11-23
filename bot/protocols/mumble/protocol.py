import asyncio
import ssl
from collections import namedtuple

from bot.ChatProtocol import ChatProtocol
import bot.protocols.mumble.Mumble_pb2 as mumble_protobuf
from .parser import MumbleParser, PACKET_NUMBERS


LOGGING = True

MumbleMessage = namedtuple("MumbleMessage", ["name", "message"])


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
    def __init__(self):
        super(MumbleProtocol, self).__init__()
        self._ping_handler = None
        self.parser = MumbleParser()

    def connection_lost(self, reason):
        print("Connection lost", reason)

    def data_received(self, data):
        message, name = self.parser.process_buffer(data)

        if message:
            m = MumbleMessage(name.lower(), message)
            self.notify_listeners(m)

    def send(self, protobuf_message):
        packet = self.parser.pack_data(protobuf_message)
        self.send_raw(packet)
