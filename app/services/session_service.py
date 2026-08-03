from sqlalchemy.orm import Session

from app.models.session import Session as SessionModel
from app.schemas.session import SessionCreate
from app.models.message import Message


def start_session(db: Session, data: SessionCreate):
    session = SessionModel(
        user_id=data.user_id
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_session_messages(db: Session, session_id: str):
    return (
        db.query(Message)
        .filter(Message.session_id == session_id)
        .order_by(Message.created_at.asc())
        .all()
    )