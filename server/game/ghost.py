import random

class Ghost:
    def __init__(self, position, region='left'):
        self.position = position
        self.direction = None
        self.next_direction = random.choice(['up','down','left','right'])
        self.region = region

    def to_dict(self):
        return {
            "position": self.position,
            "direction": self.direction,
            "next_direction": self.next_direction,
            "region": self.region
        }
