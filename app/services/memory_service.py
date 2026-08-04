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


def backfill_embeddings(db: Session, user_id: str) -> int:
    from app.services.embedding_service import create_embedding
    from app.services.vector_service import add_memory

    memories = (
        db.query(Memory)
        .filter(Memory.user_id == user_id)
        .all()
    )

    updated_count = 0
    for memory in memories:
        try:
            vector = create_embedding(memory.content)
            add_memory(
                memory_id=str(memory.id),
                content=memory.content,
                embedding=vector,
                metadata={
                    "user_id": memory.user_id,
                    "category": memory.category,
                    "importance": memory.importance,
                }
            )
            updated_count += 1
        except Exception as e:
            print(f"Error backfilling embedding to ChromaDB for memory {memory.id}: {e}")

    return updated_count


def search_memories(user_id: str, query: str):
    from app.services.search_service import semantic_search

    try:
        chroma_res = semantic_search(query, user_id=user_id)
        return {
            "documents": chroma_res.get("documents", [[]])
        }
    except Exception as e:
        print(f"ChromaDB search error: {e}")
        return {"documents": [[]]}


