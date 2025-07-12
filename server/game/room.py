from models.user import User

class Room:
    rooms: dict[str, "Room"] = {}
    def __init__(self, game_id, user1: User):
        self.game_id = game_id
        self.user1 = user1
        self.user2 = None
        self.game_stated = 'waiting'
        Room.rooms[game_id] = self

    def start_game(self):
        pass
