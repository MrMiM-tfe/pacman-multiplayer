import threading
import time
TILE_SIZE = 20
SPEED = 3

class Game:
    def __init__(self, game_id, p1_tile, p2_tile, map_layout: list[str], me):
        self.game_id = game_id
        self.TILE_SIZE = 20
        self.map = map_layout
        self.me = me
        self.speed = SPEED
        self.is_running=True

        self.p1 = [p1_tile[0] , p1_tile[1] ]
        self.p2 = [p2_tile[0] , p2_tile[1] ]
        
        self.p1_dir = None
        self.p2_dir = None
        self.p1_next_dir = None
        self.p2_next_dir = None

    def is_wall_tile(self, tile_x, tile_y):
        if 0 <= tile_y < len(self.map) and 0 <= tile_x < len(self.map[0]):
            return self.map[tile_y][tile_x] == '#'
        return True

    def is_center_of_tile(self, pos):
        return int(pos[0]) % TILE_SIZE == 0 and int(pos[1]) % TILE_SIZE == 0

    def get_tile_coords(self, pos):
        return int(pos[0] // TILE_SIZE), int(pos[1] // TILE_SIZE)

    def can_move(self, pos, direction):
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
        if self.is_center_of_tile(pos):
            if next_direction and self.can_move(pos, next_direction):
                direction = next_direction

            if not self.can_move(pos, direction):
                return pos, None, next_direction  # Stop moving

        dx, dy = 0, 0
        if direction == 'up': dy = -SPEED
        elif direction == 'down': dy = SPEED
        elif direction == 'left': dx = -SPEED
        elif direction == 'right': dx = SPEED

        pos[0] += dx
        pos[1] += dy
        return pos, direction, next_direction

    def move(self):
        self.p1, self.p1_dir, self.p1_next_dir = self.update_player(
            self.p1, self.p1_dir, self.p1_next_dir
        )
        self.p2, self.p2_dir, self.p2_next_dir = self.update_player(
            self.p2, self.p2_dir, self.p2_next_dir
        )

    def run(self):
        self.is_running = True
        game_thread = threading.Thread(target=self.game_loop)
        game_thread.daemon = True  
        game_thread.start()

    def game_loop(self):
        while self.is_running:
            self.move()
            time.sleep(1 / 45)

    def change_dir(self, direction):
        if self.me == '1':
            self.p1_next_dir = direction
        else:
            self.p2_next_dir = direction
