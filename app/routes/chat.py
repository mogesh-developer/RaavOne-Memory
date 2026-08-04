from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.chat import ChatRequest
from app.services.chat_service import chat

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("")
def chat_endpoint(data: ChatRequest, db: Session = Depends(get_db)):
    chat(db, data.user_id, data.message)
    return {
        "status": "coming soon"
    }
