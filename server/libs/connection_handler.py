import inspect
from server.libs.decorators import get_registered_gateways
from server.models import User

class ConnectionHandler:
    connected_clients: dict[str, User] = {}

    def __init__(self, sio):
        self.sio = sio
        self.gateways = [gateway_cls(sio, self.connected_clients) for gateway_cls in get_registered_gateways()]
        self.register_handlers()

    def register_handlers(self):
        for gateway in self.gateways:
            for _, method in inspect.getmembers(gateway, predicate=inspect.ismethod):
                event_name = getattr(method, "_socket_event", None)
                if event_name:
                    self.sio.on(event_name, method)
                    print(f"Registered handler: {gateway.__class__.__name__} -> '{event_name}'")

        self.sio.on("connect", self.on_connect)
        self.sio.on("disconnect", self.on_disconnect)

    def on_connect(self, sid, environ):
        print(f"Client connected: {sid}")

    def on_disconnect(self, sid):
        print(f"Client disconnected: {sid}")
        if sid in self.connected_clients:
            del self.connected_clients[sid]
