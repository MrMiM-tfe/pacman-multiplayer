import random

class Ghost:
    def __init__(self, position, region='left'):
        self.position = position  # pixel position [x, y]
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.region = region  # 'left' or 'right'

    def to_dict(self):
        return {
            "position": self.position,
            "direction": self.direction,
            "region": self.region
        }
