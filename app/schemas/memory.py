from pydantic import BaseModel

class MemorySearchRequest(BaseModel):
    user_id: str
    query: str
