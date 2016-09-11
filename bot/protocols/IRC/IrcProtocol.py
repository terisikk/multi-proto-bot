# -*- coding: utf-8 -*-

from irc.client import always_iterable, ctcp, features, is_channel

import asyncio
from bot.ChatProtocol import ChatProtocol

import bot.protocols.IRC.IrcParser as IrcParser


class IrcProtocol(ChatProtocol):
    def __init__(self, password=None):
        super(IrcProtocol, self).__init__()
        self.connected = False
        self.real_server_name = ""
        self.password = password
        self.features = features.FeatureSet()
        self.transport = None

    def connection_made(self, transport):
        self.connected = True

        self.transport = transport

        if self.password:
            self.log_on()

        for listener in self.listeners:
            listener.on_connection_made(None)

        return self

    def log_on(self):
        self.pass_(self.password)

    def reconnect(self):
        pass

    def get_server_name(self):
        return self.real_server_name or ""

    def data_received(self, data):
        #print("FROM SERVER: {}".format(line))
        event = IrcParser.unpack_data(data)
        print(event.command, event.source, event.arguments)
        setattr(event, "name", event.command.lower())
        self.notify_listeners(event)

    def _handle_message(self, arguments, command, source, tags):
        target, msg = arguments[:2]
        messages = ctcp.dequote(msg)
        if command == "privmsg":
            if is_channel(target):
                command = "pubmsg"
        else:
            if is_channel(target):
                command = "pubnotice"
            else:
                command = "privnotice"
        for m in messages:
            if isinstance(m, tuple):
                if command in ["privmsg", "pubmsg"]:
                    command = "ctcp"
                else:
                    command = "ctcpreply"

                m = list(m)
                print("command: {}, source: {}, target: {}, "
                          "arguments: {}, tags: {}".format(command, source, target, m, tags))
                if command == "ctcp" and m[0] == "ACTION":
                    pass
            else:
                print("command: {}, source: {}, target: {}, "
                          "arguments: {}, tags: {}".format(command, source, target, [m], tags))


    def _handle_other(self, arguments, command, source, tags):
        target = None
        if command == "quit":
            arguments = [arguments[0]]
        elif command == "ping":
            target = arguments[0]
        else:
            target = arguments[0] if arguments else None
            arguments = arguments[1:]
        if command == "mode":
            if not is_channel(target):
                command = "umode"
        print("command: {}, source: {}, target: {}, "
                  "arguments: {}, tags: {}".format(command, source, target, arguments, tags))

    def is_connected(self):
        return self.connected

    def action(self, target, action):
        self.ctcp("ACTION", target, action)

    def admin(self, server=""):
        self.send("ADMIN", [server])

    def cap(self, subcommand, *args):
        """
        Send a CAP command according to `the spec
        <http://ircv3.atheme.org/specification/capability-negotiation-3.1>`_.

        Arguments:

            subcommand -- LS, LIST, REQ, ACK, CLEAR, END
            args -- capabilities, if required for given subcommand

        Example:

            .cap('LS')
            .cap('REQ', 'multi-prefix', 'sasl')
            .cap('END')
        """
        cap_subcommands = set('LS LIST REQ ACK NAK CLEAR END'.split())
        client_subcommands = set(cap_subcommands) - set('NAK')
        assert subcommand in client_subcommands, "invalid subcommand"

        def _multi_parameter(args):
            """
            According to the spec::

                If more than one capability is named, the RFC1459 designated
                sentinel (:) for a multi-parameter argument must be present.

            It's not obvious where the sentinel should be present or if it
            must be omitted for a single parameter, so follow convention and
            only include the sentinel prefixed to the first parameter if more
            than one parameter is present.
            """
            if len(args) > 1:
                return (':' + args[0],) + args[1:]
            return args

        args = _multi_parameter(args)
        self.send_raw(' '.join(('CAP', subcommand) + args))

    def ctcp(self, ctcptype, target, parameter=""):
        """Send a CTCP command."""
        ctcptype = ctcptype.upper()
        tmpl = (
            "\001{ctcptype} {parameter}\001" if parameter else
            "\001{ctcptype}\001"
        )
        self.privmsg(target, tmpl.format(**vars()))

    def ctcp_reply(self, target, parameter):
        """Send a CTCP REPLY command."""
        self.notice(target, "\001{}\001".format(parameter))

    def disconnect(self, msg=""):
        if not self.connected:
            return

        self.connected = False

        self.quit(msg)

    def connection_lost(self, exc):
        print("Connection lost")
        loop.stop()

    def globops(self, text):
        self.send("GLOBOPS", sentence=text)

    def info(self, server=""):
        self.send("INFO", [server])

    def invite(self, nick, channel):
        self.send("INVITE", [nick, channel])

    def ison(self, nicks):
        self.send("ISON", nicks)

    def join(self, channel, key=""):
        self.send("JOIN", [channel, key])

    def kick(self, channel, nick, comment=None):
        self.send("KICK ", [channel, nick], sentence=comment)

    def links(self, remote_server="", server_mask=""):
        self.send("LINKS", [remote_server, server_mask])

    def list(self, channels=None, server=""):
        channel_string = ",".join(always_iterable(channels))

        self.send("LIST", [channel_string, server])

    def lusers(self, server=""):
        self.send("LUSERS", [server])

    def mode(self, target, command):
        self.send("MODE", [target, command])

    def motd(self, server=""):
        self.send("MOTD", [server])

    def names(self, channels=None):
        channel_string = ','.join(always_iterable(channels))
        self.send("NAMES", [channel_string])

    def nick(self, newnick):
        self.send("NICK", [newnick])

    def notice(self, target, text):
        # Should limit len(text) here!
        self.send("NOTICE", [target, text])

    def oper(self, nick, password):
        self.send("OPER", [nick, password])

    def part(self, channels, reason=""):
        channel_string = ",".join(always_iterable(channels))
        self.send("PART", [channel_string, reason])

    def pass_(self, password):
        self.send("PASS", [password])

    def ping(self, target, target2=""):
        self.send("PING", [target, target2])

    def pong(self, target, target2=""):
        self.send("PONG", [target, target2])

    def privmsg(self, target, text):
        self.send("PRIVMSG", [target, text])

    def quit(self, reason=None):
        # Note that many IRC servers don't use your QUIT reason
        # unless you've been connected for at least 5 minutes!
        self.send("QUIT", sentence=reason)

    def send(self, command, arguments=None, tags=None, sentence=None):
        print("TO SERVER: ", command, arguments, tags, sentence)
        message = IrcParser.pack_data(command, arguments, tags, sentence)
        self.send_raw(message)

    def squit(self, server, comment=None):
        self.send("SQUIT " , [server], sentence=comment)

    def stats(self, statstype, server=""):
        self.send("STATS ", [statstype, server])

    def time(self, server=""):
        self.send("TIME", [server])

    def topic(self, channel, new_topic=None):
        self.send("TOPIC", [channel], sentence=new_topic)

    def trace(self, target=""):
        self.send("TRACE", [target])

    def user(self, username, realname):
        self.send("USER", [username, "0", "*"], sentence=realname)

    def userhost(self, nicks):
        self.send("USERHOST", [",".join(nicks)])

    def users(self, server=""):
        self.send("USERS", [server])

    def version(self, server=""):
        self.send("VERSION", [server])

    def wallops(self, text):
        self.send("WALLOPS", sentence=text)

    def who(self, target="", op=False):
        arguments = [target]
        if op:
            arguments.append("o")
        self.send("WHO", arguments)

    def whois(self, targets):
        self.send("WHOIS", ",".join(always_iterable(targets)))

    def whowas(self, nick, maximum="", server=""):
        self.send("WHOWAS", [nick, maximum, server])

loop = asyncio.get_event_loop()
