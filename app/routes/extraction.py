from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.message import Message
from app.services.extraction_service import (
    extract_memories,
    save_memories,
)

router = APIRouter(
    prefix="/memory",
    tags=["Memory Extraction"]
)


@router.post("/extract/{session_id}")
def extract(session_id: str, db: Session = Depends(get_db)):

    messages = (
        db.query(Message)
        .filter(Message.session_id == session_id)
        .all()
    )

    if not messages:
        return []

    memories = extract_memories(messages)

    saved = save_memories(
        db=db,
        user_id=messages[0].user_id,
        session_id=session_id,
        memories=memories,
    )

    return saved