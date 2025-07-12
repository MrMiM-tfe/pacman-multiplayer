from game.map import MAP_LAYOUT, PLAYER_1_POSITION, PLAYER_2_POSITION
from game.player import Player
from models import User

class Game:
	def __init__(self, game_id, user1: User, user2: User):
		self.game_id = game_id
		self.player1 = Player(user1, PLAYER_1_POSITION)
		self.player2 = Player(user2, PLAYER_2_POSITION)
		self.map = MAP_LAYOUT

	def get_state(self):
		return {
			"game_id": self.game_id,
			"p1": self.player1.position,
			"p2": self.player2.position,
			"map": self.map
		}
	
