from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.memory import Memory
from app.vector.chroma import collection

def run_forgetting_engine(db: Session, days_threshold: int = 30, importance_limit: int = 3) -> int:
    # 1. Calculate the cutoff time (30 days ago)
    cutoff = datetime.utcnow() - timedelta(days=days_threshold)

    # 2. Query expired, low-importance memories from SQLite
    expired_memories = (
        db.query(Memory)
        .filter(Memory.updated_at < cutoff)
        .filter(Memory.importance < importance_limit)
        .all()
    )

    if not expired_memories:
        return 0

    # 3. Collect IDs to delete
    memory_ids_str = [str(m.id) for m in expired_memories]

    try:
        # 4. Purge from ChromaDB Vector Store
        collection.delete(ids=memory_ids_str)
    except Exception as e:
        print(f"Error purging from ChromaDB: {e}")
        # Note: Continue so SQLite stays synced even if Chroma fails

    # 5. Purge from SQLite
    deleted_count = 0
    for m in expired_memories:
        db.delete(m)
        deleted_count += 1
    
    db.commit()

    return deleted_count
