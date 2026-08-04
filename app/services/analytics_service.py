from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.memory import Memory


def get_user_analytics(db: Session, user_id: str) -> dict:
    # 1. Calculate total memories count
    total_memories = db.query(Memory).filter(Memory.user_id == user_id).count()

    # 2. Get category breakdowns (group by category)
    category_counts = (
        db.query(Memory.category, func.count(Memory.id))
        .filter(Memory.user_id == user_id)
        .group_by(Memory.category)
        .all()
    )
    breakdown = {category: count for category, count in category_counts}

    # 3. Calculate average importance score
    avg_importance = (
        db.query(func.avg(Memory.importance))
        .filter(Memory.user_id == user_id)
        .scalar()
    ) or 0.0

    # 4. Get last active timestamp
    last_updated_record = (
        db.query(Memory.updated_at)
        .filter(Memory.user_id == user_id)
        .order_by(Memory.updated_at.desc())
        .first()
    )
    last_active = last_updated_record[0] if last_updated_record else None

    return {
        "total_memories": total_memories,
        "category_breakdown": breakdown,
        "average_importance": round(avg_importance, 2),
        "last_active": last_active
    }
