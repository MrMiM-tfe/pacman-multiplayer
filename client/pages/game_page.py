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

        # panel_width, panel_height = self.window.get_size()
        # panel_x = (self.window.get_width() - panel_width) // 2
        # panel_y = (self.window.get_height() - panel_height) // 2

        # self.panel = pygame_gui.elements.UIPanel(
        #     relative_rect=pygame.Rect((panel_x, panel_y), (panel_width, panel_height)),
        #     manager=self.manager
        # )

        # # You could add a "Back" button for development/testing
        # self.back_button = pygame_gui.elements.UIButton(
        #     relative_rect=pygame.Rect((10, 10), (100, 30)),
        #     text="Back",
        #     manager=self.manager,
        #     container=self.panel
        # )

        self.window_width = len(self.game.map[0]) * self.tile_size
        self.window_height = len(self.game.map) * self.tile_size

        # Resize the Pygame window
        self.window = pygame.display.set_mode((self.window_width, self.window_height))

    def load_game(self, data: dict):
        self.game = Game(
            data["game_id"],
            data["p1"],
            data["p2"],
            data["map"]
        )

    def process_events(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.back_button:
                    self.switch_page("main_menu")
        
        # handle move events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.game.change_dir('up')
            elif event.key == pygame.K_DOWN:
                self.game.change_dir('down')
            elif event.key == pygame.K_LEFT:
                self.game.change_dir('left')
            elif event.key == pygame.K_RIGHT:
                self.game.change_dir('right')

    
        self.manager.process_events(event)

    def update(self, time_delta):
        self.manager.update(time_delta)

    def render(self):
        self.window.fill((0, 0, 0))

        if self.game:
            self.game.move()
            self.draw_map()
            self.draw_players()

        self.manager.draw_ui(self.window)
        pygame.display.update()

    def draw_map(self):
        colors = {
            "#": (200, 200, 200),  # Wall
            ".": (50, 50, 50),     # Dot path
            "O": (255, 255, 0),    # Power pellet
            " ": (0, 0, 0)         # Empty
        }

        for y, row in enumerate(self.game.map):
            for x, tile in enumerate(row):
                rect = pygame.Rect(
                    x * self.tile_size,
                    y * self.tile_size,
                    self.tile_size,
                    self.tile_size
                )
                pygame.draw.rect(self.window, colors.get(tile, (0, 0, 0)), rect)

    def draw_players(self):
        # Get the exact pixel positions
        p1_x, p1_y = self.game.p1
        p2_x, p2_y = self.game.p2

        # Draw player 1 (blue)
        pygame.draw.circle(
            self.window,
            (0, 0, 255),
            (
                int(p1_x + self.tile_size // 2),  # Already in pixels
                int(p1_y + self.tile_size // 2)
            ),
            self.tile_size // 2
        )

        # Draw player 2 (red)
        pygame.draw.circle(
            self.window,
            (255, 0, 0),
            (
                int(p2_x + self.tile_size // 2),  # Already in pixels
                int(p2_y + self.tile_size // 2)
            ),
            self.tile_size // 2
        )


