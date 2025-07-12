# dev_server.py

import sys
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os

SERVER_FILE = "main.py"  # adjust if needed
SERVER_DIR = os.path.dirname(os.path.abspath(__file__))

class ReloadHandler(FileSystemEventHandler):
    def __init__(self, restart_callback):
        self.restart_callback = restart_callback

    def on_any_event(self, event):
        if event.src_path.endswith(".py"):
            print(f"🔁 Change detected in: {event.src_path}")
            self.restart_callback()

def run_server():
    print("🚀 Starting server...")
    return subprocess.Popen([sys.executable, SERVER_FILE], cwd=SERVER_DIR)

def main():
    process = run_server()

    def restart():
        nonlocal process
        print("♻️ Restarting server...")
        process.kill()
        process = run_server()

    event_handler = ReloadHandler(restart)
    observer = Observer()
    observer.schedule(event_handler, path=SERVER_DIR, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("🛑 Stopping dev server...")
        observer.stop()
        process.kill()

    observer.join()

if __name__ == "__main__":
    main()
