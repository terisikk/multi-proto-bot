import asyncio


class ChatProtocol(asyncio.Protocol):
    def __init__(self):
        self.transport = None
        self.listeners = []

    def send_raw(self, message):
        self._check_transport_status()

        try:
            self.transport.write(message)
        except asyncio.TimeoutError:
            self.transport.close()

    def register_event_listener(self, listener):
        if listener not in self.listeners:
            self.listeners.append(listener)

    def notify_listeners(self, event):
        for listener in self.listeners:
            handler = getattr(listener, "on_protocol_event", None)
            if handler:
                handler(event)

    def _check_transport_status(self):
        if self.transport is None:
            raise asyncio.InvalidStateError("Not connected.")
