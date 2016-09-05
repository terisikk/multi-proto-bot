import unittest
from .. import IrcParser

class TestIrcParser(unittest.TestCase):
    def setUp(self):
        self.parser = IrcParser.IrcParser()

    def test_line_endings_are_removed(self):
        message = "abc\nabc\r\n"
        parsed = self.parser._remove_line_endings(message)
        self.assertEqual(parsed, "abcabc")