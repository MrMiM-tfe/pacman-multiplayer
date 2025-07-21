from libs.base_gateway import BaseGateway
from libs.decorators import on
from game.room import Room
from libs.response import Response
from libs.decorators import register_gateway
import random

@register_gateway
class GameGateway(BaseGateway):
	@on("create_room")
	def handle_create_game(self, sid: str):
		while True:
			game_id = random.randint(100000, 999999)
			game_id = str(game_id)
			exist_game = Room.rooms.get(game_id)
			if not exist_game:
				break
		user = self.get_user(sid)
		room = Room(game_id=game_id, user1=user)
		user.room_id = room.game_id
		self.sio.enter_room(sid, room.game_id)
		return Response.success(room)


	@on("join_room")
	def handle_join_game(self, sid: str, game_id: str):
		user = self.get_user(sid)
		room = Room.rooms.get(game_id)
		print(Room.rooms)
		if room:
			room.user2 = user
			user.room_id = room.game_id
			self.sio.enter_room(sid, room.game_id)
			room.game_state = "ready to start"
			self.sio.emit("user_joined", user.to_dict(), to=room.user1.sid)
			return Response.success(room)
		else:
			return Response.error("Room not found")
		
	@on("start_game")
	def handle_start_game(self, sid: str, game_id: str):
		room = Room.rooms.get(game_id)
		if room:
			room.start_game()
			self.sio.emit("game_started", to=room.game_id)
			return Response.success(room)
		else:
			return Response.error("Room not found")

	@on("disconnect")
	def disconnect(self, sid: str):
		user = self.get_user(sid)
		print("User disconnected:", user.username)
		if user:
			room = Room.rooms.get(user.room_id)
			if not room:
				return
			if room.user1.sid == sid:
				print("User 1 disconnected")
				self.sio.emit("room_deleted", to=room.user2.sid)
				self.sio.leave_room(sid, room.game_id)
				room.user1 = None
				room.user2 = None
			elif room.user2 and room.user2.sid == sid:
				print("User 2 disconnected")
				self.sio.leave_room(sid, room.game_id)
				self.sio.emit("user_left", to=room.user1.sid)
				room.user2 = None