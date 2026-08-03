from pydantic import BaseModel


class SessionCreate(BaseModel):
    user_id: str