import os
from dotenv import load_dotenv
import socketio
import eventlet
from libs.connection_handler import ConnectionHandler

from gateways.auth_gateway import AuthGateway
from gateways.game_gateway import GameGateway

# Load .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

HOST = os.getenv("SERVER_HOST", "localhost")
PORT = int(os.getenv("SERVER_PORT", 5000))

sio = socketio.Server(cors_allowed_origins="*")
handler = ConnectionHandler(sio)
app = socketio.WSGIApp(sio)

if __name__ == "__main__":
    print(f"Starting server on {HOST}:{PORT}")
    eventlet.wsgi.server(eventlet.listen((HOST, PORT)), app)
