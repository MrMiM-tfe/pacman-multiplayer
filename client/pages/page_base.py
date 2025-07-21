from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import MainApp

class PageBase:
    def __init__(self, window, manager, sio, app: "MainApp", switch_page_callback):
        self.window = window
        self.app = app
        self.manager = manager
        self.switch_page = switch_page_callback
        self.sio = sio
        self.running = True

    def process_events(self, event):
        raise NotImplementedError

    def update(self, time_delta):
        raise NotImplementedError

    def render(self):
        raise NotImplementedError
