import eventlet
eventlet.monkey_patch()
import os
from dotenv import load_dotenv
import socketio
from libs.connection_handler import ConnectionHandler

from gateways.auth_gateway import AuthGateway
from gateways.game_gateway import GameGateway
from db.init_db import init_db

# Load .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))


init_db()

HOST = os.getenv("SERVER_HOST", "127.0.0.1")
PORT = int(os.getenv("SERVER_PORT", 5000))

sio = socketio.Server(cors_allowed_origins="*")
handler = ConnectionHandler(sio)
app = socketio.WSGIApp(sio)

if __name__ == "__main__":
    print(f"Starting server on {HOST}:{PORT}")
    eventlet.wsgi.server(eventlet.listen((HOST, PORT)), app)
