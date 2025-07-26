from models import User
from game.map import MAP_LAYOUT

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
        
    def update_type(self, player):
        tile_x = int(self.position[0] // 20)
        mid_x = len(MAP_LAYOUT[0]) // 2

        if tile_x < mid_x:
            self.type = 'player' if player == '1' else 'ghost'
        else:
            self.type = 'ghost' if player == '1' else 'player'

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
