import argparse

import pygame
import pygame_gui
import socketio
from pages.login_page import LoginPage
from pages.main_menu_page import MainMenuPage
from pages.room_page import RoomPage
from pages.game_page import GamePage
import inspect
from libs.fake_data import game_fake_data

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
        self.window = pygame.display.set_mode(self.window_size)
        self.manager = pygame_gui.UIManager(self.window_size)
        self.clock = pygame.time.Clock()
        self.pages = {}
        self.token = None
        self.user = None
        self.current_room = None
        self.current_page = None

        if (args.offline): 
            self.initialize_pages("game", game_fake_data)
        else: 
            self.initialize_pages("login")

    def initialize_pages(self, page_name, data=None):
        def switch_page(to_page, d=None):
            self.initialize_pages(to_page, d)
        
        if (self.current_page and self.current_page.panel):
            self.current_page.panel.hide()

        self.pages = {
            "login": LoginPage(self.window, self.manager, sio, self, switch_page),
            "main_menu": MainMenuPage(self.window, self.manager, sio, self, switch_page),
            "room": RoomPage(self.window, self.manager, sio, self, switch_page),
            "game": GamePage(self.window, self.manager, sio, self, switch_page),
        }
            
        self.current_page = self.pages[page_name]
        sig = inspect.signature(self.current_page.setup_ui)
        if len(sig.parameters) > 0:
            self.current_page.setup_ui(data)
        else:
            self.current_page.setup_ui()

    def run(self):
        while self.current_page.running:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.current_page.running = False
                self.current_page.process_events(event)

            self.current_page.update(time_delta)
            self.current_page.render()

        pygame.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pacman Multiplayer Game")
    parser.add_argument('--offline', action='store_true', help="Run the game offline without connecting to the server")
    args = parser.parse_args()

    print(args)

    app = MainApp(args)
    app.run()
