from pydantic import BaseModel


# USER
class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


# CHAT
class ChatRequest(BaseModel):
    conversation_id: int
    message: str