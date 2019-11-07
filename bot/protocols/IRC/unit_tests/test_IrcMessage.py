# -*- coding: utf-8 -*-

import unittest
from ..message import IrcMessage


class TestIrcMessage(unittest.TestCase):

    def test_returns_only_command(self):
        message = IrcMessage("TRACE")
        self.assertEqual(message.to_outgoing_message(), "TRACE")

    def test_separates_one_argument_with_space(self):
        message = IrcMessage("TOPIC", ["trash"])
        self.assertEqual(message.to_outgoing_message(), "TOPIC trash")

    def test_separates_multiple_arguments_with_space(self):
        message = IrcMessage("INVITE", ["rotta", "#rotankolo"])
        self.assertEqual(message.to_outgoing_message(), "INVITE rotta #rotankolo")

    def test_separates_sentence_with_space_and_adds_colon_at_the_start(self):
        message = IrcMessage("GLOBOPS", sentence="trash hemul trash")
        self.assertEqual(message.to_outgoing_message(), "GLOBOPS :trash hemul trash")

    def test_separates_arguments_and_sentence(self):
        message = IrcMessage("KICK", ["rotta", "#rotankolo"], sentence="Ei juustoa rotalle")
        self.assertEqual(message.to_outgoing_message(), "KICK rotta #rotankolo :Ei juustoa rotalle")

    def test_handles_colon_separated_arguments(self):
        message = IrcMessage("JOIN", [",".join(["#rotankolo", "#rommiluola", "#lol.oulu"])])
        self.assertEqual(message.to_outgoing_message(), "JOIN #rotankolo,#rommiluola,#lol.oulu")
