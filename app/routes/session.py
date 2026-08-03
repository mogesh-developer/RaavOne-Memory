from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.session import SessionCreate
from app.services.session_service import start_session
from app.services.session_service import get_session_messages

router = APIRouter(prefix="/session", tags=["Session"])


@router.post("/start")
def create_session(data: SessionCreate, db: Session = Depends(get_db)):
    session = start_session(db, data)
    return {
        "status": "success",
        "session_id": session.session_id,
        "user_id": session.user_id,
        "started_at": session.started_at
    }

@router.get("/{session_id}")
def session_messages(
    session_id: str,
    db: Session = Depends(get_db),
):

    messages = get_session_messages(
        db,
        session_id,
    )

    return messages
