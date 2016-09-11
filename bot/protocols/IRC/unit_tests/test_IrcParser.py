import unittest
from .. import IrcParser

class TestIrcParser(unittest.TestCase):
    def setUp(self):
        pass

    def test_line_endings_are_removed(self):
        message = "abc\nabc\r\n"
        parsed = IrcParser._remove_line_endings(message)
        self.assertEqual(parsed, "abcabc")