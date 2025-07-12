from .database import engine
from .database import Base
from server.models import User

def init_db():
    Base.metadata.create_all(bind=engine)
