from libs.base_gateway import BaseGateway
from libs.decorators import on
from game.room import Room
from libs.response import Response
from libs.decorators import register_gateway

@register_gateway
class GameGateway(BaseGateway):
	@on("create_game")
	def handle_create_game(self, sid: str, game_id: str):
		user = self.get_user(sid)
		room = Room(game_id=game_id, user1=user)


	@on("join_game")
	def handle_join_game(self, sid: str, game_id: str):
		user = self.get_user(sid)
		room = Room.rooms.get(game_id)
		if room:
			room.user2 = user
			return Response.success(room)
		else:
			return Response.error("Room not found")