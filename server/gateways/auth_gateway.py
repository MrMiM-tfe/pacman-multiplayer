from server.libs.base_gateway import BaseGateway
from server.libs.decorators import on, register_gateway, validate
from server.db.database import SessionLocal
from server.models import User
from server.libs.response import Response
from server.validations.auth import AuthRequest
import bcrypt
import jwt
import os
from datetime import datetime, timedelta

SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'secret')

@register_gateway
class AuthGateway(BaseGateway):
    @on("authenticate")
    @validate(AuthRequest)
    def handle_login(self, sid, validated_data):
        username = validated_data.username
        password = validated_data.password

        db = SessionLocal()
        user = db.query(User).filter(User.username == username).first()

        if not user:
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            new_user = User(
                username=username,
                password_hash=hashed_password.decode()
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            user = new_user

        if bcrypt.checkpw(password.encode(), user.password_hash.encode()):
            token = self.generate_jwt_token(user.id, user.username)

            user_data = {
                "username": user.username,
                "user_id": user.id,
                "score": user.score,
                "status": user.status,
                "token": token 
            }
            
            self.connected_clients[sid] = user
            return Response.success(user_data)
        else:
            return Response.error("Invalid credentials")

    def generate_jwt_token(self, user_id, username):
        expiration_time = datetime.utcnow() + timedelta(days=7)
        payload = {
            "sub": user_id,
            "username": username,
            "exp": expiration_time
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return token
