import argparse
import time
import pygame
import pygame_gui
import socketio
from pages.login_page import LoginPage
from pages.main_menu_page import MainMenuPage
from pages.room_page import RoomPage
from pages.game_page import GamePage
import inspect
from libs.fake_data import game_fake_data
from pages.winner_page import WinnerPage

sio = socketio.Client()

try:
    sio.connect("http://127.0.0.1:5000")
    print("🔌 Connected to server")
except Exception as e:
    print(f"❌ Could not connect to server: {e}")


class MainApp:
    def __init__(self, args):
        pygame.init()
        self.window_size = (400, 300)
        self.window = pygame.display.set_mode(self.window_size, pygame.RESIZABLE)
        self.manager = pygame_gui.UIManager(self.window_size)
        self.clock = pygame.time.Clock()
        self.pages = {}
        self.token = None
        self.user = None
        self.current_room = None
        self.current_page = None
        self._delayed_init = None  # used to reinitialize after switching

        if args.offline:
            self.initialize_pages("game", game_fake_data)
        else:
            self.initialize_pages("login")

    def get_user_number(self):
        if not self.current_room:
            return
        if self.current_room['user1']['id'] == self.user['user_id']:
            return '1'
        if self.current_room['user2']['id'] == self.user['user_id']:
            return '2'

    def initialize_pages(self, page_name, data=None):
        def switch_page(to_page, d=None):
            self.switch_page(to_page, d)

        if self.current_page and self.current_page.panel:
            self.current_page.panel.hide()

        self.pages = {
            "login": LoginPage(self.window, self.manager, sio, self, switch_page),
            "main_menu": MainMenuPage(self.window, self.manager, sio, self, switch_page),
            "room": RoomPage(self.window, self.manager, sio, self, switch_page),
            "game": GamePage(self.window, self.manager, sio, self, switch_page),
            "winner": WinnerPage(self.window, self.manager, sio, self, switch_page)
        }

        self.current_page = self.pages[page_name]
        sig = inspect.signature(self.current_page.setup_ui)
        if len(sig.parameters) > 0:
            self.current_page.setup_ui(data)
        else:
            self.current_page.setup_ui()

    def switch_page(self, page_name, data=None):
        self.current_page.running = False
        def delayed_init():
            self.initialize_pages(page_name, data)
        self._delayed_init = delayed_init

    def run(self):
        while True:
            if self._delayed_init:
                self._delayed_init()
                self._delayed_init = None

            self.current_page.running = True
            while self.current_page.running:
                time_delta = self.clock.tick(60) / 1000.0
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return

                    self.current_page.process_events(event)

                self.current_page.update(time_delta)
                self.current_page.render()

    def recreate_window(self, width, height):
        print("🪟 Recreating window...")

        self.current_page.running = False

        # Clear event queue
        pygame.event.clear()
        time.sleep(0.05)

        # Reset display
        pygame.display.quit()
        pygame.display.init()

        self.window_size = (width, height)
        self.window = pygame.display.set_mode(self.window_size, pygame.RESIZABLE)
        self.manager = pygame_gui.UIManager(self.window_size)

        # Update references
        if self.current_page:
            self.current_page.window = self.window
            self.current_page.manager = self.manager
            # if hasattr(self.current_page, "setup_ui"):
            #     self.current_page.setup_ui()

        print("✅ Window recreated successfully!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pacman Multiplayer Game")
    parser.add_argument('--offline', action='store_true', help="Run the game offline without connecting to the server")
    args = parser.parse_args()

    print(args)

    app = MainApp(args)
    app.run()
