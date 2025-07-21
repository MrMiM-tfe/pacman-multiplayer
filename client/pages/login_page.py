import pygame
import pygame_gui
import threading
from pages.page_base import PageBase
import time
# from main import MainApp

class LoginPage(PageBase):
    def __init__(self, window, manager, sio, app: "MainApp", switch_page_callback):
        super().__init__(window, manager, sio, app, switch_page_callback)
        self.login_result = None

    def setup_ui(self):
        # Create a panel to hold the elements
        panel_width, panel_height = self.window.get_size()
        panel_x = (self.window.get_width() - panel_width) // 2
        panel_y = (self.window.get_height() - panel_height) // 2

        self.panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((panel_x, panel_y), (panel_width, panel_height)),
            manager=self.manager
        )

        # Auto layout parameters
        padding = 10
        input_height = 30
        label_height = 25
        current_y = padding

        # Username Label
        self.username_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, current_y), (panel_width, label_height)),
            text="Username:", manager=self.manager, container=self.panel)
        current_y += label_height + padding

        # Username Input
        self.username_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((0, current_y), (panel_width, input_height)),
            manager=self.manager, container=self.panel)
        current_y += input_height + padding

        # Password Label
        self.password_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, current_y), (panel_width, label_height)),
            text="Password:", manager=self.manager, container=self.panel)
        current_y += label_height + padding

        self.password = ""

        # Password Input
        self.password_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((0, current_y), (panel_width, input_height)),
            manager=self.manager, container=self.panel)
        self.password_input.set_text("")
        
        current_y += input_height + padding

        # Login/Register Button
        self.login_register_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, current_y), (panel_width, 40)),
            text='Login/Register', manager=self.manager, container=self.panel)
        current_y += 40 + padding

        # Message Label
        self.login_message = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, current_y), (panel_width, 30)),
            text="", manager=self.manager, container=self.panel)


    def register_handlers(self):
        pass

    def authenticate(self, username, password):
        self.sio.emit("authenticate", {"username": username, "password": password}, callback=self.on_authentication)

    def on_authentication(self, data):
        if (data['status'] == 'success'):
            self.app.token = data['data']['token']
            self.login_result = f"Welcome {data['data']['username']}"
            # time.sleep(1)
            self.switch_page("main_menu")
        else:
            self.login_result = f"{data['error']}"

    def process_events(self, event):
        if event.type == pygame.QUIT:
            self.running = False

        # replace password chars with *
        if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
            if event.ui_element == self.password_input:
                password = self.password_input.get_text()
                delta = len(password) - len(self.password)
                if delta > 0:
                    self.password += password[-delta:]
                elif delta < 0:
                    self.password = self.password[:delta]

                print(self.password)

                self.password_input.set_text("*" * len(self.password))


        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.login_register_button:
            username = self.username_input.get_text().strip()
            password = self.password

            if not username or not password:
                self.login_result = "Username and password cannot be empty."
                return

            self.login_message.set_text("Processing...")
            threading.Thread(target=self.authenticate, args=(username, password), daemon=True).start()

        self.manager.process_events(event)
    
    def update(self, time_delta):
        self.manager.update(time_delta)

    def render(self):
        if self.login_result:
            self.login_message.set_text(self.login_result)
            self.login_result = None

        self.window.fill((0, 0, 0))
        self.manager.draw_ui(self.window)
        pygame.display.update()
