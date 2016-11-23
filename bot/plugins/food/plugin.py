import json
import requests

ACTIVATOR = "!food"


def event_filter(client_type):
    def wrap(f):
        def wrapped_f(self, message):
            if message.client and message.client == "generic":
                f(self, message)

        return wrapped_f
    return wrap

class FoodPlugin(object):
    def __init__(self):
        pass

    @event_filter("generic")
    def on_publicmessage(self, message):
        print("HERE")
        print(message.message.message)
        if message.message.message == ACTIVATOR:
            print(self.get_food())

    def get_food(self):
        return "Ass burgers :D"
