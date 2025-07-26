import pygame
import pygame_gui
from pages.page_base import PageBase
from game.game import Game


class GamePage(PageBase):
    def __init__(self, window, manager, sio, app, switch_page_callback):
        super().__init__(window, manager, sio, app, switch_page_callback)
        self.game = None
        self.tile_size = 20  # Adjust tile size as needed

    def setup_ui(self, game_data):
        self.load_game(game_data)

        new_width = len(self.game.map[0]) * self.tile_size
        new_height = len(self.game.map) * self.tile_size

        print('ran 1')

        self.app.recreate_window(new_width, new_height)

        print('ran 2')

        self.listen_for_events()

    def listen_for_events(self):
        # self.sio.on('user_left', self.on_user_left)
        # self.sio.on('room_deleted', self.on_room_deleted)
        self.sio.on('game_state', self.update_game_state)

    def update_game_state(self, game_state):
        self.game.game_id = game_state["game_id"]
        self.game.map = game_state["map"]

        self.game.p1 = game_state["p1"]["position"]
        self.game.p2 = game_state["p2"]["position"]

        self.game.p1_dir = game_state["p1"]["direction"]
        self.game.p2_dir = game_state["p2"]["direction"]

        self.game.p1_next_dir = game_state["p1"]["next_direction"]
        self.game.p2_next_dir = game_state["p2"]["next_direction"]

        self.game.p1_type = game_state["p1"]["type"]
        self.game.p2_type = game_state["p2"]["type"]

        self.game.ghosts = [ghost["position"] for ghost in game_state.get("ghosts", [])]


    def load_game(self, data: dict):
        me = self.app.get_user_number()
        if (not me): me = '1'
        print(data)
        self.game = Game(
            data["game_id"],
            data["p1"]['position'],
            data["p2"]['position'],
            data["map"],
            me
        )

    def change_dir(self, direction):
        me = self.app.get_user_number()
        if (not me): return
        self.sio.emit("change_dir", {"game_id": self.game.game_id, "direction": direction, "user": me})

    def process_events(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.back_button:
                    self.switch_page("main_menu")
        
        # handle move events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.change_dir('up')
            elif event.key == pygame.K_DOWN:
                self.change_dir('down')
            elif event.key == pygame.K_LEFT:
                self.change_dir('left')
            elif event.key == pygame.K_RIGHT:
                self.change_dir('right')

    
        self.manager.process_events(event)

    def update(self, time_delta):
        self.manager.update(time_delta)

    def render(self):
        self.window.fill((0, 0, 0))

        if self.game:
            self.draw_map()
            self.draw_players()

        self.manager.draw_ui(self.window)
        pygame.display.update()

    def draw_map(self):
        colors = {
            "#": (200, 200, 200),  # Wall
        }

        for y, row in enumerate(self.game.map):
            for x, tile in enumerate(row):
                rect = pygame.Rect(
                    x * self.tile_size,
                    y * self.tile_size,
                    self.tile_size,
                    self.tile_size
                )
                center = (
                    x * self.tile_size + self.tile_size // 2,
                    y * self.tile_size + self.tile_size // 2
                )
                pygame.draw.rect(self.window, colors.get(tile, (0, 0, 0)), rect)
                if (tile == '.'):
                    pygame.draw.circle(self.window, (50, 50, 50), center, 2)
                if (tile == 'O'):
                    pygame.draw.circle(self.window, (255, 255, 0), center, 4)

    def draw_players(self):
        # Get the exact pixel positions
        p1_x, p1_y = self.game.p1
        p2_x, p2_y = self.game.p2

        # Draw player 1 (blue)
        pygame.draw.circle(
            self.window,
            (0, 0, 255) if self.game.p1_type == 'player' else (0, 255, 255),
            (
                int(p1_x + self.tile_size // 2),
                int(p1_y + self.tile_size // 2)
            ),
            self.tile_size // 2
        )

        # Draw player 2 (red)
        pygame.draw.circle(
            self.window,
            (255, 0, 0) if self.game.p2_type == 'player' else (0, 255, 255),
            (
                int(p2_x + self.tile_size // 2), 
                int(p2_y + self.tile_size // 2)
            ),
            self.tile_size // 2
        )

        for ghost in self.game.ghosts:
            x, y = ghost
            pygame.draw.rect(self.window, (255, 0, 0), (x, y, self.tile_size, self.tile_size))



