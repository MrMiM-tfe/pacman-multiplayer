from sqlalchemy import Column, String, Integer
from db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    score = Column(Integer, default=0)
    status = Column(String, default="active")

    sid = None
    room_id = None

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "score": self.score,
            "status": self.status
        }
