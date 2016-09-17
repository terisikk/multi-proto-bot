from irc.client import NickMask, events, _rfc_1459_command_regexp, message
from . import commands

class IrcMessage(object):
    def __init__(self, command, arguments=None, tags=None, sentence=None):
        self.source = None
        self.command = command
        self.arguments = arguments 
        self.tags = tags
        self.sentence = sentence

    def to_outgoing_message(self):
        msg = self.command
        msg += self._add_fields(self.arguments)
        msg += self._add_fields(self.tags)
        msg += self._add_sentence()
        return msg

    def _add_fields(self, fields):
        fieldstring = ""
        if fields is not None:
            for field in fields:
                fieldstring += self._add_field(field)

            return fieldstring
        return ""

    def _add_field(self, field):
        if field is not None:
            return " " + field.strip()
        return ""

    def _add_sentence(self):
        if self.sentence is not None:
            return " :" + self.sentence
        return ""

    @staticmethod
    def _command_from_group(group):
        command = group.lower()
        # Translate numerics into more readable strings.
        return events.numeric.get(command, command)

    @staticmethod
    def from_server_message(line):
        match = _rfc_1459_command_regexp.match(line)
        if match is None:
            print("NO MATCH: ", line)
            return None

        grp = match.group

        source = NickMask.from_group(grp("prefix"))
        command = IrcMessage._command_from_group(grp("command"))
        arguments = message.Arguments.from_group(grp('argument'))
        tags = message.Tag.from_group(grp('tags'))
        
        msg = None

        if command == "topic":
            msg = commands.Topic(*arguments)
        else: 
            msg = IrcMessage(command, arguments, tags)
            msg.source = source
        return msg
