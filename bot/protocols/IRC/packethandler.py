import re
from irc.client import MessageTooLong
from . import commands


def pack_data(command):
    msg = command.to_outgoing_message()
    return _prepare_message(msg)


def unpack_data(data):
    # UNICODE :D JA ISO-8859-15 :D
    # data = data.decode("ISO-8859-15")
    return commands.from_server_message(data)


def _prepare_message(msg):
    msg = _remove_line_endings(msg)

    sendbytes = msg.encode('utf-8') + b'\r\n'
    _raise_error_if_message_too_long(sendbytes)
    return sendbytes


def _remove_line_endings(msg):
    msg = re.sub(r"[\n\r]", "", msg)
    return msg


def _raise_error_if_message_too_long(sendbytes):
    # According to the RFC http://tools.ietf.org/html/rfc2812#page-6,
    # clients should not transmit more than 512 bytes.
    if len(sendbytes) > 512:
        # TODO: another 512 for tags
        error = "Messages limited to 512 bytes including CR/LF"
        raise MessageTooLong(error)
