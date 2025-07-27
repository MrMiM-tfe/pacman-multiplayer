import threading
import random
import time
from game.map import MAP_LAYOUT, PLAYER_1_POSITION, PLAYER_2_POSITION
from game.player import Player
from models import User
from game.ghost import Ghost
from db.database import SessionLocal

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

        self.ghosts = [
            Ghost(self._to_pixel_position((1, 11)), region='left'),
            Ghost(self._to_pixel_position((3, 13)), region='left'),
            Ghost(self._to_pixel_position((38, 11)), region='right'),
            Ghost(self._to_pixel_position((40, 13)), region='right'),
        ]

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
            "ghosts": [ghost.to_dict() for ghost in self.ghosts]
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

        self.p1.update_type('1')
        self.p2.update_type('2')
        
        if self.check_collision(self.p1.position, self.p2.position):
            if self.p1.type == 'ghost' and self.p2.type == 'player':
                self.kill_player(self.p2, self.p1) 
            elif self.p2.type == 'ghost' and self.p1.type == 'player':
                self.kill_player(self.p1, self.p2)

    def kill_player(self, p: Player, winner_p: Player):
        p.is_dead = True
        p.is_winner = False

        winner_p.is_winner = True
        self.is_running = False

        self.broadcast_game_state()
        db = SessionLocal()
        user = db.query(User).filter(User.id == winner_p.user.id).first()

        user.score += 1
        db.commit()
        db.refresh(user)

        winner_p.user.score += 1

        self.sio.emit('end_game', {'winner': winner_p.user.to_dict()}, to=self.game_id)

    def change_dir(self, player, direction):
        if player == '1':
            self.p1.next_direction = direction
        else:
            self.p2.next_direction = direction

    def move_ghosts(self):
        for ghost in self.ghosts:
            if self.is_center_of_tile(ghost.position):
                possible_directions = ['up', 'down', 'left', 'right']
                random.shuffle(possible_directions)

                # Constrain direction based on region
                ghost_tile_x, _ = self.get_tile_coords(ghost.position)
                if ghost.region == 'left' and ghost_tile_x > len(self.map[0]) // 2:
                    continue  # skip moving out of left half
                elif ghost.region == 'right' and ghost_tile_x < len(self.map[0]) // 2:
                    continue  # skip moving out of right half

                for direction in possible_directions:
                    if self.can_move(ghost.position, direction):
                        ghost.direction = direction
                        break  # pick first valid random direction

            # Move ghost
            dx, dy = 0, 0
            if ghost.direction == 'up': dy = -SPEED
            elif ghost.direction == 'down': dy = SPEED
            elif ghost.direction == 'left': dx = -SPEED
            elif ghost.direction == 'right': dx = SPEED

            ghost.position[0] += dx
            ghost.position[1] += dy

            if self.check_collision(self.p1.position, ghost.position) and self.p1.type == 'player':
                self.re_spawn('1')

            if self.check_collision(self.p2.position, ghost.position) and self.p2.type == 'player':
                self.re_spawn('2')


    def check_collision(self, player_pos, ghost_pos):
        dx = player_pos[0] - ghost_pos[0]
        dy = player_pos[1] - ghost_pos[1]
        distance_squared = dx * dx + dy * dy
        return distance_squared <= self.tile_size * self.tile_size


    
    def re_spawn(self, player_number):
        if player_number == '1':
            self.p1.position = self._to_pixel_position(PLAYER_1_POSITION)  # Reset to start
        elif player_number == '2':
            self.p2.position = self._to_pixel_position(PLAYER_2_POSITION)  # Reset to start

    def run(self):
        self.is_running = True
        game_thread = threading.Thread(target=self.game_loop)
        game_thread.daemon = True  
        game_thread.start()

    def game_loop(self):
        while self.is_running:
            self.move()
            self.move_ghosts()
            self.broadcast_game_state()
            time.sleep(1 / 60)  # 60 FPS

    def broadcast_game_state(self):
        self.sio.emit("game_state", self.get_state(), to=self.game_id)


