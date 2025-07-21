from pages.page_base import PageBase
import pygame
import pygame_gui
import sqlalchemy

class RoomPage(PageBase):
    def __init__(self, window, manager, sio, app, switch_page):
        super().__init__(window, manager, sio, app, switch_page)

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

        if self.app.current_room:
            room_id = self.app.current_room["room_id"]
            room_id = str(room_id)
        else:
            room_id = "Failed to get Info"

        user1 = self.app.current_room["user1"] if self.app.current_room else None
        user2 = self.app.current_room["user2"] if self.app.current_room else None
        user1_name = user1["username"] if user1 else "N/A"
        user2_name = user2["username"] if user2 else "N/A"
        user1_score = str(user1["score"] if user1 else 0)
        user2_score = str(user2["score"] if user2 else 0)

        game_state = self.app.current_room["game_state"] if self.app.current_room else None
    

        # Room ID Label
        self.room_id_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, current_y), (panel_width, label_height)),
            text="Room ID:" + room_id, manager=self.manager, container=self.panel)
        current_y += label_height + padding

        # Game State Label
        self.game_state_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, current_y), (panel_width, label_height)),
            text="Game State:" + game_state, manager=self.manager, container=self.panel)
        current_y += label_height + padding

        # User 1 Label
        self.user1_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, current_y), (panel_width, label_height)),
            text="User 1:" + user1_name, manager=self.manager, container=self.panel)
        
        current_y += label_height + padding

        # User 1 Score Label
        self.user1_score_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, current_y), (panel_width, label_height)),
            text="Score:" + user1_score, manager=self.manager, container=self.panel)
        current_y += label_height + padding

        # User 2 Label
        self.user2_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, current_y), (panel_width, label_height)),
            text="User 2:" + user2_name, manager=self.manager, container=self.panel)
        
        current_y += label_height + padding

        # User 2 Score Label
        self.user2_score_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, current_y), (panel_width, label_height)),
            text="Score:" + user2_score, manager=self.manager, container=self.panel)
        current_y += label_height + padding

        self.listen_for_events()

    def listen_for_events(self):
        self.sio.on('user_joined', self.on_user_joined)
        self.sio.on('user_left', self.on_user_left)
        self.sio.on('room_deleted', self.on_room_deleted)

    def unlisten_for_events(self):
        self.sio.off('user_joined', self.on_user_joined)
        self.sio.off('user_left', self.on_user_left)
        self.sio.off('room_deleted', self.on_room_deleted)

    def on_user_joined(self, data):
        print("user joined:", data)
        print(self.app.current_room)
        self.app.current_room["user2"] = data
        username = data["username"]
        score = data["score"]
        self.user2_label.set_text("User 2:" + username)
        self.user2_score_label.set_text("Score:" + str(score))
        
    def on_user_left(self, data):
        print(data)
        self.app.current_room["user2"] = None
        self.user2_label.set_text("User 2:N/A")
        self.user2_score_label.set_text("Score:0")


    def on_room_deleted(self, data):
        print(data)
        self.app.current_room = None
        self.switch_page("main_menu")

    def process_events(self, event):
        self.manager.process_events(event)

    def update(self, time_delta):
        self.manager.update(time_delta)

    def render(self):
        self.window.fill((0, 0, 0))
        self.manager.draw_ui(self.window)
        pygame.display.update()