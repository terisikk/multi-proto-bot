from . import parser

class IrcMessage(object):
    def __init__(self, command, arguments=None, tags=None, sentence=None, source=None):
        self.source = source
        self.command = command
        self.arguments = arguments 
        self.tags = tags
        self.sentence = sentence

    def to_outgoing_message(self):
        msg = ""
        msg += self._add_tags()
        msg += self.command
        msg += self._add_arguments()
        return msg

    def _add_tags(self):
        if self.tags:
            return " " + parser.tags_to_string(self.tags)
        return ""

    def _add_arguments(self):
        string = ""
        if self.arguments or self.sentence:
            string += " "
        string += parser.arguments_to_string(self.arguments, self.sentence)
        return string


