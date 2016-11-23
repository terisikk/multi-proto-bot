import struct
import bot.protocols.mumble.Mumble_pb2 as mumble_protobuf

PACKET_TYPES = {
    0: mumble_protobuf.Version,
    1: mumble_protobuf.UDPTunnel,
    2: mumble_protobuf.Authenticate,
    3: mumble_protobuf.Ping,
    4: mumble_protobuf.Reject,
    5: mumble_protobuf.ServerSync,
    6: mumble_protobuf.ChannelRemove,
    7: mumble_protobuf.ChannelState,
    8: mumble_protobuf.UserRemove,
    9: mumble_protobuf.UserState,
    10: mumble_protobuf.BanList,
    11: mumble_protobuf.TextMessage,
    12: mumble_protobuf.PermissionDenied,
    13: mumble_protobuf.ACL,
    14: mumble_protobuf.QueryUsers,
    15: mumble_protobuf.CryptSetup,
    16: mumble_protobuf.ContextActionModify,
    17: mumble_protobuf.ContextAction,
    18: mumble_protobuf.UserList,
    19: mumble_protobuf.VoiceTarget,
    20: mumble_protobuf.PermissionQuery,
    21: mumble_protobuf.CodecVersion,
    22: mumble_protobuf.UserStats,
    23: mumble_protobuf.RequestBlob,
    24: mumble_protobuf.ServerConfig,
    25: mumble_protobuf.SuggestConfig,
}


PACKET_NUMBERS = {t: n for n, t in PACKET_TYPES.items()}

HEADER_FORMAT = ">HI"


class MumblePacket():
    def __init__(self, number=None, length=0, data=None):
        self.number = number
        self.length = length
        self.data = data


class VoicePacket():
    def __init__(self):
        self.session = 0
        self.type = 0
        self.target = 0
        self.sequence = 0
        self.lengths = []
        self.frames = []

    def __str__(self):
        s = "Session: {}\nType: {}\nTarget: {}\nSequence: {}\n"
        return s.format(self.session, self.type, self.target, self.sequence)


class MumbleParser(object):
    def __init__(self):
        self.buffer = bytearray()

    def pack_data(self, protobuf_message):
        payload = protobuf_message.SerializeToString()
        packet_type = PACKET_NUMBERS[protobuf_message.__class__]
        return struct.pack(HEADER_FORMAT, packet_type, len(payload)) + payload

    def process_buffer(self, data):
        self.buffer.extend(data)
        parsed_message = None

        while True:
            packet = MumblePacket()

            try:
                packet.number, packet.length = struct.unpack_from(HEADER_FORMAT, self.buffer)
            except struct.error:
                break

            offset = self._get_message_offset(packet.length)

            if not self._enough_data_to_parse(offset):
                break

            packet.data = self._extract_raw_message(offset)

            parsed_message = self._parse_message(packet)
        return parsed_message

    def _get_message_offset(self, length):
        header = struct.Struct(HEADER_FORMAT)
        offset = header.size + length
        return offset

    def _enough_data_to_parse(self, offset):
        if len(self.buffer) < offset:
            return False
        return True

    def _extract_raw_message(self, offset):
        header = struct.Struct(HEADER_FORMAT)
        raw_message = bytes(self.buffer[header.size:offset])
        self.buffer[:] = self.buffer[offset:]
        return raw_message

    def _parse_message(self, packet):
        message_class = PACKET_TYPES[packet.number]

        if message_class == mumble_protobuf.UDPTunnel:
            parsed = self._parse_voicedata(packet.data)
        else:
            parsed = message_class()
            parsed.ParseFromString(packet.data)
        return parsed, message_class.__name__

    def _parse_voicedata(self, data):
        pass
