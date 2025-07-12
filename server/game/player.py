from server.models import User

class Player(User):
	def __init__(self, user: User, position):
		super().__init__(**user.__dict__)
		self.score = 0
		self.position = position
