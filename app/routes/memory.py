from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.message import MessageCreate
from app.services.memory_service import save_memory
from app.services.memory_service import get_history
from app.services.memory_service import get_memories

router = APIRouter(prefix="/memory", tags=["Memory"])


@router.post("/save")
def create_memory(
    data: MessageCreate,
    db: Session = Depends(get_db),
):
    message = save_memory(db, data)

    return {
        "status": "success",
        "id": message.id,
    }
@router.get("/history/{user_id}")
def get_user_history(user_id: str, db: Session = Depends(get_db)):
    messages = get_history(db, user_id)
    return messages

@router.get("/all/{user_id}")
def all_memories(
    user_id: str,
    db: Session = Depends(get_db),
):
    return get_memories(db, user_id)