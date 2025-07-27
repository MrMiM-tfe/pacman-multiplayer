from pages.page_base import PageBase
# from main import MainApp
import pygame
import pygame_gui


class WinnerPage(PageBase):
    def setup_ui(self, data):
        winner = data['winner']
        if not winner: return

        username = winner['username']
        score = winner['score']
        score = str(score)

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

        self.winner_name = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, current_y), (panel_width, label_height)),
            text="winner :" + username, manager=self.manager, container=self.panel)
        current_y += label_height + padding

        self.score = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, current_y), (panel_width, label_height)),
            text="score :" + score, manager=self.manager, container=self.panel)
        current_y += label_height + padding

        self.back = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, current_y), (panel_width, button_height)),
            text="Back", manager=self.manager, container=self.panel)
        current_y += button_height + padding



    def process_events(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.back:
                self.switch_page('room')
            # elif event.ui_element == self.join_room_button:
            #     self.join_room()

        self.manager.process_events(event)

    def update(self, time_delta):
        self.manager.update(time_delta)

    def render(self):
        self.window.fill((0, 0, 0))
        self.manager.draw_ui(self.window)
        pygame.display.update()