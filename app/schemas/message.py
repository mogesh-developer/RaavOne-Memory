from pydantic import BaseModel

class MessageCreate(BaseModel):
    user_id: str
    role: str
    text: str
    session_id: str
    