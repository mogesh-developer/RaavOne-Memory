import uuid

from sqlalchemy import Column, DateTime, String
from sqlalchemy.sql import func

from app.database import Base


class Session(Base):
    __tablename__ = "sessions"

    session_id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    user_id = Column(String, index=True, nullable=False)

    started_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    ended_at = Column(
        DateTime(timezone=True),
        nullable=True
    )