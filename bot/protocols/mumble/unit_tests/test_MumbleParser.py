import unittest
import struct
from bot.protocols.mumble.MumbleParser import MumbleParser, MumblePacket
import bot.protocols.mumble.Mumble_pb2 as mumble_protobuf


class TestMumbleParser(unittest.TestCase):
    def setUp(self):
        self.parser = MumbleParser()

    def test_offset_should_equal_header_size_plus_length(self):
        header = struct.Struct(">HI")
        length = 10
        self.assertEqual(self.parser._get_message_offset(length), header.size + length)

    def test_message_bytes_should_be_removed_from_buffer(self):
        data = bytearray([1, 2, 3, 4, 5, 6, 7, 8])
        offset = 2
        
        self.parser.buffer.extend(data)
        self.parser._extract_raw_message(offset)

        self.assertEqual(len(self.parser.buffer), len(data) - offset)
