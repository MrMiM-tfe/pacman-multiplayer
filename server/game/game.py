import threading
import time
from game.map import MAP_LAYOUT, PLAYER_1_POSITION, PLAYER_2_POSITION
from game.player import Player
from models import User

SPEED = 2 

class Game:
    def __init__(self, game_id, user1: User, user2: User, sio):
        self.game_id = game_id
        self.tile_size = 20
        self.map = MAP_LAYOUT
        self.is_running = False
        self.sio = sio

        # Set initial player positions (in pixels)
        self.p1 = Player(user1, self._to_pixel_position(PLAYER_1_POSITION))
        self.p2 = Player(user2, self._to_pixel_position(PLAYER_2_POSITION))

    def _to_pixel_position(self, tile_pos: tuple[int, int]) -> list[int]:
        x, y = tile_pos
        return [
            x * self.tile_size,
            y * self.tile_size,
        ]

    def get_state(self):
        return {
            "game_id": self.game_id,
            "p1": self.p1.to_dict(),
            "p2": self.p2.to_dict(),
            "map": self.map,
        }

    def is_wall_tile(self, tile_x, tile_y):
        # Check if the player is attempting to move into a wall
        if 0 <= tile_y < len(self.map) and 0 <= tile_x < len(self.map[0]):
            return self.map[tile_y][tile_x] == '#'
        return True  # Default to wall if out of bounds

    def get_tile_coords(self, pos):
        # Convert pixel position to tile coordinates
        return int(pos[0] // self.tile_size), int(pos[1] // self.tile_size)

    def is_center_of_tile(self, pos):
        # Check if the player is in the center of the tile
        return int(pos[0]) % self.tile_size == 0 and int(pos[1]) % self.tile_size == 0

    def can_move(self, pos, direction):
        # Check if the player can move in the given direction
        dx, dy = 0, 0
        if direction == 'up': dy = -1
        elif direction == 'down': dy = 1
        elif direction == 'left': dx = -1
        elif direction == 'right': dx = 1
        
        tile_x, tile_y = self.get_tile_coords(pos)
        next_tile_x = tile_x + dx
        next_tile_y = tile_y + dy
        
        return not self.is_wall_tile(next_tile_x, next_tile_y)

    def update_player(self, pos, direction, next_direction):
        # If the player is at the center of a tile, update direction and move
        if self.is_center_of_tile(pos):
            if next_direction and self.can_move(pos, next_direction):
                direction = next_direction

            if not self.can_move(pos, direction):
                return pos, None, next_direction  # Stop moving if wall detected

        dx, dy = 0, 0
        if direction == 'up': dy = -SPEED
        elif direction == 'down': dy = SPEED
        elif direction == 'left': dx = -SPEED
        elif direction == 'right': dx = SPEED

        pos[0] += dx
        pos[1] += dy
        return pos, direction, next_direction

    def move(self):
        # Update both players' positions based on their directions
        self.p1.position, self.p1.direction, self.p1.next_direction = self.update_player(
            self.p1.position, self.p1.direction, self.p1.next_direction
        )
        self.p2.position, self.p2.direction, self.p2.next_direction = self.update_player(
            self.p2.position, self.p2.direction, self.p2.next_direction
        )

    def change_dir(self, player, direction):
        if player == '1':
            self.p1.next_direction = direction
        else:
            self.p2.next_direction = direction

        self.broadcast_game_state()

    def run(self):
        self.is_running = True
        game_thread = threading.Thread(target=self.game_loop)
        game_thread.daemon = True  
        game_thread.start()

        # broadcast_thread = threading.Thread(target=self.broadcast_game_state_interval)
        # broadcast_thread.daemon = True
        # broadcast_thread.start()

    def game_loop(self):
        while self.is_running:
            self.move()
            self.sio.emit("game_state", self.get_state(), to=self.game_id)
            time.sleep(1 / 60)  # 60 FPS

    def broadcast_game_state_interval(self):
        while self.is_running:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
            time.sleep(1 / 60)

    def broadcast_game_state(self):
        # self.sio.emit("game_state", self.get_state(), to=self.game_id)
        pass

