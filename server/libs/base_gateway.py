from models.user import User

class BaseGateway:
    def __init__(self, sio, connected_clients: dict[str, User]):
        self.sio = sio
        self.connected_clients = connected_clients

    def get_user(self, sid):
        return self.connected_clients.get(sid)