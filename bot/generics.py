import time


class GenericEvent(object):
    def __init__(self, client, original):
        self.name = self.__class__.__name__.lower()
        self.timestamp = time.time()
        self.client = client
        self.original_event = original


class PublicMessage(GenericEvent):
    def __init__(self, client, original, text, user, channel=None):
        super().__init__(self, client, original)
        self.text = text
        self.user = user
        self.channel = channel
