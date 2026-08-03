from sqlalchemy.orm import Session
from app.models.message import Message
from app.models.memory import Memory
from app.schemas.message import MessageCreate


def save_memory(db: Session, data: MessageCreate):
    message = Message(
        user_id = data.user_id,
        role = data.role,
        text  = data.text,
        session_id = data.session_id
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def get_history(db: Session, user_id: str):
    return (
        db.query(Message)
        .filter(Message.user_id == user_id)
        .order_by(Message.created_at.asc())
        .all()
    )
def get_memories(db, user_id: str):
    return (
        db.query(Memory)
        .filter(Memory.user_id == user_id)
        .all()
    )