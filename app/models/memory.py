from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from app.database import Base



class Memory(Base):
    __tablename__ = "memories"

    id = Column(Integer, primary_key=True)

    user_id = Column(String, index=True)

    category = Column(String, index=True)

    content = Column(Text)

    importance = Column(Integer, default=1)

    source_session = Column(String)

    embedding = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )