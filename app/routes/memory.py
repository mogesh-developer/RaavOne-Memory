from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.services.profile_service import generate_user_profile
from app.services.timeline_service import generate_user_timeline
from app.services.analytics_service import get_user_analytics

from app.database import get_db
from app.schemas.message import MessageCreate
from app.schemas.memory import MemorySearchRequest
from app.services.memory_service import (
    save_memory,
    get_history,
    get_memories,
    backfill_embeddings,
    search_memories,
)
from app.services.forgetting_service import run_forgetting_engine

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

@router.post("/embed/{user_id}")
def generate_old_embeddings(user_id: str, db: Session = Depends(get_db)):
    count = backfill_embeddings(db, user_id)
    return {
        "status": "success",
        "updated_memories_count": count
    }

@router.post("/search")
def search(data: MemorySearchRequest):
    results = search_memories(data.user_id, data.query)
    return results

@router.get("/profile/{user_id}")
def get_profile_summary(user_id: str, db: Session = Depends(get_db)):
    summary = generate_user_profile(db, user_id)
    return {
        "user_id": user_id,
        "profile_summary": summary
    }

@router.post("/cleanup")
def cleanup_expired_memories(
    days: int = 30, 
    importance_limit: int = 3, 
    db: Session = Depends(get_db)
):
    deleted_count = run_forgetting_engine(db, days_threshold=days, importance_limit=importance_limit)
    return {
        "status": "success",
        "forgotten_memories_count": deleted_count
    }


@router.get("/timeline/{user_id}")
def get_timeline(user_id: str, db: Session = Depends(get_db)):
    timeline = generate_user_timeline(db, user_id)
    return {
        "user_id": user_id,
        "timeline": timeline
    }


@router.get("/analytics/{user_id}")
def get_analytics(user_id: str, db: Session = Depends(get_db)):
    stats = get_user_analytics(db, user_id)
    return {
        "user_id": user_id,
        "analytics": stats
    }