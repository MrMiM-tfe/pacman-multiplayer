from pages.page_base import PageBase
# from main import MainApp
import pygame
import pygame_gui
import sqlalchemy

class MainMenuPage(PageBase):
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
        button_height = 30
        label_height = 25
        current_y = padding

        # Welcome Label
        self.welcome_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, current_y), (panel_width, label_height)),
            text="Welcome to the Pacman Multiplayer!", manager=self.manager, container=self.panel)
        current_y += label_height + padding
        

        # Create Room Button
        self.create_room_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, current_y), (panel_width, button_height)),
            text="Create Room", manager=self.manager, container=self.panel)
        
        current_y += button_height + padding

        # Join Room Id Label
        self.join_room_id_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, current_y), (panel_width, label_height)),
            text="Room ID:", manager=self.manager, container=self.panel)
        
        current_y += label_height + padding

        # Join Room Id Input
        self.join_room_id_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((0, current_y), (panel_width, button_height)),
            manager=self.manager, container=self.panel)
        current_y += button_height + padding

        # Join Room Button
        self.join_room_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, current_y), (panel_width, button_height)),
            text="Join Room", manager=self.manager, container=self.panel)
        current_y += button_height + padding

        # Join Room Error Label
        self.join_room_error_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, current_y), (panel_width, label_height)),
            text="", manager=self.manager, container=self.panel)
        
        current_y += label_height + padding
        
        # Username Label
        self.username_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, current_y), (panel_width, label_height)),
            text="Username:", manager=self.manager, container=self.panel)
        current_y += label_height + padding

        # Your Score Label
        self.your_score_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, current_y), (panel_width, label_height)),
            text="Your Score: 0", manager=self.manager, container=self.panel)
        

    def process_events(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.create_room_button:
                self.create_room()
            elif event.ui_element == self.join_room_button:
                self.join_room()

        self.manager.process_events(event)

    def join_room(self):
        print("Joining room...")
        room_id = self.join_room_id_input.get_text()
        self.sio.emit('join_room', room_id, callback=self.on_room_joined)

    def on_room_joined(self, data):
        # print("Joined room:", data)
        if data['status'] == 'success':
            self.app.current_room = data['data']
            self.switch_page("room")
        else:
            self.join_room_error_label.set_text(data['error'])

    def create_room(self):
        self.sio.emit('create_room', callback=self.on_room_created)

    def on_room_created(self, data):
        print(data)
        if data['status'] == 'success':
            self.app.current_room = data['data']
            self.switch_page("room")
        else:
            self.join_room_error_label.set_text(data['error'])

    def update(self, time_delta):
        self.manager.update(time_delta)

    def render(self):
        self.window.fill((0, 0, 0))
        self.manager.draw_ui(self.window)
        pygame.display.update()