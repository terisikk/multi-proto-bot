from irc import events
from irc.client import always_iterable


def command_from_string(string):
    command = string.lower()
    # Translate numerics into more readable strings.
    return events.numeric.get(command, command)


TAG_REPLACES = {
    "\\:": ";",
    "\\s": " ",
    "\\n": "\n",
    "\\r": "\r",
    "\\\\": "\\",
    }


def tags_from_string(string):
    tag_items = string.split(";")
    return list(map(parse_tag, tag_items))


def tags_to_string(tagdict):
    string = ""
    for key, value in tagdict.items():
        string += key + "=" + value + ";"

    for new, old in TAG_REPLACES.items():
        string = string.replace(old, new)

    return string


def parse_tag(item):
    key, sep, value = item.partition('=')

    for old, new in TAG_REPLACES.items():
        value = value.replace(old, new)

    value = value or None
    return {
        'key': key,
        'value': value,
    }


def arguments_from_string(string):
    main, sep, ext = string.partition(" :")
    arguments = main.split()
    if sep:
        arguments.append(ext)

    return arguments


def arguments_to_string(arguments, sentence=None):
    string = " ".join(always_iterable(arguments))
    if sentence:
        if arguments:
            string += " "
        string += ":" + sentence
    return string
