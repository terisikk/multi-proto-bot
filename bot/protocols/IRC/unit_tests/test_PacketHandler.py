import unittest
from .. import packethandler

class TestPacketHandler(unittest.TestCase):
    def setUp(self):
        pass

    def test_line_endings_are_removed(self):
        message = "abc\nabc\r\n"
        parsed = packethandler._remove_line_endings(message)
        self.assertEqual(parsed, "abcabc")