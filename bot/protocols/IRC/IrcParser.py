import re
from irc.client import NickMask, events, _rfc_1459_command_regexp, message
from irc.client import MessageTooLong, InvalidCharacters


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
        if fields is not None:
            return  " " + " ".join(fields).strip()
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

    @classmethod
    def from_server_message(self, line):
        match = _rfc_1459_command_regexp.match(line)
        if match is None:
            return self

        grp = match.group

        self.source = NickMask.from_group(grp("prefix"))
        self.command = self._command_from_group(grp("command"))
        self.arguments = message.Arguments.from_group(grp('argument'))
        self.tags = message.Tag.from_group(grp('tags'))
        return self


class IrcParser(object):
    def __init__(self):
        pass

    def pack_data(self, command, arguments=None, tags=None, sentence=None):
        msg = IrcMessage(command, arguments, tags, sentence).to_outgoing_message()
        return self._prepare_message(msg)

    def unpack_data(self, line):
        return IrcMessage.from_server_message(line)        

    def _prepare_message(self, msg):
        msg = self._remove_line_endings(msg)
        
        sendbytes = msg.encode('utf-8') + b'\r\n'
        self._raise_error_if_message_too_long(sendbytes)
        return sendbytes

    def _remove_line_endings(self, msg):
        msg = re.sub(r"[\n\r]", "", msg)
        return msg

    def _raise_error_if_message_too_long(self, sendbytes):
        # According to the RFC http://tools.ietf.org/html/rfc2812#page-6,
        # clients should not transmit more than 512 bytes.
        if len(sendbytes) > 512:
            error = "Messages limited to 512 bytes including CR/LF"
            raise MessageTooLong(error)