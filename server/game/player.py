from models import User

class Player:
    def __init__(self, user: User, position):
        self.user = user
        self.score = 0
        self.position = position
        self.direction = None
        self.next_direction = None
        self.is_dead = False
        self.is_winner = False
        self.type = 'player' # player/ghost
        
    def to_dict(self):
        return {
            "score": self.score,
            "position": self.position,
            "direction": self.direction,
            "next_direction": self.next_direction,
            "is_dead": self.is_dead,
            "is_winner": self.is_winner,
            "type": self.type
        }
