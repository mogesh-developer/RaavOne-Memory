from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from app.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(String, index=True)

    role = Column(String)

    text = Column(Text)

    session_id = Column(String, index=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())