from models import User

class Player:
    def __init__(self, user: User, position):
        self.user = user
        self.score = 0
        self.position = position
