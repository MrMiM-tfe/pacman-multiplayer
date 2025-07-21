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

    def to_dict(self):
        return {
            "room_id": self.game_id,
            "user1": self.user1.to_dict() if self.user1 else None,
            "user2": self.user2.to_dict() if self.user2 else None,
            "game_state": self.game_stated
        }
