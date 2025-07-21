import inspect
from libs.decorators import get_registered_gateways
from models import User

class ConnectionHandler:
    connected_clients: dict[str, User] = {}

    def __init__(self, sio):
        self.sio = sio
        self.disconnect_handlers = []
        self.gateways = [gateway_cls(sio, self.connected_clients) for gateway_cls in get_registered_gateways()]
        print(f"Registered gateways: {len(self.gateways)}")
        self.register_handlers()

    def register_handlers(self):
        for gateway in self.gateways:
            for _, method in inspect.getmembers(gateway, predicate=inspect.ismethod):
                event_name = getattr(method, "_socket_event", None)
                if event_name:
                    if event_name == "disconnect":
                        self.disconnect_handlers.append(method)
                        print(f"Registered disconnect handler for {gateway.__class__.__name__}")
                    else:
                        self.sio.on(event_name, method)
                        print(f"Registered handler: {gateway.__class__.__name__} -> '{event_name}'")

        self.sio.on("connect", self.on_connect)
        self.sio.on("disconnect", self.on_disconnect)

    def on_connect(self, sid, environ):
        print(f"Client connected: {sid}")

    def on_disconnect(self, sid):
        print(f"Client disconnected: {sid}")
        for handler in self.disconnect_handlers:
            handler(sid)
            
        if sid in self.connected_clients:
            del self.connected_clients[sid]


