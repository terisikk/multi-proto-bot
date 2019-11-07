ACTIVATOR = "!food"


def event_filter(client_type):
    def wrap(f):
        def wrapped_f(self, message):
            if client_type == "generic":
                f(self, message)
            else:
                f(self, message.original_event)

        return wrapped_f
    return wrap


class FoodPlugin(object):
    def __init__(self):
        pass

    @event_filter("mumble")
    def on_textmessage(self, message):
        print("HERE")
        print(message.message)
        if message.message == ACTIVATOR:
            print(self.get_food())

    @event_filter("generic")
    def on_channelstate(self, message):
        print("GENERIC: ", message.timestamp)

    def get_food(self):
        return "Hauki on kala :D"
