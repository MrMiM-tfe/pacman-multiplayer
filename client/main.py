import pygame
import pygame_gui
import socketio
from pages.login_page import LoginPage
from pages.main_menu_page import MainMenuPage
from pages.room_page import RoomPage

sio = socketio.Client()

try:
    sio.connect("http://127.0.0.1:5000")
    print("🔌 Connected to server")
except Exception as e:
    print(f"❌ Could not connect to server: {e}")

class MainApp:
    def __init__(self):
        pygame.init()
        self.window_size = (400, 300)
        self.window = pygame.display.set_mode(self.window_size)
        self.manager = pygame_gui.UIManager(self.window_size)
        self.clock = pygame.time.Clock()
        self.pages = {}
        self.token = None
        self.current_room = None
        self.current_page = None

        self.initialize_pages("login")

    def initialize_pages(self, page_name):
        def switch_page(to_page):
            self.initialize_pages(to_page)
        
        if (self.current_page and self.current_page.panel):
            self.current_page.panel.hide()

        self.pages = {
            "login": LoginPage(self.window, self.manager, sio, self, switch_page),
            "main_menu": MainMenuPage(self.window, self.manager, sio, self, switch_page),
            "room": RoomPage(self.window, self.manager, sio, self, switch_page),
            # "game": GamePage(...),
        }

        if self.current_page and hasattr(self.current_page, "unlisten_for_events"):
            self.current_page.unlisten_for_events()
            
        self.current_page = self.pages[page_name]
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
    app = MainApp()
    print(app.pages["room"].app == app)
    app.run()
