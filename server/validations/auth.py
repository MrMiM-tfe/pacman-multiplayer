from pydantic import BaseModel, Field

class AuthRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Username must be between 3 and 50 characters.")
    password: str = Field(..., min_length=6, max_length=128, description="Password must be at least 6 characters long.")
