from irc.client import NickMask, events, _rfc_1459_command_regexp, message
from irc.client import always_iterable

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
            return None

        grp = match.group

        source = NickMask.from_group(grp("prefix"))
        command = IrcMessage._command_from_group(grp("command"))
        arguments = message.Arguments.from_group(grp('argument'))
        tags = message.Tag.from_group(grp('tags'))
        
        msg = IrcMessage(command, arguments, tags)
        msg.source = source
        return msg


class Away(IrcMessage):
    def __init__(self, text=""):
        super().__init__("AWAY", sentence=text)
        self.text = text

class Info(IrcMessage):
    def __init__(self, server):
        super().__init__("INFO", [server])
        self.server = server

class Invite(IrcMessage):
    def __init__(self, nick, channel):
        super().__init__("INVITE", [nick, channel])
        self.nick = nick
        self.channel = channel

class Ison(IrcMessage):
    def __init__(self, nicks):
        super().__init__("ISON", nicks)
        self.nicks = nicks

class Join(IrcMessage):
    def __init__(self, channels, keys=None):
        super().__init__("JOIN")
        self.arguments = []
        self.channels = always_iterable(channels)
        self.arguments.append(",".join(self.channels))

        self.keys = always_iterable(keys)
        self.arguments.append(",".join(self.keys))

class Kick(IrcMessage):
    def __init__(self, channel, nick, comment=None):
        super().__init__("KICK", [channel, nick], sentence=comment)
        self.channel = channel
        self.nick = nick
        self.comment = comment

class Links(IrcMessage):
    def __init__(self, remote_server="", server_mask=""):
        super().__init__("LINKS", [remote_server, server_mask])
        self.remote_server = remote_server
        self.server_mask = server_mask

class List(IrcMessage):
    def __init__(self, channels=None, server=""):
        super().__init__("LIST")
        self.channels = always_iterable(channels)
        self.server = server

        channel_string = ",".join(self.channels)
        self.arguments = [channel_string, server]

class Lusers(IrcMessage):
    def __init__(self, server=""):
        super().__init__("LUSERS", [server])
        self.server = server

class Mode(IrcMessage):
    def __init__(self, target, flags):
        super().__init__("MODE", [target, flags])
        self.target = target
        self.flags = flags

class Motd(IrcMessage):
    def __init__(self, server=""):
        super().__init__("MOTD", [server])
        self.server = server

class Names(IrcMessage):
    def __init__(self, channels=None):
        self.channels = always_iterable(channels)
        channel_string = ','.join(self.channels)
        super().__init__("NAMES", [channel_string])

class Nick(IrcMessage):
    def __init__(self, nick):
        super().__init__("NICK", [nick])
        self.nick = nick

class Notice(IrcMessage):
    def __init__(self, target, text):
        super().__init__("NOTICE", [target, text])
        self.target = target
        self.text = text

class Oper(IrcMessage):
    def __init__(self, nick, password):
        super().__init__("OPER", [nick, password])
        self.nick = nick
        self.password = password

class Part(IrcMessage):
    def __init__(self, channels, reason=""):
        self.channels = always_iterable(channels)
        channel_string = ",".join(self.channels)
        super().__init__("PART", [channel_string, reason])    

class Pass(IrcMessage):
    def __init__(self, password):
        super().__init__("PASS", [password])
        self.password = password

class Ping(IrcMessage):
    def __init__(self, target, target2=""):
        super().__init__("PING", [target, target2])
        self.target = target
        self.target2 = target2

class Pong(IrcMessage):
    def __init__(self, target, target2=""):
        super().__init__("PONG", [target, target2])
        self.target = target
        self.target2 = target2

class Privmsg(IrcMessage):
    def __init__(self, target, text):
        super().__init__("PRIVMSG", [target, text])
        self.target = target
        self.text = text

class Quit(IrcMessage):
    def __init__(self, reason=None):
        # Note that many IRC servers don't use your QUIT reason
        # unless you've been connected for at least 5 minutes!
        super().__init__("QUIT", sentence=reason)
        self.reason = reason

class Stats(IrcMessage):
    def __init__(self, statstype, server=""):
        super().__init__("STATS ", [statstype, server])
        self.statstype = statstype
        self.server = server

class Time(IrcMessage):
    def __init__(self, server=""):
        super().__init__("TIME", [server])
        self.server = server

class Topic(IrcMessage):
    def __init__(self, channel, topic=None):
        super().__init__("TOPIC", [channel], sentence=topic)
        self.channel = channel
        self.topic = topic

class Trace(IrcMessage):
    def __init__(self, target=""):
        super().__init__("TRACE", [target])
        self.target = target

class User(IrcMessage):
    def __init__(self, username, realname):
        super().__init__("USER", [username, "0", "*"], sentence=realname)
        self.username = username
        self.realname = realname

class Userhost(IrcMessage):
    def __init__(self, nicks):
        self.nicks = always_iterable(nicks)
        super().__init__("USERHOST", [",".join(self.nicks)])
        self.nicks = self.nicks

class Users(IrcMessage):
    def __init__(self, server=""):
        super().__init__("USERS", [server])
        self.server = server

class Version(IrcMessage):
    def __init__(self, server=""):
        super().__init__("VERSION", [server])
        self.server = server

class Wallops(IrcMessage):
    def __init__(self, text):
        super().__init__("WALLOPS", sentence=text)
        self.text = text

class Who(IrcMessage):
    def __init__(self, target="", op=False):
        arguments = [target]
        if op:
            arguments.append("o")
        super().__init__("WHO", arguments)
        self.target = target
        self.op = op

class Whois(IrcMessage):
    def __init__(self, targets):
        self.targets = always_iterable(targets)
        super().__init__("WHOIS", ",".join(self.targets))

class Whowas(IrcMessage):
    def __init__(self, nicks, maximum="", server=""):
        self.nicks = always_iterable(nicks)
        super().__init__("WHOWAS", [self.nicks, maximum, server])
        self.maximum = maximum
        self.server = server