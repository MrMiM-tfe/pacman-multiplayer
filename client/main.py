import pygame
import pygame_gui
import socketio
import threading

# Socket.IO client
sio = socketio.Client()

# Track login state
login_result = None

# Connect and emit login
def attempt_login(username):
    try:
        sio.connect("http://localhost:5000")
        sio.emit("login", {"username": username})
    except Exception as e:
        global login_result
        login_result = f"❌ Connection failed: {e}"

# Handle login events
@sio.on("login_success")
def on_login_success(data):
    global login_result
    login_result = f"✅ Welcome, {data['username']}"

@sio.on("login_error")
def on_login_error(data):
    global login_result
    login_result = f"🚫 {data['error']}"

# --- Pygame GUI Setup ---
pygame.init()
pygame.display.set_caption("Pac-Man Login")
window_size = (400, 300)
window = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()
manager = pygame_gui.UIManager(window_size)

username_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((100, 80), (200, 30)), manager=manager)
username_input.set_text("")

connect_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((150, 130), (100, 40)), text='Connect', manager=manager)

login_message = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((50, 200), (300, 30)), text="", manager=manager)

running = True
while running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == connect_button:
            username = username_input.get_text().strip()
            login_message.set_text("🔄 Connecting...")
            threading.Thread(target=attempt_login, args=(username,), daemon=True).start()

        manager.process_events(event)

    manager.update(time_delta)

    if login_result:
        login_message.set_text(login_result)
        login_result = None

    window.fill((0, 0, 0))
    manager.draw_ui(window)
    pygame.display.update()

pygame.quit()
