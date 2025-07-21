from models.user import User
from game.game import Game

class Room:
    rooms: dict[str, "Room"] = {}

    def __init__(self, game_id, user1: User):
        self.game_id = game_id
        self.user1 = user1
        self.user2 = None
        self.game_state = 'waiting'
        self.game = None  # <--- Game instance
        Room.rooms[game_id] = self

    def is_ready(self):
        return self.user1 is not None and self.user2 is not None

    def start_game(self):
        if not self.is_ready():
            raise Exception("Both players are not connected.")
        
        self.game = Game(self.game_id, self.user1, self.user2)
        self.game_state = 'running'
        return self.game

    def to_dict(self):
        return {
            "room_id": self.game_id,
            "user1": self.user1.to_dict() if self.user1 else None,
            "user2": self.user2.to_dict() if self.user2 else None,
            "game_state": self.game_state,
            "game": self.game.get_state() if self.game else None
        }
