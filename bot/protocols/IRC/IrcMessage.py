from irc.client import NickMask, events, _rfc_1459_command_regexp, message


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


class GlobOps(IrcMessage):
    def __init__(self, text):
        super(GlobOps, self).__init__("GLOBOPS", sentence=text)
        self.text = text

class Info(IrcMessage):
    def __init__(self, server):
        super(Info, self).__init__("INFO", [server])
        self.server = server

class Invite(IrcMessage):
    def __init__(self, nick, channel):
        pass

class Pass(IrcMessage):
    def __init__(self, password):
        super(Pass, self).__init__("PASS", [password])
        self.password = password
